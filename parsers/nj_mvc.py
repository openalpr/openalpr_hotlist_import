from .base import BaseParser
import re


class NjMvcParser(BaseParser):

    def __init__(self, config_obj):
        super(NjMvcParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "New Jersey MVC"

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle New Jersey MVC format

        Python slices for various fields (zero-indexed and end-exclusive)

        Start   End   Field Description
        =============================================
        0       10    Parse code (first character only)
        10      19    ORI (empty)
        19      27    Date of theft (empty, would be yyyymmdd format)
        27      37    License plate number
        37      39    License plate state code (two letter ISO)
        39      43    License plate year
        43      45    Vehicle style/type (NCIC code, i.e. PC)
        45      49    Vehicle year
        49      53    Vehicle make
        53      56    Vehicle model
        56      58    Unknown two-digit code
        58      65    Vehicle color

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Separate fields by column positions
        slices = {
            'parse_code': slice(0, 10),
            'ori': slice(10, 19),
            'date_of_theft': slice(19, 27),
            'license_plate': slice(27, 37),
            'state': slice(37, 39),
            'license_year': slice(39, 43),
            'vehicle_type': slice(43, 45),
            'vehicle_year': slice(45, 49),
            'make': slice(49, 53),
            'model': slice(53, 56),
            'color': slice(58, 65)}
        parsed = {name: raw_line[col_slice].strip() for name, col_slice in slices.items()}

        # Check if the list type matches this alert configuration
        if 'parse_code' in alert_config and parsed['parse_code'] != alert_config['parse_code']:
            return None

        # Check alternatives for vehicle attribute codes
        # TODO New Jersey shortens these relative to NCIC, so most aren't converted
        parsed['make'] = self.get_vehicle_make(parsed['make'])
        parsed['vehicle_type'] = self.get_vehicle_type(parsed['vehicle_type'])
        parsed['color'] = self.get_vehicle_color(parsed['color'])

        # Format description
        description = '%s %s %s %s %s - %s' % (
            alert_config['name'],
            parsed['vehicle_year'],
            parsed['color'],
            parsed['make'],
            parsed['vehicle_type'],
            parsed['state'])
        description = re.sub(' +', ' ', description)
        return {
            'plate': parsed['license_plate'].upper().replace('-', '').replace(' ', ''),
            'state': parsed['state'],
            'list_type': parsed['parse_code'],
            'description': description}

    def get_default_lists(self):
        return [
            {
                'name': 'Expired Plate',
                'parse_code': 'E'
            },
            {
                'name': 'Suspended Owner',
                'parse_code': 'S'
            },
        ]

    def get_example_format(self):
        return "S                          ABC123    NJ      1985NIS SEN04BLUE"

    def get_example_tests(self):
        return [
                {'raw_line': self.get_example_format(), 'plate': 'ABC123', 'state': 'NJ'}
               ]