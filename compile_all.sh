#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

cd resource/
python3 compile_news.py
python3 compile_papers.py
python3 compile_patents.py

cd ..

python3 compile_index.py
