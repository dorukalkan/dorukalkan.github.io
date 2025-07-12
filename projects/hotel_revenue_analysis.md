## Hotel Revenue Analysis

### Overview

#### Project description

This is an exploratory data analysis and data visualization project on a hotel dataset with aims to assess revenue performance and discover trends. EDA was carried out in MySQL by developing queries, and then the findings were visualized in Power BI by connecting the database. I focused mainly on the following questions:

- Is hotel revenue growing by year? How does it differ by hotel type?
- Should the company increase its parking lot size? Is there any trends in guests with personal cars?
- What other trends can be seen in the data? Is there seasonality?

SQL script and interactive dashboard (.pbix) files can be accessed [here](https://github.com/dorukalkan/dorukalkan.github.io/tree/main/assets/hotel_rev_analysis_appx).

#### Executive summary
Key findings include:  
➡️ There is a drastic drop in revenue in 2020, possibly due to COVID-19 pandemic. Further analysis is needed to see if this is really the case.

➡️ Current parking lot size is enough and there is no need for improvements.

➡️ Revenue spikes in the summer for resort hotels and in holiday season for city hotels. This trend can be capitalized on more with additional tailored marketing campaigns.

Find the comprehensive insights and recommendations section at the end of this page.

#### Table of contents

1. About dataset
2. Data preparation
3. Exploratory data analysis
4. Dashboard
5. Insights & recommendations

### 1. About dataset

Dataset is taken from [AbsentData](https://absentdata.com) and contains information on hotel bookings of an accommodation company. It consists of three CSV files for three years: 2018, 2019, and 2020. The dataset has several relevant columns for this project: the average daily rate of bookings, hotel types (city hotel versus resort hotel), weekday and weekend stays, arrival date, and parking spaces.

### 2. Data preparation

I started by creating a database in MySQL and importing the CSV files. Since the dataset consisted multiple files, I used the following query to create a CTE and combine them:

````SQL
USE `hotel_db`; 

WITH revenues AS ( 
SELECT * FROM hotel_db.rev_2018 
UNION 
SELECT * FROM hotel_db.rev_2019 
UNION 
SELECT * FROM hotel_db.rev_2020)
````

### 3. Exploratory data analysis

There were no separate column displaying revenue in the dataset, so I had to calculate an estimate by taking the sum of weekday and weekend stays, then multiplying it by average daily rate.

````SQL
SELECT arrival_date_year AS arrival_date, 
	ROUND(SUM((stays_in_week_nights + stays_in_weekend_nights) * adr)) AS revenue 
FROM revenues 
GROUP BY arrival_date_year;
````

I did a similar calculation to calculate the revenues by hotel type: city hotels and resort hotels, which would later be useful for comparing their performance.

````SQL
SELECT arrival_date_year AS arrival_date, hotel AS hotel_type, ROUND(SUM((stays_in_week_nights + stays_in_weekend_nights) * adr)) AS revenue 
FROM revenues 
GROUP BY arrival_date_year, hotel 
ORDER BY hotel_type, revenue DESC;
````

Lastly, I created another column showing the car parking percentage of customers.

````SQL
SELECT 
	arrival_date_year, hotel, SUM((stays_in_week_nights + stays_in_weekend _nights) * adr) AS revenue, 
	CONCAT(ROUND((SUM(required_car_parking_spaces) / SUM(stays_in_week_nights + stays_in_weekend_nights)) * 100, 2), '%') AS parking_percentage 
FROM revenues 
GROUP BY arrival_date_year, hotel;
````

### 4. Dashboard

I created an interactive dashboard utilizing the previous queries to visualize key performance metrics such as total revenue, ADR, total hotel stays, required parking spaces. I added charts with trendlines, date sliders, and a revenue table as a quick and easy way to get a sense of various KPIs.

<a href="https://github.com/dorukalkan/dorukalkan.github.io/blob/d45232ae1867a4c3087fa352517cb71854112760/assets/hotel_rev_analysis_appx/hotel_rev_dashboard.png" target="_blank">
  <img src="assets/hotel_rev_analysis_appx/hotel_rev_dashboard.png" alt="Final interactive Power BI dashboard">
</a>

### 5. Insights & recommendations

📌 Hotel revenue peaked in 2019 for both hotel types.  
2018 has the lowest revenue. The dataset is not complete for 2020 (doesn’t contain the last quarter), but when compared only by the first three quarters, 2020 falls short of 2019. 2019 has $3,91M in revenue for the first three quarters while 2020 has $3,51M. There is a drop in overall hotel stays in parallel. The drop is most pronounced in the summer months, and might be a product of the COVID-19 pandemic. By mid-2020 COVID-19 was already widespread and global lockdowns were in place, which can account for the performance drop in 2020 summer season.  
_Recommendation:_ 2020 revenue dip should be more closely examined to understand if it really is an effect of the pandemic, or whether any other factor has influence on it.

📌 Required parking space consists only a small percentage.  
The dataset shows that there is a slight increase in overall required parking space, but it actually consists a very small percentage. Neither hotel type exhibits a drastic demand for parking space.  
_Recommendation:_ There is no need to increase the parking lot size.

📌 Seasonality and holiday season effects can be seen for both hotel types.  
Hotel stays and overall revenue increase by large during the summer months for resort hotels. There is another spike in the holiday season, with city hotels seeing a larger demand than resorts.  
_Recommendation:_ Tailored marketing campaigns can be conducted for resort hotels during summer and city hotels during holiday season to maximize revenue in these peak periods.
