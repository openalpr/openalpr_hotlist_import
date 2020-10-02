from .base import BaseParser
import re


class TxTCIC(BaseParser):

    def __init__(self, config_obj):
        super(TxTCIC, self).__init__(config_obj)

    def get_parser_name(self):
        return "Texas TCIC"

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle comma-separated Texas format

        The Texas TIC list has 8 columns
            1) Record identifier with parse code
                * E: violent person
                * M: missing person
                * O: protection order
                * P: stolen plate
                * T: threat against peace officer
                * V: stolen vehicle
                * W: wanted person
                * X: sex offender
                * Y: child safety check
            2) License plate number
            3) License plate state
            4) Vehicle year
            5) Vehicle make
            6) Vehicle model
            7) Vehicle bodytype
            8) Vehicle color

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Avoid empty lines
        if re.match('^,+$', raw_line):
            return None

        # Split columns and check parse code
        columns = [c.strip() for c in raw_line.split(',')]
        if len(columns) != 8:
            raise ValueError('Expected 8 columns, but received %d' % len(columns))
        record_id, plate_number, state, year, make, model, bodytype, color = columns
        if plate_number == '':
            return None
        parse_code = record_id[1]
        if 'parse_code' in alert_config and parse_code != alert_config['parse_code']:
            return None

        # Convert vehicle abbreviations
        make = self.get_vehicle_make(make.replace('0', 'O'))
        bodytype = self.get_vehicle_type(bodytype)
        color = self.get_vehicle_color(color)

        # Format description
        description = '%s %s %s %s %s - %s' % (alert_config['name'], year, color, make, bodytype, state)
        description = re.sub(' +', ' ', description)
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': parse_code,
            'description': description}

    def get_default_lists(self):
        return [
            {
                'name': 'Violent Person',
                'parse_code': 'E'
            },
            {
                'name': 'Missing Person',
                'parse_code': 'M'
            },
            {
                'name': 'Protection Order',
                'parse_code': 'O'
            },
            {
                'name': 'Stolen Plate',
                'parse_code': 'P'
            },
            {
                'name': 'Threat Against Peace Officer',
                'parse_code': 'T'
            },
            {
                'name': 'Stolen Vehicle',
                'parse_code': 'V'
            },
            {
                'name': 'Wanted Person',
                'parse_code': 'W'
            },
            {
                'name': 'Sex Offender',
                'parse_code': 'X'
            },
            {
                'name': 'Child Safety Check',
                'parse_code': 'Y'
            },
        ]

    def get_example_format(self):
        return "TW1026325915,17MFM5,TX,2009,FORD,TK,PK,WHI"
