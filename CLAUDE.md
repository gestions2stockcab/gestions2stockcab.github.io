# Site de l'Espace dentaire Malakoff

Site statique (HTML/CSS/JS, sans framework) du centre de santé dentaire de Malakoff, généré par `build.py`.

## Commandes
- `python3 build.py` : régénère le dossier `site/` (pages, sitemap, robots, redirections).
- Aperçu local : `cd site && python3 -m http.server 8000`.
- Ne jamais modifier `site/` à la main : tout passe par `build.py`, `src/style.css`, `src/site.js` et `data/arts.json` (articles de soins).

## Le centre
- Espace dentaire Malakoff, 112 boulevard Gabriel Péri, 92240 Malakoff. Tél. 01 85 62 62 00 (joignable 24h/24, 7j/7 grâce à Recept AI).
- Domaine : espace-dentaire-malakoff.fr. Rendez-vous Doctolib (liens `DOC` et `ORTHO` en haut de `build.py`).
- Équipe : Dr Simon Atlan, Dr Laura Benchetrit, Dr Cyriele Berdah, Dr Pierre-Alexandre Bouvet, Dr Carla Levy (orthodontie), Dr Alicia Soussan (référente), Christina (assistante référente).

## Règles à respecter
- **Garder exactement les URL de l'ancien site** (`/c/<slug>/`) : référencement. Les anciennes pages non reprises sont dans `REDIR` (redirections).
- Français, apostrophes typographiques (’) et espaces propres. Ton sobre : pas de superlatifs ni de promesses (déontologie des chirurgiens-dentistes).
- Pas de cookies, pas de suivi, pas de polices externes (polices système). Les vidéos YouTube ne se chargent qu'au clic (youtube-nocookie).
- Accessibilité : contrastes, focus visible, liens explicites, `alt` sur les images.
- Thème clair (variables CSS en tête de `src/style.css`), logo SVG dans `build.py` (fonction `logo`).

## À faire
1. Mettre en ligne (GitHub Pages ou Netlify, voir `site/LISEZMOI.txt`), puis faire pointer le domaine.
2. Compléter l'hébergeur dans les mentions légales (« À COMPLÉTER ») et les faire relire.
3. Horaires : on garde ceux de l’ancien site (lundi au vendredi, 9h–19h). Doctolib affiche 9h–13h / 14h–19h30 : à mettre à jour côté Doctolib si besoin.
4. Ajouter les formations des praticiens et leurs photos (à fournir par l'équipe), puis une page « Accès » (métro, bus, accessibilité).
5. Remplacer le texte « Recept AI » par le vrai logo (fichier à fournir).
6. Vérifier la page « Vidéos orthodontie » (légendes des vidéos, le lien « Disjoncteur » a été retiré car doublon sur l'ancien site).
7. Après mise en ligne : Search Console (envoyer `sitemap.xml`), fiche Google Business (nom, adresse, téléphone, horaires, site, photos).
8. Option : chatbot IA (le chatbot actuel fonctionne par règles, voir `src/site.js`) : nécessiterait un petit service serveur.
