#!/usr/bin/python

from argparse import ArgumentParser
from email.mime.text import MIMEText
import json
import logging
from logging.handlers import RotatingFileHandler
import os
import platform
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
if sys.version_info.major == 3:
    from pyzipper import is_zipfile as is_zipfile
    from pyzipper import AESZipFile as zipreader
elif sys.version_info.major == 2:
    from zipfile import is_zipfile as is_zipfile
    from zipfile import ZipFile as zipreader
from parsers import factory
from print_alert_lists import AlertListManager


WINDOWS = platform.system().lower().find('windows') == 0


def send_email(config_obj, subject, message, logger):
    if not config_obj.get('smtp_server'):
        return

    try:
        logger.info("Sending e-mail: %s" % subject)
        smtp_server = config_obj['smtp_server'].strip()
        smtp_port = config_obj.get('smtp_port', 80)
        smtp_username = config_obj.get('smtp_username', '').strip()
        smtp_password = config_obj.get('smtp_password', '').strip()
        smtp_domain = config_obj.get('smtp_domain', '').strip()

        smtp_recipients = [config_obj.get('smtp_recipient', '').strip()]
        smtp_sender = config_obj.get('smtp_sender', '').strip()

        if smtp_port == 25:
            smtp_obj = smtplib.SMTP(smtp_server, smtp_port, smtp_domain, timeout=45)
        else:
            smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port, smtp_domain, timeout=45)

        msg = MIMEText(message, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = smtp_sender
        msg['To'] = ", ".join(smtp_recipients)

        if len(smtp_username) > 0:
            smtp_obj.login(smtp_username, smtp_password)

        smtp_obj.sendmail(smtp_sender, smtp_recipients, msg.as_string())
        smtp_obj.close()
        logger.info("E-mail sent")
    except Exception as er:
        logger.exception("Exception sending e-mail - {}".format(er))


def get_color(config_obj, color):
    if color in config_obj.get('car_colors', {}):
        return config_obj['car_colors'][color]
    return color


def import_hotlist(config_file, foreground=False, skip_upload=False):
    with open(config_file, 'r') as conf:
        # config_data = yaml.load(confin, Loader=yaml.FullLoader) # Uncomment to fix for PyYaml 5.x+
        conf_data = yaml.load(conf)

    # Setup the logging
    logger = logging.getLogger('HotlistImport Log')
    logger.setLevel(logging.DEBUG)
    if foreground or not conf_data.get('log_file'):
        handler = logging.StreamHandler()
        logger.addHandler(handler)
    else:
        # add a rotating file handler
        handler = RotatingFileHandler(conf_data['log_file'],
                                      maxBytes=conf_data.get('log_max_size_mb', 100) * 1024 * 1024,
                                      backupCount=conf_data.get('log_archives', 5))
        fmt = logging.Formatter("%(asctime)-15s: %(message)s", datefmt='%Y-%m-%dT%H:%M:%S')
        handler.setFormatter(fmt)
        logger.addHandler(handler)

    logger.info("Starting import using config: \n" + json.dumps(conf_data, indent=2))
    if 'cloud.openalpr.com' in conf_data['server_base_url'] and conf_data['server_base_url'].split(':')[0] != 'https':
        logger.warning('Cloud webserver should be prefixed with HTTPS')

    # Iterate through the list multiple times for each alert type
    # e.g., stolen vehicles, etc.
    failed_uploads = []
    warnings.simplefilter('ignore', InsecureRequestWarning)
    for alert_type in conf_data.get('alert_types', []):
        try:
            hotlist_path = alert_type['hotlist_path'] if 'hotlist_path' in alert_type else conf_data['hotlist_path']

            # First get the hotlist data (either from the network or a local file)
            # Copy the file to a temporary file to start working with it
            if hotlist_path.lower().startswith('http://') or hotlist_path.lower().startswith('https://'):
                # This is a URL, try to download it
                urllib.urlretrieve(hotlist_path, conf_data['temp_dat_file'])
            else:

                # If it's a zip file, extract it first
                password = conf_data.get('hotlist_password')
                if password is not None:
                    if sys.version_info.major != 3:
                        raise RuntimeError('Python 3.x is required for handling encrypted zip files')
                    password = password.encode('utf-8')
                if is_zipfile(hotlist_path):

                    with zipreader(hotlist_path, 'r') as zip_file:
                        all_files = zip_file.namelist()

                        if len(all_files) == 1:
                            # Just process the one file and write to output
                            content = zip_file.read(all_files[0], pwd=password)

                            lines = [l for l in content.decode("utf-8").splitlines() if l != ""]
                            with open(conf_data['temp_dat_file'], 'w') as f:
                                for l in lines:
                                    f.write("%s%s" % (l, '\n'))
                        else:
                            logger.info("The specified zip file contains multiple files.  Must specify the file in the path (e.g., c:\\hotlists\\thefile.zip\\fileinside")

                elif '.zip' in hotlist_path:
                    folder_path = os.path.dirname(hotlist_path)
                    with zipreader(folder_path, 'r') as f:
                        content = {name: f.read(name, pwd=password) for name in f.namelist()}
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
                    lines = [l for l in content[dat_file].decode("utf-8").splitlines() if l != ""]
                    with open(conf_data['temp_dat_file'], 'w') as f:
                        for l in lines:
                            f.write("%s%s" % (l, '\n'))

                elif not os.path.isfile(hotlist_path):
                    logger.error("Could not find hotlist file: %s" % (hotlist_path))
                    sys.exit(1)

                else:
                    copyfile(hotlist_path, conf_data['temp_dat_file'])

            hotlistparser = factory.get_parser(conf_data, alert_type)

            logger.info("processing alert list for " + alert_type.get('name', ''))

            hotlistparser.parse(alert_type)

            logger.info("Wrote temp CSV %s" % (conf_data['temp_csv_file']))

            if not skip_upload:
                if 'api_key' in conf_data:
                    alert_list_manager = AlertListManager(conf_data['server_base_url'], api_key=conf_data['api_key'])
                else:
                    alert_list_manager = AlertListManager(conf_data['server_base_url'],
                                                          company_id=conf_data['company_id'])

                # if they don't specify a list ID explicitly, then create it
                if 'openalpr_list_id' not in alert_type:
                    list_id = alert_list_manager.get_or_create_list(alert_type['name'])
                else:
                    list_id = alert_list_manager.get_list(alert_type['openalpr_list_id'])

                if list_id is None:
                    logger.warning(
                        "List does not exist %s (%d).  Skipping" % (alert_type['name'], alert_type['openalpr_list_id']))

                retry = 0
                total_attempts = 5
                success = False

                while retry < total_attempts and list_id is not None:
                    try:
                        retry += 1
                        logger.info("Starting upload for alert type %s (Attempt #%d)" % (alert_type['name'], retry))

                        # The CSV has been written, now let's push it to OpenALPR
                        base_url = conf_data['server_base_url']
                        if not base_url.endswith('/'):
                            base_url += '/'

                        upload_url = base_url + 'api/alert-group-import-csv/'
                        if 'api_key' in conf_data:
                            upload_url += '?api_key=' + conf_data['api_key']
                        else:
                            upload_url += '?company_id=' + conf_data['company_id']

                        with open(conf_data['temp_csv_file'], 'rb') as f:
                            postargs = {
                                'name': ('', 'import'),
                                'pk': ('', str(list_id)),
                                'files': f,
                            }

                            r = requests.post(upload_url, verify=False, files=postargs)

                            logger.info("HTTP Import response: %s" % r.content)

                            if r.status_code != 200:
                                logger.info("Non 200 Response: %d" % r.status_code)
                                raise Exception("Non 200 response code")

                        success = True
                        break

                    except Exception as e:
                        retry_seconds = 30
                        logger.exception("Caught exception %s, waiting %d seconds to retry..." % (e, retry_seconds))
                        time.sleep(retry_seconds)

                if not success:
                    logger.info("Failed to upload %s after %d attempts" % (alert_type['name'], total_attempts))
                    failed_uploads.append(alert_type['name'])

        except (KeyboardInterrupt, SystemExit):
            logger.info("Detected keyboard interrupt, exiting")
            sys.exit(1)

        except Exception as e:
            logger.exception("Caught exception - {}".format(e))
            send_email(conf_data, "OpenALPR CSV Import Unknown Error",
                       "Encountered unknown error processing CSV Import\n" + traceback.format_exc(), logger)

    exit_status = 0

    if len(failed_uploads) > 0:
        all_failures = ", ".join(failed_uploads)
        send_email(conf_data, "OpenALPR CSV Import Failure (%d)" % (len(failed_uploads)),
                   "The following services failed to upload: " + all_failures, logger)
        exit_status = 1
    elif conf_data.get('send_email_on_success'):
        send_email(conf_data, "OpenALPR CSV Import Success", "Import completed successfully", logger)

    logger.info("Import complete")
    return exit_status


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

    _exit_status = import_hotlist(config_file=options.config_file, foreground=options.foreground,
                                  skip_upload=options.skip_upload)

    sys.exit(_exit_status)
