#!/usr/bin/python

from argparse import ArgumentParser
import yaml
import os
import logging
import sys
import time
import json
from logging.handlers import RotatingFileHandler
import re
import requests
import urllib
import smtplib
from email.mime.text import MIMEText
import traceback

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

def parse_hotlist_line(raw_line, list_name, config_obj):
    # Example:
    # plate     state/vehicle type  alert_list-vehicle-color
    # 0         ILPC VMELRYEL/BLK
    #pieces = raw_line.split()

    fields = raw_line.split(' ')
    plate_number = fields[0].strip()
    state = fields[1][0:2].strip()
    county_code = fields[1][2:4]
    date_of_loss = fields[1][4:].strip()


    # Stolen vehicle, Green Honda Passenger Car (State)
    description = '%s State: %s County: %s Lost on: %s' % (list_name, state, county_code, date_of_loss)

    # Remove double spaces for empty stuff
    description = re.sub(' +', ' ', description)

    print description
    return {
        'plate': plate_number.upper().replace("-", "").replace(" ", ""),
        'state': state,
        'county_code': county_code,
        'list_type': list_name,
        'date_of_loss': date_of_loss,
        'description': description
        #'vehicle_other_info': vehicle_other_info
    }


if __name__ == "__main__":

    parser = ArgumentParser(description='OpenALPR Hotlist Parser')

    parser.add_argument( dest="config_file", action="store", metavar='config_file',
                        help="Config file used for OpenALPR Hotlist import")

    parser.add_argument('-f', '--foreground', action='store_true', default=False,
                        help="Don't log to file, log to console")

    parser.add_argument('-s', '--skip_upload', action='store_true', default=False,
                        help="Skip uploading CSVs to the server, useful for testing parse")

    # parser.add_argument( "-l", "--log_file", dest="log_file", action="store", type=str, default=None,
    #                   help="Optional field -- Location to write to log" )

    options = parser.parse_args()

    if not os.path.isfile(options.config_file):
        print "Config file does not exist"
        sys.exit(1)

    with open(options.config_file, 'r') as confin:
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

    for alert_type in config_data['alert_types']:
        try:

            # First download the list for this alert list
            urllib.urlretrieve (alert_type['hotlist_url'], config_data['temp_dat_file'])

            logger.info("processing alert list for " + alert_type['name'])
            with open(config_data['temp_csv_file'], 'w') as outcsv:

                with open(config_data['temp_dat_file'], 'r') as conffile:

                    dup_filter = {}

                    outcsv.write("Plate Number,Description,Match Strategy\n")
                    line_count = 0
                    for line in conffile:
                        line_count += 1

                        # Skip the first (header) line
                        if line_count <= 1:
                            continue

                        # Skip the last (footer) line
                        if line.startswith('TOTAL RECORD'):
                            continue

                        try:
                            line_content = parse_hotlist_line(line, alert_type['name'], config_data)
                        except Exception as e:
                            logger.exception("Failed to parse line: %d -- %s" % (line_count, line))
                            continue

                        # The user has configured a restriction on states.  ONLY import alerts that have the correct state code
                        if 'state_import' in config_data and len(config_data['state_import']) > 0:
                            if line_content['state'].upper() not in config_data['state_import']:
                                continue

                        # Skip particular alerts that are generating false positives for Brian
                        if 'skip_list' in config_data and len(config_data['skip_list']) > 0:
                            if str(line_content['plate']).upper() in config_data['skip_list']:
                                continue

                        if line_content['plate'] in dup_filter:
                            logger.info("Skipping duplicate plate %s for list %s" % (line_content['plate'], line_content['list_type']))
                            continue

                        dup_filter[line_content['plate']] = True
                        # Write this line to the CSV
                        outcsv.write("%s,%s,%s\n" % (line_content['plate'], line_content['description'], alert_type['match_strategy']))

            logger.info("Wrote temp CSV %s" % (config_data['temp_csv_file']))

            if not options.skip_upload:

                retry = 0
                total_attempts = 5
                success = False

                while retry < total_attempts:

                    try:
                        retry += 1

                        logger.info("Starting upload for alert type %s (Attempt #%d)" % (alert_type['name'], retry) )

                        # The CSV has been written, now let's push it to OpenALPR
                        base_url = config_data['server_base_url']
                        if not base_url.endswith('/'):
                            base_url += '/'

                        upload_url = base_url + 'api/alert-group-import-csv/'

                        with open(config_data['temp_csv_file'], 'rb') as f:
                            postargs = {
                                'name': ('', 'import'),
                                'company_id': ('', config_data['company_id']),
                                'pk': ('', str( alert_type['openalpr_list_id'] )),
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


    if len(failed_uploads) > 0:
        all_failures = ", ".join(failed_uploads)
        send_email(config_data, "OpenALPR CSV Import Failure (%d)" % (len(failed_uploads)), "The following services failed to upload: " + all_failures)

    elif config_data['send_email_on_success'] == True:
        send_email(config_data, "OpenALPR CSV Import Success", "Import completed successfully")


    logger.info("Import complete")