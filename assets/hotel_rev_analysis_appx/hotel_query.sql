USE `hotel_db`;

WITH revenues AS (
SELECT * FROM hotel_db.rev_2018
UNION
SELECT * FROM hotel_db.rev_2019
UNION
SELECT * FROM hotel_db.rev_2020)

-- calculating total revenue per year
SELECT arrival_date_year AS arrival_date,
	ROUND(SUM((stays_in_week_nights + stays_in_weekend_nights) * adr)) AS revenue
FROM revenues
GROUP BY arrival_date_year;


-- calculating revenue per year by hotel type
SELECT arrival_date_year AS arrival_date, 
	hotel AS hotel_type,
	ROUND(SUM((stays_in_week_nights + stays_in_weekend_nights) * adr)) AS revenue
FROM revenues
GROUP BY arrival_date_year, hotel
ORDER BY hotel_type, revenue DESC;


-- calculating required parking space
SELECT
arrival_date_year, hotel,
SUM((stays_in_week_nights + stays_in_weekend _nights) * adr) AS revenue,
CONCAT(ROUND((SUM(required_car_parking_spaces) / SUM(stays_in_week_nights +
stays_in_weekend_nights)) * 100, 2), '%') AS parking_percentage
FROM revenues GROUP BY arrival_date_year, hotel;
