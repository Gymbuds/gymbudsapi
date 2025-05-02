from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.db.models.com_post import CommunityPost
from app.db.models.community import Community
from app.db.models.post_like import PostLike
from app.db.models.post_comment import PostComment
from app.schemas.post import CommunityPostCreate, CommunityPostUpdate, PostCommentCreate

def create_post(db: Session, user_id: int, post: CommunityPostCreate) -> CommunityPost:
    community = db.query(Community).filter(Community.id == post.community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    db_post = CommunityPost(
        user_id=user_id,
        community_id=post.community_id,
        title=post.title,
        content=post.content,
        image_url=post.image_url
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, user_id: int, post_id: int, post_update: CommunityPostUpdate) -> CommunityPost:
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.image_url is not None:
        post.image_url = post_update.image_url

    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, user_id: int, post_id: int) -> None:
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()

def get_posts_by_community(db: Session, community_id: int, user_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")

    posts = db.query(CommunityPost).options(
        joinedload(CommunityPost.post_likes),
        joinedload(CommunityPost.post_comments)
    ).filter(CommunityPost.community_id == community_id).all()

    # 🔁 Add computed fields so Pydantic doesn't break
    for post in posts:
        post.like_count = len(post.post_likes)
        post.comments = post.post_comments
        post.is_liked_by_current_user = any(like.user_id == user_id for like in post.post_likes) 

    return posts

def add_like_to_post(db: Session, user_id: int, post_id: int) -> None:
    post = db.query(CommunityPost).filter_by(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = db.query(PostLike).filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked this post")

    new_like = PostLike(user_id=user_id, post_id=post_id)
    db.add(new_like)
    db.commit()

def unlike_a_post(db: Session, user_id: int, post_id: int) -> None:
    like = db.query(PostLike).filter_by(user_id=user_id, post_id=post_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    db.commit()

def add_comment_to_post(db: Session, user_id: int, post_id: int, comment: PostCommentCreate) -> PostComment:
    post = db.query(CommunityPost).filter_by(id=post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = PostComment(
        user_id=user_id,
        post_id=post_id,
        content=comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def edit_a_comment(db:Session, comment_id:int, user_id:int, update_comment: PostCommentCreate) -> PostComment:
    comment = db.query(PostComment).filter_by(id=comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")

    comment.content = update_comment.content
    db.commit()
    db.refresh(comment)
    return comment

def delete_a_comment(db: Session, comment_id: int, user_id: int) -> None:
    comment = db.query(PostComment).filter_by(id=comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()
