import os
import platform

WIDTH = 1280
HEIGHT = 720

TASK_NAME = "openALPRHotlistImporter"

if platform.system() == 'Windows':
    # Windows 
    ROOT_DIR = os.path.join(os.path.expanduser('~'), '.alpr')
    os.makedirs(ROOT_DIR, exist_ok=True)

    CONFIG_FILE = os.path.join(ROOT_DIR, 'hotlist.yaml')
    LOG_FILE = os.path.join(ROOT_DIR, 'openalpr_hotlist_import.log')
    #os.path.expanduser('~/.alpr/alpr_hotlist_importer.log')
    BAT_FILE = os.path.join(ROOT_DIR, 'alpr.bat')

else:
    # Linux

    CONFIG_FILE = '/etc/openalpr/hotlist.yaml'
    LOG_FILE = '/var/log/openalpr_hotlist_import.log'

LINUX_CRON_FILE = '/etc/cron.d/openalpr-hotlist'

US_STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


try:
    from local_settings import *
except ImportError:
    pass
