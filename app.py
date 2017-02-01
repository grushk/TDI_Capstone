from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.charts import HeatMap, bins
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9
import requests
import pandas as pd
import datetime

app = flask.Flask(__name__)
gmaps_key = "AIzaSyCz-oZKRWxA_e0DHaZujnsy937yMzYoYXM"

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
	#script, div = histogram()
	return flask.render_template('index.html',
		gmaps_key = gmaps_key
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

if __name__ == "__main__":
	print(__doc__)
	app.run(debug=True)