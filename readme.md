OpenALPR Hotlist Import
----------------------------

Automatically import a law enforcement "hotlist" into 
OpenALPR alert lists using a cron job or Windows Task

![Hotlist Import GUI](https://www.openalpr.com/images/demoscreens/openalpr_hotlist_import.png "Hotlist GUI Image")

Installation:
--------------

**Debian Linux**

1. Download the `.deb` package from the 
[release page](https://github.com/openalpr/openalpr_hotlist_import/releases)
2. Install the package 
`sudo dpkg -i openalpr-hotlist_*.deb && sudo apt-get install -f`

**Windows**

1. Download and run the `.exe` installer from the [release page](https://github.com/openalpr/openalpr_hotlist_import/releases)
2. Click on Start and search for "Hotlist".  Click on the OpenALPR Hotlist Import icon


Configuration
---------------

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
