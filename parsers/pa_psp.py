from .ncic import NcicParser


class PaPspParser(NcicParser):
    def __init__(self, config_obj):
        super(PaPspParser, self).__init__(config_obj)

    # Functions implemented by parent (NCIC parser)
