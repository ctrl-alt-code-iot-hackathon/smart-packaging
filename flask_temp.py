from flask import Flask,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DATABASE'] = 'smartpackaging'
app.config['MONGO_URI'] = 'mongodb://iot:iot123@ds263295.mlab.com:63295/smartpackaging'

mongo = PyMongo(app)
@app.route('/add',methods = ['POST', 'GET'])
def done():
    user = mongo.db.orders
    p=request.form
    #print(p['name'])
    user.insert({'name': p['name']})
    return "request tests"

if __name__ == '__main__':
    app.run(debug=True)