-- ./database/init/02-init-data.sql
USE connector_db;

-- Insert initial users (for development/testing)
INSERT INTO users (username, email, hashed_password, is_active, scopes)
VALUES
('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fM9q0K1G', true, 'read,write,admin'),
('user', 'user@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fM9q0K1G', true, 'read,write');

-- Insert initial API keys (for development/testing)
INSERT INTO api_keys (key_id, key_hash, client_id, scopes, created_at, is_active, rate_limit)
VALUES
('dev-key-001', SHA2('dev-api-key-001', 256), 'development-client', '["read", "write", "admin"]', NOW(), true, 1000),
('test-key-001', SHA2('test-api-key-001', 256), 'testing-client', '["read", "write"]', NOW(), true, 500);

-- Insert initial user permissions
INSERT INTO user_permissions (client_id, resource, action, granted_at)
VALUES
('development-client', 'database', 'read', NOW()),
('development-client', 'database', 'write', NOW()),
('development-client', 'database', 'admin', NOW()),
('testing-client', 'database', 'read', NOW()),
('testing-client', 'database', 'write', NOW());

-- Insert sample query history
INSERT INTO query_history (user_id, connection_id, query, execution_time, row_count, status, executed_at)
VALUES
('admin', 'dev-connection', 'SELECT 1', 0.001, 1, 'success', NOW()),
('user', 'dev-connection', 'SHOW TABLES', 0.005, 3, 'success', NOW());