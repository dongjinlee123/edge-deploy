# Stage 1: build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
# VITE_GRPC_HOST must be set at build time — Vite bakes it into the JS bundle.
# Pass the server's IP/hostname so browsers reach the correct Envoy endpoint.
# Example: docker build --build-arg VITE_GRPC_HOST=http://192.168.11.136:8080 .
ARG VITE_GRPC_HOST=http://localhost:8001
ENV VITE_GRPC_HOST=$VITE_GRPC_HOST
RUN npm run build

# Stage 2: serve
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
