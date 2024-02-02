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
def precipitation():
    session = Session(engine)
    stations_list = session.query(Measurement.station).distinct().all()
    session.close()

    stat = []
    for station in stations_list:
        stat_dict = {}
        stat_dict["station"] = station[0]
        stat.append(stat_dict)
    return jsonify(stat)

@app.route("/api/v1.0/tabs")
def precipitation():
    session = Session(engine)



    session.close()
@app.route("/api/v1.0/<start>")
def precipitation():
    session = Session(engine)



    session.close()
@app.route("/api/v1.0/<start>/<end>")
def precipitation():
    session = Session(engine)






    session.close()









    if __name__ == "__main__":
        app.run(debug=True)
