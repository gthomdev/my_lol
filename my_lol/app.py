import os
import riot_api_helpers
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


load_dotenv()

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure access to MySQL database
db = mysql.connector.connect(
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    passwd = os.getenv("MYSQL_PASSWORD"),
    database = os.getenv("MYSQL_DB"))

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute('CREATE TABLE person (person_id int PRIMARY KEY AUTO_INCREMENT, summoner_id VARCHAR(256), account_id VARCHAR(256), name varchar(256), revision_date varchar(256), summoner_level int)')
    return('Done!')

if __name__ == '__main__':
    app.run(debug=True)