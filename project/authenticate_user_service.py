from typing import Optional

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    Response model for user authentication. On successful authentication, provides access token and basic user info.
    """

    status: str
    access_token: Optional[str] = None
    user_id: Optional[str] = None
    error: Optional[str] = None


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Endpoint for user login/authentication.

    This function authenticates a user based on their email and password. It checks if the user exists in the database,
    and if the password matches the one stored. If authentication is successful, it returns a response with a status
    indicating success, an access token, and the user's ID. If not, it returns a failure status with an error message.

    Args:
    email (str): The email address associated with the user's account.
    password (str): The password for the user's account. This should be securely handled and hashed as part of authentication logic.

    Returns:
    AuthenticateUserResponse: Response model for user authentication. On successful authentication, provides access token and basic user info.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user.password.encode("utf-8")
    ):
        return AuthenticateUserResponse(
            status="Failure", error="Invalid email or password"
        )
    access_token = "generated_access_token_stub"
    return AuthenticateUserResponse(
        status="Success", access_token=access_token, user_id=user.id
    )
