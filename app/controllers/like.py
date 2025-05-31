from flask import Blueprint, request
from app.utils import api_response, token_required
from app import db
from app.models.like import Like
from app.models.post import Post
from app.controllers.post import post_bp
like_bp = Blueprint('like', __name__)


# UC14: Like post.
@post_bp.route('/<int:post_id>/like', methods=['POST'])
@token_required
def like_post(current_user, post_id):
    # Check target exists
    target_post = Post.query.get(post_id)
    if not target_post:
        return api_response(message="Post does not exist", status=404)
    # Check existing like
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing:
        return api_response(message="Already liked this post", status=400)
    # Create follow relationship
    like = Like(user_id=current_user.id, post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return api_response(message="Liked post successfully")

# UC15: Unlike post
@post_bp.route('/<int:post_id>/like', methods=['DELETE'])
@token_required
def unlike_post(current_user, post_id):
    # Check target exists
    target_post = Post.query.get(post_id)
    if not target_post:
        return api_response(message="Post does not exist", status=404)
  
    # Check existing like
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if not existing:
        return api_response(message="Have not liked this post", status=400)
  
    # Remove follow relationship
    try:
        db.session.delete(existing)
        db.session.commit()
        return api_response(message="Unliked post successfully")
    except Exception as e:
        db.session.rollback()
        return api_response(message=f"Error unliking post: {str(e)}", status=500)