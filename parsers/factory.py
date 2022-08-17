import sys
from .ca_doj_clew import CaClewParser
from .ga_spalder import GaSpalderParser
from .mn_ncic import MnNCICParser
from .pa_psp import PaPspParser
from .ny_state import NyStateParser
from .fl_state import FlStateParser
from .al_state import AlStateParser
from .ks_topeka import KsTopekaParser
from .simple import SimpleParser
from .co_ccic import CoCCICParser
from .ncic import NcicParser
from .nj_mvc import NjMvcParser
from .mi_state import MiStateParser
from .tx_tcic import TxTCIC
from .tx_ncic import TxNCIC
from .fl_dmv import FlDmv
from .nc_state import NcStateParser
from .ia_state import IaStateParser
from .il_leads import IlLeadsParser
from .il_sos import IlSosParser
from .in_dmv import IndianaDmvParser
from .oh_leads import OhLeadsParser
from .ct_collect import CtCollectParser
from .wa_ncic import WaNCICParser
from .wa_stolen_vehicles import WaStolenVehicles

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
    elif parser_name == 'nj_mvc':
        return NjMvcParser(config_obj)
    elif parser_name == 'ks_state':
        return KsStateParser(config_obj)
    elif parser_name == 'ks_topeka':
        return KsTopekaParser(config_obj)
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
    elif parser_name == 'in_dmv':
        return IndianaDmvParser(config_obj)
    elif parser_name == 'oh_leads':
        return OhLeadsParser(config_obj)
    elif parser_name == 'ia_state':
        return IaStateParser(config_obj)
    elif parser_name == 'il_leads':
        return IlLeadsParser(config_obj)
    elif parser_name == 'il_sos':
        return IlSosParser(config_obj)
    elif parser_name == 'ct_collect':
        return CtCollectParser(config_obj)
    elif parser_name == 'ga_spalder':
        return GaSpalderParser(config_obj)
    elif parser_name == 'mn_ncic':
        return MnNCICParser(config_obj)
    elif parser_name == 'wa_stolen_vehicles':
        return WaStolenVehicles(config_obj)
    elif parser_name == 'wa_ncic':
        return WaNCICParser(config_obj)
    else:
        print("Unable to find parser named %s" % parser_name)
        raise Exception("No parser found")
