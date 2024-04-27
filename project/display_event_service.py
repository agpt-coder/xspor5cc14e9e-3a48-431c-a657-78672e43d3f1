from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class DisplayEventResponse(BaseModel):
    """
    Response model for displaying event details to attendees. Contains all necessary event information without exposing sensitive data.
    """

    title: str
    description: str
    date: datetime
    location: str
    organizerId: str
    createdAt: datetime
    updatedAt: datetime


async def display_event(id: str) -> DisplayEventResponse:
    """
    Endpoint to retrieve and display event details for attendees

    This function is responsible for fetching details of a specific event from the database based on its ID. It aims to provide attendees with essential information about the event, including its title, description, date, location, and organizer details. The function ensures that sensitive data is not exposed in the response, focusing instead on information relevant for attendees to know about the event.

    Args:
        id (str): The unique identifier for the event to be retrieved and displayed.

    Returns:
        DisplayEventResponse: An object containing the event's details formatted and ready for presentation to attendees.

    Example:
        await display_event('a1b2c3d4-5e6f-7g8h-9i0j-k11l12m13n14')
        > DisplayEventResponse(title='Community Coding Day', description='Join us for a day of coding, networking, and fun!', date=datetime.datetime(2023, 10, 15, 9, 0), location='Tech Hub Community Center', organizerId='abc123', createdAt=datetime.datetime(2023, 9, 1, 10, 30), updatedAt=datetime.datetime(2023, 9, 10, 12, 45))
    """
    event = await prisma.models.Event.prisma().find_unique(where={"id": id})
    if event is None:
        raise ValueError("Event not found")
    return DisplayEventResponse(
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location,
        organizerId=event.organizerId,
        createdAt=event.createdAt,
        updatedAt=event.updatedAt,
    )
