from flask import Blueprint, request
from app import db
from app.utils  import api_response, token_required
from app.models.post import Post
from app.models.follow import Follow

from app.controllers.user import user_bp 
from app.controllers.post import post_bp 


# UC13: View news feed
@post_bp.route('/newsfeed', methods=['GET'])
@token_required
def view_news_feed(current_user):
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Get posts from database with pagination
    current_user_id = current_user.id
    followed_records = Follow.query.filter_by(follower_id=current_user_id).all()
    followed_ids = [f.following_id for f in followed_records]
    followed_ids.append(current_user_id)

    posts = Post.query.filter(
        Post.user_id.in_(followed_ids), # Only retrieve posts of current user from the list
        Post.deleted == False # Still filter deleted posts
    ).order_by(Post.created_at.desc())\
     .paginate(page=page, per_page=per_page, error_out=False)

    # Prepare response data
    response_data = {
        'items': [post.to_dict() for post in posts.items],
        'pagination': {
            'page': posts.page,
            'per_page': posts.per_page,
            'total': posts.total,
        }
    }

    return api_response(data=response_data)
