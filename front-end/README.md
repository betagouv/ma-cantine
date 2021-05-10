# front-end

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## Ajouter un blog

Créez un nouveau fichier `.md` dans `front-end/src/assets/blog`. Le nom du fichier va être dans l'url de l'article donc privilégiez un nom du type 'un-article-interessant' (sans éspaces ou accents).

Avant le contenu du blog, ajoutez les metadonnées comme ça:

```
---
title: Un article intéressant
date: 2021-01-30
tagline: Une courte description du article qui va être affichée dans le 'tuile' du blog.
---
```

N'utilisez pas le heading `#` dans le contenu du article, seulement `##` ou plus, car le titre dans les metadonées va être le premier heading.

Lisez plus d'information du [format markdown](https://guides.github.com/features/mastering-markdown/).