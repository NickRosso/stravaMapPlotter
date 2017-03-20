<h1>gmplot and stravalib</h1>
<p>
gmplot can be used to plot many longitude and latitude that are recorded from strava activities. This can be used to map recent bike rides, all bikes rides that you've been on, aswell as numerous other types of plots such as heatmaps. Stravalib takes in other types of activity info such as altitude, velocity smoothing, ismoving, and other misc. information.
</p>



<h2>Usage</h2>
<p>
	
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


	activities = getActivities(client, limit)

	print " looping through activities..."

	df_lst = {} 
	
	for act in activities:
		if float(act.distance) > 0 and act.manual != True:
			parse_activity(act, types)

	
	print("Drawing datapoints to html file")
	gmap.draw("mymap.html")

</p>

<h2>Results</h2>
<p>
	<b>LakeVilla</b>
	<img src='http://imgur.com/zXCUqRF'>
	<b>DeKalb</b>
	<img src='http://imgur.com/oPwYkdL'>
</p>

<h2>Installation</h2>
<p> This project requires a strava api key which is very easy to obtain, just create a strava account and send it a api request under https://www.strava.com/settings/api.</p>


<h2>Contributors</h2>
<p> Just wanted to thank strava and gmplot for the libraries to make use of personal data. This code is under the MIT License and open to the public for use. </p>

