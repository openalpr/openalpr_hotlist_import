from .base import BaseParser
import re
import datetime

class OhLeadsParser(BaseParser):

    def __init__(self, config_obj):
        super(OhLeadsParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Ohio Leads"

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle comma-separated Texas format

              OPERATION               CHAR                      01         VALUE 1
              SPACE                   CHAR                      01        
              LIC                     CHAR                      10         O => 0 convert to zero
              SPACE                   CHAR                      01
              LIS                     CHAR                      02         O => 0 convert to zero
              SPACE                   CHAR                      01
              EXP DATE                CHAR                      10         VALUE 07/07/2007
              SPACE                   CHAR                      01
              DOW                     CHAR                      10         reverse FIPS mm/dd/ccyy
              SPACE                   CHAR                      01
              VMA                     CHAR                      24         O => 0 convert to zero
              SPACE                   CHAR                      01
              VMO                     CHAR                      03         O => 0 convert to zero
              SPACE                   CHAR                      01
              VYR                     CHAR                      04         ccyy
              SPACE                   CHAR                      01
              VCO                     CHAR                      07         O => 0 convert to zero
              SPACE                   CHAR                      01
              MISC                    CHAR                      100        Warrant data (NIC/) or (IDX/)

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Avoid empty lines
        if re.match('^,+$', raw_line):
            return None

        # Skip terminal prompt lines if found:
        if re.match('^SP2-[0-9]*:', raw_line) or re.match('^and to leave', raw_line):
            return None

        ohio_list_keys = ['0H STOLEN VEHICLE', '0H WARRANT SUPP', '0H MISSING', '0H LPR CALIBRATION RECORD', '0H WARRANT' ]

        # Two formats are in the datafile
        ncicformat = True
        for listkey in ohio_list_keys:
            if listkey in raw_line:
                ncicformat = False

        if ncicformat:

            # Split columns and check parse code
            columns = [c.strip() for c in raw_line.split(' ')]

            if len(columns) != 11:
                raise ValueError('Expected 11 columns, but received %d for input: %s' %  (len(columns), raw_line))


            dummy_val, plate_number, state, record_date, expiration_date, make, model, vehicle_year, color, warrant_nix, warrant_idx = columns
            parse_code = warrant_idx[0]

        else:

            columns = [c.strip() for c in raw_line.split(' ')]

            dummy_val, plate_number, state, record_date, expiration_date, make, model, vehicle_year, color = columns[0:9]

            parse_code = " ".join(columns[9:]).strip()

        expiration_datetime = datetime.datetime.strptime(expiration_date, '%m/%d/%Y')
        today = datetime.datetime.now() + datetime.timedelta(days=1)

        if expiration_datetime < today:
            # Skip this entry because the expiration date has passed
            return None


        if plate_number == '':
            return None
        if 'parse_code' in alert_config and parse_code != alert_config['parse_code']:
            return None

        # Convert vehicle abbreviations
        make = self.get_vehicle_make(make.replace('0', 'O'))
        #bodytype = self.get_vehicle_type(bodytype)
        color = self.get_vehicle_color(color)

        # Format description
        description = '%s %s %s %s %s - %s' % (alert_config['name'], vehicle_year, color, make, model, state)
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
                'parse_code': 'S'
            },
            {
                'name': 'Suspended Registration',
                'parse_code': 'X'
            },
            {
                'name': 'State Stolen Vehicle',
                'parse_code': '0H STOLEN VEHICLE'
            },
            {
                'name': 'State Warrant Supp',
                'parse_code': '0H WARRANT SUPP'
            },
            {
                'name': 'State Missing Person',
                'parse_code': '0H MISSING'
            },


        ]

    def get_example_format(self):
        return "1 ABC123 MI 01/01/2017 04/11/2021 UHAU TL 2015 0NG/WHI M12345678 V987654321"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'GGX6728', 'state': '0H'}
               ]