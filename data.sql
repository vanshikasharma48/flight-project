SELECT *
FROM flights_cleaned
LIMIT 10;
SELECT COUNT(*) AS total_flights
FROM flights_cleaned;
SELECT AVG(arr_delay) AS avg_arrival_delay
FROM flights_cleaned;
SELECT airline,
AVG(arr_delay) AS avg_delay
FROM flights_cleaned
GROUP BY airline
ORDER BY avg_delay DESC;
SELECT *
FROM flights_cleaned
WHERE arr_delay > 60;
SELECT origin,
dest,
AVG(arr_delay) AS avg_delay
FROM flights_cleaned
GROUP BY origin, dest
ORDER BY avg_delay DESC
LIMIT 10;
SELECT month,
AVG(arr_delay) AS avg_delay
FROM flights_cleaned
GROUP BY month
ORDER BY month;
SELECT origin,
AVG(arr_delay) AS avg_delay
FROM flights_cleaned
GROUP BY origin
ORDER BY avg_delay DESC;
SELECT *
FROM flights_cleaned
WHERE distance > 2000;
SELECT delay_category,
COUNT(*) AS flights
FROM flights_cleaned
GROUP BY delay_category;