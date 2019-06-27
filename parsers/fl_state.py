from base import BaseParser
import re

with open('/home/addison/Downloads/florida.txt', 'r') as f:
    lines = [l.strip() for l in f.read().splitlines()]

class FlStateParser(BaseParser):
    def __init__(self, config_obj):
        super(FlStateParser, self).__init__(config_obj)


    def get_color(self, color):
        if color in self.config_obj['car_colors']:
            return self.config_obj['car_colors'][color]

        return color

    def parse_hotlist_line(self, raw_line, alert_config):
        # Skip the first (header) line
        if self.line_count <= 1:
            return None

        columns = [c.strip() for c in raw_line.split(';')]
        list_type = ' '.join([c.capitalize() for c in columns[0].lower().split()])
        plate_number = columns[10]
        state = columns[12]
        list_name = alert_config['name']

        # Only return results that match the "parse_code"
        if 'parse_code' in alert_config and list_type != alert_config['name']:
            return None

        # Stolen vehicle - State
        description = '{} {}'.format(list_name, state)
        description = re.sub(' +', ' ', description)

        alert_data = {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'state': state,
            'list_type': list_type,
            'description': description}
        return alert_data
