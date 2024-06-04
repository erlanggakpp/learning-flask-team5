from flask import Flask, jsonify
from db import teams, players
from controllers.teams import team_bp
from controllers.players import player_bp
from flasgger import Swagger

app = Flask(__name__)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/api-docs/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api-docs/"
}
swagger = Swagger(app, config=swagger_config)  # Initialize Flasgger

app.register_blueprint(team_bp, url_prefix='/teams')
app.register_blueprint(player_bp, url_prefix='/players')

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"



if __name__ == '__main__':
    app.run(debug=True, port=5000)