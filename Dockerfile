FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    supervisor \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    mysql-server \
    redis-server \
    nginx \
    openssl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY connector-server/requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Create application directory
RUN mkdir -p /app
WORKDIR /app

# Copy application code
COPY connector-server/ /app/

# Copy database initialization
COPY database/init/ /docker-entrypoint-initdb.d/
COPY database/conf.d/ /etc/mysql/mysql.conf.d/

# Copy Redis config
COPY redis/redis.conf /etc/redis/redis.conf

# Copy Nginx config
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Create MySQL data directory
RUN mkdir -p /var/lib/mysql /var/log/mysql /var/run/mysqld \
    && chown -R mysql:mysql /var/lib/mysql /var/log/mysql /var/run/mysqld

# Create Redis data directory
RUN mkdir -p /var/lib/redis /var/log/redis \
    && chown -R redis:redis /var/lib/redis /var/log/redis

# Create Nginx directories
RUN mkdir -p /var/log/nginx /var/cache/nginx \
    && chown -R www-data:www-data /var/log/nginx /var/cache/nginx

# Create app user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# Create supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 3306 6379 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Switch to root for supervisor (services need different users)
USER root

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]