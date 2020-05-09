import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return '''Welcome to my Homepage! <br>
        Available routes: <br>
        /api/v1.0/precipitation <br> 
        /api/v1.0/stations <br>
        /api/v1.0/tobs <br>
        /api/v1.0/start <br>
        /api/v1.0/start/end <br>
    '''

# Convert the query results to a dictionary using `date` as the 
# key and `prcp` as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.datetime(2016, 8, 24)).order_by(Measurement.date).all()
    session.close()

    prec_list = []
    for date, prcp in results:
        prec_dict = {}
        prec_dict["date"] = date
        prec_dict["prcp"] = prcp
        prec_list.append(prec_dict)
    
    return jsonify(prec_list)



# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    station_list = list(np.ravel(results))
    
    return jsonify(station_list)



# Query the dates and temperature observations of the most 
# active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for 
# the previous year.
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519397").\
        filter(Measurement.date >= dt.datetime(2016, 8, 24)).all()
    session.close()

    temp_list = []
    for date, prcp in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["prcp"] = prcp
        temp_list.append(temp_dict)
    
    return jsonify(temp_list)



# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start=None, end=None):   
    if not end:
        session = Session(engine)
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        result_list = list(np.ravel(results))
        session.close()
        return jsonify(result_list)

    session = Session(engine)    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    result_list = list(np.ravel(results))
    session.close()
    return jsonify(result_list)



if __name__ == '__main__':
    app.run(debug=True)














