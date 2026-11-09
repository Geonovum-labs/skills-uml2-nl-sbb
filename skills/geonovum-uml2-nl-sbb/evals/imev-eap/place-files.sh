#!/usr/bin/env bash
# Haalt het testmodel uit het Geonovum-register en controleert de checksum.
# Het model zelf staat niet in deze repository.
set -eu
curl -sSfL -o "IMEV3.0.2_10072025.zip" "https://register.geostandaarden.nl/informatiemodel/imev/3.0.2/IMEV3.0.2_10072025.zip"
echo "cf9083ef9f59d40442d01c40c301d19f1182079032b2ddecaf3313a0184c5e62  IMEV3.0.2_10072025.zip" | shasum -a 256 -c -
