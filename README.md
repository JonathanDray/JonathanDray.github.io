# jonathandray.github.io

Site personnel de Jonathan Dray, en ligne sur https://jonathandray.github.io

- `index.html` : la page, sans dépendance externe
- `cv.pdf` : le CV lié depuis la page
- `img/` : images des projets
- `_src/` : source de la page (`template.html`) et scripts qui la génèrent ; non publié par GitHub Pages

## Mettre à jour
- Modifier `_src/template.html`, puis regénérer avec `_src/build_site.py` (voir l'en-tête du script).
- Nouveau CV : remplacer `cv.pdf` (même nom).
- Envoyer : `git add -A && git commit -m "..." && git push`.
