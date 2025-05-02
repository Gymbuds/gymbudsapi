from fastapi import Depends,APIRouter, HTTPException
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.post import CommunityPostCreate,CommunityPostUpdate,CommunityPostResponse,PostCommentCreate,PostCommentResponse
from app.db.crud.com_post_crud import create_post,update_post,delete_post,get_posts_by_community,add_like_to_post,add_comment_to_post,unlike_a_post,edit_a_comment,delete_a_comment
from app.core.security import get_current_user 
from app.core.s3 import create_presigned_upload_url
from app.db.models.user import User
from typing import List
router=APIRouter()

@router.post("", response_model=CommunityPostResponse)
def create_community_post(
    post: CommunityPostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_post(db, current_user.id, post)

@router.patch("/{post_id}", response_model=CommunityPostResponse)
def update_community_post(
    post_id: int,
    post_update: CommunityPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_post(db, current_user.id, post_id, post_update)

@router.get("/generate-upload-url/")
def generate_community_post_upload_url(
    file_extension: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if file_extension not in ["jpeg", "jpg", "png", "mp4", "mov"]:
        raise HTTPException(status_code=400, detail="Invalid file extension")

    presigned_url, s3_file_url = create_presigned_upload_url(
        user_id=current_user.id,
        file_extension=file_extension,
        folder="community_posts"
    )

    return {
        "upload_url": presigned_url,  # Used by frontend to PUT the image
        "file_url": s3_file_url       # Final S3 URL to save into DB
    }

@router.delete("/{post_id}")
def delete_community_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_post(db, current_user.id, post_id)
    return {"success": "Post deleted"}

@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    add_like_to_post(db, current_user.id, post_id)
    return {"detail": "Post liked"}

@router.delete("/{post_id}/unlike")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unlike_a_post(db, current_user.id, post_id)
    return {"detail": "Post unliked"}

@router.post("/{post_id}/comment", response_model=PostCommentResponse)
def comment_post(
    post_id: int,
    comment: PostCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_comment_to_post(db, current_user.id, post_id, comment)

@router.put("/comments/{comment_id}", response_model=PostCommentResponse)
def edit_comment(
    comment_id: int,
    update_comment: PostCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return edit_a_comment(db, comment_id, current_user.id, update_comment)

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_a_comment(db, comment_id, current_user.id)
    return {"success": "Comment deleted"}

@router.get("/community/{community_id}", response_model=List[CommunityPostResponse])
def list_posts_for_community(community_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_posts_by_community(db, community_id, current_user.id)
