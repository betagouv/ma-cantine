#!/bin/bash

# Ensure Vite build output directory exists before collectstatic / Django startup
mkdir -p build
clever service link-addon $1 -v
echo "addon id: $1"
