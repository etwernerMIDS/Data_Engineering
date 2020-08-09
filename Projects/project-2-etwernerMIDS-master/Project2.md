# Tracking User Activity

## Erin Werner - W205 Summer 2020 - Project 2

In this project, I work at an ed. tech. firm. I've created a service that delivers assessments, and now lots of different customers (e.g., Pearson) want to publish their assessments on it. My goal is to get the data ready for data scientists who work for these customers to run queries.

My goal is to prepare the infrastructure to land the data in the form and structure it needs to be in order to be queried. This will require tools such as Docker, Kafka, Spark, HDFS, and SQL.

# Publish and Consume Messages with Kafka

First, we need to create and get into the correct directory.

```
mkdir ~/w205/project-2-etwernerMIDS
cd ~/w205/project-2-etwernerMIDS
```

Then, we need to copy the docker-compose file from Github.

```
cp ~/w205/course-content//08-Querying-Data/docker-compose.yml .
```

We also need to download the user activity data.

```
curl -L -o assessment-attempts-20180128-121051-nested.json https://goo.gl/ME6hjp
```

*Output:*
```
 % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 9096k  100 9096k    0     0  13.0M      0 --:--:-- --:--:-- --:--:-- 24.4M
```

Next, we want to spin up Docker, by utilizing the docker-compose file.

```
docker-compose up -d
```

*Output:*
```
Starting project2etwernermids_cloudera_1
Starting project2etwernermids_zookeeper_1
Starting project2etwernermids_mids_1
Starting project2etwernermids_kafka_1
Starting project2etwernermids_spark_1
```

Now, we want to check out Hadoop.

```
docker-compose exec cloudera hadoop fs -ls /tmp/
```

*Output:*
```
drwxrwxrwt   - mapred mapred              0 2018-02-06 18:27 /tmp/hadoop-yarn
drwx-wx-wx   - root   supergroup          0 2020-07-10 23:24 /tmp/hive
```

Because everything looks as it should, we can create a new Kafka topic. I will create one named 'myuseractivity' in order to reflect the data that we plan to publish to it.

```
docker-compose exec kafka kafka-topics --create --topic myuseractivity --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181
```

*Output:*
```
Created topic myuseractivity.
```

Before we move on, we want to check to make sure the topic is up.

```
docker-compose exec kafka kafka-topics --describe --topic myuseractivity --zookeeper zookeeper:32181
```

*Output:*
```
Topic: myuseractivity   PartitionCount: 1       ReplicationFactor: 1    Configs: 
        Topic: myuseractivity   Partition: 0    Leader: 1       Replicas: 1     Isr: 1
```

We should also check the data before moving forward.

```
docker-compose exec mids bash -c "cat /w205/project-2-etwernerMIDS/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c"
```

This command prints all the messages to the screen. As a result, we can visually confirm that the data will need to be unrolled later but, overall, it looks okay and can be written to the topic.

Now that we have checked the topic and the data, we can publish the messages to the Kafka.

```
docker-compose exec mids bash -c "cat /w205/project-2-etwernerMIDS/assessment-attempts-20180128-121051-nested.json | jq '.[]' -c | kafkacat -P -b kafka:29092 -t myuseractivity && echo 'Produced user activity messages.'"
```

*Output:*
```
Produced user activity messages.
```

This acts as the first part of our data engineering pipeline. In this portion of the pipeline, Kafka acts as a messageing queue/broker that ingests a stream of events and then allows that data to be accessed and transformed on another platform. Kafka holds onto the data until something else asks for it, then the data is consumed.

# Transform Messages with Spark & Land Messages in HDFS

As the messages have been published in Kafka, now our goal is transform them with Spark and land them in HDFS.

First, we need to spin up Spark.

```
docker-compose exec spark pyspark
```

Then, we can read the messages into Spark from the Kafka topic. This is how we will transform the data to be in the structure in order to be queried.

