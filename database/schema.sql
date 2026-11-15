
-- ==========================================
-- ATMOSYNC DATABASE SCHEMA
-- ==========================================

PRAGMA foreign_keys = ON;

-- 1. CONTAINERS TABLE
CREATE TABLE IF NOT EXISTS containers (
    container_id TEXT PRIMARY KEY,
    container_type TEXT,
    origin TEXT,
    destination TEXT,
    departure_time TEXT,
    expected_arrival TEXT,
    status TEXT
);

-- 2. SENSOR EVENTS TABLE
CREATE TABLE IF NOT EXISTS sensor_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    container_id TEXT NOT NULL,
    event_timestamp TEXT,
    temperature REAL,
    humidity REAL,
    location TEXT,
    FOREIGN KEY (container_id)
        REFERENCES containers(container_id)
);

-- 3. WEATHER TABLE
CREATE TABLE IF NOT EXISTS weather (
    weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    observation_time TEXT,
    temperature REAL,
    humidity REAL,
    rainfall REAL,
    wind_speed REAL,
    weather_condition TEXT
);

-- 4. COMMODITY MARKET PRICES TABLE
CREATE TABLE IF NOT EXISTS commodity_market_prices (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    commodity_name TEXT,
    market_name TEXT,
    market_location TEXT,
    price REAL,
    currency TEXT DEFAULT 'INR',
    price_timestamp TEXT
);

-- 5. MARKET ROUTES TABLE
CREATE TABLE IF NOT EXISTS market_routes (
    route_id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT,
    destination TEXT,
    distance_km REAL,
    estimated_duration_hours REAL,
    transportation_cost REAL,
    route_status TEXT
);

-- ==========================================
-- INDEXES FOR FASTER DATA RETRIEVAL
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_sensor_container
ON sensor_events(container_id);

CREATE INDEX IF NOT EXISTS idx_sensor_timestamp
ON sensor_events(event_timestamp);

CREATE INDEX IF NOT EXISTS idx_weather_location
ON weather(location);

CREATE INDEX IF NOT EXISTS idx_market_commodity
ON commodity_market_prices(commodity_name);

CREATE INDEX IF NOT EXISTS idx_routes_origin
ON market_routes(origin);
