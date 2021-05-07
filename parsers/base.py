import logging
from . import codes, fix_state


class BaseParser(object):

    def __init__(self, config_obj):
        self.config_obj = config_obj
        self.logger = logging.getLogger('HotlistImport Log')
        self.dup_filter = {}
        self.line_count = 0

    @staticmethod
    def _get_vehicle(attribute, value):
        """Safe-get lookup for vehicle attributes in NCIC codes

        :param str attribute: One of type, make, or color
        :param str value: Raw code to search for in lookup tables
        :return str: Cleaned value (if found), or the same value passed
        """
        if attribute not in ['type', 'make', 'color']:
            raise NotImplementedError('Expected attribute to be type, make, or color, but received %s' % attribute)
        mapping = codes['ncic'][attribute + 's']
        return mapping.get(value, value)

    def set_config(self, conf):
        """Update the config"""
        self.config_obj = conf

    def get_parser_name(self):
        """Return human-readable parser name"""
        raise NotImplementedError()

    def get_vehicle_color(self, value):
        """Checks for two-tone combinations with slash"""
        if '/' in value:
            color_both = value.split('/')
            if color_both[0] != color_both[1]:
                color = self._get_vehicle('color', color_both[0]) + '/' + self._get_vehicle('color', color_both[1])
            else:
                color = self._get_vehicle('color', color_both[0])
        else:
            color = self._get_vehicle('color', value)
        return color

    def get_vehicle_make(self, value):
        return self._get_vehicle('make', value)

    def get_vehicle_type(self, value):
        return self._get_vehicle('type', value)

    def parse_hotlist_line(self, raw_line, alert_config):
        """Must be implemented in the subclass doing the parsing

        :param str raw_line: Plain text line from the hotlist file
        :param dict alert_config: Containing the following keys
            * name: For display in the webserver
            * parse_code (optional): May be used depending on state's format
            * openalpr_list_id (optional): To match an existing list on the webserver
            * hotlist_path (optional): Override the default path
        :return dict or None: Containing the following keys
            * plate: License plate number
            * list_type: Identifier similar to parse code or alert type
            * description: For display in webserver
            * state (optional): Two letter ISO code
        """
        raise NotImplementedError()

    def parse(self, alert_type):
        self.dup_filter = {}

        with open(self.config_obj['temp_csv_file'], 'w') as outcsv:
            with open(self.config_obj['temp_dat_file'], 'r') as conffile:

                # Write the header
                outcsv.write("Plate Number,Description,State/Province\n")

                self.line_count = 0
                for line in conffile:
                    self.line_count += 1

                    try:
                        line_content = self.parse_hotlist_line(line, alert_type)
                    except Exception as e:
                        self.logger.exception("Failed to parse line: %d -- %s, %s" % (self.line_count, line, e))
                        continue

                    # Skip lines that aren't needed (empty plate will trigger import error on server)
                    if line_content is not None and line_content['plate'] == '':
                        continue
                    if line_content is None:
                        continue

                    # The user has configured a restriction on states.
                    # ONLY import alerts that have the correct state code
                    if self.config_obj.get('state_import'):
                        if 'state' in line_content and line_content['state'] != '':  # If no state is returned from parser, allow it
                            if line_content['state'].upper() not in self.config_obj['state_import']:
                                continue

                    # Convert the state codes (e.g., "MO" -> us-mo)
                    if 'state' in line_content:
                        line_content['state'] = fix_state(line_content['state'], self.logger)

                    # Skip particular alerts that are generating false positives
                    if self.config_obj.get('skip_list'):
                        if str(line_content['plate']).upper() in self.config_obj['skip_list']:
                            continue

                    if line_content.get('plate') in self.dup_filter:
                        self.logger.info("Skipping duplicate plate %s for list %s" %
                                         (line_content['plate'], line_content['list_type']))
                        continue

                    self.dup_filter[line_content['plate']] = True
                    # Write this line to the CSV
                    outcsv.write("%s,%s,%s\n" %
                                 (line_content['plate'], line_content['description'], line_content['state']))

    def get_default_lists(self):
        """Return a list of the default list names and parse codes for this hotlist"""
        return []

    def get_example_format(self):
        """Return an example line demonstrating what this hotlist format looks like"""
        return ""
