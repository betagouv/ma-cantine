#!/bin/bash

# Ensure Vite build output directories exist before collectstatic / Django startup
mkdir -p build frontend/dist
clever service link-addon $1 -v
echo "addon id: $1"
