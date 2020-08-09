# Project 1: Query Project

- In the Query Project, you will get practice with SQL while learning about
  Google Cloud Platform (GCP) and BiqQuery. You'll answer business-driven
  questions using public datasets housed in GCP. To give you experience with
  different ways to use those datasets, you will use the web UI (BiqQuery) and
  the command-line tools, and work with them in Jupyter Notebooks.

#### Problem Statement

- You're a data scientist at Lyft Bay Wheels (https://www.lyft.com/bikes/bay-wheels), formerly known as Ford GoBike, the
  company running Bay Area Bikeshare. You are trying to increase ridership, and
  you want to offer deals through the mobile app to do so. 
  
- What deals do you offer though? Currently, your company has several options which can change over time.  Please visit the website to see the current offers and other marketing information. Frequent offers include: 
  * Single Ride 
  * Monthly Membership
  * Annual Membership
  * Bike Share for All
  * Access Pass
  * Corporate Membership
  * etc.

- Through this project, you will answer these questions: 

  * What are the 5 most popular trips that you would call "commuter trips"? 
  
  * What are your recommendations for offers (justify based on your findings)?

- Please note that there are no exact answers to the above questions, just like in the proverbial real world.  This is not a simple exercise where each question above will have a simple SQL query. It is an exercise in analytics over inexact and dirty data. 

- You won't find a column in a table labeled "commuter trip".  You will find you need to do quite a bit of data exploration using SQL queries to determine your own definition of a communter trip.  In data exploration process, you will find a lot of dirty data, that you will need to either clean or filter out. You will then write SQL queries to find the communter trips.

- Likewise to make your recommendations, you will need to do data exploration, cleaning or filtering dirty data, etc. to come up with the final queries that will give you the supporting data for your recommendations. You can make any recommendations regarding the offers, including, but not limited to: 
  * market offers differently to generate more revenue 
  * remove offers that are not working 
  * modify exising offers to generate more revenue
  * create new offers for hidden business opportunities you have found
  * etc. 

#### All Work MUST be done in the Google Cloud Platform (GCP) / The Majority of Work MUST be done using BigQuery SQL / Usage of Temporary Tables, Views, Pandas, Data Visualizations

A couple of the goals of w205 are for students to learn how to work in a cloud environment (such as GCP) and how to use SQL against a big data data platform (such as Google BigQuery).  In keeping with these goals, please do all of your work in GCP, and the majority of your analytics work using BigQuery SQL queries.

You can make intermediate temporary tables or views in your own dataset in BigQuery as you like.  Actually, this is a great way to work!  These make data exploration much easier.  It's much easier when you have made temporary tables or views with only clean data, filtered rows, filtered columns, new columns, summary data, etc.  If you use intermediate temporary tables or views, you should include the SQL used to create these, along with a brief note mentioning that you used the temporary table or view.

In the final Jupyter Notebook, the results of your BigQuery SQL will be read into Pandas, where you will use the skills you learned in the Python class to print formatted Pandas tables, simple data visualizations using Seaborn / Matplotlib, etc.  You can use Pandas for simple transformations, but please remember the bulk of work should be done using Google BigQuery SQL.

#### GitHub Procedures

In your Python class you used GitHub, with a single repo for all assignments, where you committed without doing a pull request.  In this class, we will try to mimic the real world more closely, so our procedures will be enhanced. 

Each project, including this one, will have it's own repo.

Important:  In w205, please never merge your assignment branch to the master branch. 

Using the git command line: clone down the repo, leave the master branch untouched, create an assignment branch, and move to that branch:
- Open a linux command line to your virtual machine and be sure you are logged in as jupyter.
- Create a ~/w205 directory if it does not already exist `mkdir ~/w205`
- Change directory into the ~/w205 directory `cd ~/w205`
- Clone down your repo `git clone <https url for your repo>`
- Change directory into the repo `cd <repo name>`
- Create an assignment branch `git branch assignment`
- Checkout the assignment branch `git checkout assignment`

The previous steps only need to be done once.  Once you your clone is on the assignment branch it will remain on that branch unless you checkout another branch.

The project workflow follows this pattern, which may be repeated as many times as needed.  In fact it's best to do this frequently as it saves your work into GitHub in case your virtual machine becomes corrupt:
- Make changes to existing files as needed.
- Add new files as needed
- Stage modified files `git add <filename>`
- Commit staged files `git commit -m "<meaningful comment about your changes>"`
- Push the commit on your assignment branch from your clone to GitHub `git push origin assignment`

