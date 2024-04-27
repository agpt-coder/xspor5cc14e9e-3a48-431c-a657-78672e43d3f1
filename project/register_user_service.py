from typing import Optional

import prisma
import prisma.enums
import prisma.models
from bcrypt import gensalt, hashpw
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    A simple model to acknowledge the successful creation of a new user account. It may include an identifier of the newly created user or just a success message.
    """

    success: bool
    message: str
    userId: Optional[str] = None


async def register_user(email: str, password: str) -> RegisterUserResponse:
    """
    Endpoint for new users to create an account.

    Args:
        email (str): The email address for the new user account. It's crucial that this email is unique in the system to prevent duplicate accounts.
        password (str): The password for the new user account. It should be encrypted before being stored in the database for security reasons.

    Returns:
        RegisterUserResponse: A simple model to acknowledge the successful creation of a new user account. It may include an identifier of the newly created user or just a success message.
    """
    hashed_password = hashpw(password.encode("utf-8"), gensalt())
    try:
        existing_user = await prisma.models.User.prisma().find_unique(
            where={"email": email}
        )
        if existing_user is not None:
            return RegisterUserResponse(success=False, message="User already exists.")
        user = await prisma.models.User.prisma().create(
            data={
                "email": email,
                "password": hashed_password.decode("utf-8"),
                "role": prisma.enums.Role.LEARNER,
            }
        )
        return RegisterUserResponse(
            success=True, message="User successfully created.", userId=user.id
        )
    except Exception as e:
        return RegisterUserResponse(
            success=False, message=f"Failed to create user: {str(e)}"
        )
