from flask import Blueprint, request
from app import db
from app.utils  import api_response, token_required
from app.models.post import User

from app.controllers.user import user_bp 
from app.controllers.post import post_bp 

# UC16: Search Users by Username
@user_bp.route('/search', methods=['GET'])
@token_required
def search_users(current_user):
    username = request.args.get('username', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not username:
        return api_response(message="Username is required", status=400)

    users = User.query.filter(User.username.ilike(f'%{username}%'))\
                .paginate(page=page, per_page=per_page, error_out=False)

    if not users.items:
        return api_response(message="No users found", status=404)

    response_data = {
        'items' : [user.to_dict() for user in users.items],
        'pagination' : {
            'page' : users.page,
            'per_page' : users.per_page,
            'total' : users.total,
        }
    }

    return api_response(data=response_data, status=200)