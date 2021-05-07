from .base import BaseParser
import re


class IlLeadsParser(BaseParser):

    def __init__(self, config_obj):
        super(IlLeadsParser, self).__init__(config_obj)

    def get_parser_name(self):
        return 'Illinois LEADS'

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle Illinois LEADS format

        Every row begins with
            1) License plate number
            2) A three-part string containing
                * Two-letter state ISO code
                * NCIC vehicle type code
                * List name (parse code)

        Following the three-part string, a space may or may not precede the
        rest of the line. Regardless, the parse code never extends past column
        20 (zero-indexed). Each parse code has its own format for the remaining
        information, so they need to be handled separately once the parse code
        is identified.

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Validate plate number and parse code match
        slices = {
            'license_plate': slice(0, 8),
            'state': slice(8, 10),
            'vehicle_type': slice(10, 12),
            'parse_code': slice(12, 19)}
        parsed = {name: raw_line[col_slice].strip() for name, col_slice in slices.items()}
        if parsed['license_plate'] == '':
            return None
        if 'parse_code' in alert_config and parsed['parse_code'] != alert_config['parse_code']:
            return None

        # Then dispatch to appropriate method based on parse code
        method_name = '_parse_' + parsed['parse_code'].lower()
        try:
            info = getattr(self, method_name)(raw_line)
        except AttributeError:
            return None

        # Convert vehicle abbreviations
        bodytype = self.get_vehicle_type(parsed['vehicle_type'])

        # Format description
        parse_conversions = {
            'STOLEN': 'Stolen vehicle',
            'MISSING': 'Missing person',
            'WANTED': 'Wanted person'}
        description = '%s: %s (%s)' % (
            parse_conversions[parsed['parse_code']], bodytype, parsed['state'])
        description += ' | ' + info
        description = re.sub(' +', ' ', description)
        return {
            'plate': parsed['license_plate'].upper().replace('-', '').replace(' ', ''),
            'state': parsed['state'],
            'list_type': parsed['parse_code'],
            'description': description}

    def _parse_missing(self, raw_line):
        return self._parse_person(raw_line)

    def _parse_person(self, raw_line):
        """Extract wanted person information

        The name, sex, race, and date of birth information are already
        formatted decently in the raw line, so we can return as-is. Also,
        extra spaces will be handled by ``self.parse_hotlist_line`` when the
        description is formatted
        """
        person_info = raw_line[19:77].strip()
        leads_number = raw_line[81:].strip()
        return '%s (LEADS=%s)' % (person_info, leads_number)

    def _parse_stolen(self, raw_line):
        """Format stolen information into description"""
        slices = {
            'vehicle_year': slice(23, 25),
            'vehicle_make': slice(30, 35),
            'vehicle_model': slice(39, 43),
            'vehicle_style': slice(47, 50),
            'vehicle_color': slice(54, 62),
            'dot_number': slice(66, 73),
            'leads_number': slice(77, 85)}
        parsed = {name: raw_line[col_slice].strip() for name, col_slice in slices.items()}
        make = self.get_vehicle_make(parsed['vehicle_make'])
        color = self.get_vehicle_color(parsed['vehicle_color'])
        return "'%s %s %s (LEADS=%s)" % (parsed['vehicle_year'], color, make, parsed['leads_number'])

    def _parse_wanted(self, raw_line):
        return self._parse_person(raw_line)

    def get_default_lists(self):
        return [
            {
                'name': 'Stolen Vehicle',
                'parse_code': 'STOLEN'
            },
            {
                'name': 'Missing Person',
                'parse_code': 'MISSING'
            },
            {
                'name': 'Wanted Person',
                'parse_code': 'WANTED'
            },
        ]

    def get_example_format(self):
        return '660JEM  WIPCSTOLEN VYR/05 VMA/DODG VMO/MAG VST/4D VCO/RED     DOT/010315 LDS/V16A0661'

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': '660JEM', 'state': 'WI'}
               ]
