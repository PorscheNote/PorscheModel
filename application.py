#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
#from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)

'''
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'porschemodel':
        return 'porschenote'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
'''

cars = [
    {
        'id': 1,
        'model': 'Porsche 911 GT3 RS',
        'topspeed': '310 km/h'
    },
    {
        'id': 2,
        'model': 'Porsche Boxter S',
        'topspeed': '277 km/h'
    }
]


@app.route('/porschemodel/api/v1.0/cars', methods=['GET'])
#@auth.login_required
def get_cars():
    #return jsonify({'porschemodels': cars})
    return jsonify({'cars': [make_public_car(car) for car in cars]})


@app.route('/porschemodel/api/v1.0/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = [car for car in cars if car['id'] == car_id]
    if len(car) == 0:
        abort(404)
    return jsonify({'car': car[0]})


@app.route('/porschemodel/api/v1.0/cars', methods=['POST'])
def create_car():
    if not request.json or not 'model' in request.json:
        abort(400)
    car = {
        'id': cars[-1]['id'] + 1,
        'model': request.json['model'],
        'topspeed': request.json.get('topspeed', "")
    }
    cars.append(car)
    return jsonify({'car': car}), 201


@app.route('/porschemodel/api/v1.0/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = [car for car in cars if car['id'] == car_id]
    if len(car) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'model' in request.json and type(request.json['model']) != unicode:
        abort(400)
    if 'topspeed' in request.json and type(request.json['topspeed']) is not unicode:
        abort(400)
    car[0]['model'] = request.json.get('model', car[0]['model'])
    car[0]['topspeed'] = request.json.get('topspeed', car[0]['topspeed'])
    return jsonify({'car': car[0]})


@app.route('/porschemodel/api/v1.0/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = [car for car in cars if car['id'] == car_id]
    if len(car) == 0:
        abort(404)
    cars.remove(car[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_car(car):
    new_car = {}
    for field in car:
        if field == 'id':
            new_car['uri'] = url_for('get_car', car_id=car['id'], _external=True)
        else:
            new_car[field] = car[field]
    return new_car


if __name__ == '__main__':
    app.run(debug=True)