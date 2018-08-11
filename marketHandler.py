from eventHandler import EventSubscriber
from dao import update_items
import datetime
import time
import json
import os
import config


class MarketHandler(EventSubscriber):
    name = "Market"

    def send(self, event_data):
        # Parse the timestamp - if it's older than 2 minutes ago, don't parse it.

        print("Handling Market Event")
        # If it happened more than two minutes ago, I don't care about it.
        timestamp = event_data.get('timestamp')
        event_time = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        if (datetime.datetime.utcnow() - event_time).seconds > 120:
            print("Ignoring market event")
            return
        # Otherwise, sleep 5 seconds, waiting on the "Market.json" file to be written.
        print("sleeping 5 seconds - waiting on market data")
        time.sleep(5)
        # Load the market data form Market.json
        market_data = json.loads(open(os.path.join(config.ELITE_LOG_DIR, 'Market.json')).read())
        print(market_data.get('MarketID'))
        update_items(market_data.get('MarketID'), market_data.get('Items'))

