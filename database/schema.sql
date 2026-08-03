-- =====================================================
-- Database
-- =====================================================

CREATE DATABASE IF NOT EXISTS hpc_thermal_prediction;
USE hpc_thermal_prediction;

-- =====================================================
-- Temperature Table
-- =====================================================
CREATE TABLE IF NOT EXISTS cpu_usage (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    node VARCHAR(50) NOT NULL,
    socket INT NOT NULL,
    core INT NOT NULL,
    cpu_usage FLOAT NOT NULL,

    UNIQUE KEY unique_usage (
        timestamp,
        node,
        socket,
        core
    )
);

-- =====================================================
-- Frequency Table
-- =====================================================

CREATE TABLE IF NOT EXISTS frequency (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    node VARCHAR(50) NOT NULL,
    socket INT NOT NULL,
    core INT NOT NULL,
    frequency FLOAT NOT NULL,

    UNIQUE KEY unique_frequency (
        timestamp,
        node,
        socket,
        core
    )
);

-- =====================================================
-- CPU Usage Table
-- =====================================================

CREATE TABLE IF NOT EXISTS cpu_usage (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    node VARCHAR(50) NOT NULL,
    socket INT NOT NULL,
    core INT NOT NULL,
    cpu_usage FLOAT NOT NULL,

    UNIQUE KEY unique_usage (
        timestamp,
        node,
        socket,
        core
    )
);

-- =====================================================
-- Power Table
-- =====================================================

CREATE TABLE IF NOT EXISTS power (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    node VARCHAR(50) NOT NULL,
    socket INT NOT NULL,

    cpu_power FLOAT NOT NULL,
    memory_power FLOAT NOT NULL,
    node_power FLOAT NOT NULL,

    UNIQUE KEY unique_power (
        timestamp,
        node,
        socket
    )
);

-- =====================================================
-- Energy Table
-- =====================================================

CREATE TABLE IF NOT EXISTS energy (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    node VARCHAR(50) NOT NULL,
    socket INT NOT NULL,

    cpu_energy DOUBLE NOT NULL,
    memory_energy DOUBLE NOT NULL,
    node_energy DOUBLE NOT NULL,

    UNIQUE KEY unique_energy (
        timestamp,
        node,
        socket
    )
);

-- =====================================================
-- Temperature Prediction Table
-- =====================================================

CREATE TABLE IF NOT EXISTS temperature_predictions (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    timestamp DATETIME NOT NULL,

    prediction_for DATETIME NOT NULL,

    node VARCHAR(50) NOT NULL,

    socket INT NOT NULL,

    core INT NOT NULL,

    predicted_temperature FLOAT NOT NULL,

    actual_temperature FLOAT DEFAULT NULL,

    prediction_error FLOAT DEFAULT NULL,

    model_version VARCHAR(100) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);