#!/bin/bash
# ./database/scripts/restore.sh
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# Decompress if gzipped
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c $BACKUP_FILE | docker exec -i mysql-db mysql -u root -p$MYSQL_ROOT_PASSWORD connector_db
else
    docker exec -i mysql-db mysql -u root -p$MYSQL_ROOT_PASSWORD connector_db < $BACKUP_FILE
fi

echo "Restore completed from: $BACKUP_FILE"