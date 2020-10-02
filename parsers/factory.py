import sys
from .ca_doj_clew import CaClewParser
from .pa_psp import PaPspParser
from .ny_state import NyStateParser
from .fl_state import FlStateParser
from .al_state import AlStateParser
from .simple import SimpleParser
from .co_ccic import CoCCICParser
from .ncic import NcicParser
from .mi_state import MiStateParser
from .tx_tcic import TxTCIC
from .tx_ncic import TxNCIC
from .fl_dmv import FlDmv
from .nc_state import NcStateParser
from .ia_state import IaStateParser
# Some parsers require Python3+
if sys.hexversion >= 0x3000000:
    from .kansas_state import KsStateParser


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
    elif parser_name == 'co_ccic':
        return CoCCICParser(config_obj)
    elif parser_name == 'ncic':
        return NcicParser(config_obj)
    elif parser_name == 'ks_state':
        return KsStateParser(config_obj)
    elif parser_name == 'mi_state':
        return MiStateParser(config_obj)
    elif parser_name == 'tx_tcic':
        return TxTCIC(config_obj)
    elif parser_name == 'tx_ncic':
        return TxNCIC(config_obj)
    elif parser_name == 'fl_dmv':
        return FlDmv(config_obj)
    elif parser_name == 'nc_state':
        return NcStateParser(config_obj)
    elif parser_name == 'ia_state':
        return IaStateParser(config_obj)

    else:
        print("Unable to find parser named %s" % (parser_name))
        raise Exception("No parser found")
