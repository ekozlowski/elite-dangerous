from eventHandler import eventHandler
import dockingHandler



eventHandler.process_event({"event": "Docking", "data": "foo"})
eventHandler.process_event({"event": "Otherness", "data": "foo"})
