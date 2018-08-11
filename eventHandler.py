import sqlite3

# So, thinking about this:
# ---
# We have *events* that cause updates to *things*
#
# Seems like the right thing to do here is have a publish / subscribe model
# where events (in the Captains log) are published to some topic, and code
# can subscribe for what it's interested in.
#
# Perhaps if this becomes complex enough, I could see potentially having a
# Amazon SNS topic that receives updates.
#
# For now, I think it's safe just to have an event handler that can dispatch
# to the proper classes for updating things.
import json


class EventHandler:

    # I see this being:
    # {"Docked": (update dock db obj), (update market obj)...,
    #  "FSDJump": (update star system data)
    event_subscriptions = {}

    def process_event(self, event_data):
        event_data = json.loads(event_data)
        event_name = event_data.get("event")
        subscribers = self.event_subscriptions.get(event_name, [])
        for s in subscribers:
            s.send(event_data)
        if not subscribers:
            print(f"Unsubscribed event: {event_data}")

    def subscribe(self, event, handler):
        subscribers = self.event_subscriptions.get(event, [])
        if handler not in subscribers:
            subscribers.append(handler)
            self.event_subscriptions[event] = subscribers
        else:
            print(f"Handler {handler} already in subscribers")


eventHandler = EventHandler()


class EventSubscriber:

    name = None

    def __init__(self):
        self.subscribe(self.name)

    def subscribe(self, topic):
        eventHandler.subscribe(topic, self)

    def send(self, event_data):
        # called by the event handler - sending us data to process.
        print(f"Subscriber {self.name} received {event_data}")


