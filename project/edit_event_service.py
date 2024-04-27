from datetime import datetime
from typing import Optional

import prisma
import prisma.errors
import prisma.models
from pydantic import BaseModel


class Event(BaseModel):
    """
    This type models the structure of an event stored in the database, reflecting the updated state after an edit operation.
    """

    id: str
    title: str
    description: str
    date: datetime
    location: str


class EditEventResponse(BaseModel):
    """
    This model provides feedback after an attempt to edit an event, indicating success or failure.
    """

    success: bool
    message: str
    edited_event: Optional[Event] = None


async def edit_event(
    id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    date: Optional[datetime] = None,
    location: Optional[str] = None,
) -> EditEventResponse:
    """
    Endpoint allowing organizers to edit an existing event.

    Args:
        id (str): The unique identifier for the event to be edited.
        title (Optional[str]): The new title for the event. Optional if not changing.
        description (Optional[str]): A new detailed description of the event. Optional if not changing.
        date (Optional[datetime]): The new date and time for the event. Optional if not changing.
        location (Optional[str]): The new location where the event will be held. Optional if not changing.

    Returns:
        EditEventResponse: This model provides feedback after an attempt to edit an event, indicating success or failure.
    """
    try:
        update_data = {}
        if title:
            update_data["title"] = title
        if description:
            update_data["description"] = description
        if date:
            update_data["date"] = date
        if location:
            update_data["location"] = location
        if not update_data:
            return EditEventResponse(
                success=False, message="No update information provided."
            )
        updated_event = await prisma.models.Event.prisma().update(
            where={"id": id}, data=update_data
        )
        edited_event = Event(
            id=updated_event.id,
            title=updated_event.title,
            description=updated_event.description,
            date=updated_event.date,
            location=updated_event.location,
        )
        return EditEventResponse(
            success=True,
            message="Event successfully updated",
            edited_event=edited_event,
        )
    except prisma.errors.PrismaError as e:
        return EditEventResponse(
            success=False,
            message=f"An error occurred while updating the event: {str(e)}",
        )
    except Exception as e:
        return EditEventResponse(
            success=False, message=f"An unexpected error occurred: {str(e)}"
        )
