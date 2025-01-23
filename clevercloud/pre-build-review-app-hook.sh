#!/bin/bash

mkdir build
mkdir build/.vite
cp ./clevercloud/manifest.json build/.vite/
mkdir 2024-frontend/build
mkdir 2024-frontend/build/.vite
cp ./clevercloud/manifest.json 2024-frontend/build/.vite/
clever service link-addon $1
echo "addon id: $1"
