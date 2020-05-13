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


class TxNCIC(BaseParser):

    def __init__(self, config_obj):
        super(TxNCIC, self).__init__(config_obj)

    def get_parser_name(self):
        return "Texas NCIC"

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
