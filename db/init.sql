CREATE TABLE IF NOT EXISTS vulnerabilities (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50),
    severity VARCHAR(20),
    description TEXT,
    detected_on TIMESTAMP,
    remediation_status VARCHAR(20)
);
