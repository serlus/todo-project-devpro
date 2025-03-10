from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session

from todo.db import ActiveSession
from todo.models import User, UserDetailResponse, UserRequest, UserResponse, get_user

router = APIRouter()


@router.get('/', response_model=list[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = get_user()
    return users


@router.get('/{user_name}/', response_model=UserDetailResponse)
async def get_usert_by_user_name(*, user_name: str, session: Session = ActiveSession):
    """Get user by user_name"""
    user = get_user(user_name=user_name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    return user


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(*, user: UserRequest, session: Session = ActiveSession):
    """Creates new user"""
    # TODO: Validar informações recebidas com as constraints do banco.
    db_user = User.from_orm(user)  # Transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
