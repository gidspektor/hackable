# Use multi-architecture Node.js image
FROM node:20-alpine

# Set working directory
RUN mkdir -p /opt/app/ps-client

WORKDIR /opt/app/ps-client

# Install dependencies
COPY package.json .
RUN npm install

# Copy application code
COPY . .

# Expose frontend port
EXPOSE 80
EXPOSE 5137

CMD ["npm", "run", "build"]
