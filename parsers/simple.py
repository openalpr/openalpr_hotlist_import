from .base import BaseParser


class SimpleParser(BaseParser):
    def __init__(self, config_obj):
        super(SimpleParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Simple"

    def parse_hotlist_line(self, raw_line, alert_config):
        # Example:
        # plate

        plate_number = raw_line.strip()

        description = ''

        return {
            'plate': plate_number.upper().replace("-", "").replace(" ", ""),
            'list_type': alert_config['name'],
            'state': '',
            'description': description
        }

    def get_default_lists(self):
        return []

    def get_example_format(self):
        return "ABC123"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'ABC123', 'state': ''}
               ]