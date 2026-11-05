#!/bin/sh
# Download the comparison skills at pinned commits into eval/.cache (not redistributed).
set -e
cd "$(dirname "$0")"
get() {
  [ -d ".cache/$1" ] || git clone -q "https://github.com/$2" ".cache/$1"
  git -C ".cache/$1" fetch -q --depth 1 origin "$3"
  git -C ".cache/$1" checkout -q "$3"
}
get caveman JuliusBrussee/caveman 2e068f735253cce28256744804785f01887d9646
get ponytail DietrichGebert/ponytail 96608e078b2d5ea607c5c3b8b5a54d1c1fba6846
echo "arms ready in eval/.cache"
