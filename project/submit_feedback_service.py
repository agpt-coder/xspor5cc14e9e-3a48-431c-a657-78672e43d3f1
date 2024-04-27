from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Confirms the submission of feedback and provides the ID of the created feedback record.
    """

    success: bool
    feedbackId: str
    message: Optional[str] = None


async def submit_feedback(
    eventId: str, rating: int, content: str
) -> SubmitFeedbackResponse:
    """
    Endpoint for users to submit feedback on an event.

    Args:
        eventId (str): The ID of the event to which the feedback is being submitted.
        rating (int): The rating given by the user, on a predefined scale (e.g., 1-5).
        content (str): The textual content of the feedback provided by the user.

    Returns:
        SubmitFeedbackResponse: Confirms the submission of feedback and provides the ID of the created feedback record.

    Example:
        result = await submit_feedback("event123", 5, "Great event!")
        print(result)
        > SubmitFeedbackResponse(success=True, feedbackId="uuid-feedback-id", message="Feedback submitted successfully.")
    """
    try:
        feedback = await prisma.models.Feedback.prisma().create(
            data={
                "eventId": eventId,
                "rating": rating,
                "content": content,
                "userId": "default-user-id",
            }
        )
        return SubmitFeedbackResponse(
            success=True,
            feedbackId=feedback.id,
            message="Feedback submitted successfully.",
        )
    except Exception as e:
        return SubmitFeedbackResponse(success=False, feedbackId="", message=str(e))
