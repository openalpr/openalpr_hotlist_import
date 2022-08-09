from .base import BaseParser


class GaSpalderParser(BaseParser):
    def __init__(self, config_obj):
        super(GaSpalderParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "GA Spalder"

    def parse_hotlist_line(self, raw_line, alert_config):

        # skip if a line is empty
        if not raw_line:
            return None

        # skip if this line doesn't contain the desired parse code
        parse_code = alert_config['parse_code']
        if parse_code and parse_code.upper() not in raw_line.upper():
            return None

        # parse the line into parts
        columns = [c.strip() for c in raw_line.split(',')]

        # the first column contains the plate and the state
        plate_state = columns[0]
        plate = plate_state[0:8].strip()
        state = plate_state[8:10]

        list_type = parse_code

        # extra data
        make = columns[1]
        year = columns[2]
        model = columns[3]
        color = columns[4]

        description = '{} {} {} {} {}'.format(list_type, year, make, model, color)

        # you return your parse data
        return {
            'plate': plate,
            'list_type': list_type,
            'state': state,
            'description': description
        }

    def get_default_lists(self):
        return [
            {
                'name': 'GA Expired Plates',
                'parse_code': 'EXPIRED'
            },
            {
                'name': 'GA Suspended Owner',
                'parse_code': 'SUSPENDED'
            }
        ]

    def get_example_format(self):
        return "BUC8867 GA#9EXPIRED,FORD,2006,FUSION FUSION,RED  "

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'BUC8867', 'state': 'GA'}
               ]