from flask import Blueprint, jsonify, request
from database import Room, User
from extensions import db
from utils import get_unique_room_code

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

username = "spravce"
password = "spravce" #Think_diff3r3nt_Admin

@api_bp.route("/create_room/<room_name>", methods=["POST"])
def create_room(room_name):
    code = get_unique_room_code()
    room = Room(room_name=room_name, room_code=code)
    db.session.add(room)
    db.session.commit()
    return jsonify({"message": "Room created!", "room_code": code})

@api_bp.route("/get_rooms", methods=["GET"])
def get_rooms():
    rooms = Room.query.all()
    room_list = [{"room_code": room.room_code, "room_name": room.room_name, "users": room.user_ids, "presenters": room.presenter_ids} for room in rooms]
    return jsonify(room_list)

@api_bp.route("/get_room_info/<room_code>", methods=["GET"])
def get_room_info(room_code):
    room = Room.query.filter_by(room_code=room_code).first()
    if room:
        return jsonify({"room_code": room.room_code, "room_name": room.room_name, "users": room.user_ids})
    else:
        return jsonify({"error": "Místnost neexistuje"}), 404

@api_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username1 = data.get("username")
    password1 = data.get("password")
    if username == username1 and password == password1:
        return jsonify({"message": "Přihlášení bylo úspěšné!"})
    else:
        return jsonify({"error": "Špatné přihlašovací údaje"}), 401
    
@api_bp.route("/exists_room/<room_code>", methods=["GET"])
def exists_room(room_code):
    room = Room.query.filter_by(room_code=room_code).first()
    if room:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})

@api_bp.route("/join_room/<room_code>", methods=["POST"])
def join_room(room_code):
    room = Room.query.filter_by(room_code=room_code).first()
    if room:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "Nebyl poskytnut user_id"}), 400
        
        if user_id not in room.user_ids:
            room.user_ids.append(user_id)
            db.session.commit()
            return jsonify({"message": "Připojeno do místnosti!", "room_code": room.room_code, "users": room.user_ids})
        else:
            return jsonify({"message": "Uživatel již je v místnosti", "room_code": room.room_code, "users": room.user_ids})
    else:
        return jsonify({"error": "Místnost nenalezena"}), 404

@api_bp.route("/hi", methods=["GET"])
def hello():
    return jsonify({"message": "hi!"})
