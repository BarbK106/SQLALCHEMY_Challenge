# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine ("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"(start: a date string in the format YYY-mm-dd)<br/>"
        f"/api/v1.0/start/end<br/>"
        f"(start/end:a date string in the format YYY-mm-dd)<br/> )"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   
   last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
   
   one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   annual_prcp_data = annual_precipitation=session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= '2016-08-23', measurement.date <= '2017-08-23').\
    order_by(measurement.date).all()
   
   annual_prcp_data []
   for date, prcp in annual_prcp_data:
        results_dict = []
        results_dict["date"] = date
        results_dict["prcp"] =prcp

   return jsonify(annual_prcp_data)


@app.route("/api/v1.0/stations")
def stations():

    all_stations =session.query(station.station).all()
   
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    most_active_station = session.query(measurement).group_by(measurement.station).\
    filter(measurement.station =='USC00519281').all()

    return jsonify(most_active_station)


@app.route("api/v1.0/<start>")
def temp_data(start):

    start_date = dt.datetime.strptime(start, %Y. %m, %d")
                                      
    query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.round(func.avg(measurement.tobs))).\
    filter(measurement.date >= start_date),all()

    result = list(np.ravel(query))

    return jsonify(result)
                                  
                                      
@app.route("/api/v1.0/<start>/<end>")
def temp_data2(start, end):

    start_date = dt.datetime.strptime(start, "%Y. %m, %d")
    end_date = dt.datetime.strptime(end, "%Y. %m, %d")

    query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.round(func.avg(measurement.tobs))).\
    filter(measurement.date.between(start_date, end_date),all()


##Define main behavior
if __name__ == "__main__":
    app.run(debug=True)


