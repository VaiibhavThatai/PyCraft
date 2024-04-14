from .. import schemas, models, utils

from .. import oauth2
from fastapi import status, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, APIRouter

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    curr_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not curr_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {vote.post_id} not found",
        )
        
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if(vote.dir == 1):
        # if he has already liked the post and is trying to like again
        if found_vote:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"User {current_user.id} has already voted on the post with id {vote.post_id}")

        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully added vote"}

    else:
        # means user wants to delete vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = f"User {current_user.id} has already voted on the post with id {vote.post_id}")
        else:
            # delete_query = db.query(models.Vote).filter(models.Vote.id == vote.post_id, models.Vote.user_id == current_user.id)
            vote_query.delete(synchronize_session=False)
            db.commit()
            
        return {"Message": "Successfully deleted vote"}