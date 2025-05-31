from flask import Blueprint, request
from app.utils import api_response, token_required
from app import db
from app.models.follow import Follow
from app.models.user import User
from app.controllers.user import user_bp
follow_bp = Blueprint('follow', __name__)

# UC11: Follow another user.
@user_bp.route('/<int:user_id>/follow', methods=['POST'])
@token_required
def follow_user(current_user, user_id):
    # Cannot follow self
    if current_user.id == user_id:
        return api_response(message="Cannot follow yourself", status=400)
    # Check target exists
    target_user = User.query.get(user_id)
    if not target_user:
        return api_response(message="User does not exist", status=404)
    # Check existing follow
    existing = Follow.query.filter_by(follower_id=current_user.id, following_id=user_id).first()
    if existing:
        return api_response(message="Already following this user", status=400)
    # Create follow relationship
    follow = Follow(follower_id=current_user.id, following_id=user_id)
    db.session.add(follow)
    db.session.commit()
    return api_response(message="Followed user successfully")

# UC12: Unfollow user
@user_bp.route('/<int:user_id>/follow', methods=['DELETE'])
@token_required
def unfollow_user(current_user, user_id):
    # Cannot unfollow self
    if current_user.id == user_id:
        return api_response(message="Cannot unfollow yourself", status=400)
  
    # Check target exists
    target_user = User.query.get(user_id)
    if not target_user:
        return api_response(message="User does not exist", status=404)
  
    # Check existing follow relationship
    existing = Follow.query.filter_by(follower_id=current_user.id, following_id=user_id).first()
    if not existing:
        return api_response(message="Have not followed this user", status=400)
  
    # Remove follow relationship
    try:
        db.session.delete(existing)
        db.session.commit()
        return api_response(message="Unfollowed user successfully")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error unfollowing user: {str(e)}", status=500)