import re

from .base import BaseParser


class MnNCICParser(BaseParser):

    def __init__(self, config_obj):
        super(MnNCICParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Minnesota NCIC"

    def parse_hotlist_line(self, raw_line, alert_config):

        if self.line_count <= 1:
            return None

        columns = [c.strip() for c in raw_line.split(',')]
        list_type = columns[0][0]

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        plate_number = columns[3].strip()

        state = columns[4].strip()
        year = columns[9].strip()
        make = self.get_vehicle_make(columns[8].strip())
        model = columns[9].strip()
        color = self.get_vehicle_color(columns[11].strip())
        list_name = alert_config['name']

        vehicle_info = "%s %s %s %s" % (color, year, make, model)
        vehicle_info = vehicle_info.strip()
        description = '"{} ({}) - {}"'.format(list_name, state, vehicle_info)
        description = re.sub(' +', ' ', description)

        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'description': description,
            'list_type': list_type,
            'state': state
        }

        return alert_data

    def get_default_lists(self):
        return [
            {
                'name': 'MN NCIC Stolen Vehicle',
                'parse_code': 'V'
            },
            {
                'name': 'MN NCIC Stolen License Plate',
                'parse_code': 'P'
            },
            {
                'name': 'MN NCIC Wanted Person',
                'parse_code': 'W'
            },
            {
                'name': 'MN NCIC CPIC data',
                'parse_code': 'R'
            },
            {
                'name': 'MN NCIC Protection Order',
                'parse_code': 'H'
            },
            {
                'name': 'MN NCIC Missing Person',
                'parse_code': 'M'
            },
            {
                'name': 'MN NCIC Violent Person',
                'parse_code': 'L'
            },
            {
                'name': 'MN NCIC Group Member Capability',
                'parse_code': 'T'
            },
            {
                'name': 'MN NCIC Supervised Release',
                'parse_code': 'C'
            },
            {
                'name': 'MN NCIC National Sex Offender Registry',
                'parse_code': 'X'
            },
            {
                'name': 'MN NCIC Immigration Violator Files',
                'parse_code': 'N'
            },

        ]

    def get_example_format(self):
        return "C845996328,0H0671200,20211122,JFJ4764,0H,2022,TK,2013,CHEV,AVA,PK,CRM"

    def get_example_tests(self):
        return [
            {'raw_line': self.get_example_format(), 'plate': '85TF66', 'state': 'NY'}
        ]
