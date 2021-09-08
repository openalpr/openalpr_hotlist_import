import re

from .base import BaseParser


class KsTopekaParser(BaseParser):

    def __init__(self, config_obj):
        super(KsTopekaParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Kansas Topeka PD"

    def parse_hotlist_line(self, raw_line, alert_config):
        columns = [c.strip() for c in raw_line.split(',')]
        list_type = columns[0].strip().upper()
        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        plate_number = columns[3].strip()
        state = columns[4].strip()
        year = columns[7].strip()
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
        return "V,NY03030P0,20210609,85TF66,NY,2021,MC,2005,YAMA,CYL,MC,BLK"

    def get_example_tests(self):
        return [
            {'raw_line': self.get_example_format(), 'plate': '85TF66', 'state': 'NY'}
        ]
