from flask_restx import Api
from flask import Flask

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'  # Adaptez selon votre configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'votre-clé-secrète-jwt'  # À remplacer par une vraie clé secrète
    api = Api(app, version="1.0", title="HBnB API", description="HBnB Application API",
              security="Bearer", authorizations={
                  "Bearer": {
                      "type": "apiKey",
                      "in": "header",
                      "name": "Authorization"
                  }
              })
    db.init_app(app)


    # Register the users namespace
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.models import user, place, review, amenity, base
        db.create_all()
    return app

