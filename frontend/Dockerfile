FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Install serve to run the built application
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Command to serve the built application
CMD ["serve", "-s", "dist", "-l", "3000"] 