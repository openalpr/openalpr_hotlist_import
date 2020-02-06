OpenALPR Hotlist Import
----------------------------

Automatically import a law enforcement "hotlist" into 
OpenALPR alert lists using a cron job or Windows Task.

Installation:
--------------

**Ubuntu Linux**

1. Download the `.deb` package from this repository's 
[release page](https://github.com/openalpr/openalpr_hotlist_import/releases)
2. Install the package 
`sudo dpkg -i openalpr-hotlist_*.deb && sudo apt-get install -f`

**Windows 10**

1. Download the Miniconda3 v4.5.1 
[installer](https://repo.anaconda.com/miniconda/Miniconda3-4.5.1-Windows-x86_64.exe)
2. Run the `.exe` and follow the prompts to install Python 3.6
3. Clone this repository  
`git clone https://github.com/openalpr/openalpr_hotlist_import.git` (or 
click Download ZIP if you don't have git installed)
4. Open Anaconda Prompt and run `pip install pyyaml`

How it Works:
--------------

The `hotlistimport.py` script loads a `*.dat` file from disk or 
downloads it from a URL. The parser reads each line in the file and 
creates a CSV of alert entries to be uploaded to the OpenALPR webserver 
(either cloud on on-premise)

Currently supported formats include

1. California DOJ CLEW
2. Florida State
3. New York State
4. Pennsylvania PSP
5. Mississippi State
6. Alabama State

If your state's hotlist is not on the above list, it's possible another format 
will work -- they tend to be very similar.  If it's not supported, you can either write
a parser which inherits from `parsers.BaseParser` or send OpenALPR a 
50-100 row example from your hotlist (plate numbers can be altered if 
needed for data privacy). Then we can write a new parser for you.

Configuration
---------------

1. Make a copy of the example configuration file `hotlist.yaml.sample`. 
If you installed the deb package on Linux, it is located in the
`/etc/openalpr` folder. On Windows, check the `config` folder where you 
cloned/downloaded the repository. 
2. Provide the required fields in your YAML file 

    1. The `hotlist_path` where your `.dat` file is located (either 
on disk or a URL). If your file comes in a zip archive, specify 
 the folder name with the `.zip` extension and the script will 
 automatically extract the contents 
    2. Set the `server_base_url` for the OpenALPR webserver where you want the 
 alerts to upload. For instance, use http://localhost:9001 for an 
 on-premise server or https://cloud.openalpr.com for Cloud Stream plans
    3. The alerts will automatically be created based on the `name` provided 
 for each item in the `alert_types` list 
    4. Use your own value for `company_id` and `api_key`. Both can be found 
 on your cloud [account page](https://cloud.openalpr.com/account/my_account) 
    5. Set the `hotlist_parser` to match your state's format
    6. Provide paths for `temp_dat_file`, `temp_csv_file`, and `log_file`

3.  Configure additional optional YAML fields

    1. SMTP configuration parameters (if specified) will send an e-mail 
 on success or failure every time the script is run
    2. The `state_import` parameter (if specified) will ignore plate alerts 
 for states other than those on the list.  To import all plates, remove 
 this configuration
    3. The `skip_list` will ignore any plate numbers on that list

Running the script
--------------------

After installation on Linux, the script is configured to automatically 
run. To test it manually, run the following command:

    python /usr/share/openalpr-hotlist/hotlistimport.py -f /etc/openalpr/hotlist.yaml

On Windows, follow these additional steps to automatically run the script

1. Modify any necessary file paths in the template batch file `hotlistimport.bat`
2. Test by double clicking the batch file. If all your configuration 
parameters in the YAML are correct, you should see the new alert lists 
in your webserver
3. After a successful test, remove the `pause` line from the batch file
and add it to Windows Task Scheduler. For help, see this 
[tutorial](https://www.thewindowsclub.com/how-to-schedule-batch-file-run-automatically-windows-7)
