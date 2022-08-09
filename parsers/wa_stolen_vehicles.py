from .base import BaseParser
import re

from .utils import SafeList


class WaStolenVehicles(BaseParser):
    def __init__(self, config_obj):
        super(WaStolenVehicles, self).__init__(config_obj)

    def get_parser_name(self):
        return "WA Stolen Vehicles"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        parts = SafeList(raw_line.split(","))
        # Skip the funky short lines that don't have enough info
        if len(parts) < 7:
            return None

        vehicle_year = parts.get(7)
        vehicle_make = parts.get(8)
        vehicle_model = parts.get(9)
        vehicle_color = parts.get(11)

        vehicle_description = "%s %s %s %s" % (vehicle_color, vehicle_year, vehicle_make, vehicle_model)
        vehicle_description = vehicle_description.strip()

        list_type = 'Active Stolen Vehicles'
        incident_date = parts.get(12)
        plate_number = parts.get(2)
        state = parts.get(3)

        list_name = alert_config['name']

        # Stolen vehicle, Green Honda Passenger Car (State)
        description = '%s - %s (%s) %s' % (list_name, incident_date, state, vehicle_description)

        # Remove double spaces for empty stuff
        description = re.sub(' +', ' ', description.strip())
        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description
        }

    def get_default_lists(self):
        return []

    def get_example_format(self):
        return "EVS,WA0170600,921RQE,WA,2023,PC,5J6YH28573L041133,2003,HOND,ELE,4D,SIL,07/31/2022,22-08882,VERIFY 425 391 1035, BOTH PLATES ON VEHICLE, YES TO SEARCH, YES TO IMPOUND"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': '921RQE', 'state': 'WA'}
               ]