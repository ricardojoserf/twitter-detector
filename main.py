import sys,os,re,time,datetime
import csv, json, argparse, tweepy, importlib
import config
from numpy import genfromtxt, recfromcsv
from tweepy import OAuthHandler, Stream, StreamListener
from polyglot.text import Text

words_file = config.words_file
logs_file = config.logs_file
users_file = config.users_file
config_folder = config.config_folder
min_words = 2

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--word', required=False, action='store', help='Word to be searched. Example: basketball')
	parser.add_argument('-l', '--location', required=False, action='store', help='Location to be searched. Example: -11.03,34.51,4.22,43.85 (Spain). More in http://boundingbox.klokantech.com/ (option CSV)')
	parser.add_argument('-c', '--configFile', required=False, action='store', help='Config file in api_data (ONLY NAME, WITHOUT ROUTE). Example: config1.py')
	my_args = parser.parse_args()
	return my_args


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
		rounded_pol = "-"
	elif pol == 0:
		rounded_pol = "0"
	else:
		rounded_pol = "+"
	return rounded_pol


def get_words():
	res = []
	words_array = recfromcsv(words_file, delimiter=',',dtype=None)
	for line in words_array:
		for word in line:
			res.append(word)
	return res


def log(text):
	ts = time.time()
	timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	total = "[%s]   %s \n" % (timestamp,text)
	with open(logs_file, 'a') as file:
		file.write(total)


def csv_add_line(data):
	csvFile = open(users_file, 'a')
	csvWriter = csv.writer(csvFile)
	csvWriter.writerow(data)


class StdOutListener(tweepy.StreamListener):
	def on_data(self, data):
		decoded = json.loads(data)
		user = decoded['user']['screen_name'].encode('ascii', 'ignore')
		text = decoded['text'].encode('ascii', 'ignore').encode('ascii', 'ignore').replace('\n', '   ')
		words = get_words()
		total = 0
		for word in words:
			if word in str(text.lower()):
				total += 1
		if total >= min_words:
			try:
				polarity = getPolarity(text)
			except: 
				polarity = "Language not installed in polyglot"
			found_log = "Adding (%s,%s) to csv. Tweet: %s. Polarity: %s" % (user, total, text, polarity)
			log(found_log)
			data = [user, total, text, polarity]
			csv_add_line(data)
		return True
	def on_error(self, status):
		return False


def check_tweets(api, args):
	l = StdOutListener()
	myStream = tweepy.Stream(api.auth, l)
	args = get_args()
	q = args.word
	loc = args.location
	global min_words
	if q is not None:
		track_word = q
		log("Searching for tweets (with %s)" % track_word)
		min_words = 2
		myStream.filter(track=[track_word], async=True)
	elif loc is not None:
		location = [float(x) for x in loc.split(",")]
		log("Searching for tweets (location: %s)" % location)
		min_words = 1
		myStream.filter(locations=location, async=True)
	else:
		print ("Usage: python main.py -q {QUERY} -c {CONFIG_FILE} \npython main.py --location={LOCATION} -c {CONFIG_FILE in config/api_data} \n")

		
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
		log("Api created")
		return api
	except:
		log("Error creating API")


def main():	
	args = get_args()
	config_file = args.configFile	
	if config_file is not None:
		api_file = os.path.splitext(config_file)[0]
		api = generate_api(api_file)
		check_tweets(api,args)


if __name__ == "__main__":
	main()
