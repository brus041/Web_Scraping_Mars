from flask import Flask, render_template
import pymongo

# set up
app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
    
# store this result in Mongo as python dictionary
@app.route("/scrape")
def scrape_():
    from scrape_mars import scrape
    return scrape()

db.mars_data.insert(scrape_())

@app.route("/")
def query():
    
    return render_template("index.html", text="Serving up cool text from the Flask server!!")

if __name__ == "__main__":
    app.run(debug=True)