from .base import BaseParser
import re

car_types = {
    '0B': 'Omnibus',
    '0R': 'Organization',
    'AM': 'Ambulance',
    'AP': 'Apportioned',
    'AQ': 'Antique',
    'AR': 'Amateur Radio',
    'AT': 'All-Terrain Vehicle',
    'BU': 'Bus',
    'C0': 'Commercial',
    'CC': 'Consular Corps',
    'CI': 'City-Owned',
    'CL': 'Collegiate',
    'CM': 'Commemorative',
    'CN': 'Conservation',
    'CU': 'County-Owned',
    'DA': 'Drive Away',
    'DB': 'Dune Buggy',
    'DL': 'Dealer',
    'DP': 'Diplomatic',
    'DU': 'Duplicate',
    'DV': 'Disabled Veteran',
    'DX': 'Disabled Persons',
    'EX': 'Exempt',
    'FD': 'Fire Department',
    'FM': 'Farm Vehicle',
    'HI': 'Hearing Impaired',
    'IP': 'International Plate',
    'IT': 'In-Transit (Temporary)',
    'JJ': 'Judge or Justice',
    'LE': 'Legislative',
    'LF': 'Law Enforcement',
    'MC': 'Motorcycle',
    'MD': 'Motorcycle Dealer',
    'MF': 'Manufacturer',
    'ML': 'Military Vehicle (Canadian)',
    'MP': 'Moped',
    'MR': 'Armed Forces Reservist',
    'MV': 'Military Vehicle (US)',
    'MY': 'Military (Aircraft)',
    'NG': 'National Guard',
    'NP': 'Non-Passenger Civilian Aircraft',
    'PC': 'Passenger Car',
    'PE': 'Personalized/Customized',
    'PF': 'Professions',
    'PH': 'Doctor',
    'PP': 'Passenger Civilian Aircraft',
    'PR': 'Press',
    'PS': 'Professional Sports Team',
    'PX': 'Pharmacist',
    'RE': 'Reciprocal',
    'RV': 'Rented Vehicle or Trailer',
    'SC': 'Special Purpose',
    'SN': 'Snowmobile',
    'ST': 'State-Owned',
    'SV': 'School Vehicle',
    'TK': 'Truck',
    'TL': 'Trailer',
    'TM': 'Temporary',
    'TP': 'Transporter',
    'TR': 'Semi-truck',
    'TX': 'Taxi Cab',
    'US': 'US Government',
    'VF': 'Veteran',
    'ZZ': 'ATV and Snowmobiles',
}

car_makes = {
    "ACUR": "Acura",
    "AUDI": "Audi",
    "BMW": "BMW",
    "BUIC": "Buick",
    "CADI": "Cadillac",
    "CHEV": "Chevrolet",
    "CHRY": "Chrysler",
    "DODG": "Dodge",
    "FORD": "Ford",
    "GMC": "GMC",
    "HOND": "Honda",
    "HYUN": "Hyundai",
    "INFI": "Infiniti",
    "ISU": "Isuzu",
    "JAGU": "Jaguar",
    "JEEP": "Jeep",
    "KIA": "Kia",
    "LEXS": "Lexus",
    "LINC": "Lincoln",
    "MAZD": "Mazda",
    "MITS": "Mitsubishi",
    "NISS": "Nissan",
    "PONI": "Pontiac",
    "PONT": "Pontiac",
    "STRN": "Saturn",
    "SUBA": "Subaru",
    "SUZI": "Suzuki",
    "TOYT": "Toyota",
    "VOLV": "Volvo",
    "VOLK": "Volkswagen"
}

car_colors = {
    "AME": "Amethyst Purple",
    "BGE": "Beige",
    "BLK": "Black",
    "BLU": "Blue",
    "BRO": "Brown",
    "BRZ": "Bronze",
    "CAM": "Camouflage",
    "COM": "Chrome",
    "CPR": "Copper",
    "CRM": "Cream",
    "DBL": "Dark Blue",
    "DGR": "Dark Green",
    "GLD": "Gold",
    "GRN": "Green",
    "GRY": "Gray",
    "LAV": "Lavender Purple",
    "LBL": "Light Blue",
    "LGR": "Light Green",
    "MAR": "Maroon",
    "MVE": "Mauve",
    "ONG": "Orange",
    "PLE": "Purple",
    "PNK": "Pink",
    "RED": "Red",
    "SIL": "Silver",
    "TAN": "Tan",
    "TEA": "Teal",
    "TPE": "Taupe",
    "TRQ": "Turquoise",
    "WHI": "White",
    "YEL": "Yellow",
}


class TxTCIC(BaseParser):

    def __init__(self, config_obj):
        super(TxTCIC, self).__init__(config_obj)

    def get_parser_name(self):
        return "Texas TCIC"

    @staticmethod
    def get_vehicle(attribute, value):
        """Safe-get for vehicle attributes

        :param str attribute: One of type, make, or color
        :param str value: Raw code to search for in lookup tables
        :return str: Cleaned value (if found), or the same value passed
        """
        if attribute == 'type':
            return car_types.get(value, value)
        elif attribute == 'make':
            return car_makes.get(value, value)
        elif attribute == 'color':
            return car_colors.get(value, value)
        else:
            raise ValueError('Expected attribute to be type, make, or color, but received %s' % attribute)

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
        make = self.get_vehicle('make', make.replace('0', 'O'))
        bodytype = self.get_vehicle('type', bodytype)
        if len(color) > 1:
            if '/' in color:
                colors = color.split('/')

                # If the car is "WHI/WHI" just say "White"
                if colors[0] != colors[1]:
                    color = self.get_vehicle('color', colors[0]) + "/" + self.get_vehicle('color', colors[1])
                else:
                    color = self.get_vehicle('color', colors[0])
            else:
                color = self.get_vehicle('color', color)

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
