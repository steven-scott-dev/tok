#!/bin/bash

# Ensure Python 3 and pip are available
apt-get update -y
apt-get install -y python3 python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run the watcher
python3 watcher.py

