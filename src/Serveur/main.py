from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")

def turbo_test():
	result = subprocess.run(['python3','test.py'],capture_output=True).stdout
	return result