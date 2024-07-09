# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import re
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )


@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)

    one_year= dt.date(2017, 8, 23)-dt.timedelta(days=365)
    one_year_date = dt.date(one_year.year, one_year.month, one_year.day)

    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_date).all()

    precipitation_dict = dict(results)

    return jsonify(precipitation_dict) 


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    stations = []
    for station,name,lat,lon,elev in results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = elev
        stations.append(station_dict)

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
     session = Session(engine)

     results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281')\.filter(Measurement.date>='2016-08-23').all()

     tobs_list = []
     for date, tobs in results:
         tobs_dict = {}
         tobs_dict["Date"] = date
         tobs_dict["Tobs"] = tobs
         tob_obs.append(tobs_dict)

     return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")

def temps_start(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\filter(Measurement.date >= start).all()

    session.close()

    temps = []
    for min, avg, max in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min
        temps_dict['Average Temperature'] = avg
        temps_dict['Maximum Temperature'] = max
        temps.append(temps_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    temps = []
    for min, avg, max in results:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min
        temps_dict['Average Temperature'] = avg
        temps_dict['Maximum Temperature'] = max
        temps.append(temps_dict)

    return jsonify(temps)


if __name__ == '__main__':
    app.run(debug=True)
