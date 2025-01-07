# Use Node.js image
FROM node:20

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application code
COPY ./ ./

# Build Vue.js application
RUN npm run build

# Use nginx to serve static files
FROM nginx:latest
COPY --from=0 /app/dist /usr/share/nginx/html

# Expose frontend port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
