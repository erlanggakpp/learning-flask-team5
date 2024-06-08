from flask import Blueprint, jsonify, request
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.append(parent_dir)
from db import teams, players
from flasgger import swag_from
from functools import wraps
import copy

team_bp = Blueprint('teams', __name__)

class CustomException(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(message)

def handle_custom_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": e.message}), e.error_code
    return decorated_function

@team_bp.get("/")
@swag_from(os.path.join(current_dir, '..', 'swagger_doc', 'get_teams.yml'))
@handle_custom_exceptions
def get_teams():
    if len(teams) == 0:
        raise CustomException("There are no registered teams yet", 400)
    return jsonify({"teams": teams}), 200
    
@team_bp.post("/")
@swag_from(os.path.join(current_dir, '..', 'swagger_doc', 'create_teams.yml'))
@handle_custom_exceptions
def create_teams():
    data = request.get_json()
    validate_team_data(data)
    teams.append({"id": len(data)+1, **data})
    return jsonify({"team": data}), 201

@team_bp.get("/<int:id>")
@handle_custom_exceptions
def get_specific_team(id):
    target_team = None
    for team in teams:
        if team["id"] == id:
            target_team = copy.deepcopy(team)
            break
    if target_team is None:
        raise CustomException(f"There are no registered teams with ID: {id}", 400)
    team_players = []
    for player in players:
        if player["team_id"] == id:
            team_players.append(player)
    target_team["players"] = team_players
    return jsonify({"team": target_team}), 200
    
@team_bp.put("/<int:id>")
@swag_from(os.path.join(current_dir, '..', 'swagger_doc', 'edit_teams.yml'))
@handle_custom_exceptions
def edit_specific_team(id):
    target_team = None
    data = request.get_json()
    validate_team_data(data)
    for team in teams:
        if team["id"] == id:
            target_team = team
            break
    if target_team is None:
        raise CustomException(f"There are no registered teams with ID: {id}", 400)
    target_team.update(data)
    return jsonify({"message": f"Sucessfully edited team with ID: {id}"}), 200

    
def validate_team_data(data):
    required_fields = ['name', 'city']
    for field in required_fields:
        if field not in data:
            raise CustomException("Ensure Team's name and city is provided!", 422)
        
        if not data[field]:
            raise CustomException("Ensure Team's name and city is value is correct!", 422)
        


