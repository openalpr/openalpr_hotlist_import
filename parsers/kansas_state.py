from .base import BaseParser
from collections import OrderedDict
from datetime import date
import re

car_types = {
    'PC': 'Passenger Car',
    'TL': 'Trailer'
}

car_makes = {
    "FORD": "Ford",
    "DODG": "Dodge",
    "TOYT": "Toyota",
    "CHEV": "Chevrolet",
    "NISS": "Nissan",
    "BUIC": "Buick",
    "HOND": "Honda",
    "GMC": "GMC",
    "CADI": "Cadillac",
    "KIA": "Kia",
    "SUBA": "Subaru",
    "JEEP": "Jeep",
    "PONT": "Pontiac",
    "INFI": "Infinit",
    "ACUR": "Acura",
    "SUZI": "Suzuki",
    "MITS": "Mitsubishi",
    "HYUN": "Hyundai",
    "LINC": "Lincoln",
    "VOLV": "Volvo"
}

car_colors = {
    "WHI": "White",
    "RED": "Red",
    "GLD": "Gold",
    "GRN": "Green",
    "YEL": "Yellow",
    "BLK": "Black",
    "SIL": "Silver",
    "GRY": "Gray",
    "ONG": "Orange",
    "BLU": "Blue",
    "TAN": "Tan"
}


