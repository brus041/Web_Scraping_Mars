from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo

# set up
app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
    
# store this result in Mongo as python dictionary
@app.route("/scrape")
def scrape_():
    from scrape_mars import scrape
    return scrape()

#db.mars_data.insert(scrape_())

@app.route("/")
def query():
    mars = mongo.db.mars_data.find_one()
    
    # Return the template with the teams list passed in
    return render_template('index.html', data = mars)


if __name__ == "__main__":
    app.run(debug=True)