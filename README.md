# twitter-detector
Detect people in Twitter tweeting specific words. Testing it in a Raspberry Pi 2



## Usage

*python main.py --location={COORDINATES} -c {CONFIG_FILE in api_data/}*

*python main.py -q basketball -c {CONFIG_FILE in api_data/}*

**If -c s not used, it uses all config_files in api_data/**



## Examples

*python main.py --location=44.419944,-10.454478,34.255792,3.005975 -c config_file_1.py*

*python main.py -q basketball -c config_file_2.py*



## Installation

sudo apt install git python-pip python-dev build-essential python-numpy libicu-dev

git clone https://github.com/rjruizfdez/twitter-detector

sudo pip install tweepy polyglot

polyglot download sentiment2.en sentiment2.es sentiment2.fr sentiment2.ar sentiment2.ru sentiment2.hu
