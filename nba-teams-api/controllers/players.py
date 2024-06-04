from flask import Blueprint, jsonify
from db import players

player_bp = Blueprint('players', __name__)

@player_bp.get("/")
def get_players():
    try:
        if len(players) == 0:
            raise Exception("There are no registered players yet")
        return jsonify({"players": players}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 200