Once you are done, go to the GitHub web interface and create a pull request comparing the assignment branch to the master branch.  Add your instructor, and only your instructor, as the reviewer.  The date and time stamp of the pull request is considered the submission time for late penalties. 

If you decide to make more changes after you have created a pull request, you can simply close the pull request (without merge!), make more changes, stage, commit, push, and create a final pull request when you are done.  Note that the last data and time stamp of the last pull request will be considered the submission time for late penalties.

---

## Parts 1, 2, 3

We have broken down this project into 3 parts, about 1 week's work each to help you stay on track.

**You will only turn in the project once  at the end of part 3!**

- In Part 1, we will query using the Google BigQuery GUI interface in the cloud.

- In Part 2, we will query using the Linux command line from our virtual machine in the cloud.

- In Part 3, we will query from a Jupyter Notebook in our virtual machine in the cloud, save the results into Pandas, and present a report enhanced by Pandas output tables and simple data visualizations using Seaborn / Matplotlib.

---

## Part 1 - Querying Data with BigQuery

### SQL Tutorial

Please go through this SQL tutorial to help you learn the basics of SQL to help you complete this project.

SQL tutorial: https://www.w3schools.com/sql/default.asp

### Google Cloud Helpful Links

Read: https://cloud.google.com/docs/overview/

BigQuery: https://cloud.google.com/bigquery/

Public Datasets: Bring up your Google BigQuery console, open the menu for the public datasets, and navigate to the the dataset san_francisco.

- The Bay Bike Share has two datasets: a static one and a dynamic one.  The static one covers an historic period of about 3 years.  The dynamic one updates every 10 minutes or so.  THE STATIC ONE IS THE ONE WE WILL USE IN CLASS AND IN THE PROJECT. The reason is that is much easier to learn SQL against a static target instead of a moving target.

- (USE THESE TABLES!) The static tables we will be using in this class are in the dataset **san_francisco** :

  * bikeshare_stations

  * bikeshare_status

  * bikeshare_trips

- The dynamic tables are found in the dataset **san_francisco_bikeshare**

### Some initial queries

Paste your SQL query and answer the question in a sentence.  Be sure you properly format your queries and results using markdown. 

- **What's the size of this dataset? (i.e., how many trips)**

```sql
SELECT count(*)
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```
::: notes The size of this dataset/number of trips is 983,648. :::

- **What is the earliest start date and time and latest end date and time for a trip?**


```sql
SELECT min(start_date) AS st_time, max(end_date) AS end_time
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
```


| st_time | end_time  | 
| :-----: | :-: | 
| 2013-08-29 09:08:00 UTC | 2016-08-31 23:48:00 UTC |


::: notes Across all trips, the earliest start date and time is '2013-08-29 09:08:00 UTC' and the latest end date and time is '2016-08-31 23:48:00 UTC'. :::


```sql
SELECT min(start_date) AS st_time, max(end_date) AS end_time, trip_id, (duration_sec/3600) AS hours 
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
GROUP BY trip_id, hours
ORDER BY hours DESC
LIMIT 1
```


| st_time | end_time  |  trip_id  | hours |
| :-----: | :-: | :-: | :-: | 
| 2014-12-06 21:59:00 UTC | 2015-06-24 20:18:00 UTC |  568474  | 4797.333333333333 |


::: notes For a single trip, the earliest start date and time is '2014-12-06 21:59:00 UTC' and latest end date and time is '2015-06-24 20:18:00 UTC'. :::

- **How many bikes are there?**

```sql
SELECT count(distinct bike_number) AS total_bikes
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```
::: notes There are 700 bikes. :::

### Questions of your own
- Make up 3 questions and answer them using the Bay Area Bike Share Trips Data.  These questions MUST be different than any of the questions and queries you ran above.

- **Question 1: What are the 5 most popular hours to use the bike share service?**

  * *Answer*: The most popular hours are 4-6 PM and 8-9 AM, with 5 PM being the most popular hour to use the bike share service. These are common starting/ending work hours, indicating that people might be using the bike share service as a vehicle in their commute.
  
  
