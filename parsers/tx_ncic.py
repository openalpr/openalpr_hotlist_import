from .base import BaseParser
import re


class TxNCIC(BaseParser):

    def __init__(self, config_obj):
        super(TxNCIC, self).__init__(config_obj)

    def get_parser_name(self):
        return "Texas NCIC"

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle comma-separated Texas format

        The Texas TIC list has 8 columns
            1) Record identifier with parse code
                * B: stolen boats
                * C: supervised release
                * H: protection order
                * M: missing person
                * N: deported felons
                * P: stolen plate
                * R: stolen Canadian vehicle
                * T: gang member/terrorist
                * V: stolen vehicle
                * W: wanted person
                * X: sex offender
            2) Originating state record identifier
            3) Original record date in yyyymmdd format
            4) License plate number
            5) License plate state
            6) Current vehicle registration year
            7) Vehicle year
            8) Vehicle make
            9) Vehicle model
            10) Vehicle bodytype
            11) Vehicle color

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Avoid empty lines
        if re.match('^,+$', raw_line):
            return None

        # Split columns and check parse code
        columns = [c.strip() for c in raw_line.split(',')]
        if len(columns) != 11:
            raise ValueError('Expected 11 columns, but received %d' % len(columns))
        record_id, state_record_id, record_date, plate_number, state, registration_year, vehicle_year, make, model, bodytype, color = columns
        parse_code = record_id[0]
        if plate_number == '':
            return None
        if 'parse_code' in alert_config and parse_code != alert_config['parse_code']:
            return None

        # Convert vehicle abbreviations
        make = self.get_vehicle_make(make.replace('0', 'O'))
        bodytype = self.get_vehicle_type(bodytype)
        color = self.get_vehicle_color(color)

        # Format description
        description = '%s %s %s %s %s - %s' % (alert_config['name'], vehicle_year, color, make, bodytype, state)
        description = re.sub(' +', ' ', description)
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': parse_code,
            'description': description}

    def get_default_lists(self):
        return [
            {
                'name': 'Stolen Boat',
                'parse_code': 'B'
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
                'name': 'Missing Person',
                'parse_code': 'M'
            },
            {
                'name': 'Deported Felon',
                'parse_code': 'N'
            },
            {
                'name': 'Stolen Plate',
                'parse_code': 'P'
            },
            {
                'name': 'Stolen Canadian Plate',
                'parse_code': 'R'
            },
            {
                'name': 'Gang Member/Terrorist',
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
        ]

    def get_example_format(self):
        return "C165399977,0H0671200,20200124,GGX6728,0H,2021,2009,D0DG,CHA,4D,GRY"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'GGX6728', 'state': '0H'}
               ]