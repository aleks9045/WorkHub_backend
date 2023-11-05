from datetime import datetime
from typing import Union, Any

# from app.schemas import TokenPayload, SystemUser
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import select




