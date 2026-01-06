# Stage 1: Build Vue App
FROM node:18-alpine as build-stage

WORKDIR /app

# Copy package info
# Context is root, so we copy frontend/package.json
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend .

# Build
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine as production-stage

# Copy build artifacts from previous stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy custom Nginx config
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
