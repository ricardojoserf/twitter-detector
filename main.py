import sys,os,re,time,datetime
import csv, json, argparse, tweepy, importlib
from numpy import genfromtxt, recfromcsv
from tweepy import OAuthHandler, Stream, StreamListener
from polyglot.text import Text

words_file = 'config/words.csv'
logs_file = 'results/logs'
users_file = 'results/users.csv'
config_folder='config/api_data'


def timestamp(text):
	ts = time.time()
	timestamp_ = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	total = "[%s]   %s" % (timestamp_,text)
	logger_add_line(total+ " \n")


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--word', required=False, action='store', help='Word')
	parser.add_argument('-l', '--location', required=False, action='store', help='Location')
	parser.add_argument('-c', '--configFile', required=False, action='store', help='Config file')
	my_args = parser.parse_args()
	return my_args


def get_words():
	res = []
	words_array = recfromcsv(words_file, delimiter=',',dtype=None)
	for line in words_array:
		for word in line:
			res.append(word)
	return res


def generate_api(module_name):
	sys.path.insert(0, config_folder)
	api_file = importlib.import_module(module_name)
	consumer_key = api_file.consumer_key
	consumer_secret = api_file.consumer_secret
	access_token = api_file.access_token
	access_token_secret = api_file.access_token_secret
	try:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = tweepy.API(auth)
		timestamp("Api created")
		return api
	except:
		timestamp("Error creating API")


def logger_add_line(data):
	with open(logs_file, 'a') as file:
		file.write(data)


def csv_add_line(data):
	csvFile = open(users_file, 'a')
 	csvWriter = csv.writer(csvFile)
	csvWriter.writerow(data)


def get_api_files():
	res = []
	files_list = os.listdir(config_folder)
	for i in files_list:
		if i.endswith('.py'):
			res.append(os.path.splitext(i)[0])
	return res

def getPolarity(init_text):
	text = Text(init_text)
	total_pol = 0.0
	count=0
	pol=0.0
	for w in text.words: 
		if(w.polarity!=0):
			total_pol += w.polarity
			count+=1
	if count!=0:
		pol = float(total_pol)/float(count)

	rounded_pol="0"
	if pol<0:
		rounded_pol = "Negative"
	elif pol == 0:
		rounded_pol = "Neutral"
	else:
		rounded_pol = "Positive"
	return rounded_pol


class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)
        user = decoded['user']['screen_name'].encode('ascii', 'ignore')
        text = decoded['text'].encode('ascii', 'ignore').encode('ascii', 'ignore').replace('\n', '   ')
        words = get_words()
        total = 0
        for word in words:
        	if word in str(text.lower() ):
        		total += 1
        if total > 1:
		try:
	        	polarity = getPolarity(text)
		except: 
			polarity = "Nan"
	       	found_log = "Adding (%s,%s) to csv. Tweet: %s. Polarity: %s" % (user, total, text, polarity)
	       	data = [user, total, text, polarity]
        	csv_add_line(data)
        	timestamp(found_log)
        return True
    def on_error(self, status):
        return False


def check_tweets(api, args):
	l = StdOutListener()
	myStream = tweepy.Stream(api.auth, l)
	args = get_args()
	q = args.word
	loc = args.location
	if q is not None:
		track_word = q
		timestamp("Searching for tweets (with %s)" % track_word)
		myStream.filter(track=[track_word], async=True)
	elif loc is not None:
		location = [float(x) for x in loc.split(",")]
		timestamp("Searching for tweets (location: %s)" % location)
		myStream.filter(locations=location)
	else:
		print "Use -l for location or -q for searching query"
		

def main():	
	args = get_args()
	config_file = args.configFile	
	if config_file is not None:
		api_file = os.path.splitext(config_file)[0]
		api = generate_api(api_file)
		check_tweets(api,args)
	else:
		api_files_list = get_api_files()
		for api_file in api_files_list:
			api = generate_api(api_file)
			check_tweets(api, args)

if __name__ == "__main__":
    main()
