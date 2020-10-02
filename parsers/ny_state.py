from .base import BaseParser
import re


PLATE_FIELDS_START = 0
STATE_START = 10
VEHICLE_TYPE_START = 12
LIST_TYPE_START = 15
VEHICLE_MAKE_START = 16
VEHICLE_COLOR_START = 20


class NyStateParser(BaseParser):

    def __init__(self, config_obj):
        super(NyStateParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "New York State"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Example:
        # plate     state/vehicle type  alert_list-vehicle-color
        # 0         ILPC VMELRYEL/BLK

        # Parse codes
        # M - MISSING PERSON ASSOCIATED WITH REGISTRATION/PLATE
        # P - STOLEN LICENSE PLATE
        # R - STOLEN CANADIAN LICENSE PLATE
        # S - SEX OFFENDER ASSOCIATED WITH REGISTRATION/PLATE
        # T - POSSIBLE TERRORIST ASSOCIATED WITH REGISTRATION/PLATE
        # V - STOLEN MOTOR VEHICLE OR TRAILER WITH MAKE/COLOR
        # W - WANTED PERSON ASSOCIATED WITH REGISTRATION/PLATE
        # X - SUSPENDED REGISTRATION OR FALSIFIED REGISTRATION
        # Z - CLIENT ID SUSPENDED OPERATING PRIVILEGE IN NEW YORK

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        plate_number = raw_line[PLATE_FIELDS_START:STATE_START].strip()
        state = raw_line[STATE_START:VEHICLE_TYPE_START].strip()
        vehicle_type = raw_line[VEHICLE_TYPE_START:LIST_TYPE_START].strip()

        list_type = raw_line[LIST_TYPE_START].strip()
        make = self.get_vehicle_make(raw_line[VEHICLE_MAKE_START:VEHICLE_COLOR_START].strip())
        color = self.get_vehicle_color(raw_line[VEHICLE_COLOR_START:].strip())
        list_name = alert_config['name']

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code']:
            return None

        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s %s %s %s - %s' % (list_name, color, make, vehicle_type, state)

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description)

        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description
        }

    def get_default_lists(self):
        return [
            {
                'name': 'Stolen Vehicle',
                'parse_code': 'V'
            },
            {
                'name': 'Missing Person',
                'parse_code': 'M'
            },
            {
                'name': 'Stolen Plate',
                'parse_code': 'P'
            },
            {
                'name': 'Stolen Canadian Plate',
                'parse_code': 'R'
            },
            {
                'name': 'Sex Offender',
                'parse_code': 'S'
            },
            {
                'name': 'Possible Terrorist',
                'parse_code': 'T'
            },
            {
                'name': 'Wanted Person',
                'parse_code': 'W'
            }
        ]

    def get_example_format(self):
        return "ABC1234   NYPASXBUICWH"
