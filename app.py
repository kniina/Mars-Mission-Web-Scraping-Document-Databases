# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route that finds documents from Mongo and renders index.html template
@app.route("/")
def index():
    
    # Find data
    marsInfo = mongo.db.marsInfo.find_one()

    # return template and data
    return render_template("index.html", marsInfo = marsInfo)

# Route that will trigger scrape functions
@app.route('/scrape')
def scrape():

    marsInfo = mongo.db.marsInfo

    # Run scraped functions
    data = scrape_mars.scrape()

    # Store results into a dictionary
    marsInfo = {
        "title": data["title"],
        "text": data["text"],
        "featured_image_url": data["featured_image_url"], 
        "mars_table": data["mars_table"],
        "hemisphere_image_urls": data["hemisphere_image_urls"]
        } 
    
    # # Insert mars factoids into database
    mongo.db.marsInfo.insert_one(marsInfo)
   
    # Redirect back to home page
    return redirect("/", code=302)

# Run app
if __name__ == "__main__":
    app.run(debug=True)
