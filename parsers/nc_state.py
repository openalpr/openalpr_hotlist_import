from .ncic import NcicParser


class NcStateParser(NcicParser):
    def __init__(self, config_obj):
        super(NcStateParser, self).__init__(config_obj)

    # Functions implemented by parent (NCIC parser)

    def get_parser_name(self):
        return "North Carolina State"
