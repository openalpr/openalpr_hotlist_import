from .base import BaseParser
import sys
import re

class CoCCICParser(BaseParser):
    def __init__(self, config_obj):
        super(CoCCICParser, self).__init__(config_obj)


    def get_color(self, color):
        if color in self.config_obj['car_colors']:
            return self.config_obj['car_colors'][color]

        return color

    def parse_hotlist_line(self, raw_line, alert_config):

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        PLATE_FIELDS_START = 0
        STATE_START = 10
        LIST_TYPE_START = 12
        VEHICLE_INFO_START = 34


        plate_number = raw_line[PLATE_FIELDS_START:STATE_START].strip()
        state = raw_line[STATE_START:LIST_TYPE_START].strip()
        list_type = raw_line[LIST_TYPE_START:VEHICLE_INFO_START].strip()

        vehicle_other_info = raw_line[VEHICLE_INFO_START:].strip()


        list_name = alert_config['name']

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code']:
            return None

        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s - %s' % (list_name, vehicle_other_info)

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description)

        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description
            #'vehicle_type': vehicle_type,
            #'make': make,
            #'color': color,
            #'vehicle_other_info': vehicle_other_info
        }




    def get_default_lists(self):
        return [
            {
            'name': 'CCIC Attempt To Locate',
            'parse_code': 'Attempt To Locate'
            },
            {
            'name': 'CCIC Felony Warrant',
            'parse_code': 'Felony Warrant'
            },
            {
            'name': 'CCIC Local Warrant',
            'parse_code': 'Local Warrant'
            },
            {
            'name': 'CCIC Reported Lost',
            'parse_code': 'Reported Lost'
            },
            {
            'name': 'CCIC Sexual Offender',
            'parse_code': 'Sexual Offender'
            },
            {
            'name': 'CCIC Stolen/Car Jacking',
            'parse_code': 'Stolen/Car Jacking/Ca'
            },
            {
            'name': 'CCIC Stolen Plate',
            'parse_code': 'Stolen Plate'
            },
            {
            'name': 'CCIC Stolen Vehicle',
            'parse_code': 'Stolen Vehicle'
            },
            {
            'name': 'CCIC Used in Felony',
            'parse_code': 'Used in Felony or By'
            },
            {
            'name': 'CCIC Used in Misdemeanor',
            'parse_code': 'Used in Misdemeanor o'
            }
        ]



    def get_example_format(self):
        return "ABC123    COAttempt To Locate     2002 FORD FOC BLK"

