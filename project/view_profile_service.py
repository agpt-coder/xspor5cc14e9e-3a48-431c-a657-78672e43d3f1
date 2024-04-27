import prisma
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Represents a concise summary of the user's profile, including essential details but omitting sensitive information like passwords.
    """

    id: str
    email: str
    role: str
    createdAt: str
    updatedAt: str


async def view_profile(user_id: str) -> UserProfileResponse:
    """
    Endpoint for users to view their profile

    Args:
    user_id (str): Identifier for the user whose profile is being accessed. This is usually extracted from the user's authentication token.

    Returns:
    UserProfileResponse: Represents a concise summary of the user's profile, including essential details but omitting sensitive information like passwords.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if user:
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            role=user.role.name,
            createdAt=user.createdAt.isoformat(),
            updatedAt=user.updatedAt.isoformat(),
        )
    raise Exception("User not found")
