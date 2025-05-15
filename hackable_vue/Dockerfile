# Stage 1: Build the Vue app
FROM node:20-alpine

# Set working directory
RUN mkdir -p /opt/app/ps-client

WORKDIR /opt/app/ps-client

# Install dependencies
COPY package.json .
RUN npm install

# Copy application code
COPY . .

CMD ["npm", "run", "build"]
