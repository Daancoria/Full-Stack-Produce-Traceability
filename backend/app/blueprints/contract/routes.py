#CRUD for Contracts

from . import contracts_bp
from .contractSchemas import contract_schema, contract_schemas
from backend.app.models import Contract, db
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, delete

#----------CREATE CONTRACT----------
@contracts_bp.route('/', methods=['POST'])
def create_contract():
    try:
        new_contract = contract_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.add(new_contract)
    db.session.commit()
    return contract_schema.jsonify(new_contract), 201

#----------Get All Contracts------
@contracts_bp.route('/', methods=['GET'])
def get_contracts():
    query = select(Contract)
    result = db.session.execute(query).scalars().all()
    return contract_schemas.jsonify(result), 200
    

#----------GET CONTRACT BY ID----------
@contracts_bp.route('/<int:id>', methods=['GET'])
def get_contract_by_id(id):
    contract = db.session.get(Contract, id)
    if not contract:
        return jsonify({"error": "Contract not found"}), 404
    return contract_schema.jsonify(contract), 200




#----------UPDATE CONTRACT----------
@contracts_bp.route('/<int:id>', methods=['PUT'])
def update_contract(id):
    query= select(Contract).where(Contract.id == id)
    contract= db.session.execute(query).scalars().first()
    if contract== None:
        return jsonify({"error": "Contract not found"}), 404
    try:
        updated_contract = contract_schema.load(request.json, instance=contract, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    db.session.commit()
    return contract_schema.jsonify(updated_contract), 200
    

#----------DELETE CONTRACT----------

@contracts_bp.route('/<int:id>', methods=['DELETE'])
def delete_contract(id):
    query = select(Contract).where(Contract.id == id)
    contract = db.session.execute(query).scalars().first()
    if not contract:
        return jsonify({"error": "Contract not found"}), 404
    
    db.session.delete(contract)
    db.session.commit()
    return jsonify({"message": "Contract deleted successfully"}), 200
