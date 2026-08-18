import subprocess, re, json, sys
pdf, out = sys.argv[1], sys.argv[2]
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
pages = txt.split('\f')
found = {}
for i, p in enumerate(pages, 1):
    for k in re.findall(r'⟦([^⟧]+)⟧', p):
        found.setdefault(k, i)
json.dump(found, open(out, 'w'))
print(len(pages)-1, 'pages;', len(found), 'markers')
