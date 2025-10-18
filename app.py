from flask import Flask
from flask_cors import CORS

# blueprint of WWP
from WWP.interface import bp as WWP_bp

app = Flask(__name__)
CORS(app, origins=["https://wwp.20age1million.com"])

# interfaces of WWP
app.register_blueprint(WWP_bp)      


# running
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)