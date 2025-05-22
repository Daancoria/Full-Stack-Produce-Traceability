from backend.app.models import Contract
from backend.app.extensions import db, ma

class ContractSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contract
        load_instance = True
        include_fk = True
        sqla_session = db.session

contract_schema = ContractSchema()
contract_schemas = ContractSchema(many=True)