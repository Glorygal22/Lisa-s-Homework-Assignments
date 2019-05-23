# Import Dependencies
from flask import Flask, render_template
import pymongo
import scrape_mars
import requests

app = Flask(__name__)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
# database = mars_info_db
db = client.mars_info_db
collection = db.mars

@app.route("/")
def home():
    # data = list(db.mars.find())
    # print(data)
    return render_template("index.html", mars_data = mars_data)

@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()
    collection.update({}, mars, upsert=True)
    # db.mars.insert_one(mars_data)
    return "data"


if __name__ == "__main__":
    app.run(debug=True)