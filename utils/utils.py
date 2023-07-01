import os
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')
export_directory = config.get('utils', 'export_directory')

class Utils:

    def export_to_txt(table, file_name):
        file_path = os.path.join(export_directory, file_name)
        with open(file_path, "w") as f:
            for row in table:
                f.write(", ".join(row) + "\n")

    def export_to_json(data, file_name):
        file_path = os.path.join(export_directory, file_name)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def export_to_csv(data, file_name):
        file_path = os.path.join(export_directory, file_name)
        data.to_csv(file_path, index=False)