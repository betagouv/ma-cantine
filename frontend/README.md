# frontend (Vue 2)

Legacy Vue 2 + Vuetify app, built with **Vite** and loaded by Django via [`django-vite`](https://github.com/MrBin99/django-vite) (`app="vue2"`).

## Setup

```
npm ci --ignore-scripts
```

### Dev (HMR on port 8080)

```
npm run dev
```

Serve the app through Django on port 8000 (not Vite’s port).

### Production build

```
npm run build
```

Outputs hashed assets + `dist/manifest.json` for Django.
