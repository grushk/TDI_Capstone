from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.charts import HeatMap, bins
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9
from datetime import datetime
import requests
import pandas as pd
import numpy as np
import datetime
import json
import googlemaps
#from flask_googlemaps import Map

app = flask.Flask(__name__)
gmaps_key = "AIzaSyCz-oZKRWxA_e0DHaZujnsy937yMzYoYXM"
wu_key = '784ea582c4d13bc7'
gmaps = googlemaps.Client(key=gmaps_key)

def getitem(obj, item, default):
	if item not in obj:
		return default
	else:
		return obj[item]

data=pd.read_csv('static/data/small_sample.csv')

def histogram():
	d = data.groupby(['pickup_hour'])['tpep_pickup_datetime'].count()
	plot = figure(width=400, height=400, title="Taxi Rides per Hour in Sample - Not an Overlap with Rush Hour")
	plot.vbar(x=list(d.index), width=0.5, bottom=0, top=list(d), color="#CAB2D6")
	script, div = components(plot)
	return script, div

def heatmap():
	plot = figure(width=400, height=400, title="Travel Speed by Wind Speed")
	plot.scatter(data['HOURLYWindSpeed'], data['Travel.Speed.MPH'])
	script, div = components(plot)
	return script, div

def scatter():
	plot = figure(width=400, height=400, title="Travel Speed by Temperature")
	plot.scatter(data['HOURLYWETBULBTEMPF'], data['Travel.Speed.MPH'])
	script, div = components(plot)
	return script, div

@app.route('/')
def main():
	return flask.redirect('/index')


@app.route('/index')
def index():
	#mymap = Map(
    #    identifier="view-side",
    #    lat=37.4419,
    #    lng=-122.1419,
    #    markers=[(37.4419, -122.1419)]
    #)
	return flask.render_template('index.html',
		gmaps_key = gmaps_key
		#mymap=mymap
	)

@app.route('/analysis')
def about():
	script1, div1 = histogram()
	script2, div2 = heatmap()
	script3, div3 = scatter()
	return flask.render_template('analysis.html',
		plot_script1=script1,
		plot_div1=div1,
		plot_script2=script2,
		plot_div2=div2,
		plot_script3=script3,
		plot_div3=div3,
		js_resources = INLINE.render_js(),
		css_resources = INLINE.render_css()
	)

@app.route('/ajax', methods = ['POST'])
def ajax_request():
    date = flask.request.form['datepicker']
    time = flask.request.form['timepicker']
    origin = flask.request.form['origin'].replace(' ','+')
    destination = flask.request.form['destination'].replace(' ','+')
    if origin == "" or destination == "":
    	origin = "Central+Park"
    	destination = "JFK+Airport"
    uri  = 'https://maps.googleapis.com/maps/api/directions/json?origin='+origin+'&destination='+destination+'&mode=driving&key='+gmaps_key
    response = requests.get(uri)
    dirs = json.loads(response.text)


    uri = 'http://api.wunderground.com/api/' + wu_key + '/hourly10day/q/NY/New_York_City.json'
    response = requests.get(uri)
    data = json.loads(response.text)
    fc = data['hourly_forecast']
    hour = str(int(time[:2]) + (1 if int(time[-2:]) >= 30 else 0) + 4)
    lst = [x for x in fc if x['FCTTIME']['year'] == date[:4] and x['FCTTIME']['mon_padded'] == date[5:7] and x['FCTTIME']['mday_padded'] == date[8:] and x['FCTTIME']['hour'] == hour]
    if len(lst)>0:
    	forecast = lst[0]
    	return flask.jsonify(icon_url=forecast['icon_url'], temp=forecast['temp']['english'], dir=dirs)
    else:
    	return flask.jsonify(icon_url="", temp="Error: Weather forecast not found. Please confirm date is in the next ten days.", dir=dirs)

if __name__ == "__main__":
	print(__doc__)
	app.run(debug=True)