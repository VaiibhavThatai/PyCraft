# importing other files first
from .. import schemas, models

from fastapi import FastAPI, Response, status, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from typing import List
from typing import Optional

from .. import oauth2

from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    search: Optional[str] = "",
    limit: int = 10,
    skip: int = 0,
):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)

    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    # LEFT INNER JOIN BY DEFAULT IN SQL ALCHEMY
    # results = db.query(models.Post).join(models.Vote, models.Vote.post_id == models.Post.id).all()

    # MAKING IT LEFT OUTER, WHICH IS WHAT WE WANT
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    #  you have to convert the mapping into a list to return it.
    results = list(map(lambda x: x._mapping, results))

    return results


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    # print(current_user.email)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/{id}", response_model=schemas.PostResponse)
@router.get("/{id}", response_model=schemas.PostOut)
def get_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    curr_post = db.query(models.Post).filter(models.Post.id == id).first()

    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} not found",
        )
    if result.Post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to perform this action",
        )

    return result


# & DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    delete_post_query = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id = {id} not found",
        )

    # check if owner is deleting his own post only
    if delete_post_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to perform this action",
        )

    # if exits lets delete
    delete_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# & UPDATE:
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    update_post_query = db.query(models.Post).filter(models.Post.id == id)

    if not update_post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )

    # check if his own post
    if update_post_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized to perform this action",
        )

    # If the post exists, we have to send all the new data
    update_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_post_query.first()
