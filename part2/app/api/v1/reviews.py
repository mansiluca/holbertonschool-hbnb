from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request, jsonify

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        # Placeholder for the logic to register a new review
        data = request.get_json()
        try:
            new_review = facade.create_review(
                text=data['text'],
                rating=data['rating'],
                user_id=data['user_id'],
                place_id=data['place_id']
            )
            return {'message': 'Review created successfully', 'id': new_review.id}, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        reviews = facade.get_all_reviews()
        return {'reviews': [review.to_dict() for review in reviews]}, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        review_id = request.view_args['review_id']
        review = facade.get_review_by_id(review_id)
        if review:
            return review.to_dict(), 200
        else:
            return {'message': 'Review not found'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        data = request.get_json()
        review_id = request.view_args['review_id']
        try:
            updated_review = facade.update_review(
                review_id,
                text=data['text'],
                rating=data['rating'],
                user_id=data['user_id'],
                place_id=data['place_id']
            )
            return {'message': 'Review updated successfully', 'id': updated_review.id}, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        review_id = request.view_args['review_id']
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        else:
            return {'message': 'Review not found'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        place_id = request.view_args['place_id']
        reviews = facade.get_reviews_by_place_id(place_id)
        if reviews:
            return {'reviews': [review.to_dict() for review in reviews]}, 200
        else:
            return {'message': 'Place not found'}, 404