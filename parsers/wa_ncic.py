from .base import BaseParser
import sys
import re


class WaNCICParser(BaseParser):
    def __init__(self, config_obj):
        super(WaNCICParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "WA NCIC"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        LIST_TYPE_START = 2
        LIST_TYPE_END = 3

        INCIDENT_DATE_START = 19
        INCIDENT_DATE_END = 27

        PLATE_FIELDS_START = 27
        PLATE_FIELDS_END = 37

        LICENSE_PLATE_STATE_START = 37
        LICENSE_PLATE_STATE_END = 39

        list_type = raw_line[LIST_TYPE_START:LIST_TYPE_END].strip()
        incident_date = raw_line[INCIDENT_DATE_START:INCIDENT_DATE_END].strip()
        plate_number = raw_line[PLATE_FIELDS_START:PLATE_FIELDS_END].strip()
        state = raw_line[LICENSE_PLATE_STATE_START:LICENSE_PLATE_STATE_END].strip().replace("0", "O")

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code']:
            return None

        list_name = alert_config['name']

        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s - %s (%s)' % (list_name, incident_date, state)

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
        return "21V0128839WAKCS000020211006BN0W111   WA2022PC"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'BN0W111', 'state': 'WA'}
               ]