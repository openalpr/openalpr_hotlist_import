from .base import BaseParser
import re


class CaClewParser(BaseParser):

    def __init__(self, config_obj):
        super(CaClewParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "California DOJ CLEW"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Example:
        # plate     state/vehicle type  alert_list-vehicle-color
        # 0         ILPC VMELRYEL/BLK
        # pieces = raw_line.split()

        # Skip the last (footer) line
        if raw_line.startswith('TOTAL RECORD'):
            return None

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        plate_number = raw_line[0:8].strip()
        state = raw_line[8:10].strip()
        county_code = raw_line[10:12]
        date_of_loss = raw_line[12:].strip()

        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s State: %s County: %s Lost on: %s' % (alert_config['name'], state, county_code, date_of_loss)

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description)

        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': alert_config['name'],
            'description': description
            # 'vehicle_other_info': vehicle_other_info
        }

    def get_default_lists(self):
        return [
            {
                'name': 'Stolen Vehicles',
                'parse_code': 'svs.tbl'
            },
            {
                'name': 'Felony Vehicles',
                'parse_code': 'sfr.tbl'
            },
            {
                'name': 'Stolen License Plates',
                'parse_code': 'slr.tbl'
            }
        ]

    def get_example_format(self):
        return "ABC1234 CA1220190515"


    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'ABC1234', 'state': 'CA', 'description': 'test State: CA County: 12 Lost on: 20190515'}
               ]

