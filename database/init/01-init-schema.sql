CREATE DATABASE IF NOT EXISTS connector_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE connector_db;

-- API Keys table
CREATE TABLE api_keys (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key_id VARCHAR(16) UNIQUE NOT NULL,
    key_hash VARCHAR(128) UNIQUE NOT NULL,
    client_id VARCHAR(100) NOT NULL,
    scopes JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    rate_limit INT DEFAULT 1000,
    last_used TIMESTAMP NULL,
    INDEX idx_key_hash (key_hash),
    INDEX idx_client_id (client_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Query history table
CREATE TABLE query_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100),
    connection_id VARCHAR(100),
    query TEXT,
    execution_time FLOAT,
    row_count INT,
    status ENUM('success', 'error'),
    error_message TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_executed_at (executed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User permissions table
CREATE TABLE user_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id VARCHAR(100) NOT NULL,
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_permission (client_id, resource, action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