```
messages = spark \
  .read \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:29092") \
  .option("subscribe","myuseractivity") \
  .option("startingOffsets", "earliest") \
  .option("endingOffsets", "latest") \
  .load()
```

We want to cache this to cut back on warnings later.

```
messages.cache()
```

*Output:*
```
DataFrame[key: binary, value: binary, topic: string, partition: int, offset: bigint, timestamp: timestamp, timestampType: int]
```

To get a better idea of what the messages look like, we can check the schema.

```
messages.printSchema()
```

*Output:*
```
root
 |-- key: binary (nullable = true)
 |-- value: binary (nullable = true)
 |-- topic: string (nullable = true)
 |-- partition: integer (nullable = true)
 |-- offset: long (nullable = true)
 |-- timestamp: timestamp (nullable = true)
 |-- timestampType: integer (nullable = true)
```

We can also look at the messages themselves.

```
messages.show()
```

*Output:*

| key|               value|         topic|partition|offset|           timestamp|timestampType|
| :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     0|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     1|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     2|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     3|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     4|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     5|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     6|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     7|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     8|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|     9|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    10|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    11|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    12|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    13|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    14|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    15|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    16|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    17|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    18|1969-12-31 23:59:...|            0|
|null|[7B 22 6B 65 65 6...|myuseractivity|        0|    19|1969-12-31 23:59:...|            0|

'only showing top 20 rows'

However, this is not the ideal format for our data. So, we can convert our messages to strings and then look at those results.

```
useract=messages.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
useract.show()
useract.printSchema()
```

*Output:*

| key|               value|
| :-----: | :-----: |
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|
|null|{"keen_timestamp"...|

'only showing top 20 rows'

```
root
 |-- key: string (nullable = true)
 |-- value: string (nullable = true)
```

We can also get a sense of the size of our data set.

```
useract.count()
```

*Output:*
```
3280
```

Now, we can then write these messages to HDFS.

```
useract.write.parquet("/tmp/useract")
```

In a separate terminal, we can check our results.

```
docker-compose exec cloudera hadoop fs -ls /tmp/useract/
```

*Output:*
```
Found 2 items
-rw-r--r--   1 root supergroup          0 2020-07-11 23:17 /tmp/useract/_SUCCESS
-rw-r--r--   1 root supergroup    2513546 2020-07-11 23:17 /tmp/useract/part-00000-0c930967-dde9-4ed3-ae7c-a3f75c2a89f1-c000.snappy.parquet
```

Back in the Spark ternimal, we need to deal with unicode.

```
import sys
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
```

Next, we need to unroll the .json data. This step is very important as it is the key transformation that will allow us to query the data later. JSON, or JavaScript Object Notation, is a minimal, readable format for structuring data. It is used primarily to transmit data between a server and web application. As a result, there could be nested values within values that we need to consider as we unroll the data. 

This is the case with the field 'sequences' as it is a multiple questions field. In order to address this issue, we will want to convert the nested values into strings and store them all togther as an array-like structure. That will serve as the value in the 'sequences' field. Then, the rest of the fields can be parsed and collectively make up our data set.

```
import json

#converts all values to strings
raw = useract.select(useract.value.cast('string'))

# Loads the data and converts each line to a row
assessments = spark.read.json(raw.rdd.map(lambda j: j.value))
assessments.show()
```

*Output:*

|        base_exam_id|certification|           exam_name|   keen_created_at|             keen_id|    keen_timestamp|max_attempts|           sequences|          started_at|        user_exam_id|
| :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
|37f0a30a-7464-11e...|        false|Normal Forms and ...| 1516717442.735266|5a6745820eb8ab000...| 1516717442.735266|         1.0|[1,[false,2,1,1,4...|2018-01-23T14:23:...|6d4089e4-bde5-4a2...|
|37f0a30a-7464-11e...|        false|Normal Forms and ...| 1516717377.639827|5a674541ab6b0a000...| 1516717377.639827|         1.0|[1,[false,1,2,1,4...|2018-01-23T14:21:...|2fec1534-b41f-441...|
|4beeac16-bb83-4d5...|        false|The Principles of...| 1516738973.653394|5a67999d3ed3e3000...| 1516738973.653394|         1.0|[1,[false,3,0,1,4...|2018-01-23T20:22:...|8edbc8a8-4d26-429...|
|4beeac16-bb83-4d5...|        false|The Principles of...|1516738921.1137421|5a6799694fc7c7000...|1516738921.1137421|         1.0|[1,[false,2,2,0,4...|2018-01-23T20:21:...|c0ee680e-8892-4e6...|
|6442707e-7488-11e...|        false|Introduction to B...| 1516737000.212122|5a6791e824fccd000...| 1516737000.212122|         1.0|[1,[false,3,0,1,4...|2018-01-23T19:48:...|e4525b79-7904-405...|
|8b4488de-43a5-4ff...|        false|        Learning Git| 1516740790.309757|5a67a0b6852c2a000...| 1516740790.309757|         1.0|[1,[true,5,0,0,5,...|2018-01-23T20:51:...|3186dafa-7acf-47e...|
|e1f07fac-5566-4fd...|        false|Git Fundamentals ...|1516746279.3801291|5a67b627cc80e6000...|1516746279.3801291|         1.0|[1,[true,1,0,0,1,...|2018-01-23T22:24:...|48d88326-36a3-4cb...|
|7e2e0b53-a7ba-458...|        false|Introduction to P...| 1516743820.305464|5a67ac8cb0a5f4000...| 1516743820.305464|         1.0|[1,[true,5,0,0,5,...|2018-01-23T21:43:...|bb152d6b-cada-41e...|
|1a233da8-e6e5-48a...|        false|Intermediate Pyth...|  1516743098.56811|5a67a9ba060087000...|  1516743098.56811|         1.0|[1,[true,4,0,0,4,...|2018-01-23T21:31:...|70073d6f-ced5-4d0...|
|7e2e0b53-a7ba-458...|        false|Introduction to P...| 1516743764.813107|5a67ac54411aed000...| 1516743764.813107|         1.0|[1,[false,0,1,0,1...|2018-01-23T21:42:...|9eb6d4d6-fd1f-4f3...|
|4cdf9b5f-fdb7-4a4...|        false|A Practical Intro...|1516744091.3127241|5a67ad9b2ff312000...|1516744091.3127241|         1.0|[1,[false,3,1,0,4...|2018-01-23T21:45:...|093f1337-7090-457...|
|e1f07fac-5566-4fd...|        false|Git Fundamentals ...|1516746256.5878439|5a67b610baff90000...|1516746256.5878439|         1.0|[1,[true,1,0,0,1,...|2018-01-23T22:24:...|0f576abb-958a-4c0...|
|87b4b3f9-3a86-435...|        false|Introduction to M...|  1516743832.99235|5a67ac9837b82b000...|  1516743832.99235|         1.0|[1,[false,4,1,1,6...|2018-01-23T21:40:...|0c18f48c-0018-450...|
|a7a65ec6-77dc-480...|        false|   Python Epiphanies|1516743332.7596769|5a67aaa4f21cc2000...|1516743332.7596769|         1.0|[1,[false,4,0,2,6...|2018-01-23T21:34:...|b38ac9d8-eef9-495...|
|7e2e0b53-a7ba-458...|        false|Introduction to P...| 1516743750.097306|5a67ac46f7bce8000...| 1516743750.097306|         1.0|[1,[false,4,1,0,5...|2018-01-23T21:41:...|bbc9865f-88ef-42e...|
|e5602ceb-6f0d-11e...|        false|Python Data Struc...|1516744410.4791961|5a67aedaf34e85000...|1516744410.4791961|         1.0|[1,[false,3,0,1,4...|2018-01-23T21:51:...|8a0266df-02d7-44e...|
|e5602ceb-6f0d-11e...|        false|Python Data Struc...|1516744446.3999851|5a67aefef5e149000...|1516744446.3999851|         1.0|[1,[false,3,0,0,3...|2018-01-23T21:53:...|95d4edb1-533f-445...|
|f432e2e3-7e3a-4a7...|        false|Working with Algo...| 1516744255.840405|5a67ae3f0c5f48000...| 1516744255.840405|         1.0|[1,[true,4,0,0,4,...|2018-01-23T21:50:...|f9bc1eff-7e54-42a...|
|76a682de-6f0c-11e...|        false|Learning iPython ...| 1516744023.652257|5a67ad579d5057000...| 1516744023.652257|         1.0|[1,[false,2,0,0,2...|2018-01-23T21:46:...|dc4b35a7-399a-4bd...|
|a7a65ec6-77dc-480...|        false|   Python Epiphanies|1516743398.6451161|5a67aae6753fd6000...|1516743398.6451161|         1.0|[1,[true,6,0,0,6,...|2018-01-23T21:35:...|d0f8249a-597e-4e1...|

'only showing top 20 rows'

We can confirm from the results above that the field 'sequences' contains array-like structures as values, where each is made up of the nested data. Because we were able to successfully unroll the data, we can save the results to HDFS.

```
assessments.write.parquet("/tmp/extracted_messages")
```

In a separate terminal, we can check all of our files in HDFS.
```
docker-compose exec cloudera hadoop fs -ls /tmp/
```

*Output:*
```
drwxr-xr-x   - root   supergroup          0 2020-07-11 23:39 /tmp/extracted_messages
drwxrwxrwt   - mapred mapred              0 2018-02-06 18:27 /tmp/hadoop-yarn
drwx-wx-wx   - root   supergroup          0 2020-07-11 23:36 /tmp/hive
drwxr-xr-x   - root   supergroup          0 2020-07-11 23:38 /tmp/useract
```

Last, in order to query the data and glean information from it, we can save the data as a SQL Table.

```
assessments.registerTempTable('assessments')
```

Now, we are able to run queries against our data.

```
spark.sql("select assessments.exam_name from assessments limit 10").show()
```

*Output:*

|           exam_name|
| :-----: |
|Normal Forms and ...|
|Normal Forms and ...|
|The Principles of...|
|The Principles of...|
|Introduction to B...|
|        Learning Git|
|Git Fundamentals ...|
|Introduction to P...|
|Intermediate Pyth...|
|Introduction to P...|

This portion then acts as the backend-part of our data engineering pipeline. In this portion of the pipeline, Spark accesses and transforms the user activity data into a dataset that can be queried using SQL. Those results are then stored and saved in HDFS.

# Data

In order to show the data scientists at these other companies the kinds of data that they will have access to, I will run some queries to address some basic buisness questions that they might have. These queries will reflect what I believe they might need to know about the data in order to address their questions about these data.

## Initial Queries

### 1.) How many assesstments are in the dataset?

This business question will give us an idea about the size of our data, which provides context to the scope of our data for our customers.

```
spark.sql("select count(*) from assessments").show()
```

|count(1)|
| :-----: | 
|    3280|

However, it is possible to have repeat rows from unrolling the .json file. So, we can look for the number of distinct rows.

```
spark.sql("select count(distinct *) from assessments").show()
```

|count(DISTINCT base_exam_id, certification, exam_name, keen_created_at, keen_id, keen_timestamp, max_attempts, sequences, started_at, user_exam_id)|
| :-----: | 
|                                                                                                                                               3110|

These results prove that there are repeated data entries. So, we can create a new dataset and write that to HDFS as well.

```
unique_assessments = spark.sql("select distinct * from assessments")       
unique_assessments.write.parquet("/tmp/unique_assessments")
```

In the separate terminal, we can check our results.
```
docker-compose exec cloudera hadoop fs -ls /tmp/
```

*Output:*
```
drwxr-xr-x   - root   supergroup          0 2020-07-11 23:39 /tmp/extracted_messages
drwxrwxrwt   - mapred mapred              0 2018-02-06 18:27 /tmp/hadoop-yarn
drwx-wx-wx   - root   supergroup          0 2020-07-11 23:36 /tmp/hive
drwxr-xr-x   - root   supergroup          0 2020-07-11 23:40 /tmp/unique_assessments
drwxr-xr-x   - root   supergroup          0 2020-07-11 23:38 /tmp/useract
```

We can also save that as a new table to query from.
```
unique_assessments.registerTempTable('unique_assessments')
```

Now, we can look at the size of our new data subset.

```
spark.sql("select count(*) from unique_assessments").show()
```
                                                       
|count(1)|
| :-----: |
|    3242|

We can see that this count is higher than the original number of distinct rows. This is because 'SELECT DISTINCT' will include null values in the result set while 'COUNT(DISTINCT)' returns the number of unique nonnull values. Yet, this count is still less than the size of the original data set, so we can assume the repeated rows have now been removed. We will use the unique-row data set moving forward with our analysis.

### 2.) What's the name of your Kafka topic? How did you come up with that name?

The name of my Kafka topic is 'myuseractivity'. This is because it reflects the data that has been published onto that topic as well as the overall goal of this project. In this context, we deliver assessments to users. Our goal is then to learn about user activity in relation to the assessments that they take. Essentially, we are trying to track user activity and that inspired the representative topic name.

### 3.) How many people took Learning Git?

This buisness question will provide some insight to how popular a specific assessment is. Information about a particular assessment is useful to our customers as it will provide specific product demand information that can influence decisions.

```
spark.sql("select count(unique_assessments.exam_name) from unique_assessments where unique_assessments.exam_name ='Learning Git' ").show()
```

|count(exam_name)|
| :-----: |
|             390|

So, 390 people from our data set took the assessment 'Learning Git'.

### 4.) What is the least common course taken? And the most common?

These buisness questions will give us more specific information about the popularity/non-populairity of certain assessments. This could then help our clients to understand what assessments and potential promotions they should be offering to their users. It could also inspire new assessments to be developed that are similar or a continuation of a popular assessment.

The least common course taken: 

```
spark.sql("select unique_assessments.exam_name, count(unique_assessments.exam_name) AS exam_count from unique_assessments group by unique_assessments.exam_name order by exam_count asc limit 1").show(truncate = False)
```

|           exam_name|exam_count|
| :-----: | :-----: | 
|Learning to Visualize Data with D3.js |         1|


The most common course taken: 

```
spark.sql("select unique_assessments.exam_name, count(unique_assessments.exam_name) AS exam_count from unique_assessments group by unique_assessments.exam_name order by exam_count desc limit 1").show()
```

|   exam_name|exam_count|
| :-----: | :-----: | 
|Learning Git|       390|

## Additional Queries

### 5.) What is the earliest start date and time and latest start date and time for an assessment?

This buisness question will give us an idea about the duration in which the events of the data set occurred, which provides even more context to the scope of our data for our customers. 

```
spark.sql("select min(unique_assessments.started_at) as earliest, max(unique_assessments.started_at) AS latest from unique_assessments").show(truncate = False)
```

|earliest                |latest                  |
| :-----: | :-----: |
|2017-11-21T00:42:08.990Z|2018-01-28T19:17:53.796Z|

So, the overall assessment data spans from the end of November 2017 to the end of January 2018. This is a time period of about 2-3 months.

### 6.) What are the 5 most popular dates to start an assessment?

This buisness question will help to provide insight as to when users are taking assessments. This is helpful for our customers as this could allow them to offer promotions at ideal times or even add additional assessments before peak days.

```
spark.sql("select to_date(unique_assessments.started_at), count(to_date(unique_assessments.started_at)) AS start_count from unique_assessments group by to_date(unique_assessments.started_at)order by start_count desc limit 5").show()
```
                                
|to_date(unique_assessments.`started_at`)|start_count|
| :-----: | :-----: |
|                       2017-12-05|        123|
|                       2017-12-11|         97|
|                       2017-12-20|         91|
|                       2017-12-18|         91|
|                       2017-12-14|         84|

We can see that many assessments were started at the beginning-middle of our time span. The five most popular dates occurred within a two week span of each other.

### 7.) How many users are there? Are there any users that took the same exam more than once?

These buisness questions will offer more insight to user-specific acitivty. This is especially useful for our customers as the overall goal is to track user activity in relation to the assessments that they take.

Number of users:

```
spark.sql("select count(distinct unique_assessments.user_exam_id) from unique_assessments").show()
```
                                            
|count(DISTINCT user_exam_id)|
| :-----: | 
|                        3242|

We can see that the number of distinct users is the same as the number of rows in this data set. This means that each row represents a user-assessment pair. So, it is fair to assume that no users took the same exam more than once. Yet, we can still check this with another query.

Number of times assessment taken per user:
```
spark.sql("select unique_assessments.user_exam_id as user, count(unique_assessments.user_exam_id) as num_exams from unique_assessments group by unique_assessments.user_exam_id order by num_exams desc").show(truncate = False)
```                   
                      
|user                                |num_exams|
| :-----: | :-----: |
|569c5fee-fe6e-4b1c-b936-d7465534b693|1        |
|72f55f46-4056-4eb7-8419-f1ab9e96325f|1        |
|ba0677f0-88e4-43c8-947b-6393e8cd1797|1        |
|d47809a0-2ffa-45e9-b82c-3c2976c1597c|1        |
|b695671e-67e0-422f-9035-2cf7f9d6e208|1        |
|06a9fc3f-e8c2-4872-b098-bdb441689ff4|1        |
|4ff87b99-ce82-458d-ae23-b2a96c5e998b|1        |
|89d8acd5-d1d6-402d-89d8-17adcf061172|1        |
|7c4c9719-32aa-4b98-bf2a-ef61461fe161|1        |
|59f6bd14-c139-40c7-bd4c-28e0d0740f43|1        |
|a2f32550-dcaf-4a8d-aaa7-a2b6d68d30d3|1        |
|f9cc7604-10c9-4c53-a834-5aa037d46455|1        |
|79347651-7576-493f-9933-04326ed8fd59|1        |
|9939c667-e6bb-4825-b85a-e4b9b178ca30|1        |
|96718356-4414-44ba-9bef-0ee5921ca635|1        |
|14f33788-3d27-4828-bc6c-fe9f4a10a001|1        |
|e73b0e3a-f958-4e42-9c17-00a5d996b947|1        |
|39548078-275f-4842-b984-848bcdc03000|1        |
|28bfe739-0e6d-4024-8d2d-dbba6d4a1097|1        |
|904eec10-0087-472d-8886-d507b411331e|1        |                                     

This confirms that users take each assessment only once.

With these results, the data scientists from our customers have a better idea of the data they will have access to in order to make data-driven decisions.

# Clean Up

Once we are done running our queries, we need to take everything down.

So, to start, we need to exit Spark.

```
exit()
```

Next, we want to get our command line history. First, we will get our history from Spark.

```
docker-compose exec spark cat /root/.python_history > my_spark_history.txt
```

Then, we can get our overall history from Docker.

```
history > etwernerMIDS-history.txt
```

Last, we can take Docker down.

```
docker-compose down
```

*Output:*
```
Stopping project2etwernermids_kafka_1 ... done
Stopping project2etwernermids_spark_1 ... done
Stopping project2etwernermids_mids_1 ... done
Stopping project2etwernermids_zookeeper_1 ... done
Stopping project2etwernermids_cloudera_1 ... done
Removing project2etwernermids_kafka_1 ... done
Removing project2etwernermids_spark_1 ... done
Removing project2etwernermids_mids_1 ... done
Removing project2etwernermids_zookeeper_1 ... done
Removing project2etwernermids_cloudera_1 ... done
Removing network project2etwernermids_default
```

## The End