| hr | popularTime  | 
| :-----: | :-: | 
| 17 | 46936 |
| 8 | 43730 |
| 16 | 43254 |
| 9 | 41649 |
| 18 | 40350 |
  
  
  
  * *SQL query*:

```sql
WITH tempTable AS ( 
    SELECT start_date, 
    EXTRACT(HOUR FROM start_date) AS hr 
    FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
    GROUP BY start_date) 
SELECT hr, count(hr) AS popularTime 
FROM tempTable 
GROUP BY hr 
ORDER BY popularTime DESC 
LIMIT 5;
```


- **Question 2: How long, on average, does a round trip take? One way?**

  * *Answer*: A round trip, on average, takes about 99 minutes. A one way trip, on average, takes about 14 minutes. So, round trips are substantially longer than one way trips.
  
| avg_RoundTrip | 
| :-----: | 
| 99.02484007863502 |
  
  
| avg_OneWay | 
| :-----: | 
| 14.219261749410407 |  
  
  * *SQL query*:
  
  ```sql
  WITH tempTable AS (
    SELECT (duration_sec/60) AS time, 
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
    WHERE start_station_id = end_station_id)
  SELECT AVG(time) AS avg_RoundTrip
  FROM tempTable;

  WITH tempTable AS (
    SELECT (duration_sec/60) AS time, 
    FROM `bigquery-public-data.san_francisco.bikeshare_trips`
    WHERE start_station_id != end_station_id)
  SELECT AVG(time) AS avg_OneWay
  FROM tempTable;
  ```

- **Question 3: What is the most popular starting station and how many rides start there? End station?**

  * *Answer*: The most popular starting station is San Francisco Caltrain (Townsend at 4th), which is station #70. A total of 72,683 rides started from this location. The most popular end station is also San Francisco Caltrain (Townsend at 4th), station #70. A total of 92,014 ended at this stop. So, more rides tend to end here, yet this is still a very busy station.
  

| name | st  | num_rides  |
| :-----: | :-: | :-: |
| San Francisco Caltrain (Townsend at 4th) | 70 | 72683 |


| name | st  | num_rides  |
| :-----: | :-: | :-: |
| San Francisco Caltrain (Townsend at 4th) | 70 | 92014 |

  
  * *SQL query*: 
  ```sql
  WITH tempTable AS (
    SELECT start_station_id AS st, count(*) AS num_rides
    FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
    GROUP BY start_station_id 
    ORDER BY num_rides DESC
    LIMIT 1)
  SELECT name, st, num_rides
  FROM tempTable AS trips JOIN `bigquery-public-data.san_francisco.bikeshare_stations` AS stations 
    ON trips.st = stations.station_id
  WHERE stations.station_id = trips.st 
  GROUP BY name, st, num_rides
  
  WITH tempTable AS (
    SELECT end_station_id AS st, count(*) AS num_rides
    FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
    GROUP BY end_station_id 
    ORDER BY num_rides DESC
    LIMIT 1)
  SELECT name, st, num_rides
    FROM tempTable AS trips JOIN `bigquery-public-data.san_francisco.bikeshare_stations` AS stations 
    ON trips.st = stations.station_id
  WHERE stations.station_id = trips.st 
  GROUP BY name, st, num_rides

  ```

### Bonus activity queries (optional - not graded - just this section is optional, all other sections are required)

The bike share dynamic dataset offers multiple tables that can be joined to learn more interesting facts about the bike share business across all regions. These advanced queries are designed to challenge you to explore the other tables, using only the available metadata to create views that give you a broader understanding of the overall volumes across the regions(each region has multiple stations)

We can create a temporary table or view against the dynamic dataset to join to our static dataset.

Here is some SQL to pull the region_id and station_id from the dynamic dataset.  You can save the results of this query to a temporary table or view.  You can then join the static tables to this table or view to find the region:
```sql
#standardSQL
select distinct region_id, station_id
from `bigquery-public-data.san_francisco_bikeshare.bikeshare_station_info`
```

- Top 5 popular station pairs in each region

- Top 3 most popular regions(stations belong within 1 region)

- Total trips for each short station name in each region

- What are the top 10 used bikes in each of the top 3 region. these bikes could be in need of more frequent maintenance.

---

## Part 2 - Querying data from the BigQuery CLI 

