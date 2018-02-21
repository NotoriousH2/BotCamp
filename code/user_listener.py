#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sys
from datetime import *

#________________________________read file and write each line in an array

def load_from_file (f):
	filename = open(f, 'r')
	contents = filename.read()
	filename.close()
	items = [name for name in contents.split('\n') if name]                
	return items

#Variables that contains the user credentials to access Twitter API

#==================Add Twitter Authentication key==================

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

# inputs from terminal
input_file_name = sys.argv[1] +'.txt'
try:
	input_file = open(input_file_name,'r')
except:
	print "No bots found for this topic to report"
	sys.exit() 
output_file_name = sys.argv[2] + '.txt'
output_file = open(output_file_name,'w')

listen_time = int(sys.argv[3]) * 4 #insecond

loc=sys.argv[1].rfind('/')
loc2= sys.argv[1][:loc].rfind('/')
log_file_name = sys.argv[1][:loc2+1] + "log.txt"
log_file=open(log_file_name,'a')

#___________________________________________________________________

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
	
	def __init__(self, api=None):
		super(StdOutListener, self).__init__()
		self.prev_time = datetime.now()
		self.next_time = datetime.now()
	
	def on_data(self, data):
		self.next_time = datetime.now()
		if (self.next_time - self.prev_time).total_seconds() < listen_time: 
			try:
				#x = json.loads(data)
				#output_file.write(str(x['created_at']) + "," + str(x['user']['screen_name']) + "," + str(x['user']['id'])+ "\n")
				output_file.write(str(data))
				return True
			except:
				return True
		else:
			return False
	def on_error(self, status):
		print status


if __name__ == '__main__':

	print datetime.now()
	log_file.write("Start Listening: " + str(datetime.now()) + '\n')
	reported_id = load_from_file (input_file_name)
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	
	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	user_filter = []
	for i in range (len(reported_id)):
		user_filter.append(str(reported_id[i]))
	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	#stream.filter(track=['apple', 'samsung', 'ios', 'android', 'galaxy', 'iphone', 'nexus' , 'microsoft' ,'google'])
	#print user_filter
	if len(user_filter) > 5000:
		try:
			stream.filter(follow = user_filter[0:4999])
		except:
			pass
				
	else:
		try:
			stream.filter(follow = user_filter)
		except IncompleteRead:
			sys.exit()
	print "Listening Finished!"
	log_file.write("Listening Finished!: " + str(datetime.now()) + '\n')
	
