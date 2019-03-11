from flask import Flask,request
from flask_pymongo import PyMongo
from ast import literal_eval


app = Flask(__name__)

app.config['MONGO_DATABASE'] = 'smartpackaging'
app.config['MONGO_URI'] = 'mongodb://iot:iot123@ds263295.mlab.com:63295/smartpackaging'

mongo = PyMongo(app)

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

        user.insert({'driver':'Not assigned','vibration':'Good','longitude':'','latitude':'','status':'at_office', 'current':p['from_city'],
                     'from_address':p['from_address'],'from_city':p['from_city'],'from_pincode':p['from_pincode'],'to_address':p['to_address'],
                     'to_city':p['to_city'],'to_pincode':p['to_pincode'],'category':p['category'],'path':path,'tempered':'False'})
        return '0'
    except:
        return '1'


@app.route('/track_cust',methods=['POST','GET'])
def track_cust():
    try:
        user = mongo.db.orders
        p = request.form
        data = user.find({'_id':p['_id']})
        for i in data:
            ans = i
        return "[1], [2], [3], [4]".format(ans['status'], ans['current'], ans['longitude'], ans['latitude'])
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
        users.update({'location':p['from']},{ '$push': {'adj_office':{'to':p['to'],'cost':p['cost']}}})
        return '0'
    except:
        return '1'

@app.route('/admin', methods=['POST','GET'])
def admin_():
    try:
        p = request.get_data()
        a = p.decode("utf-8")
        a = literal_eval(a)
        name = "Admin"
        passw = '12345'
        if name == a['name'] and passw == a['password']:
            return '0'
        else:
            return '1'
    except:
        return '1'

@app.route('/hardware', methods=['POST','GET'])
def hardware():
    try:
        user = mongo.db.orders
        p = request.form
        #
        # Decide using training on data generated by testing by our own and then tested using logistic regression
        #
        data = user.find({'_id': p['_id']})
        for i in data:
            ans = i
        threshold = 200
        if p['vibration'] >= threshold:
            ans['vibration']='Bad'
        ans['longitude'] = p['longitude']
        ans['latitude'] = p['latitude']
        #condition if in any of the office
        if abs(p['longitude']-ans['longitude'])>10 and abs(p['latitude']-ans['latitude'])>10:
            if ans['current'] == ans['route'][-1]:
                user.update({'_id': p['_id']}, {'$set': {'status':'Delivered'}})
            else:
                c = 0
                for i in range(0,len(ans['route'])-1):
                    if ans['next'] == ans['route'][i]:
                        break
                    c = c+1
                if c == len(ans['route'])-1:
                    return c-1;
                user.update({'_id': p['_id']},{'$set':{'current':ans['next'], 'status':'At office', 'next':ans['route'][c+1],'tempered':p['tempered']}})
    except:
        return '1'

@app.route('/driver',methods=['POST','GET'])
def driver_():
    try:
        user = mongo.db.orders
        p = request.form
        a = user.update({'from_city':p['from_city'],'to_city':p['to_city']},{'status':'At route','driver':p['name'],'driver_contact':p['contact']})
        k = []
        for i in a:
            k.append(i['_id'])
        return str (k)[1:-1]
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
        return "[1], [2], [3], [4], [5], [6], [7], [8]".format(ans['current'], ans['longitude'], ans['latitude'], ans['next'],
                                                                   ans['status'], ans['vibration'], ans['driver'], ans['tempered'])
    except:
        return '1'


if __name__ == '__main__':
    app.run(debug=True)