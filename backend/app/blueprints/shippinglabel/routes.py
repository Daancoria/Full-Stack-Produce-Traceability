#CRUD FOR SHIPPING LABELS

from . import shippinglabel_bp
from .shippingSchemas import shippingLabel_schema, shippingLabel_schemas
from backend.app.models import ShippingLabel, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, delete

#----------CREATE SHIPPING LABEL----------
@shippinglabel_bp.route('/', methods=['POST'])
def create_shipping_label():
    try:
        new_shipping_label = shippingLabel_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(new_shipping_label)
    db.session.commit()
    return shippingLabel_schema.jsonify(new_shipping_label), 201

#----------Get All Shipping Labels------
@shippinglabel_bp.route('/', methods=['GET'])
def get_shipping_labels():
    query = select(ShippingLabel)
    result = db.session.execute(query).scalars().all()
    return shippingLabel_schemas.jsonify(result), 200

#----------GET SHIPPING LABEL BY ID----------
@shippinglabel_bp.route('/<int:id>', methods=['GET'])
def get_shipping_label_by_id(id):
    shipping_label = db.session.get(ShippingLabel, id)
    if not shipping_label:
        return jsonify({"error": "Shipping label not found"}), 404
    return shippingLabel_schema.jsonify(shipping_label), 200

#----------UPDATE SHIPPING LABEL----------
@shippinglabel_bp.route('/<int:id>', methods=['PUT'])
def update_shipping_label(id):
    query = select(ShippingLabel).where(ShippingLabel.id == id)
    shipping_label = db.session.execute(query).scalars().first()
    if shipping_label is None:
        return jsonify({"error": "Shipping label not found"}), 404
    try:
        updated_shipping_label = shippingLabel_schema.load(request.json, instance=shipping_label, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.commit()
    return shippingLabel_schema.jsonify(updated_shipping_label), 200

#----------DELETE SHIPPING LABEL----------
@shippinglabel_bp.route('/<int:id>', methods=['DELETE'])
def delete_shipping_label(id):
    query = select(ShippingLabel).where(ShippingLabel.id == id)
    shipping_label = db.session.execute(query).scalars().first()
    if shipping_label is None:
        return jsonify({"error": "Shipping label not found"}), 404
    db.session.delete(shipping_label)
    db.session.commit()
    return jsonify({"message": "Shipping label deleted successfully"}), 200

