
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(255) NOT NULL,
    value NUMERIC NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

