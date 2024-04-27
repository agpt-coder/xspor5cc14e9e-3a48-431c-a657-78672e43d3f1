from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class User(BaseModel):
    """
    User object model representing the updated profile.
    """

    id: str
    email: str
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class EditUserProfileResponse(BaseModel):
    """
    Model for the response after a user edits their profile. It could represent a success status or the updated user profile data.
    """

    status: str
    message: Optional[str] = None
    updated_user: Optional[User] = None


async def edit_profile(
    email: str, name: str, bio: Optional[str] = None, avatar_url: Optional[str] = None
) -> EditUserProfileResponse:
    """
    Endpoint for users to edit their profile.

    Args:
        email (str): The new email address for the user's account.
        name (str): The user's full name after update.
        bio (Optional[str]): A short biography or description about the user.
        avatar_url (Optional[str]): URL link to the new avatar image for the user's profile.

    Returns:
        EditUserProfileResponse: Model for the response after a user edits their profile.
        It could represent a success status or the updated user profile data.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"email": email})
        if user:
            updated_user_data = await prisma.models.User.prisma().update(
                where={"email": email},
                data={
                    "email": email,
                    "name": name,
                    "bio": bio,
                    "avatarUrl": avatar_url,
                },
            )
            updated_user = User(
                id=updated_user_data.id,
                email=updated_user_data.email,
                name=updated_user_data.name,
                bio=updated_user_data.bio,
                avatar_url=updated_user_data.avatar_url,
            )  # TODO(autogpt): Cannot access attribute "name" for class "User"
            #     Attribute "name" is unknown. reportAttributeAccessIssue
            return EditUserProfileResponse(
                status="success",
                message="User profile updated successfully.",
                updated_user=updated_user,
            )
        else:
            return EditUserProfileResponse(status="error", message="User not found.")
    except Exception as e:
        return EditUserProfileResponse(
            status="error", message=f"An error occurred: {str(e)}"
        )
