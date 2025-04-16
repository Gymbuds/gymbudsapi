from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models.com_post import CommunityPost
from app.db.models.community import Community
from app.schemas.post import CommunityPostCreate, CommunityPostUpdate

def create_post(db: Session, user_id: int, post: CommunityPostCreate) -> CommunityPost:
    community = db.query(Community).filter(Community.id == post.community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    db_post = CommunityPost(
        user_id=user_id,
        community_id=post.community_id,
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

def get_posts_by_community(db: Session, community_id: int):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return db.query(CommunityPost).filter(CommunityPost.community_id == community_id).all()