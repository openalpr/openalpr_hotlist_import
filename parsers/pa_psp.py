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
        TAG_DATE_START = 39

        VEHICLE_YEAR_START = 45
        MAKE_START = 49
        MODEL_START = 53
        COLOR_START = 58

        tag_date = raw_line[TAG_DATE_START:TAG_DATE_START+4].strip()
        vehicle_year = raw_line[VEHICLE_YEAR_START:VEHICLE_YEAR_START+4].strip()
        vehicle_make = raw_line[MAKE_START:MAKE_START+4].strip()
        vehicle_model = raw_line[MODEL_START:MODEL_START+3].strip()
        vehicle_color = raw_line[COLOR_START:].strip()

        vehicle_description = "%s %s %s %s" % (vehicle_color, vehicle_year, vehicle_make, vehicle_model)
        vehicle_description = vehicle_description.strip()


        list_type = raw_line[LIST_TYPE_START:LIST_TYPE_END].strip()
        incident_date = raw_line[INCIDENT_DATE_START:INCIDENT_DATE_END].strip()
        plate_number = raw_line[PLATE_FIELDS_START:PLATE_FIELDS_END].strip()
        state = raw_line[LICENSE_PLATE_STATE_START:LICENSE_PLATE_STATE_END].strip().replace("0", "O")

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code']:
            return None

        list_name = alert_config['name']



        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s - %s (%s) %s' % (list_name, incident_date, state, vehicle_description)

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description.strip())



        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description
        }


    def get_default_lists(self):
        return [
            {
            'name': 'Amber Alert',
            'parse_code': 'A'
            },
            {
            'name': 'Felony',
            'parse_code': 'F'
            },
            {
            'name': 'Wanted Person',
            'parse_code': 'W'
            },
            {
            'name': 'Stolen Vehicle',
            'parse_code': 'V'
            },
            {
            'name': 'Stolen Plate',
            'parse_code': 'P'
            },
            {
            'name': 'Missing Person',
            'parse_code': 'M'
            },
            {
            'name': 'Supervised Release',
            'parse_code': 'C'
            },
            {
            'name': 'Protection Order',
            'parse_code': 'H'
            },
            {
            'name': 'Protective Interest',
            'parse_code': 'K'
            },
            {
            'name': 'Violent Person',
            'parse_code': 'L'
            },
            {
            'name': 'Stolen Canadian Vehicle',
            'parse_code': 'R'
            },
            {
            'name': 'Gang/Terrorist Member',
            'parse_code': 'T'
            },
            {
            'name': 'Sex Offender',
            'parse_code': 'X'
            },
        ]


    def get_example_format(self):
        return "V123456789LA057020020190509AB123456  CA2009MC2009YAMACYLMCBLK"

