#!/bin/bash
# ./database/scripts/backup.sh
BACKUP_DIR="/opt/database/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup MySQL database
docker exec mysql-db mysqldump -u root -p$MYSQL_ROOT_PASSWORD connector_db > $BACKUP_DIR/mysql_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/mysql_backup_$DATE.sql

echo "Backup completed: $BACKUP_DIR/mysql_backup_$DATE.sql.gz"