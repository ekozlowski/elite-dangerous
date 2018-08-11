import os
import config
import json
import time


class EventFile:

    def __init__(self, path):
        self.path = path
        self.metadata = {"seek_pos": 0, "st_mtime": 0}
        self.metadata_path = self.path + ".processed.json"
        self.read_metadata()

    def read_metadata(self):
        if os.path.exists(self.metadata_path):
            self.metadata = json.loads(open(self.metadata_path, 'r').read())

    def save_metadata(self):
        json.dump(self.metadata, open(self.metadata_path, 'w'))

    def record_new_modtime(self):
        self.metadata['st_mtime'] = os.stat(self.path).st_mtime

    def has_been_modified(self):
        return self.metadata.get("st_mtime") != os.stat(self.path).st_mtime

    def get_events(self):
        if not self.has_been_modified():
            return
        fp = open(self.path, 'r')
        fp.seek(self.metadata.get('seek_pos'))
        line = fp.readline()
        while line:
            print(f"fp position is {fp.tell()}")
            self.metadata['seek_pos'] = fp.tell()
            self.record_new_modtime()
            self.save_metadata()
            yield line
            line = fp.readline()


def get_events():
    begin = time.time()
    files = os.listdir(config.ELITE_LOG_DIR)
    files = [x for x in files if x.endswith('.log')]
    for f in files:
        ef = EventFile(os.path.join(config.ELITE_LOG_DIR, f))
        for event in ef.get_events():
            yield event.strip()
    end = time.time()
    print("Event feed completed in %.02f seconds." % (end - begin,))