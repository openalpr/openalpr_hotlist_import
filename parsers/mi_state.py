from .base import BaseParser
import re


def multiple_replace(text, replacements):
    """Apply multiple regex substitutions to text

    :param str text: Text to perform replacements on
    :param dict replacements: Before:after key value pairs
    :return str: With replacements applied
    """
    regex = re.compile("(%s)" % "|".join(map(re.escape, replacements.keys())))
    return regex.sub(lambda mo: replacements[mo.string[mo.start():mo.end()]], text)


class MiStateParser(BaseParser):

    def __init__(self, config_obj):
        super(MiStateParser, self).__init__(config_obj)

    def get_parser_name(self):
        return "Michigan State"

    def parse_hotlist_line(self, raw_line, alert_config):
        """Handle Michigan state line format

        Python slices for various fields (zero-indexed and end-exclusive)

        Start   End   Field Description
        =============================================
        10      19    Originating agency ORI
        19      27    Date of incident
        27      37    License plate number
        37      39    License plate state
        43      45    License plate type (bodytype)
        45      49    Vehicle year
        49      53    Vehicle make
        53      56    Vehicle model
        56      58    Vehicle style
        58      65    Vehicle color
        65      100   Record type/description

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Configuration details for the particular alert list
        :return dict: Plate number, state, list type, and description
        """

        # Separate fields by column positions
        slices = {
            'ori': slice(10, 19),
            'incident_date': slice(19, 27),
            'license_plate': slice(27, 37),
            'state': slice(37, 39),
            'license_year': slice(39, 43),
            'vehicle_type': slice(43, 45),
            'vehicle_year': slice(45, 49),
            'make': slice(49, 53),
            'model': slice(53, 56),
            'style': slice(56, 58),
            'color': slice(58, 65),
            'parse_code': slice(65, 100)}
        parsed = {name: raw_line[col_slice].strip() for name, col_slice in slices.items()}

        # Check if the list type matches this alert configuration
        parsed['parse_code'] = multiple_replace(
            text=parsed['parse_code'].lower().title(),
            replacements={'Ncic': 'NCIC', 'Mi': 'MI', 'Cpic': 'CPIC'})
        if 'parse_code' in alert_config and parsed['parse_code'] != alert_config['parse_code']:
            return None

        # Check alternatives for vehicle attribute codes
        parsed['make'] = self.get_vehicle_make(parsed['make'].replace('0', 'O'))
        parsed['vehicle_type'] = self.get_vehicle_type(parsed['vehicle_type'])
        parsed['color'] = self.get_vehicle_color(parsed['color'])

        # Format description
        parsed['state'] = parsed['state'].replace('0', 'O')
        description = '%s %s %s %s %s - %s' % (
            alert_config['name'],
            parsed['vehicle_year'],
            parsed['color'],
            parsed['make'],
            parsed['vehicle_type'],
            parsed['state'])
        description = re.sub(' +', ' ', description)
        return {
            'plate': parsed['license_plate'].upper().replace("-", "").replace(" ", ""),
            'state': parsed['state'],
            'list_type': parsed['parse_code'],
            'description': description}

    def get_default_lists(self):
        list_types = [
            'Missing Person MI',
            'Stolen Vehicle MI',
            'Stolen Plate MI',
            'Wanted Person MI',
            'Icle MI',
            'Son MI',
            'Te MI',
            'Supervised Visit NCIC',
            'Protection Order NCIC',
            'CPIC Data Record NCIC',
            'Stolen Plate NCIC',
            'Gang Or Suspected Terrorist NCIC',
            'Sex Offender NCIC',
            'Missing Person NCIC',
            'Wanted Person NCIC',
            'Stolen Vehicle NCIC',
            'NCIC',
        ]
        return [{'name': n, 'parse_code': n} for n in list_types]

    def get_example_format(self):
        return "M035777045WIMPD006320200403AHG5263   WI2020PC2003CHEVSUBLLBLK    MISSING PERSON NCIC"
