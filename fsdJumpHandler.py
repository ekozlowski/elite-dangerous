from eventHandler import EventSubscriber
from dao import update_star_system
import boto3
import config

# TODO: Make CMDR name variable, and preserve state of System & Docked station so we can message in the event of an offline event.


def update_page(star_system):
    s3 = boto3.resource('s3')
    out = f"""
<html>
<head>
  <title>Where in the Universe is CMDR {config.CMDR_NAME}?</title>
</head>
<body>
    <p>CMDR Miradan is currently in the {star_system} system.</p>
</body>
</html>
    """
    s3.Bucket(config.S3_SITE_BUCKET).put_object(Key=config.LOCATION_PAGE, Body=out, ContentType='text/html', CacheControl="no-cache")



def update_page_offline(last_star_system):
    s3 = boto3.resource('s3')
    out = f"""
<html>
<head>
  <title>Where in the Universe is CMDR {config.CMDR_NAME}?</title>
</head>
<body>
    <p>CMDR {config.CMDR_NAME} is currently <b>OFFLINE</b>, but was last seen docked at Gelfland Orbital in the {last_star_system} system.</p>
</body>
</html>
    """
    s3.Bucket('edwardkozlowski.com').put_object(Key='elite_location.html', Body=out, ContentType='text/html', CacheControl="no-cache")



class FSDJumpHandler(EventSubscriber):
    name = "FSDJump"

    def send(self, event_data):
        print("Handling FSD Jump")
        # handle the FSD Jump event.  Already a dictionary.
        star_system = event_data.get('StarSystem')
        system_address = event_data.get('SystemAddress')
        x_pos, y_pos, z_pos = event_data.get('StarPos')
        update_star_system(star_system, system_address, x_pos, y_pos, z_pos)
        update_page(star_system)


fsdHandler = FSDJumpHandler()

if __name__ == "__main__":
    update_page_offline("HIP 12635")