- Use BQ from the Linux command line:

  * General query structure

    ```
    bq query --use_legacy_sql=false '
        SELECT count(*)
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```

### Queries

1. Rerun the first 3 queries from Part 1 using bq command line tool (Paste your bq
   queries and results here, using properly formatted markdown):

  * **What's the size of this dataset? (i.e., how many trips)**
  
    ```
    bq query --use_legacy_sql=false '
        SELECT count(*)
        FROM 
            `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```
  
::: notes The size of this dataset/number of trips is 983,648. :::

  * **What is the earliest start time and latest end time for a trip?**
  
    ```
    bq query --use_legacy_sql=false '
        SELECT min(start_date) AS st_time, max(end_date) AS end_time
        FROM 
            `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```
  
| st_time | end_time  | 
| :-----: | :-: | 
| 2013-08-29 09:08:00 UTC | 2016-08-31 23:48:00 UTC |


::: notes Across all trips, the earliest start date and time is '2013-08-29 09:08:00 UTC' and the latest end date and time is '2016-08-31 23:48:00 UTC'. :::

  * **How many bikes are there?**
  
    ```
    bq query --use_legacy_sql=false '
        SELECT count(distinct bike_number) AS total_bikes
        FROM 
            `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```
    
::: notes There are 700 bikes. :::

2. New Query (Run using bq and paste your SQL query and answer the question in a sentence, using properly formatted markdown):

  * **How many trips are in the morning vs in the afternoon?**
    
    ```
    bq query --use_legacy_sql=false '
        WITH tempTable AS ( 
            SELECT EXTRACT(HOUR FROM start_date) AS hr,
            FROM 
                `bigquery-public-data.san_francisco.bikeshare_trips` ) 
        SELECT 
            COUNT(CASE WHEN hr <= 12 then 1 ELSE NULL END) AS Morning,
            COUNT(CASE WHEN hr > 12 then 1 ELSE NULL END) AS Afternoon
        FROM 
            tempTable '
    ```
    
| Morning | Afternoon  | 
| :-----: | :-: | 
| 459289 | 524359 |

::: notes By dividing the morning and afternoon as 0-12 and 12-24, there are 459,289 total trips taken in the morning and 524,359 total trips taken in the afternoon. So, there are more afternoon trips, making up 53% of the total trips. :::

### Project Questions
Identify the main questions you'll need to answer to make recommendations (list
below, add as many questions as you need).

- Question 1: What are the most popular routes taken?

- Question 2: How long, on average, do the popular routes take?

- Question 3: What are the most popular routes and times?

- Question 4: What is the average ride duration of customers compared to subscribers?

- Question 5: During the 'rush hours', how many bikes are available, on average, at popular starting stations?

- Question 6: What are the most popular round trips and how long, on average, do those rides take? 

### Answers

Answer at least 4 of the questions you identified above You can use either
BigQuery or the bq command line tool.  Paste your questions, queries and
answers below.

- **Question 1: What are the most popular routes taken?**
  * *Answer:* The most popular route is from Harry Bridges Plaza (Ferry Building) to Embarcadero at Sansome.
  
| start_station_name | end_station_name  |  s_st  | e_st | num_rides |
| :-----: | :-: | :-: | :-: | :-: | 
| Harry Bridges Plaza (Ferry Building) | Embarcadero at Sansome |  50  | 60 | 9150 |
| San Francisco Caltrain 2 (330 Townsend) | Townsend at 7th | 69 | 65 | 8508 |
| 2nd at Townsend | Harry Bridges Plaza (Ferry Building) | 61 | 50 | 7620 |
| Harry Bridges Plaza (Ferry Building) | 2nd at Townsend | 50 | 61 | 6888 | 
| Embarcadero at Sansome | Steuart at Market | 60 | 74 | 6874 |
| Townsend at 7th | San Francisco Caltrain 2 (330 Townsend) | 65 | 69 | 6836 |
| Embarcadero at Folsom | San Francisco Caltrain (Townsend at 4th) | 51 | 70 | 6351 |
| San Francisco Caltrain (Townsend at 4th) | Harry Bridges Plaza (Ferry Building) | 70 | 50 | 6215 |
| Steuart at Market | 2nd at Townsend | 74 | 61 | 6039 |
| Steuart at Market | San Francisco Caltrain (Townsend at 4th) | 74 | 70 | 5959 |
  
  
  * *SQL query:*
  
  ```sql
    WITH tempTable AS (
      SELECT start_station_id AS s_st, end_station_id AS e_st, count(*) AS num_rides
      FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
      GROUP BY start_station_id, end_station_id 
      ORDER BY num_rides DESC
      LIMIT 10)
    SELECT stations.name AS start_station_name, stations1.name AS end_station_name, s_st, e_st, num_rides,
    FROM tempTable AS trips 
    LEFT JOIN `bigquery-public-data.san_francisco.bikeshare_stations` AS stations 
      ON trips.s_st = stations.station_id 
    LEFT JOIN `bigquery-public-data.san_francisco.bikeshare_stations` AS stations1 
      ON trips.e_st = stations1.station_id 
    GROUP BY start_station_name, end_station_name, s_st, e_st, num_rides
    ORDER BY num_rides DESC
  ```

- **Question 2: How long, on average, do the popular routes take?**
  * *Answer:* The most popular route takes 20 minutes on average.
  
|  s_st  | e_st | num_rides | minutes
| :-----: | :-: | :-: | :-: | 
| 50  | 60 | 9150 | 20.0 |
| 69 | 65 | 8508 | 5.0 |
| 61 | 50 | 7620 | 10.0 |
| 50 | 61 | 6888 | 11.0 |
| 60 | 74 | 6874 | 9.0 |
| 65 | 69 | 6830 | 5.0 |
| 51 | 70 | 6351 | 12.0 |
| 70 | 50 | 6215 | 13.0 |
| 74 | 61 | 6039 | 10.0 |
| 74 | 70 | 5959 | 12.0 |
  
  * *SQL query:*
  
  ```sql
  SELECT start_station_id AS s_st, end_station_id AS e_st, count(*) AS num_rides, ROUND(AVG(duration_sec/60)) AS minutes,
  FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
  WHERE (duration_sec/60) > 2
  GROUP BY start_station_id, end_station_id 
  ORDER BY num_rides DESC
  LIMIT 10
  ```

- **Question 3: What are the most popular routes and times during the week?**
  * *Answer:* The most popular ride and time is from station 50 to 61 at 8am. We can also see that another popular time and route is 
            from station 61 to 50 at 4 and 5 PM, indicating that this is a common commuter trip.
  
  
|  hr  | num_rides | start_station_id | end_station_id
| :-----: | :-: | :-: | :-: | 
| 8  | 2680 | 50 | 61 |
| 16 | 1910 | 51 | 70 |
| 17 | 1808 | 60 | 74 |
| 17 | 1704 | 61 | 50 |
| 16 | 1655 | 61 | 50 |
| 17 | 1554 | 64 | 77 |
| 8 | 1549 | 50 | 60 |
| 8 | 1545 | 74 | 60 |
| 9 | 1532 | 74 | 61 |
| 9 | 1511 | 77 | 64 |  


  * *SQL query:*
  
  ```sql
  WITH tempTable AS ( 
      SELECT start_date, start_station_id, end_station_id,
      EXTRACT(HOUR FROM start_date) AS hr 
      FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
      WHERE EXTRACT(DAYOFWEEK FROM start_date) > 1 AND EXTRACT(DAYOFWEEK FROM start_date) < 7
      GROUP BY start_date, start_station_id, end_station_id
      ORDER BY hr) 
  SELECT hr, count(hr) AS num_rides, start_station_id, end_station_id 
  FROM tempTable 
  GROUP BY hr, start_station_id, end_station_id 
  ORDER BY num_rides DESC 
  LIMIT 10
  ```
  
- **Question 4: What is the average ride duration of customers compared to subscribers?**
  * *Answer:* Customers, on average, take hour long trips. Subcribers, on the other hand, tend to take shorter trips.
  
| subscriber_type | minutes  | 
| :-----: | :-: | 
| Customer | 62.0 |  
| Subscriber | 10.0 |
  
  
  * *SQL query:*
  
  ```sql
  SELECT subscriber_type, ROUND(AVG(duration_sec/60)) AS minutes
  FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
  GROUP BY subscriber_type
  ```

- **Question 5: During the 'rush hours', how many bikes are available, on average, at popular starting stations?**
  * *Answer:* Roughly 8 bikes are available at the most popular hour/station (8 am at station 70). 
  
|  bikes  | hr | popHr | start_station_id |
| :-----: | :-: | :-: | :-: | 
| 8.8  | 8 | 17540 | 70 |
| 13.0 | 8 | 15264 | 69 |
| 11.0 | 7 | 12886 | 70 |
| 11.0 | 8 | 12067 | 50 |
| 9.0 | 9 | 9575 | 69 |
| 6.0 | 9 | 8884 | 70 |
| 9.0 | 8 | 8812 | 55 |
| 12.0 | 8 | 7094 | 74 |
| 11.0 | 17 | 6246 | 61 |
| 13.0 | 18 | 6245 | 70 | 

  
  * *SQL query:*
  
  ```sql
  WITH tempTable AS ( 
  SELECT ROUND(AVG(bikes_available)) AS bikes, station_id,
    EXTRACT(HOUR FROM time) AS hour 
  FROM `bigquery-public-data.san_francisco.bikeshare_status` AS status
  GROUP BY hour, station_id
  ORDER BY hour)
  SELECT tempTable.bikes,
    EXTRACT(HOUR FROM start_date) AS hr, 
    COUNT(EXTRACT(HOUR FROM start_date)) AS popHr,
    start_station_id
  FROM `bigquery-public-data.san_francisco.bikeshare_trips` AS trips
  JOIN tempTable ON EXTRACT(HOUR FROM start_date) = tempTable.hour
     AND tempTable.station_id = start_station_id
  GROUP BY hr, bikes, start_station_id
  ORDER BY popHr DESC
  LIMIT 10
  ```

- **Question 6: What are the most popular round trips and how long, on average, do those rides take?** 
  * *Answer:* The most popular round trip station is Embarcadero at Sansome, station #60, and the rides, on average, take roughly an hour and 10 minutes.
  
|  station  | num_rides | time | name |
| :-----: | :-: | :-: | :-: | 
| 60  | 2866 | 72.0 | Embarcadero at Sansome |
| 50 | 2364 | 100.0 | Harry Bridges Plaza (Ferry Building) |
| 35 | 1184 | 141.0 | University and Emerson |
| 67 | 944 | 136.0 | Market at 4th |
| 74 | 911 | 91.0 | Steuart at Market |
  
  
  * *SQL query:*
  
  ```sql
  SELECT start_station_id AS station, count(*) AS num_rides,
      ROUND(AVG((duration_sec/60))) AS time, start_station_name AS name
  FROM `bigquery-public-data.san_francisco.bikeshare_trips`
  WHERE start_station_id = end_station_id
  GROUP BY start_station_id, name
  ORDER BY num_rides DESC
  LIMIT 5
  ```

---

## Part 3 - Employ notebooks to synthesize query project results

### Get Going

Create a Jupyter Notebook against a Python 3 kernel named Project_1.ipynb in the assignment branch of your repo.

#### Run queries in the notebook 

At the end of this document is an example Jupyter Notebook you can take a look at and run.  

You can run queries using the "bang" command to shell out, such as this:

```
! bq query --use_legacy_sql=FALSE '<your-query-here>'
```

- NOTE: 
- Queries that return over 16K rows will not run this way, 
- Run groupbys etc in the bq web interface and save that as a table in BQ. 
- Max rows is defaulted to 100, use the command line parameter `--max_rows=1000000` to make it larger
- Query those tables the same way as in `example.ipynb`

Or you can use the magic commands, such as this:

```sql
%%bigquery my_panda_data_frame

select start_station_name, end_station_name
from `bigquery-public-data.san_francisco.bikeshare_trips`
where start_station_name <> end_station_name
limit 10
```

```python
my_panda_data_frame
```

#### Report in the form of the Jupter Notebook named Project_1.ipynb

- Using markdown cells, MUST definitively state and answer the two project questions:

  * What are the 5 most popular trips that you would call "commuter trips"? 
  
  * What are your recommendations for offers (justify based on your findings)?

- For any temporary tables (or views) that you created, include the SQL in markdown cells

- Use code cells for SQL you ran to load into Pandas, either using the !bq or the magic commands

- Use code cells to create Pandas formatted output tables (at least 3) to present or support your findings

- Use code cells to create simple data visualizations using Seaborn / Matplotlib (at least 2) to present or support your findings

### Resource: see example .ipynb file 

[Example Notebook](example.ipynb)

