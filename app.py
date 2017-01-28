from __future__ import print_function

import flask

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
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


@app.route("/")
def histogram():
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	plot = figure(width=300, height=300)
	plot.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1,2,3], color="#CAB2D6")
	script, div = components(p)
	html = flask.render_template(
		'index.html',
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources
	)
	return encode_utf8(html)


@app.route('/')
def main():
	return flask.redirect('/index')


@app.route('/index')
def index():
	return flask.render_template('index.html')


if __name__ == "__main__":
	print(__doc__)
	app.run(debug=False)