FROM mysql:8.0-debian

# Install additional tools
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy custom configuration
COPY conf.d/*.cnf /etc/mysql/conf.d/

# Copy initialization scripts
COPY init/*.sql /docker-entrypoint-initdb.d/

# Create backup directory
RUN mkdir -p /backups && chmod 755 /backups

# Add health check script
COPY scripts/healthcheck.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/healthcheck.sh

# Set proper permissions
RUN chown -R mysql:mysql /var/lib/mysql /var/log/mysql

EXPOSE 3306

# Use custom entrypoint if needed
# COPY docker/entrypoint.sh /usr/local/bin/
# ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["mysqld"]