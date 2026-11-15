
-- ==========================================
-- ATMOSYNC ANALYTICS QUERIES
-- ==========================================

-- 1. Display all containers
SELECT *
FROM containers;


-- 2. Display sensor information
SELECT *
FROM sensor_events;


-- 3. Get average temperature per container
SELECT
    container_id,
    AVG(temperature) AS average_temperature
FROM sensor_events
GROUP BY container_id;


-- 4. Get maximum temperature per container
SELECT
    container_id,
    MAX(temperature) AS maximum_temperature
FROM sensor_events
GROUP BY container_id;


-- 5. Identify containers with high temperature
SELECT
    container_id,
    temperature,
    humidity,
    event_timestamp
FROM sensor_events
WHERE temperature > 8;


-- 6. Identify containers with high humidity
SELECT
    container_id,
    humidity,
    event_timestamp
FROM sensor_events
WHERE humidity > 80;


-- 7. Get weather information
SELECT *
FROM weather;


-- 8. Calculate average weather temperature
SELECT
    location,
    AVG(temperature) AS average_temperature
FROM weather
GROUP BY location;


-- 9. Compare commodity market prices
SELECT
    commodity_name,
    market_name,
    market_location,
    price,
    currency
FROM commodity_market_prices
ORDER BY commodity_name, price ASC;


-- 10. Find cheapest market for each commodity
SELECT
    commodity_name,
    market_name,
    MIN(price) AS minimum_price
FROM commodity_market_prices
GROUP BY commodity_name;


-- 11. Display transportation routes
SELECT *
FROM market_routes;


-- 12. Find shortest transportation routes
SELECT
    origin,
    destination,
    distance_km,
    estimated_duration_hours
FROM market_routes
ORDER BY distance_km ASC;


-- 13. Container and sensor information together
SELECT
    c.container_id,
    c.origin,
    c.destination,
    s.temperature,
    s.humidity,
    s.event_timestamp
FROM containers c
JOIN sensor_events s
ON c.container_id = s.container_id;


-- 14. Container monitoring summary
SELECT
    container_id,
    COUNT(*) AS total_sensor_readings,
    AVG(temperature) AS avg_temperature,
    MAX(temperature) AS max_temperature,
    AVG(humidity) AS avg_humidity
FROM sensor_events
GROUP BY container_id;
