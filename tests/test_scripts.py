"""Offline tests van de scripts van de skill, zonder AI-assistent.

Draaien vanuit de root van de repository, met een Python waarin de pakketten uit
skills/geonovum-uml2-nl-sbb/requirements.txt staan:

    python3 -m unittest discover -s tests -v

De SHACL-validatie haalt het NL-SBB-profiel uit het register en draait alleen met
BK_NETWERK=1.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "geonovum-uml2-nl-sbb")
BK = os.path.join(SKILL, "scripts", "bk.py")
FIXTURE = os.path.join(ROOT, "tests", "fixtures", "fietsparkeren.xmi")
sys.path.insert(0, os.path.join(SKILL, "scripts"))


def bk(werkmap, *args, invoer=None, ok=True):
    r = subprocess.run([sys.executable, BK, *args], cwd=werkmap, input=invoer, capture_output=True, text=True)
    if ok and r.returncode != 0:
        raise AssertionError(f"bk.py {' '.join(args)} gaf exitcode {r.returncode}:\n{r.stdout}\n{r.stderr}")
    return r


def termen(werkmap):
    with open(os.path.join(werkmap, "uit", "termen.tsv"), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


class Keten(unittest.TestCase):
    """De hele keten van bk.py op het fictieve model Fietsparkeren."""

    @classmethod
    def setUpClass(cls):
        cls.w = tempfile.mkdtemp(prefix="bk-test-")
        bk(cls.w, "start", FIXTURE, "--package", "Fietsparkeren")
        bk(cls.w, "analyseer")
        bk(cls.w, "overnemen", "--alle")
        bk(cls.w, "analyseer")
        bk(cls.w, "genereer")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.w, ignore_errors=True)

    def test_inventaris_alleen_gekozen_package(self):
        inv = json.load(open(os.path.join(self.w, "werk", "inventaris.json")))
        namen = {c["name"] for c in inv["elementen"].values()}
        self.assertEqual(len(namen), 7)
        self.assertNotIn("GeoObject", namen)
        self.assertIn("GeoObject", inv["externe_klassen"].values())

    def test_geen_open_vragen_na_overnemen(self):
        punten = json.load(open(os.path.join(self.w, "werk", "beslispunten.json")))
        self.assertEqual([p["code"] for p in punten if p["soort"] == "VRAAG"], [])

    def test_aantallen_en_termen(self):
        t = {r["voorkeursterm"]: r for r in termen(self.w)}
        self.assertEqual(len(t), 21)
        # zelfde attribuutnaam, andere definitie -> objecttype-context
        self.assertIn("naam stalling", t)
        self.assertIn("naam fietsenrek", t)
        # zelfde waarde, andere definitie -> automatisch gesplitst
        self.assertIn("type rek overig", t)
        self.assertIn("type stalling overig", t)
        # zelfde waarde, alleen leestekens anders -> één begrip
        self.assertIn("onbekend", t)
        self.assertEqual(t["capaciteit fietsen"]["notatie"], "Stalling.capaciteitFietsen")

    def test_kader_is_geldige_turtle_met_collecties(self):
        import rdflib
        from rdflib.namespace import RDF, SKOS
        g = rdflib.Graph().parse(os.path.join(self.w, "uit", "kader.ttl"))
        self.assertEqual(len(set(g.subjects(RDF.type, SKOS.Concept))), 21)
        self.assertEqual(len(set(g.subjects(RDF.type, SKOS.Collection))), 3)
        self.assertEqual(len(set(g.subjects(RDF.type, SKOS.ConceptScheme))), 1)

    def test_ontbrekende_definitie_in_log(self):
        log = open(os.path.join(self.w, "uit", "beslissingen.md"), encoding="utf-8").read()
        self.assertIn("Geen definitie in het model: 'kluis code'", log)

    def test_review_in_delen_met_compleetheidscontrole(self):
        bk(self.w, "review", "--opnieuw")
        idx = json.load(open(os.path.join(self.w, "review", "index.json")))
        self.assertEqual(idx["aantal"], 21)
        # onvolledig: review klaar weigert
        self.assertNotEqual(bk(self.w, "review", "klaar", ok=False).returncode, 0)
        # alles ok, behalve begrippen met een signaal: die krijgen een opmerking
        delen = [os.path.join(self.w, "review", d["bestand"]) for d in idx["delen"]]
        regels = []
        for pad in delen:
            for blok in open(pad, encoding="utf-8").read().split("\n### ")[1:]:
                nr = blok.split(" |")[0]
                sig = re.search(r"^signalen: (.*)$", blok, re.M).group(1)
                regels.append(f"{nr} ok" + ("" if sig == "-" else " | signaal gezien, voor de test niet terecht"))
        bk(self.w, "oordeel", invoer="\n".join(regels))
        bk(self.w, "review", "klaar")
        self.assertTrue(os.path.exists(os.path.join(self.w, "reports", "review.md")))
        # een termcorrectie: oordelen van ongewijzigde begrippen blijven staan
        bk(self.w, "zet", "attributen.term_correcties[Fietskluis.kluisCode]", "kluiscode")
        bk(self.w, "genereer")
        uit = bk(self.w, "review", "--opnieuw").stdout
        self.assertIn("20 oordelen overgenomen", uit)

    def test_rapport_bevat_cijfers(self):
        bk(self.w, "rapport")
        r = open(os.path.join(self.w, "reports", "rapport.md"), encoding="utf-8").read()
        self.assertIn("begrippen: attribuut", r)
        self.assertIn("<!-- LLM:", r)


class ProjectControle(unittest.TestCase):
    def setUp(self):
        self.w = tempfile.mkdtemp(prefix="bk-test-")
        bk(self.w, "start", FIXTURE, "--package", "Fietsparkeren")

    def tearDown(self):
        shutil.rmtree(self.w, ignore_errors=True)

    def test_tikfout_in_sleutel(self):
        bk(self.w, "zet", "kader.uri", "http://example.org/fiets")
        uit = bk(self.w, "zet", "termen.camelcase_splitse", "false", ok=False).stdout
        self.assertIn("bedoel je 'camelcase_splitsen'", uit)
        self.assertNotEqual(bk(self.w, "controleer", ok=False).returncode, 0)

    def test_zet_tekst_met_dubbele_punt(self):
        bk(self.w, "zet", "kader.omschrijving", "Begrippen uit IMGeo 2.2: objecttypen en waarden")
        import yaml
        proj = yaml.safe_load(open(os.path.join(self.w, "project.yaml"), encoding="utf-8"))
        self.assertEqual(proj["kader"]["omschrijving"], "Begrippen uit IMGeo 2.2: objecttypen en waarden")

    def test_alleen_lezen_project_yaml(self):
        bk(self.w, "zet", "kader.uri", "http://example.org/fiets")
        os.chmod(os.path.join(self.w, "project.yaml"), 0o444)
        bk(self.w, "zet", "kader.titel", "Fietsparkeren")
        self.assertIn("Fietsparkeren", open(os.path.join(self.w, "project.yaml"), encoding="utf-8").read())

    def test_overnemen_overschrijft_bestaande_keuze_niet(self):
        bk(self.w, "zet", "kader.uri", "http://example.org/fiets")
        bk(self.w, "zet", "relaties.gebruik.TypeRek", "[Fietsenrek, type]")
        bk(self.w, "zet", "relaties.gebruik.StatusStalling", "[Stalling, null]")
        bk(self.w, "analyseer")
        bk(self.w, "overnemen", "--alle")
        import yaml
        proj = yaml.safe_load(open(os.path.join(self.w, "project.yaml"), encoding="utf-8"))
        self.assertEqual(proj["relaties"]["gebruik"]["StatusStalling"], ["Stalling", None])

    def test_onbekende_klasse_in_gebruik(self):
        bk(self.w, "zet", "kader.uri", "http://example.org/fiets")
        bk(self.w, "zet", "relaties.gebruik.StatusStalling", "[Bestaatniet, null]", ok=False)
        uit = bk(self.w, "controleer", ok=False).stdout
        self.assertIn("klasse 'Bestaatniet' bestaat niet", uit)


class Termen(unittest.TestCase):
    def setUp(self):
        import kern
        self.T = kern.Termen(kern.laad_keuzes())
        self.Tc = kern.Termen(kern._merge(kern.laad_keuzes(), {"termen": {"cijfers_scheiden": True}}))

    def test_camelcase_en_afkortingen(self):
        self.assertEqual(self.T.humanize("aantalVerkeersgegevensWeg"), "aantal verkeersgegevens weg")
        self.assertEqual(self.T.humanize("BGTObject"), "BGT object")
        self.assertEqual(self.T.waarde("F4"), "F4")
        self.assertEqual(self.T.waarde("GT5"), "GT5")

    def test_cijfers_scheiden(self):
        self.assertEqual(self.Tc.humanize("golflengte12_5"), "golflengte 12,5")

    def test_local_name_houdt_cijfergroepen_apart(self):
        import kern
        self.assertNotEqual(kern.local_name("golflengte 12,5"), kern.local_name("golflengte 125"))

    def test_contextterm_bij_keuze(self):
        import genereer
        self.assertEqual(genereer.context_term("afstand", "afstand of geometrie van de overige contour"),
                         "afstand van de overige contour")
        self.assertEqual(genereer.context_term("stof", "stof of stofcategorie"), "stof bij keuze stof of stofcategorie")
        self.assertEqual(genereer.context_term("naam", "stalling"), "naam stalling")
        # de context staat al in de term: niet nog eens achterplakken
        self.assertEqual(genereer.context_term("type scheiding", "scheiding"), "type scheiding")

    def test_woorden_behouden(self):
        self.assertEqual(self.T.humanize("IMGeo-object"), "IMGeo-object")
        self.assertEqual(self.T.humanize("statusIMGeoObject"), "status IMGeo object")
        self.assertEqual(self.T.waarde("IMGeo-object"), "IMGeo-object")

    def test_ij_en_losse_hoofdletter(self):
        self.assertEqual(self.T.waarde("obstakelIJzervloer"), "obstakel ijzervloer")
        self.assertEqual(self.T.waarde("klasseA"), "klasse A")

    def test_codes_standaard_ongewijzigd(self):
        # zonder de nieuwe opties blijft het gedrag zoals het was
        self.assertEqual(self.T.waarde("veel25tot50"), "veel25tot50")
        self.assertEqual(self.T.waarde("ISO17892d4v2016"), "iso17892d4v2016")
        self.assertEqual(self.T.waarde("GBKNonbekend"), "gbknonbekend")

    def test_getallen_normcodes_afkortingen(self):
        import kern
        T = kern.Termen(kern._merge(kern.laad_keuzes(), {"termen": {
            "getallen": True, "normcodes": True, "afkortingen": ["RTK-GPS", "GPS", "PP", "AHN", "GBKN", "PE"]}}))
        gevallen = {
            "veel25tot50": "veel 25 tot 50", "zeerVeel50tot75": "zeer veel 50 tot 75",
            "fractie 16tot31.5mm": "fractie 16 tot 31,5 mm", "fractie 1400umtot2mm": "fractie 1400 µm tot 2 mm",
            "1400kPa": "1400 kPa", "klasseA_v2006": "klasse A v2006", "zoutwaterMinstens50000": "zoutwater minstens 50000",
            "ISO17892d4v2016": "ISO 17892-4:2016", "ASTM_D4767v2011": "ASTM D4767:2011", "EN1997d2v2007": "EN 1997-2:2007",
            "ISO14688d1v2019NEN8990v2020": "ISO 14688-1:2019 NEN 8990:2020", "fijnNEN5104": "fijn NEN 5104",
            "NEN5104Synthetisch": "NEN 5104 synthetisch",
            "RTKGPS0tot2cm": "RTK-GPS 0 tot 2 cm", "GPS200tot1000cm": "GPS 200 tot 1000 cm", "PPgroot": "PP groot",
            "PPzeerKlein": "PP zeer klein", "GBKNonbekend": "GBKN onbekend", "AHNOnbekend": "AHN onbekend",
            "peHighDensity": "PE high density", "pe": "PE",
            # blijven staan: afkortingen met cijfers, versies, gewone woorden die met een afkorting beginnen
            "AHN3": "AHN3", "WGS84": "WGS84", "QM1": "QM1", "SIKB2001vanafV6.0": "sikb 2001 vanaf v6.0",
            "peilbuis": "peilbuis", "Pleistoceen": "pleistoceen",
        }
        for code, term in gevallen.items():
            self.assertEqual(T.waarde(code), term, code)
        self.assertEqual(T.humanize("Standaardverdeling fractie groter63um"), "standaardverdeling fractie groter 63 µm")

    def test_analyse_stelt_codes_voor(self):
        w = tempfile.mkdtemp(prefix="bk-codes-")
        try:
            os.makedirs(os.path.join(w, "werk"))
            lijst = {"name": "Methode", "type": "uml:Enumeration", "stereo": None, "pkg": "M", "abstract": False,
                     "doc": "", "alias": None, "gens": [], "tags": {},
                     "attrs": [{"id": f"w{i}", "name": n, "doc": f"Methode {n}.", "tags": {}} for i, n in
                               enumerate(["RTKGPS0tot2cm", "GPS200tot1000cm", "GPSOnbekend", "ISO17892d4v2016"])]}
            with open(os.path.join(w, "werk", "inventaris.json"), "w", encoding="utf-8") as f:
                json.dump({"bron": "t.xmi", "elementen": {"L": lijst}, "externe_klassen": {}}, f)
            bk(w, "analyseer")
            with open(os.path.join(w, "werk", "beslispunten.json"), encoding="utf-8") as f:
                p = {x["code"]: x for x in json.load(f)}
            v = p["termen-codes"]["voorstel"]["termen"]
            self.assertTrue(v["getallen"] and v["normcodes"])
            self.assertEqual(v["afkortingen"], ["GPS", "RTKGPS"])  # GPSOnbekend -> GPS, niet GPSO
        finally:
            shutil.rmtree(w, ignore_errors=True)


class Voorstellen(unittest.TestCase):
    """Heuristische voorstellen van analyseer: alias, kader en samenvoegen van waarden."""

    def test_alias_engels_of_nederlands(self):
        import analyseer
        bro = [("Booronderzoek", "BoreholeResearch"), ("Registratiegeschiedenis", "RegistrationHistory"),
               ("Weggegraven laag", "ExcavatedLayer"), ("Tussentijdse gebeurtenis", "IntermediateEvent")]
        imgeo = [("BuildingInstallation", "Gebouwinstallatie"), ("WaterBody", "Waterdeel"),
                 ("AuxiliaryTrafficArea", "OndersteunendWegdeel"), ("CityFurniture", "Straatmeubilair")]
        self.assertTrue(analyseer.alias_engels(bro))
        self.assertFalse(analyseer.alias_engels(imgeo))
        self.assertFalse(analyseer.alias_engels([("Boring", "Boring")]))  # gelijke namen tellen niet

    def test_kader_uit_bovenliggende_package(self):
        import analyseer
        obj = {"k": {"pkg_path": ["Geotechnisch booronderzoek (BHR-GT)", "Model"]}}
        v = analyseer.kader_voorstel({"packages": ["Model"], "bron": "BHR-GT_conceptueel-2.2.xml"}, obj)
        self.assertEqual(v["uri"], "http://definities.geostandaarden.nl/bhr-gt")
        self.assertEqual(v["titel"], "Begrippenkader Geotechnisch booronderzoek (BHR-GT)")
        v = analyseer.kader_voorstel({"packages": ["Fietsparkeren"], "bron": "f.xmi"}, {"k": {"pkg_path": ["Fietsparkeren"]}})
        self.assertEqual((v["uri"], v["titel"]), ("http://definities.geostandaarden.nl/fietsparkeren",
                                                  "Fietsparkeren-begrippenkader"))

    def test_samenvoegen_niet_bij_andere_getallen(self):
        import analyseer
        anders = [("grof", [("Grindmediaanklasse", "De grindmediaan is gelijk aan of groter dan 20 mm en kleiner dan 63 mm."),
                            ("Zandmediaanklasse", "De zandmediaan is groter dan 630 μm en kleiner dan of gelijk aan 2000 μm.")]),
                  ("geotextiel", [("A", "Een antropogeen bestanddeel: textiel en folies die meestal uit kunststof bestaan."),
                                  ("B", "Antropogeen materiaal: textiel en folies die meestal uit kunststof bestaan.")]),
                  ("veel", [("Fijn", "De fractie 2-5,6 mm maakt tussen 25 en 50 procent van de massa uit."),
                            ("Grof", "De fractie 16-63 mm maakt tussen 25 en 50 procent van de massa uit.")])]
        v = analyseer.split_voorstel(anders)["waarden"]
        self.assertEqual(v["zelfde_begrip"], ["geotextiel"])
        self.assertEqual(v["automatisch_splitsen"], "{lijst} {waarde}")


class Signalen(unittest.TestCase):
    def test_termvoorstel_bij_leestekens(self):
        sys.argv = ["bk.py", "help"]
        import bk as bkmod
        v = bkmod.term_voorstel
        self.assertEqual(v("recreatie: camping"), "camping")
        self.assertEqual(v("benzine- / olieput"), "benzine- of olieput")
        self.assertEqual(v("greppel, droge sloot"), "greppel of droge sloot")
        self.assertEqual(v("meer, plas, ven, vijver"), "meer, plas, ven of vijver")
        self.assertEqual(v("(haven)kraan"), "havenkraan")
        self.assertEqual(v("maatschappelijke en/of publieksvoorziening"), "maatschappelijke of publieksvoorziening")
        self.assertIsNone(v("brandkraan / -put"))


class Package(unittest.TestCase):
    def test_voorstel_uit_bestandsnaam(self):
        sys.argv = ["bk.py", "help"]
        import bk as bkmod
        boom = ["Kies ...", "Geostandaarden", "  3610-MIM-Datatypen", "  NEN3610", "    Waardelijsten", "  IMGolf"]
        self.assertEqual(bkmod.package_voorstel(boom, "NEN3610-2022-template-20221116.xmi"), "NEN3610")

    def test_voorbeeld_uit_bestandsnaam(self):
        sys.argv = ["bk.py", "help"]
        import bk as bkmod
        self.assertEqual(bkmod.voorbeeld_voorstel("IMGeo.xmi", []), "imgeo")
        self.assertEqual(bkmod.voorbeeld_voorstel("IMGeluid_v3_1_1.xmi", []), "imgeluid")
        self.assertEqual(bkmod.voorbeeld_voorstel("IMEV3.0.2_10072025.zip", []), "imev")
        self.assertEqual(bkmod.voorbeeld_voorstel("NEN3610-2022-template-20221116.xmi", []), "nen3610")
        self.assertIsNone(bkmod.voorbeeld_voorstel("fietsparkeren.xmi", ["Fietsparkeren"]))

    def test_voorbeeld_kopieren_met_schrijfrechten(self):
        w = tempfile.mkdtemp(prefix="bk-test-")
        try:
            bk(w, "start", FIXTURE, "--package", "Fietsparkeren")
            bk(w, "voorbeeld", "nen3610")
            self.assertTrue(os.access(os.path.join(w, "project.yaml"), os.W_OK))
            self.assertNotEqual(bk(w, "voorbeeld", "nen3610", ok=False).returncode, 0)  # bestaat al
        finally:
            shutil.rmtree(w, ignore_errors=True)


def schrijf(pad, tekst):
    with open(pad, "w", encoding="utf-8") as f:
        f.write(tekst)


def lees_json(pad):
    with open(pad, encoding="utf-8") as f:
        return json.load(f)


def kolomlijst(naam, kolommen=("Waarde", "IMBRO", "Omschrijving")):
    """Waardelijst zoals in de BRO-catalogi: alleen kolommen, geen waarden."""
    return {"name": naam, "type": "uml:DataType", "stereo": "Referentielijst", "pkg": "Model", "abstract": False,
            "doc": f"De lijst {naam}.", "alias": None, "gens": [], "tags": {
                "Locatie": f"https://voorbeeld.nl/lists/{naam}.xml"},
            "attrs": [{"id": f"{naam}-{k}", "name": k, "doc": f"Kolom {k}.", "type": "Tekst",
                       "stereo": "Referentie element", "tags": {}} for k in kolommen]}


class WaardenExtern(unittest.TestCase):
    """Extern beheerde waardelijsten: herkennen (analyseer) en vullen (bk.py waarden)."""

    def setUp(self):
        self.w = tempfile.mkdtemp(prefix="bk-extern-")
        self.lijsten = ["Kleur", "Vorm", "Coördinaatstelsel"]
        self.inv = {"bron": "test.xmi", "packages": ["Model"], "zonder": [], "externe_klassen": {},
                    "elementen": {f"L{i}": kolomlijst(n) for i, n in enumerate(self.lijsten)}}
        self.inv["elementen"]["K"] = {"name": "Ding", "type": "uml:Class", "stereo": "Objecttype", "pkg": "Model",
                                      "abstract": False, "doc": "Een ding.", "alias": None, "gens": [], "tags": {},
                                      "attrs": [{"id": "a", "name": "kleur", "doc": "De kleur.", "type": "Kleur",
                                                 "stereo": None, "tags": {}}]}
        os.makedirs(os.path.join(self.w, "werk"))
        os.makedirs(os.path.join(self.w, "lijsten"))
        schrijf(os.path.join(self.w, "werk", "inventaris.json"), json.dumps(self.inv, ensure_ascii=False))
        rij = "<{l}><Waarde>{w}</Waarde><IMBRO>v</IMBRO><Omschrijving>{d}</Omschrijving></{l}>"
        schrijf(os.path.join(self.w, "lijsten", "Kleur.xml"), "<domeintabel>" + rij.format(l="Kleur", w="rood", d="De kleur rood.")
            + rij.format(l="Kleur", w="donkerBlauw", d="De kleur donkerblauw.") + "</domeintabel>")
        schrijf(os.path.join(self.w, "lijsten", "Vorm.xml"), "<domeintabel>" + rij.format(l="Vorm", w="rond", d="Zonder hoeken.") + "</domeintabel>")
        # bestandsnaam zonder trema, zoals in de BRO-repository
        schrijf(os.path.join(self.w, "lijsten", "Coordinaatstelsel.xml"), "<domeintabel>" + rij.format(l="X", w="RD", d="Rijksdriehoeksmeting.") + "</domeintabel>")

    def tearDown(self):
        shutil.rmtree(self.w, ignore_errors=True)

    def test_herkent_kolomlijsten_met_voorstel(self):
        bk(self.w, "analyseer")
        p = {x["code"]: x for x in lees_json(os.path.join(self.w, "werk", "beslispunten.json"))}
        self.assertEqual(p["waarden-extern"]["soort"], "VRAAG")
        ex = p["waarden-extern"]["voorstel"]["waarden"]["extern"]
        self.assertEqual(ex["bron"], "https://voorbeeld.nl/lists/{lijst}.xml")
        self.assertEqual((ex["naam"], ex["definitie"], ex["tags"]), ("Waarde", "Omschrijving", ["IMBRO"]))
        self.assertIn("0 waarden", p["overzicht"]["titel"])  # kolommen tellen niet als waarden
        self.assertNotIn("waarden-samen", p)

    def test_waarden_ophalen_en_status(self):
        bk(self.w, "zet", "kader.uri", "http://voorbeeld.nl/kader")
        bk(self.w, "zet", "waarden.extern.bron", "lijsten/{lijst}.xml")
        self.assertIn("bk.py waarden", bk(self.w, "status").stdout)
        uit = bk(self.w, "waarden").stdout
        self.assertIn("3 waardelijsten gevuld met 4 waarden", uit)
        inv = lees_json(os.path.join(self.w, "werk", "inventaris.json"))
        kleur = next(c for c in inv["elementen"].values() if c["name"] == "Kleur")
        self.assertEqual([a["name"] for a in kleur["attrs"]], ["rood", "donkerBlauw"])
        self.assertEqual(kleur["attrs"][0]["doc"], "De kleur rood.")
        self.assertEqual(kleur["kolommen"], ["Waarde", "IMBRO", "Omschrijving"])
        self.assertNotIn("bk.py waarden", bk(self.w, "status").stdout)
        bk(self.w, "analyseer")
        bk(self.w, "overnemen", "--alle")
        bk(self.w, "genereer")
        t = {r["voorkeursterm"]: r for r in termen(self.w)}
        self.assertEqual(t["donker blauw"]["soort"], "waarde")
        self.assertIn("RD", t)

    def test_onbekende_sleutel_en_bron_zonder_lijst(self):
        bk(self.w, "zet", "kader.uri", "http://voorbeeld.nl/kader")
        r = bk(self.w, "zet", "waarden.extern.bron", "lijsten/alles.xml", ok=False)
        self.assertIn("{lijst}", r.stdout)


@unittest.skipUnless(os.environ.get("BK_NETWERK") == "1", "SHACL-validatie haalt het profiel uit het register (BK_NETWERK=1)")
class Validatie(unittest.TestCase):
    def test_shacl_telling(self):
        w = tempfile.mkdtemp(prefix="bk-test-")
        try:
            for stap in (["start", FIXTURE, "--package", "Fietsparkeren"], ["analyseer"], ["overnemen", "--alle"],
                         ["analyseer"], ["genereer"], ["valideer"]):
                bk(w, *stap)
            s = open(os.path.join(w, "reports", "shacl-samenvatting.txt")).read()
            tel = re.findall(r"Violation (\d+), Warning (\d+), Info (\d+)", s)[-1]
            # alleen 'kluis code' heeft geen definitie
            self.assertEqual(tel[0], "1")
        finally:
            shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
