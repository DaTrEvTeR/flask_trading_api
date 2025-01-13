import json
from app.models import Strategy
from app.config.db import db
from app.config.redis import redis_client
from app.config.message_broker import channel
from app.config.responses import (
    STRATEGY_CREATED_RESPONSE,
    STRATEGY_UPDATED_RESPONSE,
    STRATEGY_DELETED_RESPONSE,
    FORBIDDEN_RESPONSE,
    STRATEGY_NOT_FOUND_RESPONSE,
)


class StrategiesService:
    @staticmethod
    def create_strategy(data, user_id):
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

        return STRATEGY_CREATED_RESPONSE

    @staticmethod
    def get_strategies(user_id):
        cached_strategies = redis_client.get(f"strategies_{user_id}")
        if cached_strategies:
            return json.loads(cached_strategies), 200

        strategies = Strategy.query.filter_by(user_id=user_id).all()
        strategies_list = [strategy.to_dict() for strategy in strategies]

        redis_client.setex(f"strategies_{user_id}", 3600, json.dumps(strategies_list))

        return strategies_list, 200

    @staticmethod
    def update_strategy(strategy_id, data, user_id):
        strategy = Strategy.query.get(strategy_id)
        if not strategy:
            return STRATEGY_NOT_FOUND_RESPONSE

        if strategy.user_id != user_id:
            return FORBIDDEN_RESPONSE

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

        redis_client.delete(f"strategies_{user_id}")

        message = f"User {user_id} updated strategy {strategy_id}"
        channel.basic_publish(exchange="", routing_key="strategy_queue", body=message)

        return STRATEGY_UPDATED_RESPONSE

    @staticmethod
    def delete_strategy(strategy_id, user_id):
        strategy = Strategy.query.get(strategy_id)
        if not strategy:
            return STRATEGY_NOT_FOUND_RESPONSE

        if strategy.user_id != user_id:
            return FORBIDDEN_RESPONSE

        db.session.delete(strategy)
        db.session.commit()

        redis_client.delete(f"strategies_{user_id}")

        return STRATEGY_DELETED_RESPONSE

    @staticmethod
    def simulate_strategy(strategy_id, data, user_id):
        strategy = Strategy.query.get(strategy_id)
        if not strategy or strategy.user_id != user_id:
            return FORBIDDEN_RESPONSE

        historical_data = data.get("historical_data", [])
        buy_threshold = strategy.buy_conditions["threshold"]
        sell_threshold = strategy.sell_conditions["threshold"]

        total_trades, profit_loss, wins, losses, max_drawdown, balance = 0, 0, 0, 0, 0, 0

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

        return {
            "strategy_id": strategy_id,
            "total_trades": total_trades,
            "profit_loss": profit_loss,
            "win_rate": win_rate,
            "max_drawdown": max_drawdown,
        }, 200
