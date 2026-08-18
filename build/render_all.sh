#!/bin/zsh
# Full multi-pass build: page numbers + blank versos so chapters open on right-hand pages, then assemble the PDFs.
set -e
BUILD="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$BUILD")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
rm -f "$BUILD/pages.json" "$BUILD/blanks.json"
zsh "$BUILD/render.sh"
TOTAL=$(pdfinfo "$BUILD/book.pdf" | awk '/^Pages/{print $2}')
python3 "$BUILD/blanks.py" "$BUILD/pages.json" "$BUILD/blanks.json" "$TOTAL"
zsh "$BUILD/render.sh"
zsh "$BUILD/render.sh"
# cover
python3 "$BUILD/cover.py"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$BUILD/cover.pdf" "file://$BUILD/cover.html" 2>/dev/null
# web edition
cd "$BUILD" && MODE=web IMG_MODE=inline python3 book.py "$BUILD" >/dev/null
mkdir -p "$ROOT/print-files" "$ROOT/web"
python3 - "$BUILD" "$ROOT" <<'PY'
import sys
from pypdf import PdfReader, PdfWriter
B, R = sys.argv[1], sys.argv[2]
cov = PdfReader(B+'/cover.pdf'); inter = PdfReader(B+'/book.pdf')
w = PdfWriter(); w.add_page(cov.pages[0])
for p in inter.pages: w.add_page(p)
w.add_page(cov.pages[1]); w.write(R+'/Grandma-on-the-Farm.pdf')
w2 = PdfWriter()
for p in inter.pages: w2.add_page(p)
w2.write(R+'/print-files/Grandma-on-the-Farm-interior.pdf')
print(len(inter.pages), 'interior pages')
PY
cp "$BUILD/cover.pdf" "$ROOT/print-files/Grandma-on-the-Farm-cover.pdf"
cp "$BUILD/book_web.html" "$ROOT/web/Grandma-on-the-Farm-web.html"
cp "$BUILD/recipes.json" "$ROOT/recipes.json"
echo done
