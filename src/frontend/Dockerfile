# Stage 1: Build Angular app
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy all project files and build the Angular application
COPY . .
RUN npm run build:ssr

# Stage 2: Serve the app using Node.js
FROM node:18-alpine

WORKDIR /app

# Copy build artifacts from the previous stage
COPY --from=build /app/dist /app/dist
COPY --from=build /app/package*.json /app/

# Install production dependencies
RUN npm install --production && npm prune --production

# Expose the port for the SSR server
EXPOSE 4000

# Start the Angular SSR server
CMD ["node", "--trace-uncaught", "--trace-warnings", "/app/dist/my-chat-frontend/server/main.js"]
