# A imagem oficial oferece variantes amd64 e arm64; sem fixar plataforma.
FROM nginx:alpine
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html styles.css script.js /usr/share/nginx/html/
COPY img/guilherme.jpeg img/favicon.ico img/favicon-16x16.png img/favicon-32x32.png img/apple-touch-icon.png img/android-chrome-192x192.png img/android-chrome-512x512.png img/site.webmanifest /usr/share/nginx/html/img/
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
