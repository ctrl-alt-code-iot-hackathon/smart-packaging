from flask import Flask,request
from flask_pymongo import PyMongo
from ast import literal_eval
from bson.objectid import ObjectId
from priodict import priorityDictionary

app = Flask(__name__)

app.config['MONGO_DATABASE'] = 'smartpackaging'
app.config['MONGO_URI'] = 'mongodb://iot:iot123@ds263295.mlab.com:63295/smartpackaging'

mongo = PyMongo(app)

@app.route('/add_office',methods=['POST','GET'])
def office_Add():
    #try:
    user = mongo.db.office
    p = request.get_data()
    print(p)
    a = p.decode("utf-8")
    p = literal_eval(a)
    user.insert({'name':p['name'],'address':p['address'],'longitude':p['longitude'],'latitude':p['latitude'], 'adj_office':[]})
    return '0'
    # except:
    #     return '1'

@app.route('/add_order', methods=['POST','GET'])
def order_Add():
    try:
        user = mongo.db.orders
        p = request.get_data()
        a = p.decode("utf-8")
        p = literal_eval(a)

        # shortest path
        path = []
        user.insert({'driver':'Not assigned','vibration':'Good','longitude':'','latitude':'','status':'at_office', 'current':p['from'],
                     'from_address':p['from_address'],'from_city':p['from'],'from_pincode':p['from_pin'],'to_address':p['to_address'],
                     'to_city':p['to'],'to_pincode':p['to_pin'],'category':p['category'],'path':path,'tampered':'False'})
        return '0'
    except:
        return '1'


@app.route('/track_cust',methods=['POST','GET'])
def track_cust():
    try:
        user = mongo.db.orders
        p = request.get_data()
        a = p.decode("utf-8")
        p = literal_eval(a)
        print(str(p['_id']))
        ans = user.find_one({"_id":ObjectId(p['_id'])})
        return "{0}, {1}, {2}, {3}".format(ans['status'], ans['current'], ans['longitude'], ans['latitude'])
    except:
        return '1'

@app.route('/office_list', methods=['POST','GET'])
def off_list():
    try:
        user = mongo.db.office
        off_list = user.distinct('name')
        return str(off_list)[1:-1]
    except:
        return '1'

@app.route('/add_route', methods=['POST','GET'])
def add_route():
    try:
        p = request.get_data()
        a = p.decode("utf-8")
        p = literal_eval(a)
        users = mongo.db.office
        users.update({'name':p['from']},{ '$push': {'adj_office':{'name':p['to'],'cost':p['cost']}}})
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

@app.route('/update-data', methods=['POST','GET'])
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
                    return c-1
                user.update({'_id': p['_id']},{'$set':{'current':ans['next'], 'status':'At office', 'next':ans['route'][c+1],'tempered':p['tempered']}})
    except:
        return '1'

@app.route('/driver-req-packages',methods=['POST','GET'])
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
    # try:
    user = mongo.db.orders
    p = request.get_data()
    a = p.decode("utf-8")
    p = literal_eval(a)
    ans = user.find_one({"_id": ObjectId(p['order_id'])})
    #route = str(ans['path'])
    return "{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(ans['current'], ans['longitude'], ans['latitude'], ans['next'], ans['status'], ans['vibration'], ans['driver'], ans['tampered'])
    # except:
    #     return '1'


def get_priorityDict():
    office = mongo.db.office
    allOffices = office.find()
    G = dict()
    for eachOffice in allOffices:
        G[eachOffice['name']] = dict()
        for eachAdjOffice in eachOffice['adj_office']:
            G[eachOffice['name']][eachAdjOffice['name']] = int(eachAdjOffice['cost'])
    return G

def Dijkstra(G,start,end=None):
	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		print(G)
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					print("valueerror")
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)
			
def shortestPath(G,start,end):
	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path
    

if __name__ == '__main__':
    app.run(debug=True)
    print(get_priorityDict())
    print(shortestPath(get_priorityDict(), 'Lynn', 'Brooklyn'))
