# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from pymongo import MongoClient

from flask import Flask, jsonify, render_template, request, url_for, redirect

app = Flask(__name__)
#################################################
# Database Setup
#################################################
client = MongoClient('localhost', 27017)

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tabs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    start_date = '2016-08-23'
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > start_date).all()
    session.close()

    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precip.append(precip_dict)
    return jsonify(precip)      

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_list = session.query(Measurement.station).distinct().all()
    session.close()

    stat = []
    for station in stations_list:
        stat_dict = {}
        stat_dict["station"] = station[0]
        stat.append(stat_dict)
    return jsonify(stat)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    start_date = '2016-08-23'
    most_active_stations = session.query(Measurement.date, Measurement.tobs).filter((Measurement.station == 'USC00519281') & (Measurement.date > start_date)).all()
    session.close()

    temp_obs = []
    for date, tobs in most_active_stations:
        temp_obs_dict = {}
        temp_obs_dict['Date'] = date
        temp_obs_dict['Temperature'] = tobs
        temp_obs.append(temp_obs_dict)
    return jsonify(temp_obs)


@app.route("/api/v1.0/<start>")
def temp_statistics(start_date):
    session = Session(engine)
    min_max_avg = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    temp_data = []
    for tobs in min_max_avg:
        temp_dict = {}
        temp_dict['Minimum'] = min_max_avg[0][0]
        temp_dict['Maximum'] = min_max_avg[0][1]
        temp_dict['Average'] = min_max_avg[0][2]
        temp_data.append(temp_dict)
    return jsonify(temp_data)



@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start_date=None, end_date=None):
    session = Session(engine)
    start_end_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter((Measurement.date >= start_date)&(Measurement.date <= end_date)).all()
    session.close()

    temp_data = []
    for tobs in start_end_stats:
        temp_dict = {}
        temp_dict['Minimum'] = start_end_stats[0][0]
        temp_dict['Maximum'] = start_end_stats[0][1]
        temp_dict['Average'] = start_end_stats[0][2]
        temp_data.append(temp_dict)
    return jsonify(temp_data)    



    if __name__ == "__main__":
        app.run(debug=True)
