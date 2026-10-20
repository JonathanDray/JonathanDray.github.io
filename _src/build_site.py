"""Build the artifact page and the GitHub Pages page from site/template.html."""
import base64
import re
import sys
from pathlib import Path

site = Path(sys.argv[1])
t = (site / "template.html").read_text(encoding="utf-8")


def data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()


# Artifact: fragment, no CV link, photo and screenshots inline
art = re.sub(r"<!--CV-->.*?<!--/CV-->", "", t, flags=re.S).replace("<!--BODY-->\n", "")
if "{{PHOTO_SRC}}" in art:
    art = art.replace("{{PHOTO_SRC}}", data_uri(site / "photo.jpg"))
art = re.sub(r"\{\{IMG:([\w-]+)\}\}", lambda m: data_uri(site / "img" / f"{m.group(1)}.jpg"), art)
(site / "jonathan-dray.html").write_text(art, encoding="utf-8")

# GitHub Pages: full document, photo.jpg, CV link kept
head, body = t.split("<!--BODY-->\n")
body = body.replace("<!--CV-->", "").replace("<!--/CV-->", "").replace("{{PHOTO_SRC}}", "photo.jpg")
body = re.sub(r"\{\{IMG:([\w-]+)\}\}", r"img/\1.jpg", body)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + '</head>\n<body>\n' + body + '</body>\n</html>\n')
(site / "pages-index.html").write_text(page, encoding="utf-8")
