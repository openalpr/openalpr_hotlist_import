#!/usr/bin/python
import requests
from argparse import ArgumentParser
import yaml
import os
import sys
import json

#https://cloud.openalpr.com/api/alert-lists/

if __name__ == "__main__":
    parser = ArgumentParser(description='OpenALPR Hotlist Parser')

    parser.add_argument( dest="config_file", action="store", metavar='config_file',
                        help="Config file used for OpenALPR Hotlist import")


    options = parser.parse_args()

    if not os.path.isfile(options.config_file):
        print "Config file does not exist"
        sys.exit(1)

    with open(options.config_file, 'r') as confin:
        config_data = yaml.load(confin, Loader=yaml.FullLoader)


    list_url='%s/api/alert-lists/?company_id=%s' % (config_data['server_base_url'], config_data['company_id'])
    r = requests.get(list_url, verify=False)

    if r.status_code != 200:
        print("Non 200 Response: %d" % (r.status_code))
        sys.exit(1)
        
    data_obj = json.loads(r.content)
    for result in data_obj['results']:
    	print (result['name'])
    	print ("  -ID: " + str(result['id']))
    	print ("")