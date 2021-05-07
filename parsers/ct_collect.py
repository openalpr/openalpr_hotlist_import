from .base import BaseParser
import re


class CtCollectParser(BaseParser):

    def __init__(self, config_obj):
        super(CtCollectParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Florida DMV"

    def get_example_format(self):
        """There are really 4 different formats, this is just expired licenses"""
        return "ABC123  All Terrain                   Honda                         TRX350TM                      AT                            Red                           2005Regular                       20170930EX"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'parse_code': '*', 'plate': 'ABC123', 'state': 'CT'}
               ]


    def get_default_lists(self):
        return [
            {
                'name': 'Collect Expired License',
                'parse_code': '*',
                'match_strategy': 'exact',
            }
        ]

    def parse_hotlist_line(self, raw_line, alert_config):


  # <field name="PlateNumber" from="01" to="08" />
  # <field name="plateClassName" from="09" to="38" />
  # <field name="make" from="39" to="69" />
  # <field name="model" from="70" to="100" />
  # <field name="style" from="101" to="131" />
  # <field name="PrimaryColor" from="132" to="162" />
  # <field name="Year" from="163" to="167" />
  # <field name="VehicleUsage" from="168" to="198" />
  # <field name="RegistrationExpiration" from="199" to="207" />
  # <field name="RegistartionStatus" from="208" to="209" />
  # </record>

        plate_number = raw_line[0:8].strip()
        plate_class_name = raw_line[8:38].strip()
        make = raw_line[38:68].strip()
        model = raw_line[68:98].strip()
        style = raw_line[98:128].strip()
        color = raw_line[128:158].strip()
        year = raw_line[158:162].strip()
        vehicle_usage = raw_line[162:192].strip()
        reg_exp = raw_line[192:200].strip()
        reg_status = raw_line[200:202].strip()
        state = 'CT'


        list_name = alert_config['name']

        # Stolen vehicle, Green Honda Passenger Car (State)
        description = f'{color} {year} {make} {model} Expired: {reg_exp}'

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description)

        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': alert_config['name'],
            'description': description
        }
