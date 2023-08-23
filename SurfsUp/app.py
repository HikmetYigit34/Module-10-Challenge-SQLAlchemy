# Part 2: Design Your Climate App

# Import the dependencies. ----------------------------------------------------
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup---------------------------------------------------------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model--------------------------------
Base = automap_base()

# reflect the tables-----------------------------------------------------------
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB------------------------------
session = Session(engine)

# Flask Setup------------------------------------------------------------------
app = Flask(__name__)


# Flask Routes-----------------------------------------------------------------
# List all the available routes------------------------------------------------
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
	    f"<h1 style='color:blue; background:#eef; padding:10px'>Welcome to Hawaii Surf API </h1>"
        f"Available Routes:<br/>"
        f"<hr/>"

        f"/api/v1.0/precipitation &nbsp; &nbsp; "
	    f"<a href='/api/v1.0/precipitation'>click here for link</a><br/>"
        f"<ul>List of prior year rain totals from all stations"
		f"</ul><hr/>"

        f"/api/v1.0/stations &nbsp; &nbsp; "
		f"<a href='/api/v1.0/stations'>click here for link</a><br/>"
        f"<ul>List of Station numbers and names"
		f"</ul><hr/>"
    
		f"/api/v1.0/tobs &nbsp; &nbsp; "
		f"<a href='/api/v1.0/tobs'>click here for link</a><br/>"
        f"<ul> List of prior year temperatures from all stations"
		f"</ul><hr/>"

        f"/api/v1.0/start &nbsp; &nbsp; "
		f"<a href='/api/v1.0/2017-06-01'>click here for link</a><br/>"
        f"<ul>When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date"
 		f"<li>if you enter url 127.0.0.1:5000/api/v1.0/2017-06-01 you will get [69.0,78.04042553191489,87.0] </li>"
		f"</ul><hr/>"

		f"/api/v1.0/start/end &nbsp; &nbsp; "
		f"<a href='/api/v1.0/2017-06-01/2017-06-30'>click here for link</a><br/>"
        f"<ul> When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive"
		f"<li>if you enter url 127.0.0.1:5000/api/v1.0/2017-06-01/2017-06-30 you will get temps:[71.0,77.21989528795811,83.0]"
		f"</ul><hr/>"
    )
	
# Convert the query results from precipitation analysis------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():
	"""Return a list of rain fall for prior year"""
    # Calculate the date 1 year ago from last date in database
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	# Query for the date and precipitation for the last year
	precipitation = session.query(Measurement.date, Measurement.prcp).\
		filter(Measurement.date >= prev_year).all()
	session.close()
    # Dict with date as the key and prcp as the value
	precip = {date: prcp for date, prcp in precipitation}
	return jsonify(precip)
	
# Return a JSON list of stations from the dataset------------------------------
@app.route("/api/v1.0/stations")
def stations():
	stations_query = session.query(Station.name, Station.station)
	stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
	return jsonify(stations.to_dict())

# Return a JSON list of temperature observations for the previous year-----------
@app.route("/api/v1.0/tobs")
def tobs():
	"""Return a list of rain fall for prior year"""
    # Calculate the date 1 year ago from last date in database
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	# Query for the date and tobs for the last year
	temps = session.query(Measurement.date, Measurement.tobs).\
		filter(Measurement.date >= prev_year).all()
	session.close()
    # Dict with date as the key and tobs as the value
	t = {date: tobs for date, tobs in temps}
	return jsonify(t)
	

# For a specified start, ------------------------------------------------------
# calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date	
@app.route("/api/v1.0/<start>")
def get_data(start):
	start_date= dt.datetime.strptime(start, '%Y-%m-%d')
	#end_date= dt.datetime.strptime(2017-8-23, '%Y-%m-%d')
	#last_year = dt.timedelta(days=365)
	end_date = dt.date(2017, 8, 23)
	start = start_date
	end=end_date

	all_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
		filter(Measurement.date >= start).\
		filter(Measurement.date <= end).all()
	all = list(np.ravel(all_data))
	return jsonify(all)

# For a specified start date and end date, ------------------------------------
# calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)	
	
	
#------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
#------------------------------------------------------------------------------
	
