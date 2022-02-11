from flask import Flask, jsonify
import sqlalchemy, inspect

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# SQLAlchemy
from sqlalchemy import create_engine, func, inspect
# main file
#import climate_starterJ

#################################################
# Database Setup
#################################################
# create engine
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model--automap classes
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
measurement = Base.classes.measurement
Station = Base.classes.station


# Create a session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def justice_league():
    """Return the justice league data as json"""
def precipitation():
    return jsonify(precipitation)

@app.route('/')
def index():
    return (
        f'Surfs Up! Welcome to the Hawaii Climate Analysis API!<br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary

@app.route('/api/v1.0/precipitation')
def precipitation():
    '''Return the precipation data for the recent year of data'''
    # Calculate the date 1 year ago from the last data point in the data set
    recentDate = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    precipitDF = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > recentDate).all()


@app.route('/api/v1.0/stations')
def stations():
    '''Return a list of all of the stations'''
    # Return a JSON list of stations from the dataset
    stations1 = session.query(Station.station).all()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations1))
    print(all_stations)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route('/api/v1.0/tobs')
def tobs():
    '''Return the temperature observations (tobs) for the last year of data'''
    # Calculate the date 1 year ago from the last data point in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the dates and temperature observations of the most active station for the last year of data
    active_station_data = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()
    # Return a JSON list of temperature observations (TOBS) for the previous year
    temperature_observations = list(np.ravel(active_station_data))
    return jsonify(temperature_observations)



@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')

def dates(start=None, end=None):
    '''Return the minimum (TMIN), maximum (TMAX), and average (TAVG) temperature between given start and end dates or after a given start date'''
    # Return a JSON list of the minimum tempe, the avg temp, and the max temp for a given start or start-end range.
    # When given the start only, calculate 'TMIN', 'TMAX', and 'TAVG' 
    # for all dates greater than and equal to the start date.
    # When given the start and the end date, calculate the 'TMIN', 'TMAX', and 'TAVG' 
    # for dates between the start and end date inclusive.


    # Create stats to be calculated by user input
    input = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
  
    # If just a start date is given then 
    # calculate TMIN, TMAX, TAVG for dates greater than and equal to the start date
    if not end:
        after_start_date = session.query(*input).\
            filter(Measurement.date >= start).all()
        # Convert the list of tuples into a normal list
        after_temp_stats = list(np.ravel(after_start_date))
        return jsonify(after_temp_stats)
    return jsonify({"error": f"No information found... {after_start_date} not found."}), 404

    # If both a start and end date are given then
    # calculate TMIN, TMAX, TAVG between and including the given dates
    between_dates = session.query(*input).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Convert the list of tuples into a normal list
    between_temp_stats = list(np.ravel(between_dates))
    return jsonify(between_temp_stats)


if __name__ == "__main__":
    app.run(debug=True)
