# Project 3: Understanding User Behavior

## Erin Werner - W205 Summer 2020

- You're a data scientist at a game development company  

- Your latest mobile game has two events you're interested in tracking: `buy a
  sword` & `join guild`

- Each has metadata characterstic of such events (i.e., sword type, guild name,
  etc)

## Table of Contents

- docker_compose.yml

File definition for running multi-container Docker applications.

- game_api.py

Instrumented webapp with the game definition of events.

- write_sword_stream.py

Script that filters and separates the stream of game events and writes them to HDFS.

- W205 - Project 3.ipynb

Notebook that outlines the end-to-end data engineering process and includes basic analysis.

## Tasks

- Instrument your API server to log events to Kafka

- Assemble a data pipeline to catch these events: use Spark streaming to filter
  select event types from Kafka, land them into HDFS/parquet to make them
  available for analysis using Presto

- Use Apache Bench to generate test data for your pipeline

- Produce an analytics report where you provide a description of your pipeline
  and some basic analysis of the events

Use a notebook to present your queries and findings. Remember that this
notebook should be appropriate for presentation to someone else in your
business who needs to act on your recommendations.

It's understood that events in this pipeline are _generated_ events which make
them hard to connect to _actual_ business decisions.  However, we'd like
students to demonstrate an ability to plumb this pipeline end-to-end, which
includes initially generating test data as well as submitting a notebook-based
report of at least simple event analytics.
