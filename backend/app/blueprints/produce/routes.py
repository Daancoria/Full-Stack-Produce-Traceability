#CRUD for produce_bp 
from . import produce_bp
from .produceSchemas import produce_schema, produce_schemas
from backend.app.models import Produce, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, delete


#----------CREATE PRODUCE----------

@produce_bp.route('/', methods=['POST'])
def create_produce():
    try:
        new_produce = produce_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(new_produce)
    db.session.commit()
    return produce_schema.jsonify(new_produce), 201


#----------GET ALL PRODUCE----------

@produce_bp.route('/', methods=['GET'])
def get_produce():
    query = select(Produce)
    result = db.session.execute(query).scalars().all()
    return produce_schemas.jsonify(result), 200

#----------GET PRODUCE BY ID----------

@produce_bp.route('/<int:id>', methods=['GET'])
def get_produce_by_id(id):
    produce = db.session.get(Produce, id)
    if not produce:
        return jsonify({"error": "Produce not found"}), 404
    return produce_schema.jsonify(produce), 200

#----------UPDATE PRODUCE----------

@produce_bp.route('/<int:id>', methods=['PUT'])
def update_produce(id):
    query= select(Produce).where(Produce.id == id)
    produce= db.session.execute(query).scalars().first()

    if produce== None:
        return jsonify({"error": "Produce not found"}), 404
    try:
        updated_produce = produce_schema.load(request.json, instance=produce, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    db.session.commit()
    return produce_schema.jsonify(updated_produce), 200

#----------DELETE PRODUCE----------
@produce_bp.route('/<int:id>', methods=['DELETE'])
def delete_produce(id):
    query = select(Produce).where(Produce.id == id)
    produce = db.session.execute(query).scalars().first()

    db.session.delete(produce)
    db.session.commit()
    return jsonify({"message": "Produce deleted successfully"}), 200