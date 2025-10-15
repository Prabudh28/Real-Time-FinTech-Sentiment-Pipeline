import os
import time
import json
import random
import asyncio
import configparser  # <-- Reads the config file
from faker import Faker
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- Configuration ---
# Reads the connection string from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
EVENT_HUB_CONNECTION_STR = config['azure_event_hub']['connection_string']
EVENT_HUB_NAME = "eh-news-headlines"

# Initialize Faker for synthetic data generation
fake = Faker()

# Initialize NLTK's VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# --- Data Generation Logic (No changes needed here) ---
COMPANIES = ["InnovateFin", "QuantumBank", "ApexPay", "StellarCap", "FutureVest", "DigitalAsset Inc."]
POSITIVE_EVENTS = ["announces record profits", "secures major funding", "launches new AI platform", "partners with tech giant", "gets regulatory approval"]
NEGATIVE_EVENTS = ["faces data breach inquiry", "reports unexpected losses", "under investigation by FCA", "announces layoffs", "service outage affects millions"]
NEUTRAL_TOPICS = ["releases quarterly report", "updates terms of service", "attends global finance summit", "appoints new CTO"]
REGULATORS = ["The FCA", "The Bank of England", "UK Treasury"]

def generate_headline():
    """Generates a synthetic Fin-Tech news headline and analyzes its sentiment."""
    headline_type = random.choice(['positive', 'negative', 'neutral'])
    
    if headline_type == 'positive':
        company = random.choice(COMPANIES)
        event = random.choice(POSITIVE_EVENTS)
        headline = f"Breaking: {company} stock soars as it {event}."
    elif headline_type == 'negative':
        company = random.choice(COMPANIES)
        event = random.choice(NEGATIVE_EVENTS)
        regulator = random.choice(REGULATORS)
        headline = f"Alert: {regulator} probes {company} after it {event}."
    else: # neutral
        company = random.choice(COMPANIES)
        topic = random.choice(NEUTRAL_TOPICS)
        headline = f"News: {company} {topic} this week."

    sentiment_scores = analyzer.polarity_scores(headline)
    compound_score = sentiment_scores['compound']

    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    event_data = {
        'headline': headline,
        'company': company,
        'sentiment': sentiment,
        'compound_score': compound_score,
        'timestamp': time.time()
    }
    
    return event_data

# --- Main Producer Logic (No changes needed here) ---
async def run():
    """Creates an EventHubProducerClient, sends events in a loop."""
    if not EVENT_HUB_CONNECTION_STR:
        raise ValueError("Connection string is not found in config.ini file. Make sure the file exists and is correct.")

    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        eventhub_name=EVENT_HUB_NAME
    )
    
    print("Starting data producer... Press Ctrl+C to stop.")
    
    try:
        async with producer:
            while True:
                data = generate_headline()
                event_data_batch = await producer.create_batch()
                event_data_batch.add(EventData(json.dumps(data)))
                await producer.send_batch(event_data_batch)
                print(f"Sent: {data['headline']} | Sentiment: {data['sentiment']}")
                await asyncio.sleep(random.uniform(1, 4))
    except KeyboardInterrupt:
        print("\nStopping data producer.")
    finally:
        print("Producer stopped.")

if __name__ == "__main__":
    asyncio.run(run())

