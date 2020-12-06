import os
from riot_api_helpers import get_summoner_by_name, get_matches_for_account, get_match_for_match_id
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


load_dotenv()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure access to MySQL database
db_connection = mysql.connector.connect(
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    passwd = os.getenv("MYSQL_PASSWORD"),
    database = os.getenv("MYSQL_DB"))

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = db_connection.cursor()

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route('/', methods=["GET"])
def index():
    """Show homepage with form to submit Summoner Name"""
    if request.method=="GET":
        return render_template("index.html")

@app.route('/summoner', methods=["POST"])
def summoner():
        if request.method=="POST":
            requested_summoner = request.form.get("summoner")
            summoner_response_dict = get_summoner_by_name(requested_summoner)
            statement = "INSERT INTO person (summoner_id, account_id, name, summoner_level) VALUES(%s, %s, %s, %s)"
            statement_data = [summoner_response_dict["id"], summoner_response_dict["account_id"], summoner_response_dict["name"], summoner_response_dict["summoner_level"]]
            db.execute(statement,statement_data)
            db_connection.commit()
            return redirect("/")

# For each game in match history we need
# Win/Loss
# Champion Played
# Score
# Item 1,2,3,4,5,6
# Other participants, their team, their champion, their summoner name  

# To start with we just need the last 10 games the summoner played, their champion and their outcome

if __name__ == '__main__':
    app.run(debug=True)