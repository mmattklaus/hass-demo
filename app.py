from flask import Flask, render_template, request
from flask_socketio import SocketIO

import RPi.GPIO as io

io.setmode(io.BOARD)
io.setwarnings(False)

RED_LED = 8
BLUE_LED = 10

io.setup(RED_LED, io.OUT, initial=io.LOW)
io.setup(BLUE_LED, io.OUT, initial=io.LOW)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def home():
	app_name = "The HASS Project"
	return render_template("index.html", app=app_name)


@app.route("/create", methods=["GET", "POST"])
def create():
	return render_template("create.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'GET':
		email = request.args.get("email")	
		password = request.args.get("password")
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']

	return "Your email is: {} & Password: {}".format(email, password)


@socketio.on('led-state')
def handle_message(message):
	Type = message['type']
	Value = message['value']
	# print("Type: {} Value: {}".format(Type, Value))
	if Type == 'red':
		io.output(RED_LED, Value)
	elif Type == 'blue':
		io.output(BLUE_LED, Value)


if __name__ == '__main__':
	socketio.run(app, debug=True, host="0.0.0.0")