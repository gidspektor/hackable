# Use multi-architecture Node.js image
FROM node:20-slim

# Set working directory
WORKDIR /vue/app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy application code
COPY . /vue/app

# Expose frontend port
EXPOSE 80

CMD ["npm", "-run", "build"]
