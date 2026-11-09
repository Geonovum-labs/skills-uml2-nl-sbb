#!/usr/bin/env bash
# Haalt het testmodel uit het Geonovum-register en controleert de checksum.
# Het model zelf staat niet in deze repository.
set -eu
curl -sSfL -o "IMGeo.xmi" "https://register.geostandaarden.nl/informatiemodel/imgeo/2.2/IMGeo.xmi"
echo "3f621deddf4ce7d9c4d0211907d757ded9c4a9ab3f4a06ceb3bc9f8749859123  IMGeo.xmi" | shasum -a 256 -c -
