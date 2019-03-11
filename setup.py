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
        user.insert({'location':p['location'],'pincode':p['pincode'],'longitude':p['longitude'],'latitude':p['latitude'], 'adj_office':[]})
        return '0'
    except:
        return '1'

@app.route('/add_order', methods=['POST','GET'])
def order_Add():
    try:
        user = mongo.db.orders
        p = request.form

        # shortest path
        path = []

        user.insert({'longitude':'','latitude':'','status':'at_office', 'current':p['from_city'],'from_address':p['from_address'],'from_city':p['from_city'],'from_pincode':p['from_pincode'],'to_address':p['to_address'],'to_city':p['to_city'],'to_pincode':p['to_pincode'],'category':p['category'],'path':path})
        return '0'
    except:
        return '1'


@app.route('/track_cust',methods=['POST','GET'])
def track_cust():
    try:
        user = mongo.db.orders
        p = request.form
        data = user.find({'id':p['_id']})
        for i in data:
            ans = i
        return "[1], [2], [3]".format(ans['status'], ans['current'], ans['longitude'], ans['latitude'])
    except:
        return '1'

@app.route('/office_list', methods=['POST','GET'])
def off_list():
    try:
        user = mongo.db.office
        off_list = user.distinct('location')
        return str(off_list[1:-1])
    except:
        return '1'

@app.route('/add_route', methods=['POST','GET'])
def add_route():
    try:
        p = request.form
        users = mongo.db.office
        up_lis = users.find({'location':p['from']})
        # might be
        for i in up_lis:
            ans = i['adj_office']
        ans.append(p['to'])
        users.update({'location':p['from']},{'adj_office':ans})
        return '0'
    except:
        return '1'

@app.route('/admin', methods=['POST','GET'])
def admin_():
    try:
        p = request.form
        name = "Admin"
        passw = '12345'
        if name == p['name'] and passw == p['password']:
            return '0'
        else:
            return '1'
    except:
        return '1'

@app.route('/track_admin', methods=['POST','GET'])
def track_admin():
    try:
        user = mongo.db.orders
        p = request.form
        data = user.find({'id':p['_id']})
        for i in data:
            ans = i
        route = str(ans['path'])
        return "[1], [2], [3], [4],".format(ans['current'], ans['longitude'], ans['latitude'], route, )
    except:
        return '1'



if __name__ == '__main__':
    app.run(debug=True)