import sys,os,re,time,datetime
import csv, json, argparse, tweepy, importlib
from numpy import genfromtxt, recfromcsv
from tweepy import OAuthHandler, Stream, StreamListener

words_file = 'config/words.csv'
logs_file = 'results/logs'
users_file = 'results/users.csv'
config_folder='config/api_data'


def timestamp(text):
	ts = time.time()
	timestamp_ = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	total = "[%s]   %s" % (timestamp_,text)
	logger_add_line(total+ " \n")
	
	print total
	
	

def get_args():
	parser = argparse.ArgumentParser()
	#parser.add_argument('-q', '--query', required=True, action='store', help='Query')
	my_args = parser.parse_args()
	
	return my_args


def get_words():
	res = []
	#words_array = genfromtxt(words_file, delimiter=',',dtype=None)
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
	
	try:
		csvWriter.writerow(data)
	
	except:
		pass


def get_api_files():
	res = []
	files_list = os.listdir(config_folder)
	
	for i in files_list:
		if i.endswith('.py'):
			res.append(os.path.splitext(i)[0])
	
	return res


class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        decoded = json.loads(data)
        user = decoded['user']['screen_name'].encode('ascii', 'ignore')
        text = decoded['text'].encode('ascii', 'ignore').encode('ascii', 'ignore')
        words = get_words()
        total = 0

        for word in words:
        	if word in str(text):
        		total += 1

        if total > 1:
	       	found_log = "Adding (%s,%s) to csv. Tweet: %s" % (user, total, text)
	       	data = [user, total, text]
        	csv_add_line(data)
        	timestamp(found_log.replace('\n', ''))

        return True

    def on_error(self, status):

        return False


def check_tweets(api, args):
	l = StdOutListener()
	myStream = tweepy.Stream(api.auth, l)
	words = get_words()
	track_word = words[0]
	timestamp("Searching for tweets (with %s)" % track_word)
	myStream.filter(track=[track_word])


def main():	
	# Arguments
	args = get_args()
	api_files_list = get_api_files()

	for api_file in api_files_list:
		# Get tweets
		api = generate_api(api_file)
		# Check tweets
		check_tweets(api, args)



if __name__ == "__main__":
    main()