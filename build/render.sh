#!/bin/zsh
# Re-render the book from build/merged.json. Run from anywhere: zsh build/render.sh
set -e
BUILD="$(cd "$(dirname "$0")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cd "$BUILD"
MODE=print python3 book.py "$BUILD" >/dev/null
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$BUILD/book.pdf" --virtual-time-budget=60000 "file://$BUILD/book.html" 2>/dev/null
python3 paginate.py "$BUILD/book.pdf" "$BUILD/pages.json"
