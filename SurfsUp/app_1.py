# Part 2: Design Your Climate App
# Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:
# 1. /
#   	o	Start at the homepage.
#   	o	List all the available routes.
# 2. /api/v1.0/precipitation
#   	o	Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#   	o	Return the JSON representation of your dictionary.
# 3. /api/v1.0/stations
#   	o	Return a JSON list of stations from the dataset.
# 4. /api/v1.0/tobs
#   	o	Query the dates and temperature observations of the most-active station for the previous year of data.
#   	o	Return a JSON list of temperature observations for the previous year.
# 5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
#   	o	Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#   	o	For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#   	o	For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
# Hints
#   	•	Join the station and measurement tables for some of the queries.
#   	•	Use the Flask jsonify function to convert your API data to a valid JSON response object.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 





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


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"

    )