openalpr_hotlist_import
----------------------------

This script automatically imports a "hotlist" into OpenALPR alert lists.  It is configured as a nightly cron job on the OpenALPR webserver.

Installation:
--------------

To install, install the .deb package onto the webserver:

    sudo dpkg -i openalpr_hotlist_import.py
    sudo apt-get install -f


How it Works:
--------------

The import script downloads a data file from the URLs configured in each alert_types->hotlist_url.  The data files are expected to be in the following format:

    6FXU585 CA0420150407
    ^^^^^^^
    LICENSE
           ^
           WHITE SPACE DELIMITER (1 CHAR)
            ^^
            STATE (2 CHAR)
              ^^
              COUNTY CODE (2 CHAR)
                                  ^^^^^^^^
                                  DATE OF LOSS (YYYYMMDD)

This is the data format used in California.  Other law enforcement databases may be different.

Each file will be parsed and uploaded to the OpenALPR web server to a particular OpenALPR List ID. 

Configuration
---------------

Copy the configuration file in /etc/openalpr/hotlist.yaml.sample to /etc/openalpr/hotlist.yaml

Edit the hotlist.yaml file to use your own company_id, alert list configuration (openalpr_list_id, name, and hotlist_url), and other parameters.

The SMTP configuration parameters, if configured, will send an e-mail on success or failure every time the script is run.

The state_import parameter (if configured) will ignore plate alerts for states other than those on the list.  To import all plates, remove this configuration.

The skip_list will ignore any plate numbers on that list.

To find the Alert List ID, first create the Alert List in the OpenALPR Web UI, then open the "Network Console" tab in the web tools.  Each time you click on an alert list, the URL that it requests will contain the alert list ID.

Running the script
--------------------

After installation, the script is configured to automatically run.  To test it manually, run the following command:

    python /usr/share/openalpr-hotlist/hotlistimport.py -f /etc/openalpr/hotlist.yaml

