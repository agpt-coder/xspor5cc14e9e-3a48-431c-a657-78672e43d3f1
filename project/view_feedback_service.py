from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class FeedbackData(BaseModel):
    """
    Structure representing a single piece of feedback, including content, rating, and any additional relevant metadata.
    """

    content: str
    rating: int
    submittedAt: str
    anonymous: bool


class FeedbackViewResponse(BaseModel):
    """
    Response model that contains the list of feedback for the requested event. This includes the feedback content, the rating, and metadata such as submission date and possibly user anonymized information if applicable.
    """

    feedbacks: List[FeedbackData]


async def view_feedback(eventId: str) -> FeedbackViewResponse:
    """
    Endpoint for users to view feedback on an event.

    This function retrieves feedbacks for a given eventId from the database,
    and formats them into a FeedbackViewResponse object, taking into account each feedback's anonymity setting.

    Args:
        eventId (str): The unique identifier of the event for which feedback is being requested.

    Returns:
        FeedbackViewResponse: Response model that contains the list of feedback for the requested event.
        This includes the feedback content, the rating, and metadata such as submission date and possibly user anonymized information if applicable.
    """
    feedback_records = await prisma.models.Feedback.prisma().find_many(
        where={"eventId": eventId}, include={"User": True}
    )
    feedbacks = [
        FeedbackData(
            content=record.content,
            rating=record.rating,
            submittedAt=record.createdAt.isoformat(),
            anonymous=record.User is None,
        )
        for record in feedback_records
    ]
    return FeedbackViewResponse(feedbacks=feedbacks)
