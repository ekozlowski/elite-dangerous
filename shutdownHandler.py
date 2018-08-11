from eventHandler import EventSubscriber
from dao import update_star_system
import boto3


def update_page(star_system):
    s3 = boto3.resource('s3')
    out = f"""
<html>
<head>
  <title>Where in the Universe is CMDR Miradan?</title>
</head>
<body>
    <p>CMDR Miradan is currently in the {star_system} system.</p>
</body>
</html>
    """
    s3.Bucket('edwardkozlowski.com').put_object(Key='elite_location.html', Body=out, ContentType='text/html', CacheControl="no-cache")


class FSDJumpHandler(EventSubscriber):
    name = "Shutdown"

    def send(self, event_data):
        print("Handling Shutdown")
        star_system = event_data.get('StarSystem')
        system_address = event_data.get('SystemAddress')
        x_pos, y_pos, z_pos = event_data.get('StarPos')
        update_star_system(star_system, system_address, x_pos, y_pos, z_pos)
        update_page(star_system)


fsdHandler = FSDJumpHandler()

if __name__ == "__main__":
    update_page("rar")