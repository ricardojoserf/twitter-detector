# twitter-detector
Detect people in Twitter tweeting specific words and analyze the data. Testing it in a Raspberry Pi 2


## Usage
Create a listener from a word (query):
```
python main.py -q {WORD} -c {CONFIG_FILE in api_data/}
```

Create a listener from a location:
```
python main.py --location={COORDINATES} -c {CONFIG_FILE in api_data/}
```


## Examples

```
python main.py -q basketball -c config_file_1.py


python main.py --location=-18.26,27.5,4.64,43.85 -c config_file_2.py
```


## Installation

```
sudo sh install/install.sh
```