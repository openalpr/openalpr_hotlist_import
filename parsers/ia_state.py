from .base import BaseParser
import re


class IaStateParser(BaseParser):

    def __init__(self, config_obj):
        super(IaStateParser, self).__init__(config_obj)

    def get_parser_name(self):
        return 'Iowa State'

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle comma-separated Iowa format

        The Iowa State list has 7 columns
            1) License plate number
            2) License plate expiration year (9999 = unknown)
            3) NCIC vehicle type code
            4) Two-letter state ISO (including some Canadian provinces)
            5) Originating agency case number
            6) Reason code
                * B: stolen boat (not on list currently)
                * SR: supervised release
                * PO: protective order/interest or violent person
                * MP: missing person
                * N: deported felon (not on list currently)
                * LP: stolen plate
                * CNVP: stolen Canadian plate
                * VGT: violent gang member/terrorist
                * SFV: stolen/forfeited vehicle
                * WP: wanted person
                * SOR: sex offender
            7) Originating agency identifier (ORI)

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Avoid empty lines
        if re.match('^,+$', raw_line):
            return None

        # Split columns and check parse code
        columns = [c.strip() for c in raw_line.split(',')]
        if len(columns) != 7:
            return None
        plate_number, plate_expiration, bodytype, state, case_number, parse_code, ori = columns
        if plate_number == '':
            return None
        if 'parse_code' in alert_config and parse_code != alert_config['parse_code']:
            return None

        # Convert vehicle abbreviations
        bodytype = self.get_vehicle_type(bodytype)

        # Format description
        description = '%s %s (state=%s ORI=%s case number=%s)' % (
            alert_config['name'], bodytype, state, ori, case_number)
        description = re.sub(' +', ' ', description)
        return {
            'plate': plate_number.upper().replace('-', '').replace(' ', ''),
            'state': state,
            'list_type': parse_code,
            'description': description}

    def get_default_lists(self):
        return [
            {
                'name': 'Supervised Release',
                'parse_code': 'SR'
            },
            {
                'name': 'Protection Order',
                'parse_code': 'PO'
            },
            {
                'name': 'Missing Person',
                'parse_code': 'MP'
            },
            {
                'name': 'Stolen Plate',
                'parse_code': 'LP'
            },
            {
                'name': 'Stolen Canadian Plate',
                'parse_code': 'CNVP'
            },
            {
                'name': 'Violent Gang Member/Terrorist',
                'parse_code': 'VGT'
            },
            {
                'name': 'Stolen/Forfeited Vehicle',
                'parse_code': 'SFV'
            },
            {
                'name': 'Wanted Person',
                'parse_code': 'WP'
            },
            {
                'name': 'Sex Offender',
                'parse_code': 'SOR'
            },
        ]

    def get_example_format(self):
        return 'BMAC272   ,2020,TK,ON,R004163992,CNVP,ON3251500'

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'BMAC272', 'state': 'ON'}
               ]