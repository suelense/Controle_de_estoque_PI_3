from flask import Blueprint, request, jsonify
from controleestoquev2 import db, Item

api_bp = Blueprint('api', __name__)

@api_bp.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify(items)

