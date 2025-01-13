from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .strategies_service import StrategiesService
from ..config.responses import INVALID_INPUT_RESPONSE
from ..utils.is_data_full import is_data_full
from ..utils.is_data_have_one_of_the_attributes import is_data_have_one_of_the_attributes


strategy_bp = Blueprint("strategies", __name__)


@strategy_bp.route("/", methods=["POST"])
@jwt_required()
def create_strategy():
    data = request.json
    if not is_data_full(data, "name", "description", "asset_type", "buy_conditions", "sell_conditions", "status"):
        response, status = INVALID_INPUT_RESPONSE
        return jsonify(response), status
    user_id = int(get_jwt_identity())
    response, status = StrategiesService.create_strategy(data, user_id)
    return jsonify(response), status


@strategy_bp.route("/", methods=["GET"])
@jwt_required()
def get_strategies():
    user_id = int(get_jwt_identity())
    response, status = StrategiesService.get_strategies(user_id)
    return jsonify(response), status


@strategy_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_strategy(id):
    data = request.json
    if not is_data_have_one_of_the_attributes(
        data, "name", "description", "asset_type", "buy_conditions", "sell_conditions", "status"
    ):
        response, status = INVALID_INPUT_RESPONSE
        return jsonify(response), status
    user_id = int(get_jwt_identity())
    response, status = StrategiesService.update_strategy(id, data, user_id)
    return jsonify(response), status


@strategy_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_strategy(id):
    user_id = int(get_jwt_identity())
    response, status = StrategiesService.delete_strategy(id, user_id)
    return jsonify(response), status


@strategy_bp.route("/<int:strategy_id>/simulate", methods=["POST"])
@jwt_required()
def simulate_strategy(strategy_id):
    data = request.json
    if not is_data_full(data, "historical_data"):
        response, status = INVALID_INPUT_RESPONSE
        return jsonify(response), status
    user_id = int(get_jwt_identity())
    response, status = StrategiesService.simulate_strategy(strategy_id, data, user_id)
    return jsonify(response), status
