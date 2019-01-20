# twitter-detector
Detect people in Twitter tweeting specific words and analyze the users data. 

The list of words is a CSV file (*"config/words.csv"*) with columns in different languages. The program creates a **Twitter listener** from a *query* or a *location*, and stores any tweet containing one or more words in the CSV file.

Then, it is possible to analyze the *"results/users.csv"* file with *analyze_users.py*.


## Usage
Create a listener from a word (query):
```
python main.py -q {WORD} -c {CONFIG_FILE in api_data/}
```

Create a listener from a location:
```
python main.py --location={COORDINATES} -c {CONFIG_FILE in api_data/}
```

Analyze the users found:
```
python analyze_users.py
```


## Examples

```
python main.py -q isis -c config_file_1.py


python main.py --location=-18.26,27.5,4.64,43.85 -c config_file_2.py
```


## Installation

```
sudo sh install/install.sh
```