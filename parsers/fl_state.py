from .base import BaseParser
import re


class FlStateParser(BaseParser):

    def __init__(self, config_obj):
        super(FlStateParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Florida State"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        columns = [c.strip() for c in raw_line.split(';')]
        list_type = columns[0].strip().upper()
        plate_number = columns[10].strip()
        state = columns[12].strip()
        # ori = columns[1].strip()
        ori_description = columns[2].strip()
        oca = columns[3].strip()
        oan = columns[4].strip()
        pcn = columns[5].strip()
        ncic = columns[6].strip()
        list_name = alert_config['name']

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['parse_code'].upper():
            return None

        extra_info = ""
        if len(oca) > 0:
            extra_info = "OCA: " + oca
        elif len(oan) > 0:
            extra_info = "OAN: " + oan
        elif len(pcn) > 0:
            extra_info = "PCN: " + pcn
        elif len(ncic) > 0:
            extra_info = "NCIC: " + ncic
        # Stolen vehicle - State
        description = '"{} ({}) - {}, {}"'.format(list_name, state, ori_description, extra_info)
        description = re.sub(' +', ' ', description)

        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description}
        return alert_data


    def get_example_format(self):
        return "STOLEN LICENSE PLATE;FL0123456;TALLAHASSEE POLICE DEPARTMENT;11-1234;;P123456789;P554433221;01/03/2019;N;01/01/2019 00:03:00;ABC123;2019;FL;PC;01/06/2019 16:03:04"


    def get_default_lists(self):
        return [
            {
                'name': 'Stolen License Plate',
                'parse_code': 'STOLEN LICENSE PLATE'
            },
            {
                'name': 'Stolen Vehicle',
                'parse_code': 'STOLEN VEHICLE'
            },
        ]