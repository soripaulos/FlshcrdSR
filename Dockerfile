# Multi-stage Dockerfile for Flutter Web App
FROM ubuntu:22.04 as builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    xz-utils \
    zip \
    libglu1-mesa \
    && rm -rf /var/lib/apt/lists/*

# Install Flutter
RUN curl -fsSL https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.16.0-stable.tar.xz | tar -xJ -C /opt
ENV PATH="$PATH:/opt/flutter/bin"

# Enable Flutter web
RUN flutter config --enable-web
RUN flutter doctor

# Set working directory
WORKDIR /app

# Copy pubspec files
COPY pubspec.* ./

# Get dependencies
RUN flutter pub get

# Copy source code
COPY . .

# Build for web
RUN flutter build web --release --web-renderer html

# Production stage
FROM nginx:alpine

# Copy built web app to nginx
COPY --from=builder /app/build/web /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]