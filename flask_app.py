from backend.app import create_app
from backend.app.models import db

app = create_app('DevelopmentConfig')  # Change to 'DevelopmentConfig' or 'TestingConfig' as needed


with app.app_context():
    #db.drop_all()  # Drop all tables if they exist
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)  