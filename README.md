# twitter-detector
Detect people in Twitter tweeting specific words


## Usage

*python tweets.py --location={COORDINATES} -c {CONFIG_FILE in api_data/}*

*python tweets.py -q basketball -c {CONFIG_FILE in api_data/}*

**If -c s not used, it uses all config_files in api_data/**


## Examples

*python tweets.py --location=44.419944,-10.454478,34.255792,3.005975 -c config_file_1.py*

*python tweets.py -q basketball -c config_file_2.py*
