from .ca_doj_clew import CaClewParser
from .pa_psp import PaPspParser
from .ny_state import NyStateParser
from .fl_state import FlStateParser
from .al_state import AlStateParser
from .simple import SimpleParser

def get_parser(config_obj, alert_type):

    if 'hotlist_parser' in alert_type:
        parser_name = alert_type['hotlist_parser']
    else:
        parser_name = config_obj['hotlist_parser']

    if parser_name == 'ca_doj_clew':
        return CaClewParser(config_obj)
    elif parser_name == 'pa_psp':
        return PaPspParser(config_obj)
    elif parser_name == 'ny_state':
        return NyStateParser(config_obj)
    elif parser_name == 'fl_state':
        return FlStateParser(config_obj)
    elif parser_name == 'al_state':
        return AlStateParser(config_obj)
    elif parser_name == 'simple':
        return SimpleParser(config_obj)

    else:
        print("Unable to find parser named %s" % (parser_name))
        raise Exception("No parser found")
