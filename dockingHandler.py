from eventHandler import EventSubscriber
from dao import update_station


class DockingHandler(EventSubscriber):
    """
    Handles the docking event, fired when a ship docks in a starport.
    """
    name = "Docked"

    def send(self, event_data):
        update_station(
            star_system=event_data.get('StarSystem'),
            station_name=event_data.get('StationName'),
            station_type=event_data.get('StationType'),
            market_id=event_data.get('MarketID')
        )


