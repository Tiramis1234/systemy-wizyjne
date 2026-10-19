FROM node:22-slim

WORKDIR /frontend

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 4173
# vite preview serves the built app and proxies /api to the backend (see vite.config.js).
CMD ["npx", "vite", "preview", "--host", "0.0.0.0", "--port", "4173"]
