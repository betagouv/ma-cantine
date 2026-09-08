#!/bin/bash

# Ensure Vite build output directories exist before collectstatic / Django startup
# (STATICFILES_DIRS points at both; django-vite reads each app's manifest.json)
mkdir -p build frontend/dist
