### file for interfaces ###
# APIs:
# /api/WWP/getDisplayData  () -> {alice : [amount of payment, number of payment], 
#                                   bob : [a, n], ...}
# to display data
#
# /api/WWP/getNextPayment () -> {Alice : weight,
#                                Bob : weight, ...}
# to get weight for next payment
#
# /api/WWP/writeNewPayment {"name": "Alice", "amount": 12.34, "time": "2099-12-31"} -> {"result": ...}, exit code
# to write new payment

from flask import Blueprint, request, jsonify
from WWP.opData import opData
bp = Blueprint("WWP", __name__, url_prefix="/api/WWP")

#return a json file that contain: persons with their spending data
@bp.route("/getDisplayData", methods = ["GET"])
def getDisplayData():
    opdata = opData()
    return jsonify(opdata.getDisplayData())

@bp.route("/getNextPayment", methods = ["GET"])
def getNextPayment():
    opdata = opData()
    return jsonify(opdata.getNextPayment())

@bp.route("/writeNewPayment", methods = ["POST"])
def writeNewPayment():
    data = request.get_json()
    if not data:
        return jsonify({"result":"Error, no data received."}), 400
    try:
        name = data["name"]
        amount = round(float(data["amount"]), 2)
        time = data["time"]
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({"result": f"Invalid data format: {str(e)}"}), 400
    opdata = opData()
    opdata.writeNewPayment(name, amount, time)
    return jsonify({"result": "write successfully!"}), 200