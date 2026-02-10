#!/usr/bin/env bash
set -e

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install jupyter jupytext

echo "Run: source .venv/bin/activate"
echo "Then: jupyter notebook"
