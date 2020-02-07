from .base import BaseParser
import re


PLATE_FIELDS_START = 0
STATE_START = 10
VEHICLE_TYPE_START = 12
LIST_TYPE_START = 15
VEHICLE_MAKE_START = 16
VEHICLE_COLOR_START = 20

car_types = {
    'PC': 'Passenger Car',
    'TL': 'Trailer'
}

car_makes = {
    "FORD": "Ford",
    "DODG": "Dodge",
    "TOYT": "Toyota",
    "CHEV": "Chevrolet",
    "NISS": "Nissan",
    "BUIC": "Buick",
    "HOND": "Honda",
    "GMC": "GMC",
    "CADI": "Cadillac",
    "KIA": "Kia",
    "SUBA": "Subaru",
    "JEEP": "Jeep",
    "PONT": "Pontiac",
    "INFI": "Infinit",
    "ACUR": "Acura",
    "SUZI": "Suzuki",
    "MITS": "Mitsubishi",
    "HYUN": "Hyundai",
    "LINC": "Lincoln",
    "VOLV": "Volvo"
}

car_colors = {
    "WHI": "White",
    "RED": "Red",
    "GLD": "Gold",
    "GRN": "Green",
    "YEL": "Yellow",
    "BLK": "Black",
    "SIL": "Silver",
    "GRY": "Gray",
    "ONG": "Orange",
    "BLU": "Blue",
    "TAN": "Tan"
}


class NyStateParser(BaseParser):

    def __init__(self, config_obj):
        super(NyStateParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "New York State"

    def get_color(self, color):
        if color in car_colors:
            return car_colors[color]

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
        make = raw_line[VEHICLE_MAKE_START:VEHICLE_COLOR_START].strip()
        color = raw_line[VEHICLE_COLOR_START:].strip()

        if len(make) > 1:
            if make in car_makes:
                make = car_makes[make]
        if len(color) > 1:

            if '/' in color:
                color_both = color[-7:].split('/')

                # If the car is "WHI/WHI" just say "White"
                if color_both[0] != color_both[1]:
                    color = self.get_color(color_both[0]) + " / " + self.get_color(color_both[1])
                else:
                    color = self.get_color(color_both[0])

            else:
                color_candidate = color[-3:]
                if color_candidate in car_colors:
                    color = car_colors[color_candidate]
                else:
                    pass
                    # print "UNKNOWN COLOR: " + color_candidate



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
