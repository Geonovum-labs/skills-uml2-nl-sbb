#!/usr/bin/env bash
# Haalt het testmodel uit het Geonovum-register en controleert de checksum.
# Het model zelf staat niet in deze repository.
set -eu
curl -sSfL -o "IMGeluid_v3_1_1.xmi" "https://register.geostandaarden.nl/informatiemodel/img/3.1.1/IMGeluid_v3_1_1.xmi"
echo "74ba7e772e9998e58645879eb401fd18416da5b289ef9bb2780f8f34ee154f3b  IMGeluid_v3_1_1.xmi" | shasum -a 256 -c -
