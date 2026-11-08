#!/usr/bin/env bash
# Haalt het testmodel uit het Geonovum-register en controleert de checksum.
# Het model zelf staat niet in deze repository.
set -eu
curl -sSfL -o "NEN3610-2022-template-20221116.xmi" "https://register.geostandaarden.nl/informatiemodel/nen3610/2022/NEN3610-2022-template-20221116.xmi"
echo "dfac5f4fe662bc1707ee328220e8305b472765225046f9b6b0ca259b63e1969e  NEN3610-2022-template-20221116.xmi" | shasum -a 256 -c -
