<h1>gmplot and stravalib</h1>
<p>
gmplot can be used to plot many longitude and latitude that are recored from strava activities. This can be used to map recent bike rides, all bikes rides that you've been on, aswell as numerous other types of plots such as heatmaps.
</p>



<h2> Usage</h2>
<p>
	# data points from dataframe 
	df['lat'] = map(split_lat, (df['latlng']))
	df['long'] = map(split_long, (df['latlng']))
	
	gmap.plot(df['lat'], df['long'], 'red', edge_width=1)
	
	
	print("Drawing datapoints to html file")
	gmap.draw("mymap.html")
</p>



<h2>Installation</h2>
<p> This project requires a strava api key which is very easy to obtain. You just need a strava account and send it a api request.</p>


<h2>Contributors</h2>
<p> Just wanted to thank strava and gmplot for the libraries to make use of personal data </p>

