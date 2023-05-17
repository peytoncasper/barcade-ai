from flask import Blueprint
from flask import Flask, jsonify, request

import db

# app_bp = Blueprint('game', __name__)




#
# @app_bp.route('/game/state', methods=['GET'])
# def get_game_state():
#     state = game.get_state()
#     return jsonify({'state': state})
#
# @app_bp.route('/agent/action', methods=['POST'])
# def trigger_agent_action():
#     data = request.json
#     observation = data['observation']
#
#     agent.observe(observation)
#     next_action = agent.get_next_action()
#
#     return jsonify(next_action)
#

# @app_bp.route('/game', methods=['GET'])
# def get_active_games():
#     games = db.get_active_games()
#     return jsonify({'games': games})
#
# @app_bp.route('/game/types', methods=['GET'])
# def get_game_types():
#     return jsonify({'types': ['towers_of_hanoi']})