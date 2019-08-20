openalpr_hotlist_import
----------------------------

This script automatically imports a law enforcement "hotlist" into OpenALPR alert lists.  It is configured as a daily cron job or Windows Task.

Installation:
--------------

**Ubuntu Linux**

1. Download the `.deb` package from this repository's [release page](https://github.com/openalpr/openalpr_hotlist_import/releases)
2. Install the package `sudo dpkg -i openalpr-hotlist_*.deb && sudo apt-get install -f`

**Windows 10**

1. Download the Miniconda3 v4.5.1 [installer](https://repo.anaconda.com/miniconda/Miniconda3-4.5.1-Windows-x86_64.exe)
2. Run the `.exe` and follow the prompts to install Python 3.6
3. Clone this repository  `git clone https://github.com/openalpr/openalpr_hotlist_import.git` (or click Download ZIP if you don't have git installed)
    

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

Edit the hotlist.yaml file to use your own company_id, alert list configuration (name, and hotlist_url), and other parameters.

The SMTP configuration parameters, if configured, will send an e-mail on success or failure every time the script is run.

The state_import parameter (if configured) will ignore plate alerts for states other than those on the list.  To import all plates, remove this configuration.

The skip_list will ignore any plate numbers on that list.

The alerts will automatically be created based on the "name" provided on the alert list

Running the script
--------------------

After installation, the script is configured to automatically run.  To test it manually, run the following command:

    python /usr/share/openalpr-hotlist/hotlistimport.py -f /etc/openalpr/hotlist.yaml

