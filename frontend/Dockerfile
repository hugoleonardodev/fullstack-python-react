# Frontend Dockerfile
FROM node:18-alpine AS build

WORKDIR /frontend

# Copy package files
# COPY package.json package-lock.json public/ src/ ./
# COPY package-lock.json ./
# COPY public/ ./
# COPY src/ ./
COPY . .

# Install dependencies
RUN npm i

# Copy all frontend files
# COPY frontend/ ./

# Build the React app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /frontend/build /usr/share/nginx/html

# Copy nginx config if needed
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]