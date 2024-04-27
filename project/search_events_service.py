from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class EventSummary(BaseModel):
    """
    A summary representation of an event, including essential details.
    """

    id: str
    title: str
    description: str
    date: str
    location: str
    type: str


class SearchEventsResponse(BaseModel):
    """
    Responds with a list of events that match the search and filter criteria.
    """

    events: List[EventSummary]


async def search_events(
    keywords: str, date: str, location: str, type: str
) -> SearchEventsResponse:
    """
    Endpoint for users to search and filter events based on keywords, date, location, and event type.

    Args:
        keywords (str): Keywords to match in the event's title or description.
        date (str): The specific date or date range to filter events. Expected format: "YYYY-MM-DD".
        location (str): The location to filter events by.
        type (str): The type of event to filter by.

    Returns:
        SearchEventsResponse: Responds with a list of events that match the search and filter criteria.

    Example:
        result = await search_events(keywords="science", date="2023-01-31", location="New York", type="Conference")
        print(result)
    """
    query_filters = {
        "where": {
            "AND": [
                {
                    "description": {"contains": keywords},
                    "title": {"contains": keywords},
                },
                {"date": {"equals": date}},
                {"location": {"equals": location}},
            ]
        }
    }
    events = await prisma.models.Event.prisma().find_many(**query_filters)
    event_summaries = [
        EventSummary(
            id=event.id,
            title=event.title,
            description=event.description,
            date=event.date.strftime("%Y-%m-%d"),
            location=event.location,
            type="",
        )
        for event in events
    ]
    return SearchEventsResponse(events=event_summaries)
