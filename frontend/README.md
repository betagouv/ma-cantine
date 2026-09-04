# frontend (Vue 2)

Legacy Vue 2 + Vuetify app, built with **Vite**. Django still loads assets via `django-webpack-loader` (`{% render_bundle 'app' %}`), using a Vite plugin that writes `dist/webpack-stats.json`.

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

Outputs hashed assets + `dist/webpack-stats.json` for Django.
