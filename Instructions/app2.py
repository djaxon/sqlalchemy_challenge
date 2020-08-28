import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

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
app2 = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app2.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
        )


@app2.route("/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all preciptation between 8/23/17 and 8/23/16"""

    # Convert the query results to a
    # dictionary using date as the key and prcp as the value.

    prcp_data=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').\
    order_by(Measurement.date).all()


    session.close()

    return jsonify(prcp_data)


@app2.route("/stations")
def station_name():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all preciptation between 8/23/17 and 8/23/16"""

    # Create list of stations

    station_name=session.query(Station.station).all()

    session.close()

    return jsonify(station_name)

@app2.route("/tobs")
def LTM_temps():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all preciptation between 8/23/17 and 8/23/16"""

    # Query dates and temps of the most active station for the last year
    
    temps = [Measurement.date, func.avg(Measurement.tobs).label('temp')]
         
    LTM_temps = session.query(*temps).\
        filter(Measurement.date > '2016-08-09').\
        filter(Measurement.station == 'USC00519281').\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    session.close()

    return jsonify(LTM_temps)

# @app2.route("/api/v1.0/Station")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station,elevation).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app2.run(debug=True)
