from flask import Flask, jsonify
from controllers.teams import team_bp
from controllers.players import player_bp
from flasgger import Swagger
from os import environ
from dotenv import load_dotenv

# Ini untuk load environment variables
load_dotenv()

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
    # cara menggunakan .env
    SECRET_KEY = environ.get('SECRET_KEY')
    API_KEY = environ.get('API_KEY')    
    return f"Hello! API_KEY: {API_KEY}. SECRET_KEY: {SECRET_KEY}"



if __name__ == '__main__':
    # Cara menggunakan
    # if environ.get('FLASK_ENV') == 'development':
    #     app.config['DEBUG'] = True
    # else:
    #     app.config['DEBUG'] = False
    app.run(debug=True)