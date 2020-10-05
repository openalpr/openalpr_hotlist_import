from .base import BaseParser
import re


class IlSosParser(BaseParser):

    def __init__(self, config_obj):
        super(IlSosParser, self).__init__(config_obj)

    def get_parser_name(self):
        return 'Iowa State'

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle Illinois SOS format

        This is a fixed width format with 4 columns
            1) License plate number
            2) A three-part string containing
                * Two-letter state ISO code
                * NCIC vehicle type code
                * List name (parse code)
            3) DOT number
            4) Plate expiration in MMYY

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Avoid empty lines
        if re.match('^,+$', raw_line):
            return None

        # Validate plate number and parse code match
        slices = {
            'license_plate': slice(0, 9),
            'state': slice(9, 11),
            'vehicle_type': slice(11, 13),
            'parse_code': slice(13, 21),
            'dot_and_exp': slice(21, 40)}
        parsed = {name: raw_line[col_slice].strip() for name, col_slice in slices.items()}
        if parsed['license_plate'] == '':
            return None
        if 'parse_code' in alert_config and parsed['parse_code'] != alert_config['parse_code']:
            return None

        # Convert vehicle abbreviations
        bodytype = self.get_vehicle_type(parsed['vehicle_type'])

        # Format description
        description = '%s %s %s (%s)' % (
            alert_config['name'], bodytype, parsed['state'], parsed['dot_and_exp'])
        description = re.sub(' +', ' ', description)
        return {
            'plate': parsed['license_plate'].upper().replace('-', '').replace(' ', ''),
            'state': parsed['state'],
            'list_type': parsed['parse_code'],
            'description': description}

    def get_default_lists(self):
        return [
            {
                'name': 'Suspended License',
                'parse_code': 'SUSPEND'
            },
            {
                'name': 'Revoked License',
                'parse_code': 'REVOKED'
            },
        ]

    def get_example_format(self):
        return '15386VDE ILFMREVOKED DOT/032910 EXP/0721'
