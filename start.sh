#!/bin/bash

# Ensure pip3 is available
apt-get update -y
apt-get install -y python3 python3-pip

# Install Python dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run your watcher
python3 watcher.py
