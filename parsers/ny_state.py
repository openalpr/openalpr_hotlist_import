from .base import BaseParser
import re


PLATE_FIELDS_START = 0
STATE_START = 10
VEHICLE_TYPE_START = 12
LIST_TYPE_START = 15
VEHICLE_INFO_START = 16


class NyStateParser(BaseParser):
    def __init__(self, config_obj):
        super(NyStateParser, self).__init__(config_obj)

    def get_color(self, color):
        if color in self.config_obj['car_colors']:
            return self.config_obj['car_colors'][color]

        return color

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
        vehicle_other_info = raw_line[VEHICLE_INFO_START:].strip()

        color = ''
        make = ''
        if len(vehicle_other_info) > 1:

            make_start = 0
            make_end = len(vehicle_other_info)
            if '/' in vehicle_other_info:
                color_both = vehicle_other_info[-7:].split('/')

                # If the car is "WHI/WHI" just say "White"
                if color_both[0] != color_both[1]:
                    color = self.get_color(color_both[0]) + " / " + self.get_color(color_both[1])
                else:
                    color = self.get_color(color_both[0])

                make_end = len(vehicle_other_info) - 7
            else:
                color_candidate = vehicle_other_info[-3:]
                if color_candidate in self.config_obj['car_colors']:
                    color = self.config_obj['car_colors'][color_candidate]
                    make_end = len(vehicle_other_info) - 3
                else:
                    pass
                    # print "UNKNOWN COLOR: " + color_candidate

            make = vehicle_other_info[make_start:make_end]
            if make in self.config_obj['car_makes']:
                make = self.config_obj['car_makes'][make]
            else:
                pass
                # print "UNKNOWN MAKE: " + make

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
            # 'vehicle_type': vehicle_type,
            # 'make': make,
            # 'color': color,
            # 'vehicle_other_info': vehicle_other_info
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
