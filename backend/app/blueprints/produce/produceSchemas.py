from backend.app.models import Produce
from backend.app.extensions import db, ma

class ProduceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Produce
        load_instance = True
        include_fk = True
        sqla_session = db.session

produce_schema = ProduceSchema()
produce_schemas = ProduceSchema(many=True)