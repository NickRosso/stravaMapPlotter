#!/usr/bin/python
import stravalib
import BaseHTTPServer
import webbrowser
import pandas as pd 
import datetime
import urlparse
import gmplot



client_id, secret = open('client.secret').read().strip().split(',')
port = 5000
url = 'http://localhost:%d/authorized' % port
allDone = False
types = ['time', 'latlng']
limit = 150

client = stravalib.client.Client()
authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)
print 'Opening: %s' % authorize_url

webbrowser.open(authorize_url)
gmap = gmplot.GoogleMapPlotter(41.939, -88.7767, 10)

def use_Code(code):
	access_token = client.exchange_code_for_token(client_id=client_id, client_secret=secret, code=code)
	
	client.access_token = access_token
	athlete = client.get_athlete()
	print("For %(id)s, I now have an access token %(token)s" % {'id': athlete.id, 'token': access_token})	

	return client

def getActivities(client, limit):
	activities = client.get_activities(limit=limit)
	assert len(list(activities)) == limit
	for item in activities:
		print item

	return activities

def get_Streams(client, activity, types):
	streams = client.get_activity_streams(activity, types=types, series_type='time')
	return streams

def data_Frame(dict, types):
	print dict,types
	df = pd.DataFrame()

	for item in types:
		if item in dict.keys():
			df.append(item.data)
	df.fillna('',inplace=True)
	return df

def parse_activity(act, types):
	act_id = act.id
	name = act.name
	print str(act_id), str(act.name), act.start_date

	streams = get_Streams(client, act_id, types)
	df = pd.DataFrame()

	for item in types:
		if item in streams.keys():
			df[item] = pd.Series(streams[item].data, index=None)
		df['act_id'] = act.id
		df['act_startDate'] = pd.to_datetime(act.start_date)
		df['act_name'] = name

	df['lat'] = map(split_lat, (df['latlng']))
	df['long'] = map(split_long, (df['latlng']))

	gmap.plot(df['lat'], df['long'], 'red', edge_width=1)
	#gmap.heatmap(df['lat'],df['long'])

	return df

def calc_time(time_sec, start_date):
	try:
		timestamp = start_date + datetime.timedelta(seconds=int(time_sec))
	except:
		print ' time processing error : ' + str(time_sec)
		timestamp = start_date
	return timestamp

def split_lat(series):
	lat = series[0]
	return lat

def split_long(series):
	long = series[1]
	return long

def concatdf(df_lst):
	return pd.concat(df_lst, ignore_index=False)



class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_head(self):
		return self.do_GET()

	def do_GET(self):

		self.wfile.write('<script>window.close();</script>')
		code = urlparse.parse_qs(urlparse.urlparse(self.path).query)['code'][0]

		client = use_Code(code)

		activities = getActivities(client, limit)

		print " looping through activities..."

		df_lst = {} 

		for act in activities:
			if float(act.distance) > 0 and act.manual != True:
				parse_activity(act, types)

		

		gmap.draw("mymap.html")	


		


httpd = BaseHTTPServer.HTTPServer(('localhost', port), MyHandler)

while not allDone:
	httpd.handle_request()

