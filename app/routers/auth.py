from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model = schemas.Token)
# def login(user_creds: schemas.UserLogin, db: Session = Depends(get_db)):
def login(
    user_creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # OAuth2 form returns username and password and not email as fields
    user = (
        db.query(models.User).filter(models.User.email == user_creds.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Now check the password
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # Return token
    return {"access_token": access_token, "token_type": "bearer"}
