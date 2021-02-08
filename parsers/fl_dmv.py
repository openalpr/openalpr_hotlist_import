from .base import BaseParser
import re


class FlDmv(BaseParser):

    def __init__(self, config_obj):
        super(FlDmv, self).__init__(config_obj)

    def get_parser_name(self):
        return "Florida DMV"

    def get_example_format(self):
        """There are really 4 different formats, this is just expired licenses"""
        return "Y83YPH,FL,EXPIRED DRIVER LICENSES - ,G650510522640,05/14/2018,M,W,68,75,2016,WHI,NISS,7/9/2020 6:55:57 PM"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'parse_code': 'EXPIRED DRIVER LICENSES', 'plate': 'Y83YPH', 'state': 'FL'}
               ]


    def get_default_lists(self):
        return [
            {
                'name': 'DMV Expired License',
                'parse_code': 'EXPIRED DRIVER LICENSES',
                'match_strategy': 'exact',
                'hotlist_path': 'FlExpiredLicense.txt'
            },
            {
                'name': 'DMV Expired Tag',
                'parse_code': 'Expired Tag',
                'match_strategy': 'exact',
                'hotlist_path': 'FlExpiredTag.txt'
            },
            {
                'name': 'DMV Sanctioned Driver',
                'parse_code': 'SUSPENDED/REVOKED/CANCELLED LICENSE',
                'match_strategy': 'exact',
                'hotlist_path': 'FlSanctionedDriver.txt'
            },
            {
                'name': 'DMV Sex Offender',
                'parse_code': 'SEXUAL OFFENDERS/PREDATORS',
                'match_strategy': 'exact',
                'hotlist_path': 'FlSexOffender.txt'
            },
        ]

    def parse_hotlist_line(self, raw_line, alert_config):
        """Dispatch to sub-methods based on parse code"""
        if self.line_count <= 1:
            return None
        if alert_config['parse_code'] == 'EXPIRED DRIVER LICENSES':
            return self.parse_expired_license(raw_line, alert_config)
        elif alert_config['parse_code'] == 'Expired Tag':
            return self.parse_expired_tag(raw_line, alert_config)
        elif alert_config['parse_code'] == 'SUSPENDED/REVOKED/CANCELLED LICENSE':
            return self.parse_sanctioned_driver(raw_line, alert_config)
        elif alert_config['parse_code'] == 'SEXUAL OFFENDERS/PREDATORS':
            return self.parse_sex_offender(raw_line, alert_config)
        else:
            raise ValueError('Unknown parse code {}'.format(alert_config['parse_code']))

    def parse_expired_license(self, raw_line, alert_config):

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        # Divide columns
        columns = [c.strip() for c in raw_line.split(',')]
        plate_number = columns[0]
        state = columns[1]
        list_type = re.sub('\s[^A-Z]+$', '', columns[2].upper())
        vehicle_color = self.get_vehicle_color(columns[10])
        vehicle_make = self.get_vehicle_make(columns[11])

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        # Format description
        description = '{} {} {} {}'.format(alert_config['name'], vehicle_color, vehicle_make, state)
        description = re.sub(' +', ' ', description)
        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description}
        return alert_data

    def parse_expired_tag(self, raw_line, alert_config):

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        # Divide columns (report info can include color, make, both, or neither)
        columns = [c for c in raw_line.split(',')]
        plate_number = columns[0].strip()
        state = columns[1].strip()
        report_info = columns[2].split()
        list_type = ' '.join(report_info[:2])
        if columns[2].endswith(' '):
            vehicle_color = self.get_vehicle_color(report_info[-1])
            vehicle_make = ''
        elif '  ' in columns[2]:
            vehicle_color = ''
            vehicle_make = self.get_vehicle_make(report_info[-1])
        else:
            vehicle_color = self.get_vehicle_color(report_info[-2])
            vehicle_make = self.get_vehicle_make(report_info[-1])

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code']:
            return None

        # Format description
        description = '{} {} {} {}'.format(alert_config['name'], vehicle_color, vehicle_make, state)
        description = re.sub(' +', ' ', description)
        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description}
        return alert_data

    def parse_sanctioned_driver(self, raw_line, alert_config):

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        # Divide columns
        columns = [c.strip() for c in raw_line.split(',')]
        plate_number = columns[0]
        state = columns[1]
        list_type = re.sub('\s[^A-Z]+$', '', columns[2].upper())
        vehicle_color = self.get_vehicle_color(columns[9])
        vehicle_make = self.get_vehicle_make(columns[10])

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        # Format description
        description = '{} {} {} {}'.format(alert_config['name'], vehicle_color, vehicle_make, state)
        description = re.sub(' +', ' ', description)
        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description}
        return alert_data

    def parse_sex_offender(self, raw_line, alert_config):

        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        # Divide columns

        columns = [c.strip() for c in raw_line.split(',')]
        plate_number = columns[0]
        state = columns[1]
        list_type = columns[2].upper()
        vehicle_color = self.get_vehicle_color(columns[12])
        vehicle_make = self.get_vehicle_make(columns[13])

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        # Format description
        description = '{} {} {} {}'.format(alert_config['name'], vehicle_color, vehicle_make, state)
        description = re.sub(' +', ' ', description)
        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description}
        return alert_data
