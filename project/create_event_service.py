from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CreateEventResponse(BaseModel):
    """
    Provides the details of the created event along with a confirmation message.
    """

    message: str
    event_id: str
    title: str
    date: datetime
    location: str


async def create_event(
    title: str, description: str, date: datetime, location: str
) -> CreateEventResponse:
    """
    Endpoint for organizers to create a new event.

    Args:
        title (str): The title of the event.
        description (str): A detailed description of the event.
        date (datetime): The scheduled date and time for the event.
        location (str): The physical or virtual location where the event will take place.

    Returns:
        CreateEventResponse: Provides the details of the created event along with a confirmation message.

    Example:
        response = await create_event("AI Conference", "A conference about AI innovations", datetime.now(), "Virtual")
        print(response.message)  # should print "Event successfully created."
    """
    current_organizer_id = "UUID-of-the-authenticated-organizer"
    new_event = await prisma.models.Event.prisma().create(
        data={
            "title": title,
            "description": description,
            "date": date,
            "location": location,
            "organizerId": current_organizer_id,
        }
    )
    return CreateEventResponse(
        message="Event successfully created.",
        event_id=new_event.id,
        title=new_event.title,
        date=new_event.date,
        location=new_event.location,
    )
