from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import scrape_mars

#Create a Flask instance
app= Flask(__name__)

#Using PyMongo to create a connection 
app.config["MONGO_URI"]= "mongodb:localhost:27017/mars_app"
mongo=PyMongo(app)

#route to render index.html template using data from MongoDB
@app.route("/")
def index():
    mars_data=mongo.db.mars_data.find_one()
    return render_template("index.html",mars_data=mars_data)

#route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_data=scrape_mars.scrape()

    #Update the Mongo DB using update and upsert to add if it's new
    mongo.db.mars_data.update({},mars_data, upsert=True)
    return 'Scraping Successful!'

if __name__=="__main__":
    app.run(debug=True)

