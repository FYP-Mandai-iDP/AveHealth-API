from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
import os
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
CORS(app)

## Item
class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  content = db.Column(db.String(120), unique=True, nullable=False)

  def __init__(self, title, content):
    self.title = title
    self.content = content

  @app.route('/items/<id>', methods=['GET'])
  def get(id):
    item = Item.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)

  @app.route('/items', methods=['GET'])
  def get_items():
    items = []
    for item in db.session.query(Item).all():
      del item.__dict__['_sa_instance_state']
      items.append(item.__dict__)
    print(items)
    return jsonify(items)

  @app.route('/items', methods=['POST'])
  def create_item():
    body = request.get_json()
    db.session.add(Item(body['title'], body['content']))
    db.session.commit()
    return "item created"

  @app.route('/items/<id>', methods=['PUT'])
  def update_item(id):
    body = request.get_json()
    db.session.query(Item).filter_by(id=id).update(
      dict(title=body['title'], content=body['content']))
    db.session.commit()
    return "item updated"

  @app.route('/items/<id>', methods=['DELETE'])
  def delete_item(id):
    db.session.query(Item).filter_by(id=id).delete()
    db.session.commit()
    return "item deleted"

## attendance
class Attendance(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  zone = db.Column(db.String(80), unique=False, nullable=False)
  rfid_id = db.Column(db.String(80), unique=False, nullable=False)
  weight = db.Column(db.Float, unique=False, nullable=False)
  image_path = db.Column(db.String(120), unique=False, nullable=False)
  timestamp = db.Column(db.String(120), unique=False, nullable=False)
  device_id = db.Column(db.Integer, unique=False, nullable=False)
  

  def __init__(self, zone, rfid_id, weight, image_path, timestamp, device_id):
    self.zone = zone
    self.rfid_id = rfid_id
    self.weight = weight
    self.image_path = image_path
    self.timestamp = timestamp
    self.device_id = device_id

  @app.route('/attendances/<id>', methods=['GET'])
  def get_attendance(id):
    attendance = Attendance.query.get(id)
    del attendance.__dict__['_sa_instance_state']
    return jsonify(attendance.__dict__)

  @app.route('/attendances', methods=['GET'])
  def get_attendances():
    attendances = []
    for attendance in db.session.query(Attendance).all():
      del attendance.__dict__['_sa_instance_state']
      attendances.append(attendance.__dict__)
    print(attendances)
    return jsonify(attendances)

  @app.route('/attendances', methods=['POST'])
  def create_attendance():
    body = request.get_json()
    timestamp = body['timestamp']
    rfid = body['rfid_id']
    # zone, rfid_id, weight, image_path, timestamp, device_id
    db.session.add(Attendance(body['zone'], body['rfid_id'], body['weight'], body['image_path'], body['timestamp'], body['device_id']))
    db.session.commit()

    # Get Average
    try:
      lst = []
      weight = []
      for A in db.session.query(Attendance).all():
        # del bird.__dict__['_sa_instance_state']
        lst.append(A.__dict__)
      for i in lst:
        if i['rfid_id'] == body['rfid_id']:
          weight.append(i['weight'])
      
      birds = []
      for bird in db.session.query(Bird).all():
        # del bird.__dict__['_sa_instance_state']
        birds.append(bird.__dict__)

      for i in birds:
        if i['rfid_id'] == rfid:
          body = i

      if len(weight) <= 10:
        average_weight = round(sum(weight)/len(weight)) # average
      else:
        average_weight = round(sum(weight[-10:])/10) # average

      db.session.query(Bird).filter_by(rfid_id=rfid).update(
        dict(name=body['name'], rfid_id=body['rfid_id'], weight=average_weight, image_path=body['image_path'], timestamp=timestamp))
      db.session.commit()
      return "attendance created" + "\t\t" + str(average_weight)

    except:
      db.session.add(Bird("nameless", body['rfid_id'], body['weight'], body['image_path'], body['timestamp']))
      db.session.commit()
      return "attendance created"

  @app.route('/attendances/<id>', methods=['PUT'])
  def update_attendance(id):
    body = request.get_json()
    db.session.query(Attendance).filter_by(id=id).update(
      dict(zone=body['zone'], rfid_id=body['rfid_id'], weight=body['weight'], image_path=body['image_path'], timestamp=body['timestamp'], device_id=body['device_id']))
    db.session.commit()
    return "attendance updated"

  @app.route('/attendances/<id>', methods=['DELETE'])
  def delete_attendance(id):
    db.session.query(Attendance).filter_by(id=id).delete()
    db.session.commit()
    return "attendance deleted"

## bird
class Bird(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=False, nullable=False)
  rfid_id = db.Column(db.String(80), unique=False, nullable=False)
  weight = db.Column(db.Float, unique=False, nullable=False)
  image_path = db.Column(db.String(120), unique=False, nullable=False)
  timestamp = db.Column(db.String(120), unique=False, nullable=False)
  

  def __init__(self, name, rfid_id, weight, image_path, timestamp):
    self.name = name
    self.rfid_id = rfid_id
    self.weight = weight
    self.image_path = image_path
    self.timestamp = timestamp

  @app.route('/birds/<id>', methods=['GET'])
  def get_bird(id):
    bird = Bird.query.get(id)
    del bird.__dict__['_sa_instance_state']
    return jsonify(bird.__dict__)

  @app.route('/birds', methods=['GET'])
  def get_birds():
    birds = []
    for bird in db.session.query(Bird).all():
      del bird.__dict__['_sa_instance_state']
      birds.append(bird.__dict__)
    print(birds)
    return jsonify(birds)

  @app.route('/birds', methods=['POST'])
  def create_bird():
    body = request.get_json()
    # name, rfid_id, weight, image_path, timestamp
    db.session.add(Bird(body['name'], body['rfid_id'], body['weight'], body['image_path'], body['timestamp']))
    db.session.commit()

    return "bird created"

  # @app.route('/birds/<id>', methods=['PUT'])
  # def update_bird(id):
  #   body = request.get_json()
  #   db.session.query(Bird).filter_by(id=id).update(
  #     dict(name=body['name'], rfid_id=body['rfid_id'], weight=body['weight'], image_path=body['image_path'], timestamp=body['timestamp']))
  #   db.session.commit()
  #   return "bird updated"

  @app.route('/birds/rfid/<rfid>', methods=['PUT'])
  def update_bird_RFID(rfid):
    updated_body = request.get_json()
    birds = []
    for bird in db.session.query(Bird).all():
      # del bird.__dict__['_sa_instance_state']
      birds.append(bird.__dict__)
    for i in birds:
      if i['rfid_id'] == rfid:
        body = i
    db.session.query(Bird).filter_by(rfid_id=rfid).update(
      dict(name=body['name'], rfid_id=body['rfid_id'], weight=updated_body['weight'], image_path=body['image_path'], timestamp=body['timestamp']))
    db.session.commit()
    return "bird updated"

  @app.route('/birds/<id>', methods=['DELETE'])
  def delete_bird(id):
    db.session.query(Bird).filter_by(id=id).delete()
    db.session.commit()
    return "bird deleted"


db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)