class KsStateParser(BaseParser):

    def __init__(self, config_obj):
        super(KsStateParser, self).__init__(config_obj)
        self.regex = {
            'format1_list_type': re.compile('#[0-9]\s([A-Z\s/]+)\s?.*[!-]'),
            'format5_list_type': re.compile('#[0-9]\s(.+)[0-9]{8}'),
            'valid_year': re.compile('[0-9]{4}'),
            'format3_line': re.compile('#[0-9][A-Z\s]*[0-9]{2}/[0-9]{2}/[0-9]{4}'),
            'format3_split': re.compile('^[A-Z-\s]{2,}([0-9]{4}.*)'),
            'format3_split_alt': re.compile('^[A-Z-\s]{2,}-([A-Z]{3,}.*)'),  # When vehicle year is not provided
            'empty_plate': re.compile('^[^-0-9a-zA-Z]+#'),
            'plate_start': re.compile('[\w\s]+-?[\w\s]+[A-Z\s]*#[0-9]+')}

    def get_parser_name(self):
        return "Kansas State"

    def get_color(self, options, default=''):
        """Convert color codes

        :param [str] options: List of keys to check in order of preference. If
            duplicate options are passed, they will be filtered out while
            preserving the original list order
        :param str default: Value to return if no keys in ``options`` match
        :return str: Human readable color label
        """
        options = list(OrderedDict.fromkeys(options))
        color = default
        for o in options:
            if color == default:
                color = car_colors.get(o, default)
            else:
                break
        return color

    def get_make(self, options, default=''):
        """Convert vehicle make codes

        :param [str] options: List of keys to check in order of preference. If
            duplicate options are passed, they will be filtered out while
            preserving the original list order
        :param str default: Value to return if no keys in ``options`` match
        :return str: Human readable vehicle make
        """
        options = list(OrderedDict.fromkeys(options))
        make = default
        for o in options:
            if make == default:
                make = car_makes.get(o, default)
            else:
                break
        return make

    def get_plate_info(self, raw_line, canadian=False):
        """This is consistently the first two items for all formats, so handle jointly

        :param str raw_line: Full hotlist line
        :param bool canadian: Whether this is a Canadian entry line (format 2)
        :return 2-tuple(str): Plate number and capitalized state ISO code
        """
        split_token = 'CANADIAN ENTRY' if canadian else '#'
        plate_info = raw_line.split(split_token)[0]
        if ' ' in plate_info:
            *plate_number, state = re.split('\s+', plate_info)
            plate_number = ''.join(plate_number)
        else:
            plate_number, state = plate_info[:-2], plate_info[-2:]
        if canadian:
            state = f'CA-{state}'
        return plate_number, state

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle various Kansas line formats

        :param raw_line: Multiple possible formats. Bracketed items are optional
            and quotes designate literal string as opposed to variable name or
            character class (i.e. @ for letters and # for numbers)

            1) plate[ ]state"CANADIAN ENTRY - CHECK" bodytypeCode [yearMakeColor]stateAgencyORI date
            2) plate state"#"# listName! [message - "Check"] bodytypeCode [yearMakeColor]StateAgencyORI date
            3) plate state"#"#[@@]slashFormatDate@@-@@-@@[ ][year]-[make]-[model]-[color]@####### [listName-]comments
            4) plate state"#4 Suspended" bodytypeName "Lg" # county
            5) plate [state]"#8" listName date [year] make model bodytypeCode color "KSRO" "KS"#######

        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """
        # Skip the header lines and empty plate numbers
        is_header = self.line_count <= 3
        no_plate = self.regex['empty_plate'].match(raw_line)
        dummy_starts = ('unknown', 'none', 'notag', 'platenumks', 'k-state', 'not\s?availa', 'temp', '60[\s-]+day')
        clean_line = raw_line.strip().lower()
        dummy_plate = False
        for start in dummy_starts:
            if re.match(start, clean_line):
                dummy_plate = True
                break
        empty_line = len(raw_line.strip()) == 0
        if any([is_header, no_plate, dummy_plate, empty_line]):
            return None

        # Determine which format the current line follows
        if 'CANADIAN ENTRY' in raw_line:
            return self._parse_format1(raw_line)
        elif '!' in raw_line or '- check' in raw_line.lower():
            return self._parse_format2(raw_line)
        elif self.regex['format3_line'].search(raw_line):
            return self._parse_format3(raw_line)
        elif '#4 Suspended' in raw_line and self.regex['plate_start'].match(raw_line):
            return self._parse_format4(raw_line)
        elif '#8' in raw_line and self.regex['plate_start'].match(raw_line):
            return self._parse_format5(raw_line)
        else:
            return None

    def _parse_format1(self, raw_line):
        """Canadian entry items"""
        # Get plate and state
        plate_number, state = self.get_plate_info(raw_line, canadian=True)

        # Split up vehicle attributes
        bodytype_code, vehicle_info = raw_line.split(' ')[-3:-1]
        year, make, color = self._parse_vehicle_info(vehicle_info)
        description = f'{color} {year} {make} {car_types.get(bodytype_code, "")} ({state})'
        description = re.sub('\s+', ' ', description.strip())
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': 'Canadian Entry',
            'description': description}

    def _parse_format2(self, raw_line):
        """List name delimited by exclamation mark"""
        # Get plate and state
        plate_number, state = self.get_plate_info(raw_line)

        # Determine list type
        matches = self.regex['format1_list_type'].search(raw_line)
        if matches is not None and len(matches.groups()) == 1:
            list_type = re.sub('\s+[A-Z]$', '', matches.group(1).strip())
        else:
            raise ValueError('Format 2: no matches found for list type')

        # Split up vehicle attributes
        bodytype_code, vehicle_info = raw_line.split(' ')[-3:-1]
        year, make, color = self._parse_vehicle_info(vehicle_info)
        description = f'{color} {year} {make} {car_types.get(bodytype_code, "")} ({state})'
        description = re.sub('\s+', ' ', description.strip())
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type.title(),
            'description': description}

    def _parse_format3(self, raw_line):
        """Warrants - slash formatted date and dashes between most fields"""
        # Get plate and state
        plate_number, state = self.get_plate_info(raw_line)

        # Search for vehicle information
        without_date = re.split('[0-9]{2}/[0-9]{2}/[0-9]{4}', raw_line)[1]
        vehicle_and_list = self.regex['format3_split'].findall(without_date.strip())
        if len(vehicle_and_list) != 1:
            vehicle_and_list = self.regex['format3_split_alt'].findall(without_date.strip())
        vehicle_and_list = vehicle_and_list[0]
        vehicle_info, *comments_list = re.split('\s+', re.sub('\s*-\s*', '-', vehicle_and_list))
        if vehicle_info.isnumeric():
            year, make, color = ('', ) * 3
        else:
            year, make, color = self._parse_vehicle_info(re.sub('-', '', vehicle_info))

        # Find list name (if provided)
        list_codes = {
            'ALCOHOLICWAR': 'Alcoholic Warrant',
            'ALLERGIESWAR': 'Allergies Warrant',
            'ARMED/DANGPOI': 'Armed/Dangerous Person of Interest',
            'ARMED/DANGWAR': 'Armed/Dangerous Warrant',
            'ARMED/DANGWNT': 'Armed/Dangerous Warrant',
            'DRUGABUSEWAR': 'Drug Abuse Warrant',
            'ESCAPERSKWAR': 'Escape Risk Warrant',
            'OTHERWAR': 'Warrant',
            'POI': 'Person of Interest',
            'VIOLTENDPOI': 'Violent Tendencies Person of Interest',
            'VIOLTENDWAR': 'Violent Tendencies Warrant',
            'WAR': 'Warrant',
            'WNT': 'Warrant'}
        comments = ' '.join(comments_list).split(':')[0]
        if '-' in comments:
            if 'MISSING-PERSON' in comments:
                list_type = 'Missing Person'  # Only one with a "-" in the list type
            else:
                code = re.split('(?<=[A-Z])-[A-Z]', comments)[0].strip()
                list_type = list_codes[re.sub('\s', '', code)]
        else:
            list_type = 'Generic'

        # Format return description
        description = f'{color} {year} {make} ({state})'
        description = re.sub('\s+', ' ', description.strip())
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type.title(),
            'description': description}

    def _parse_format4(self, raw_line):
        """Simple suspended list - no agency ORI or vehicle make/model/year/color info"""
        # Get plate and state
        plate_number, state = self.get_plate_info(raw_line)

        # Determine list type and vehicle bodytype
        components = raw_line.split()
        assert len(components) >= 8, f'Expected 8 or more components, found {len(components)}'
        list_type = components[2]
        bodytype_year = ' '.join(components[3:-3])
        potential_year = self.regex['valid_year'].findall(bodytype_year)
        if len(potential_year) == 1:
            year = int(potential_year[0])
            bodytype = re.sub(potential_year[0], '', bodytype_year).strip()
        else:
            year = ''
            bodytype = bodytype_year

        # Format return description
        description = f'{year} {bodytype} ({state})'
        description = re.sub('\s+', ' ', description.strip())
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type.title(),
            'description': description}

    def _parse_format5(self, raw_line):
        """Space delimited columns"""
        # Get plate and state
        plate_number, state = self.get_plate_info(raw_line)

        # Determine list type
        matches = self.regex['format5_list_type'].search(re.sub('/', '', raw_line))
        if matches is not None and len(matches.groups()) == 1:
            list_type = matches.group(1).strip()
        else:
            raise ValueError('Format 5: no matches found for list type')

        # Split up vehicle attributes
        bodytype_code, vehicle_info = raw_line.split(' ')[-3:-1]
        year, make, color = self._parse_vehicle_info(vehicle_info)
        description = f'{color} {year} {make} {car_types.get(bodytype_code, "")} ({state})'
        description = re.sub('\s+', ' ', description.strip())
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type.title(),
            'description': description}

    def _parse_vehicle_info(self, vehicle_info):
        """Handle vehicle string with no delimiters

        :param str vehicle_info: Matching line format 1 or 2 where the state
            agency ORI is always included, but vehicle info may or may not be
            included
        :return 3-tuple(str): Including year, make, and color
        """

        # Check if year is included and valid
        potential_year = vehicle_info[:4]
        year = ''
        if self.regex['valid_year'].match(potential_year):
            vehicle_info = vehicle_info[4:]
            if 1900 < int(potential_year) <= int(date.strftime(date.today(), '%Y')):
                year = int(potential_year)

        # Remove the agency ORI and return early is there is nothing left
        vehicle_info = vehicle_info[:-9]
        if vehicle_info == '':
            return ('', ) * 3

        # Attempt to match car make/color (check variable length since string has no delimiters)
        min_make_code = min([len(code) for code in car_makes.keys()])
        max_make_code = max([len(code) for code in car_makes.keys()])
        make = self.get_make([vehicle_info[:min_make_code], vehicle_info[:max_make_code]])

        min_color_code = min([len(code) for code in car_colors.keys()])
        max_color_code = max([len(code) for code in car_colors.keys()])
        if '/' in vehicle_info:
            other, color2_code = vehicle_info.split('/')
            color2 = car_colors.get(color2_code, '')
            color1 = self.get_color([other[-max_color_code:], other[-min_color_code:]])
            if color1 == color2:
                color = color1
            elif color2 != '':
                color = f'{color1}/{color2}'
            else:
                color = color1
        else:
            color = self.get_color([vehicle_info[-min_color_code:], vehicle_info[-max_color_code:]])
        return year, make, color

    def get_default_lists(self):
        list_types = [
            'Stolen Vehicle',
            'Stolen Plate',
            'Missing Person',
            'Protective Order',
            'Canadian Entry',
            'Gang/Terrorist Org',
            'Warrant',
            'Suspended Or Revoked Registration',
            'Supervised Release',
            'Suspended',
            'Registered Offender',
            'Generic',
            'Armed/Dangerous Warrant',
            'Violent Tendencies Warrant',
            'Person Of Interest',
            'Drug Abuse Warrant',
            'Violent Tendencies Person Of Interest',
            'Alcoholic Warrant',
            'Armed/Dangerous Person Of Interest',
            'Escape Risk Warrant',
            'Allergies Warrant',
        ]
        return [{'name': n} for n in list_types]

    def get_example_format(self):
        return 'ABC123 KS#3 STOLEN PLATE! PC 2016CHEVMALSWSILTX0790300 20200122'
