#!/usr/bin/python
import requests
from argparse import ArgumentParser
import yaml
import os
import sys
import json


# https://cloud.openalpr.com/api/alert-lists/
# TODO build all URLs with os.path.join to ensure we don't have any double //
# TODO update alprweb Django code to accept POST with or without trailing forward slash
# TODO compatibility option for on-prem webservers which don't support v2 alert API

class AlertListManager:

    def __init__(self, server_url, company_id=None, api_key=None):
        self.server_url = server_url
        self.company_id = company_id
        self.api_key = api_key

        list_url = '%s/api/v2/alert-lists/' % self.server_url

        if self.api_key:
            list_url += '?api_key=' + self.api_key
        else:
            list_url += '?company_id=' + self.company_id

        list_url += '&page_size=5000'

        retries = 0
        success = False
        while retries < 5:
            r = requests.get(list_url, verify=False)

            if not r.ok:
                retries += 1
                time.sleep(3.0)
                continue

            success = True
            break

        if not success:
            raise Exception("Unable to request alert data from web server (status code %d)" % (r.status_code))

        data_obj = json.loads(r.content)
        self.alert_lists = data_obj

    def print_lists(self):
        for result in self.alert_lists:
            print("{}  -ID: {}\n".format(result['name'], result['id']))

    def get_list(self, alert_id):
        for result in self.alert_lists:
            if result['id'] == alert_id:
                return alert_id

    def get_or_create_list(self, name):

        for result in self.alert_lists:
            if result['name'] == name:
                return result['id']

        # List doesn't already exist, let's create it

        list_url = '%s/api/v2/alert-lists/' % self.server_url

        if self.api_key:
            list_url += '?api_key=' + self.api_key
        else:
            list_url += '?company_id=' + self.company_id

        postargs = {
            'name': name
        }

        if self.api_key:
            postargs['api_key'] = self.api_key
        else:
            postargs['company_id'] = self.company_id

        r = requests.post(list_url, verify=False, data=postargs)

        if r.status_code != 200 and r.status_code != 201:
            print(r.content)
            raise Exception("Non 200 response code: %d" % r.status_code)

        data_obj = json.loads(r.content)
        return data_obj['id']


if __name__ == "__main__":

    parser = ArgumentParser(description='OpenALPR Hotlist Parser')

    parser.add_argument(dest="config_file", action="store", metavar='config_file',
                        help="Config file used for OpenALPR Hotlist import")

    options = parser.parse_args()

    if not os.path.isfile(options.config_file):
        print("Config file does not exist")
        sys.exit(1)

    with open(options.config_file, 'r') as confin:
        # config_data = yaml.load(confin, Loader=yaml.FullLoader) # Uncomment to fix for PyYaml 5.x+
        config_data = yaml.load(confin)

    _api_key = None
    _company_id = None
    if 'api_key' in config_data:
        _api_key = config_data['api_key']
    else:
        _company_id = config_data['company_id']

    alert_list_manager = AlertListManager(config_data['server_base_url'], company_id=_company_id, api_key=_api_key)

    alert_list_manager.print_lists()
