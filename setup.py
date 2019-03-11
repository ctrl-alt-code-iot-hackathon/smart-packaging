from flask import Flask,request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DATABASE'] = 'smartpackaging'
app.config['MONGO_URI'] = 'mongodb://iot:iot123@ds263295.mlab.com:63295/smartpackaging'

mongo = PyMongo(app)
# @app.route('/order_place',methods = ['POST', 'GET'])
# def done():
#     user = mongo.db.orders
#     p = request.form
#     user.insert({'name': p['name']})
#     return "request tests"

@app.route('/add_office',methods=['POST','GET'])
def office_Add():
    try:
        user = mongo.db.office
        p = request.form
        user.insert({'location':p['location'],'pincode':p['pincode'],'longitude':p['longitude'],'latitude':p['latitude']})
        return '0'
    except:
        return '1'

# @app.route('/add_order', methods=['POST','GET'])
# def order_Add():
#     try:
#         user = mongo.db.orders
#         p = request.form
#         user.insert({'address':})

#
# @app.route('/main_page',methods=['POST','GET'])
# def main_page()
#     try:

if __name__ == '__main__':
    app.run(debug=True)