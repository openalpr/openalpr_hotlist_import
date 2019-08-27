#!/usr/bin/python

from argparse import ArgumentParser
from email.mime.text import MIMEText
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from shutil import copyfile
import smtplib
import sys
import time
import traceback
import urllib
import warnings
import yaml
import zipfile
from parsers import factory
from print_alert_lists import AlertListManager


def send_email(config_obj, subject, message):
    if 'smtp_server' not in config_obj or config_obj['smtp_server'] is None or config_obj['smtp_server'].strip() == '':
        return

    try:
        logger.info("Sending e-mail: %s" % (subject))
        smtp_server = config_obj['smtp_server'].strip()
        smtp_port = config_obj['smtp_port']
        smtp_username = config_obj['smtp_username'].strip()
        smtp_password = config_obj['smtp_password'].strip()
        smtp_domain = config_obj['smtp_domain'].strip()

        smtp_recipients = [config_obj['smtp_recipient'].strip()]
        smtp_sender = config_obj['smtp_sender'].strip()

        if smtp_port == 25:
            smtpObj = smtplib.SMTP(smtp_server, smtp_port, smtp_domain, timeout=45)
        else:
            smtpObj = smtplib.SMTP_SSL(smtp_server, smtp_port, smtp_domain, timeout=45)

        msg = MIMEText(message, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = smtp_sender
        msg['To'] = ", ".join(smtp_recipients)

        if len(smtp_username) > 0:
            smtpObj.login(smtp_username, smtp_password)

        smtpObj.sendmail(smtp_sender, smtp_recipients, msg.as_string())
        smtpObj.close()
        logger.info("E-mail sent")
    except:
        logger.exception("Exception sending e-mail")


def get_color(config_obj, color):
    if color in config_obj['car_colors']:
        return config_obj['car_colors'][color]

    return color


if __name__ == "__main__":

    parser = ArgumentParser(description='OpenALPR Hotlist Parser')

    parser.add_argument(dest="config_file", action="store", metavar='config_file',
                        help="Config file used for OpenALPR Hotlist import")

    parser.add_argument('-f', '--foreground', action='store_true', default=False,
                        help="Don't log to file, log to console")

    parser.add_argument('-s', '--skip_upload', action='store_true', default=False,
                        help="Skip uploading CSVs to the server, useful for testing parse")

    options = parser.parse_args()

    options.config_file = os.path.realpath(options.config_file)
    if not os.path.isfile(options.config_file):
        print("Config file does not exist")
        sys.exit(1)

    with open(options.config_file, 'r') as confin:
        # config_data = yaml.load(confin, Loader=yaml.FullLoader) # Uncomment to fix for PyYaml 5.x+
        config_data = yaml.load(confin)

    if options.foreground or 'log_file' not in config_data or config_data['log_file'] == None or len(config_data['log_file']) <= 0:

        logger = logging.getLogger('HotlistImport Log')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    else:
        # Setup the logging
        logger = logging.getLogger("HotlistImport Log")
        logger.setLevel(logging.DEBUG)

        # add a rotating file handler
        handler = RotatingFileHandler(config_data['log_file'], maxBytes=config_data['log_max_size_mb'] * 1024 * 1024,
                                      backupCount=config_data['log_archives'])

        fmt = logging.Formatter("%(asctime)-15s: %(message)s", datefmt='%Y-%m-%dT%H:%M:%S')
        handler.setFormatter(fmt)

        logger.addHandler(handler)

    logger.info("Starting import")
    logger.info("using config:\n" + json.dumps(config_data, indent=2))

    # Iterate through the list multiple times for each alert type
    # e.g., stolen vehicles, etc.

    failed_uploads = []
    warnings.simplefilter('ignore', InsecureRequestWarning)
    for alert_type in config_data['alert_types']:
        try:

            if 'hotlist_path' in alert_type:
                hotlist_path = alert_type['hotlist_path']
            else:
                hotlist_path = config_data['hotlist_path']

            # First get the hotlist data (either from the network or a local file)
            # Copy the file to a temporary file to start working with it
            if hotlist_path.lower().startswith('http://') or hotlist_path.lower().startswith('https://'):
                # This is a URL, try to download it
                urllib.urlretrieve(hotlist_path, config_data['temp_dat_file'])
            else:
                folder_path = os.path.dirname(hotlist_path)
                if folder_path.endswith(".zip"):
                    with zipfile.ZipFile(folder_path, "r") as f:
                        content = {name: f.read(name) for name in f.namelist()}
                    zip_name = os.path.dirname(hotlist_path).split(os.sep)[-1].split('.')[0]
                    dat_file = os.path.basename(hotlist_path)
                    if dat_file not in content:
                        dat_file_alt = os.path.join(zip_name, os.path.basename(hotlist_path))
                        if dat_file_alt not in content:
                            logging.error("Neither {} nor {} exist in zip archive {}".format(
                                dat_file, dat_file_alt, folder_path))
                            sys.exit(1)
                        else:
                            dat_file = dat_file_alt
                    lines = [l for l in content[dat_file].decode("utf-8").split(os.linesep) if l != ""]
                    with open(config_data["temp_dat_file"], "w") as f:
                        for l in lines:
                            f.write("%s%s" % (l, os.linesep))
                elif not os.path.isfile(hotlist_path):
                        logger.error("Could not find hotlist file: %s" % (hotlist_path))
                        sys.exit(1)
                else:
                    copyfile(hotlist_path, config_data['temp_dat_file'])

            hotlistparser = factory.get_parser(config_data, alert_type)

            logger.info("processing alert list for " + alert_type['name'])

            hotlistparser.parse(alert_type)

            logger.info("Wrote temp CSV %s" % (config_data['temp_csv_file']))

            if not options.skip_upload:

                if 'api_key' in config_data:
                    alert_list_manager = AlertListManager(config_data['server_base_url'], api_key=config_data['api_key'])
                else:
                    alert_list_manager = AlertListManager(config_data['server_base_url'], company_id=config_data['company_id'])

                # if they don't specify a list ID explicitly, then create it
                if 'openalpr_list_id' not in alert_type:
                    list_id = alert_list_manager.get_or_create_list(alert_type['name'])
                else:
                    list_id = alert_list_manager.get_list(alert_type['openalpr_list_id'])

                if list_id is None:
                    logger.warning("List does not exist %s (%d).  Skipping" % (alert_type['name'], alert_type['openalpr_list_id']))

                retry = 0
                total_attempts = 5
                success = False

                while retry < total_attempts and list_id is not None:

                    try:
                        retry += 1

                        logger.info("Starting upload for alert type %s (Attempt #%d)" % (alert_type['name'], retry) )

                        # The CSV has been written, now let's push it to OpenALPR
                        base_url = config_data['server_base_url']
                        if not base_url.endswith('/'):
                            base_url += '/'

                        upload_url = base_url + 'api/alert-group-import-csv/'
                        if 'api_key' in config_data:
                            upload_url += '?api_key=' + config_data['api_key']
                        else:
                            upload_url += '?company_id=' + config_data['company_id']

                        with open(config_data['temp_csv_file'], 'rb') as f:
                            postargs = {
                                'name': ('', 'import'),
                                'pk': ('', str(list_id)),
                                'files': f,
                            }

                            r = requests.post(upload_url, verify=False, files=postargs)

                            logger.info("HTTP Import response: %s" % (r.content))

                            if r.status_code != 200:
                                logger.info("Non 200 Response: %d" % (r.status_code))
                                raise Exception("Non 200 response code")
                                continue


                        success = True
                        break

                    except:
                        retry_seconds = 30
                        logger.exception("Caught exception, waiting %d seconds to retry..." % (retry_seconds))
                        time.sleep(retry_seconds)

                if not success:
                    logger.info("Failed to upload %s after %d attempts" % (alert_type['name'], total_attempts))
                    failed_uploads.append(alert_type['name'])

        except (KeyboardInterrupt, SystemExit):
            logger.info("Detected keyboard interrupt, exiting")
            sys.exit(1)

        except:
            logger.exception("Caught exception")
            send_email(config_data, "OpenALPR CSV Import Unknown Error", "Encountered unknown error processing CSV Import\n" + traceback.format_exc())


    exit_status = 0

    if len(failed_uploads) > 0:
        all_failures = ", ".join(failed_uploads)
        send_email(config_data, "OpenALPR CSV Import Failure (%d)" % (len(failed_uploads)), "The following services failed to upload: " + all_failures)
        exit_status = 1

    elif config_data['send_email_on_success'] == True:
        send_email(config_data, "OpenALPR CSV Import Success", "Import completed successfully")


    logger.info("Import complete")

    sys.exit(exit_status)
