from eventHandler import eventHandler
from eventFeeder import get_events
import time
import dockingHandler
import fsdJumpHandler
import marketHandler

def main_loop():
    while True:
        time.sleep(3)
        #print("Heartbeat -> ", time.time())
        for event in get_events():
            try:
                eventHandler.process_event(event)
            except Exception as e:
                print(f"WARNING*** Event caused exception -> {event}")
                print(f"Exception: {e}")
                pass


if __name__ == "__main__":
    main_loop()

