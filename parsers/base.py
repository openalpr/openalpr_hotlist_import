import logging


class BaseParser(object):

    def __init__(self, config_obj):
        self.config_obj = config_obj
        self.logger = logging.getLogger('HotlistImport Log')
        self.dup_filter = {}
        self.line_count = 0

    def set_config(self, conf):
        """
        Update the config
        :param conf:
        :return:
        """
        self.config_obj = conf

    def get_parser_name(self):
        """
        Return human-readable parser name
        :return:
        """
        raise NotImplementedError()

    def parse_hotlist_line(self, raw_line, alert_config):
        # This function must be implemented in the subclass doing the parsing
        raise NotImplementedError()

    def parse(self, alert_type):
        self.dup_filter = {}

        with open(self.config_obj['temp_csv_file'], 'w') as outcsv:
            with open(self.config_obj['temp_dat_file'], 'r') as conffile:

                # Write the header
                outcsv.write("Plate Number,Description,Match Strategy\n")

                self.line_count = 0
                for line in conffile:
                    self.line_count += 1

                    try:
                        line_content = self.parse_hotlist_line(line, alert_type)
                    except Exception as e:
                        self.logger.exception("Failed to parse line: %d -- %s, %s" % (self.line_count, line, e))
                        continue

                    # Skip lines that aren't needed
                    if line_content is None:
                        continue

                    # The user has configured a restriction on states.
                    # ONLY import alerts that have the correct state code
                    if self.config_obj.get('state_import'):
                        if 'state' in line_content:  # If no state is returned from parser, allow it
                            if line_content['state'].upper() not in self.config_obj['state_import']:
                                continue

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
                                 (line_content['plate'], line_content['description'], alert_type['match_strategy']))

    # Return a list of the default list names and parse codes for this hotlist
    def get_default_lists(self):
        return []

    # Return an example line demonstrating what this hotlist format looks like
    def get_example_format(self):
        return ""
