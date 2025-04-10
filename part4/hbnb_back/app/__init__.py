from flask_restx import Api
from flask import Flask

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_class="config.DevelopmentConfig"):
    # Créer l'objet Flask d'abord
    app = Flask(__name__)
    
    # Puis configurer l'application
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config_class)
    
    # Créer l'API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API',
              security='Bearer Auth', authorizations={
                  'Bearer Auth': {
                      'type': 'apiKey',
                      'in': 'header',
                      'name': 'Authorization',
                      'description': "Jwt authorization header"
                  }
              })
    
    from flask_cors import CORS

    CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials":True}})
    
    @app.route('/api/v1/auth/login', methods=['OPTIONS'])
    def options():
        """Handle CORS preflight request for login endpoint."""
        return '', 200
    
    @app.route('/api/v1/places', methods=['OPTIONS'])
    def handle_options():
        return '', 200
    
    @app.route('/api/v1/places/<place_id>', methods=['OPTIONS'])
    def handle_options_place(place_id):
        return '', 200
    
    @app.route('/api/v1/places/<place_id>/reviews', methods=['OPTIONS'])
    def handle_options_reviews_get(place_id):
        return '', 200
    
    @app.route('/api/v1/reviews', methods=['OPTIONS'])
    def handle_options_reviews_post():
        return '', 200

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)   
    
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # Créer les tables
    with app.app_context():
        db.create_all()
        
    return app