#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"


@app.route("/purchase_a_sword")
def purchase_a_sword():
    purchase_sword_event = {'event_type': 'purchase_sword',
                            'description': 'very good sword'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

@app.route("/purchase_a_knife")
def purchase_a_knife():
    purchase_knife_event = {'event_type': 'purchase_knife',
                            'description': 'very sharp knife'}
    log_to_kafka('events', purchase_knife_event)
    return "Knife Purchased!\n"

@app.route("/join_a_guild")
def join_a_guild():
    join_guild_event = {'event_type':'join_guild',
                        'description': 'very nice group'}
    log_to_kafka('events', join_guild_event)
    return "Joined Guild!\n"

@app.route("/sell_a_sword")
def sell_a_sword():
    sell_sword_event = {'event_type': 'sell_sword',
                        'description': 'goodbye sword'}
    log_to_kafka('events',sell_sword_event)
    return "Sold Sword!\n"

@app.route("/sell_a_knife")
def sell_a_knife():
    sell_knife_event = {'event_type': 'sell_knife',
                        'description': 'goodbye knife'}
    log_to_kafka('events',sell_knife_event)
    return "Sold Knife!\n"

@app.route("/leave_a_guild")
def leave_a_guild():
    leave_guild_event = {'event_type': 'leave_guild',
                        'description': 'goodbye guild'}
    log_to_kafka('events',leave_guild_event)
    return "Left Guild!\n"

