from backend.app.models import ShippingLabel
from backend.app.extensions import db, ma

class ShippingLabelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingLabel
        load_instance = True
        include_fk = True
        sqla_session = db.session

shippingLabel_schema = ShippingLabelSchema()
shippingLabel_schemas = ShippingLabelSchema(many=True)