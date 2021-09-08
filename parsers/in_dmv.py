from .base import BaseParser
import re


class IndianaDmvParser(BaseParser):

    def __init__(self, config_obj):
        super(IndianaDmvParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Indiana DMV"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Skip the first (header) line
        # if self.line_count <= 1:
        #     return None

        columns = [c.strip() for c in raw_line.split(',')]
        list_type = alert_config['name']
        plate_number = columns[20].strip()
        state = columns[16].strip()

        year = columns[18].strip()
        vehicle_info = f"{year} {columns[17].strip()}".strip()

        list_name = alert_config['name']

        # Only return results that match the "parse_code"
        #if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
        #    return None

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
                'name': 'ISP Expired Registration',
                'parse_code': '*',
                'match_strategy': 'exact'
            }
        ]

    def get_example_format(self):
        return "11111,JOHN,SIMPSON,DOE,02/21/1911,123-456-7890,1 Main St,,PLEASANTVILLE,IN,12345-1111,MARION,REGULAR ID CARD,HABITUAL TRAFFIC VIOLATOR - LIFE,N,02/21/2022,IN,CENTURY CUSTOM -CCC,2021,PC,TR1234ZAL"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'TR1234ZAL', 'state': 'IN'}
               ]
