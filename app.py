from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.charts import HeatMap, bins
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9
from bokeh.sampledata.autompg import autompg
import requests
import pandas as pd
import datetime

app = flask.Flask(__name__)


def getitem(obj, item, default):
	if item not in obj:
		return default
	else:
		return obj[item]

data=pd.read_csv('static/data/small_sample.csv')

def histogram():
	plot = figure(width=300, height=300)
	plot.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1,2,3], color="#CAB2D6")
	script, div = components(plot)
	return script, div

def heatmap():
	plot = HeatMap(autompg, x=bins('mpg'), y=bins('displ'), stat='mean', values='cyl', palette=RdYlGn6)
	script, div = components(plot)
	return script, div

@app.route('/')
def main():
	return flask.redirect('/index')


@app.route('/index')
def index():
	#script, div = histogram()
	return flask.render_template('index.html'
	)

@app.route('/analysis')
def about():
	script1, div1 = histogram()
	script2, div2 = heatmap()
	return flask.render_template('analysis.html',
		plot_script1=script1,
		plot_div1=div1,
		plot_script2=script2,
		plot_div2=div2,
		js_resources = INLINE.render_js(),
		css_resources = INLINE.render_css()
	)

if __name__ == "__main__":
	print(__doc__)
	app.run(debug=True)