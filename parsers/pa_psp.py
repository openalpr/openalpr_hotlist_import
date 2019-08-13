from .base import BaseParser
import sys
import re

class PaPspParser(BaseParser):
    def __init__(self, config_obj):
        super(PaPspParser, self).__init__(config_obj)


    def parse_hotlist_line(self, raw_line, alert_config):
        # Example:
        # plate     state/vehicle type  alert_list-vehicle-color
        # 0         ILPC VMELRYEL/BLK
        #pieces = raw_line.split()

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        LIST_TYPE_START = 0
        LIST_TYPE_END = 1


        INCIDENT_DATE_START = 19
        INCIDENT_DATE_END = 27

        PLATE_FIELDS_START = 27
        PLATE_FIELDS_END = 37

        LICENSE_PLATE_STATE_START = 37
        LICENSE_PLATE_STATE_END = 39

        list_type = raw_line[LIST_TYPE_START:LIST_TYPE_END].strip()
        incident_date = raw_line[INCIDENT_DATE_START:INCIDENT_DATE_END].strip()
        plate_number = raw_line[PLATE_FIELDS_START:PLATE_FIELDS_END].strip()
        state = raw_line[LICENSE_PLATE_STATE_START:LICENSE_PLATE_STATE_END].strip().replace("0", "O")

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code']:
            return None

        list_name = alert_config['name']



        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s - %s (%s)' % (list_name, incident_date, state)

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description)



        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description
        }
