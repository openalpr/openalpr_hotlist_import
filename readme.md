# OpenALPR Hotlist Import

Automatically import a law enforcement "hotlist" into 
OpenALPR alert lists using a cron job or Windows Task


## Installation

**Debian Linux**

1. Download the `.deb` package from the 
[release page](https://github.com/openalpr/openalpr_hotlist_import/releases)
2. Install the package 
`sudo dpkg -i openalpr-hotlist_*.deb && sudo apt-get install -f`

**Windows**

1. Download and run the `.exe` installer from the [release page](https://github.com/openalpr/openalpr_hotlist_import/releases)
2. Click on Start and search for "Hotlist".  Click on the OpenALPR Hotlist Import icon


## Configuration

After opening the GUI, you will need to 

1. Select your parser from the dropdown list. Check the example format to ensure 
   that it matches the content of your file
    1. In most cases, you should keep the default list names and parse codes
    2. If your state's hotlist is not on the above list, it's possible another 
    format will work - they tend to be very 
    similar. If it's not supported, please send OpenALPR a 50-100 row example from 
    your hotlist (plate numbers can be altered if needed for data privacy)
2. Set the location of your hotlist file (both filepath and URL are supported)
3. Enter the URL for the OpenALPR webserver where you want the alerts to upload
    1. http://localhost:9001 for an on-premise server  
    2. https://cloud.openalpr.com for Cloud Stream plans
    3. https://police.openalpr.com for police department accounts
4. Set your company ID and API key (both are found from your webserver's 
   [account page](https://cloud.openalpr.com/account/my_account))
5. Configure optional fields
    1. State Import: a list of comma-separated, two-letter postal codes. If included,
    the import will only include plates from the specified states. Leave blank to 
    import all plates
    2. Plates to Skip: ignores any specified plate numbers. Duplicate entries are 
    automatically filtered by default
6. Click save to store your configuration, and then click test
7. If the test was successful, set an autorun time and re-save

### Manual Configuration Settings

### Web Server Settings

```
# Configuration for Hotlist import

# The base URL for the target Scout/OpenALPR Web Server

server_base_url: http://localhost:9001

# If your web server is setup for company_id authentication, you may
# place it here

company_id: yourcompanyid

# If your web server is using a user's api key, then it goes here
# Note: you must have company_id or api_key based auth to import parsed
# lists into the web server

api_key: your api key
```

### Source List Settings
```
# The name of the parser that should be applied. See `factory.py` for a full list of supported
# hotlist parser names

hotlist_parser: ca_doj_clew

# Where we can find the source file. Specifying a local file path or an HTTP download URL is supported.
# Zip files are also supported. 

hotlist_path: localfile.txt

# If your source file is a URL that is protected via HTTP Basic Authentication,
# you may enter the credentials here. Note, you must provide both for the authentication to be
# applied when downloading the source file.

hotlist_http_basic_username: myuser
hotlist_http_basic_password: myuserpassword 

# If your source file is a protected zip, you may enter the password here

hotlist_password=zip_password

# You can optionally override the path and name of the file that is sourced.

temp_dat_file: /tmp/hotlistimport.dat

# You can optionally override the path and name of the converted hotlist file. 
# This is the file that is output after parsing and is uploaded to the web server

temp_csv_file: /tmp/hotlistimport.csv
```

### Log Settings
```
log_file: /var/log/openalpr/hotlist.log

# Hot many historical log files to keep
log_archives: 5

# Max log file size
log_max_size_mb: 100
```

### Source Plate Filter Settings
```
# This setting is used to whitelist states. Only import records
# which match this state list. An empty list allows all states.

state_import:
  - CA
  - OR
  - NV
  - AZ

# This list is used to filter known false alerts. That is,
# if there are plates that you do not want to upload to the web server,
# add them here.

skip_list:
  - '0'
  - '00'
  - '000'
  - '190'
```

### Notification Settings
```
# These email settings are used to notify of hostlist activities such as
# when a hotlist fails to parse or upload, or when things are working as
# they should

smtp_server: 
smtp_domain:
smtp_recipient: 
smtp_sender: 
smtp_port: 25
smtp_username: 
smtp_password: 
send_email_on_success: False
```

### Alert Types Settings

Alert Types are used to split a single hotlist into various alert lists based
on a category code or you may use them to add additional hotlists into a single configuration.
In general, there are no limits to the amount of lists you may have.

```
alert_types:
  - name: Stolen Vehicle
    openalpr_list_id: 1
    parse_code: Z
    hotlist_path: http://localhost:9099/svs.tbl
  - name: Person Of Interest
    parse_code: Person Of Interest
    match_strategy: exact
```


- `name`: The name of the alert group as shown on the web server backoffice
- `openalpr_list_id`: if you know the database id of the list, you may enter it here
- `parse_code`: this is the code that will be evaluated for this list. You must know this
based on your source list. The source agency may be able to provide you a hotlist reference guide to
figure out what parse codes or categories you will need.
     - **Example**: To create a list of all "Stolen Vehicles" from the main hostlist file, the agency
  may advise to use the parse_code "Z". In certain cases, the parse code could be a literal
  "Stolen Vehicle".
- `hotlist_path`: you may override the "parent" hotlist_path from above if the source file is located
else where for this specific list. The file may be local or remote.
