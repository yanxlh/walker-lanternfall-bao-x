#!/usr/bin/env python3
"""Convert Bao's A4 GDD (Lanternfall_Game_Design_Document.docx, v0.3) to Markdown so the godot-gdd checker can read
it. Text is copied as written: Title -> #, Heading 1 -> ##, Heading 2 -> ###, bullets -> "- ", tables -> pipe tables.
The two embedded images are omitted; their caption paragraphs stay. Needs python-docx.

    python docx_to_md.py Lanternfall_Game_Design_Document.docx > GDD-v0.3.md
"""
import hashlib, sys
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

src = sys.argv[1]
doc = Document(src)
sha = hashlib.sha256(open(src, "rb").read()).hexdigest()
out = [f"<!-- Converted from {src} (SHA-256 {sha}) by pitch/gdd/docx_to_md.py. Text as written; images omitted. -->", ""]
for el in doc.element.body.iterchildren():
    tag = el.tag.split("}")[1]
    if tag == "p":
        p = Paragraph(el, doc)
        text, style = p.text.strip(), p.style.name
        if not text:
            continue
        if style.startswith(("Title", "Heading")) and out and out[-1].startswith("- "):
            out.append("")
        if style == "Title":
            out += [f"# {text}", ""]
        elif style == "Heading 1":
            out += [f"## {text}", ""]
        elif style == "Heading 2":
            out += [f"### {text}", ""]
        elif style.startswith("List"):
            out.append(f"- {text}")
        else:
            if out and out[-1].startswith("- "):
                out.append("")
            out += [text, ""]
    elif tag == "tbl":
        if out and out[-1].startswith("- "):
            out.append("")
        t = Table(el, doc)
        rows = [[c.text.strip().replace("|", "\\|").replace("\n", " ") for c in r.cells] for r in t.rows]
        out.append("| " + " | ".join(rows[0]) + " |")
        out.append("|" + "---|" * len(rows[0]))
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
        out.append("")
print("\n".join(out).rstrip() + "\n", end="")
