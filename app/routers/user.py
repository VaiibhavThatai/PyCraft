# importing other files first
from .. import schemas, models, utils

from fastapi import status, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session

from fastapi import Depends, APIRouter

# from ..main import app
# NOT LIKE THIS
# We won't use app, we'll router
router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # execute the sqlalchemy command to create a new user

    # before creating the user we have to hash the password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())

    # add, commit and refresh
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# & GETTING USER BY PASSWORD
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' not found",
        )

    return user
