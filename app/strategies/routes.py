import json

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..config.message_broker import channel
from ..config.redis import redis_client
from ..config.db import db
from ..models import Strategy


strategy_bp = Blueprint("strategies", __name__)


@strategy_bp.route("/", methods=["POST"])
@jwt_required()
def create_strategy():
    """
    Creates a new strategy for the authenticated user.

    **Method:** `POST`

    **Request Body:**
    json
    {
      "name": str,
      "description": str,
      "asset_type": str,
      "buy_conditions": dict[str, any],
      "sell_conditions": dict[str, any],
      "status": str
    }

    **Response:**
    - `201 Created`
    json
    {
      "message": "Strategy created successfully"
    }
    """
    data = request.json
    user_id = int(get_jwt_identity())
    new_strategy = Strategy(
        name=data["name"],
        description=data["description"],
        asset_type=data["asset_type"],
        user_id=user_id,
        buy_conditions=data["buy_conditions"],
        sell_conditions=data["sell_conditions"],
        status=data["status"],
    )
    db.session.add(new_strategy)
    db.session.commit()
    db.session.refresh(new_strategy)
    redis_client.delete(f"strategies_{user_id}")
    message = f"User {user_id} created strategy {new_strategy.id}"
    channel.basic_publish(exchange="", routing_key="strategy_queue", body=message)
    return jsonify({"message": "Strategy created successfully"}), 201


@strategy_bp.route("/", methods=["GET"])
@jwt_required()
def get_strategies():
    """
    Retrieves all strategies for the authenticated user, using a cache if available.

    **Method:** `GET`

    **Response:**
    - `200 OK`
    json
    [
        {
            "id": int,
            "name": str,
            "description": str,
            "asset_type": str,
            "buy_conditions": dict[str, any],
            "sell_conditions": dict[str, any],
            "status": str,
        }
    ]
    """
    user_id = int(get_jwt_identity())
    cached_strategies: str | None = redis_client.get(f"strategies_{user_id}")
    if cached_strategies:
        return jsonify(json.loads(cached_strategies))
    strategies: list[Strategy] = Strategy.query.filter_by(user_id=user_id).all()
    strategies_list = [strategy.to_dict() for strategy in strategies]
    redis_client.setex(f"strategies_{user_id}", 3600, json.dumps(strategies_list))
    return jsonify(strategies_list)


@strategy_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_strategy(id):
    """
    Updates a specific strategy by ID for the authenticated user.

    **Method:** `PATCH`

    **Request Body:**
    json
    {
      "name": Optional[str],
      "description": Optional[str],
      "asset_type": Optional[str],
      "buy_conditions": Optional[dict[str, any]],
      "sell_conditions": Optional[dict[str, any]],
      "status": Optional[str]
    }

    **Response:**
    - `200 OK`
    json
    {
      "message": "Strategy updated successfully"
    }
    """
    data: dict = request.json
    strategy = Strategy.query.get_or_404(id)
    user_id_from_jwt = int(get_jwt_identity())
    if strategy.user_id != user_id_from_jwt:
        return jsonify({"message": "Forbidden"}), 403

    if data.get("name"):
        strategy.name = data["name"]
    if data.get("description"):
        strategy.description = data["description"]
    if data.get("asset_type"):
        strategy.asset_type = data["asset_type"]
    if data.get("buy_conditions"):
        strategy.buy_conditions = data["buy_conditions"]
    if data.get("sell_conditions"):
        strategy.sell_conditions = data["sell_conditions"]
    if data.get("status"):
        strategy.status = data["status"]

    db.session.commit()
    redis_client.delete(f"strategies_{strategy.user_id}")
    message = f"User {strategy.user_id} updated strategy {strategy.id}"
    channel.basic_publish(exchange="", routing_key="strategy_queue", body=message)
    return jsonify({"message": "Strategy updated successfully"})


@strategy_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_strategy(id):
    """
    Deletes a strategy for the authenticated user.

    **Method:** `DELETE`

    **Response:**
    - `200 OK`
    json
    {
      "message": "Strategy deleted successfully"
    }
    """
    strategy = Strategy.query.get_or_404(id)
    user_id_from_jwt = int(get_jwt_identity())
    if strategy.user_id != user_id_from_jwt:
        return jsonify({"message": "Unauthorized"}), 403
    db.session.delete(strategy)
    db.session.commit()
    redis_client.delete(f"strategies_{strategy.user_id}")
    return jsonify({"message": "Strategy deleted successfully"})


@strategy_bp.route("/<int:id>/simulate", methods=["POST"])
@jwt_required()
def simulate_strategy(id):
    """
    Simulates a strategy using historical market data.

    **Method:** `POST`

    **Request Body:**
    json
    {
      "historical_data": [
            {
                "date": "2024-06-01",
                "open": 100.5,
                "close": 102.3,
                "high": 103.0,
                "low": 99.8,
                "volume": 150000
            },
            {
                "date": "2024-06-02",
                "open": 102.3,
                "close": 104.7,
                "high": 105.5,
                "low": 101.2,
                "volume": 180000
            },
        ]
    }

    **Response:**
    - `200 OK`
    json
    {
      "strategy_id": 1,
      "total_trades": 2,
      "profit_loss": 5,
      "win_rate": 50,
      "max_drawdown": -10
    }
    """
    strategy = Strategy.query.get_or_404(id)
    if strategy.user_id != int(get_jwt_identity()):
        return jsonify({"message": "Unauthorized"}), 403

    historical_data = request.json.get("historical_data", [])
    buy_threshold = strategy.buy_conditions["threshold"]
    sell_threshold = strategy.sell_conditions["threshold"]

    total_trades = 0
    profit_loss = 0
    wins = 0
    losses = 0
    max_drawdown = 0
    balance = 0

    for event in historical_data:
        momentum = event["close"] - event["open"]
        if momentum > buy_threshold:
            balance -= event["close"]
            total_trades += 1
        elif momentum < sell_threshold:
            profit_loss += event["close"] - balance
            total_trades += 1
            if event["close"] - balance > 0:
                wins += 1
            else:
                losses += 1
            max_drawdown = min(max_drawdown, event["close"] - balance)
            balance = 0

    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

    return jsonify(
        {
            "strategy_id": id,
            "total_trades": total_trades,
            "profit_loss": profit_loss,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
        }
    )
