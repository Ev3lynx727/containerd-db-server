-- ./database/init/03-init-permissions.sql
USE connector_db;

-- Grant permissions to connector_user
GRANT ALL PRIVILEGES ON connector_db.* TO 'connector_user'@'%';
GRANT REPLICATION CLIENT ON *.* TO 'connector_user'@'%';
GRANT REPLICATION SLAVE ON *.* TO 'connector_user'@'%';

-- Flush privileges
FLUSH PRIVILEGES;

-- Create additional users if needed
-- CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'readonly_pass';
-- GRANT SELECT ON connector_db.* TO 'readonly_user'@'%';

-- Create backup user
CREATE USER IF NOT EXISTS 'backup_user'@'%' IDENTIFIED BY 'backup_pass';
GRANT SELECT, LOCK TABLES, SHOW VIEW ON connector_db.* TO 'backup_user'@'%';
GRANT RELOAD, PROCESS, SUPER ON *.* TO 'backup_user'@'%';

FLUSH PRIVILEGES;