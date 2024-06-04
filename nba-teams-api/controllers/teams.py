from flask import Blueprint, jsonify, request
from db import teams, players
import copy

team_bp = Blueprint('teams', __name__)

@team_bp.get("/")
def get_teams():
    """
    Get all teams
    ---
    responses:
      200:
        description: A list of teams
        schema:
          type: object
          properties:
            teams:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  city:
                    type: string
      400:
        description: There are no registered teams yet
    """
    try:
        if len(teams) == 0:
            raise Exception("There are no registered teams yet")
        return jsonify({"teams": teams}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 200
    
@team_bp.post("/")
def create_teams():
    try:
        data = request.get_json()
        validate_team_data(data)
        teams.append(data)
        return jsonify({"team": data}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 401

@team_bp.get("/<int:id>")
def get_specific_team(id):
    try:
        target_team = None
        for team in teams:
            if team["id"] == id:
                target_team = copy.deepcopy(team)
                break
        if target_team is None:
            raise Exception(f"There are no registered teams with ID: {id}")
        team_players = []
        for player in players:
            if player["team_id"] == id:
                team_players.append(player)
        target_team["players"] = team_players
        return jsonify({"team": target_team}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
@team_bp.put("/<int:id>")
def edit_specific_team(id):
    try:
        target_team = None
        data = request.get_json()
        validate_team_data(data)
        for team in teams:
            if team["id"] == id:
                target_team = team
                break
        if target_team is None:
            raise Exception(f"There are no registered teams with ID: {id}")
        target_team.update(data)
        return jsonify({"message": f"Sucessfully edited team with ID: {id}"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
def validate_team_data(data):
    required_fields = ['name', 'city']
    for field in required_fields:
        if field not in data:
            raise Exception("Ensure Team's name and city is provided!")
        
        if not data[field]:
            raise Exception("Ensure Team's name and city is value is correct!")

