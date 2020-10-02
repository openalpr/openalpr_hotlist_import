from .base import BaseParser
import re


class AlStateParser(BaseParser):

    def __init__(self, config_obj):
        super(AlStateParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Alabama State"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Skip the first (header) line
        # if self.line_count <= 1:
        #     return None

        columns = [c.strip() for c in raw_line.split(',')]
        list_type = columns[7].strip().upper()
        plate_number = columns[0].strip()
        state = columns[8].strip()
        # ori = columns[2].strip()
        make = self.get_vehicle_make(columns[3].strip())
        model = columns[4].strip()
        color = self.get_vehicle_color(columns[5].strip())
        year = columns[6].strip()
        list_name = alert_config['name']

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        vehicle_info = "%s %s %s %s" % (color, year, make, model)
        vehicle_info = vehicle_info.strip()
        # Stolen vehicle - State
        description = '"{} ({}) - {}"'.format(list_name, state, vehicle_info)
        description = re.sub(' +', ' ', description)

        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description
        }

        return alert_data

    def get_default_lists(self):
        return [
            {
                'name': 'Stolen Vehicles',
                'parse_code': 'Stolen Vehicle or Vehicle Part'
            }
        ]

    def get_example_format(self):
        return "Taghere1,,V000000000,CHEV,,RED,1985,Stolen Vehicle or Vehicle Part,WA"
