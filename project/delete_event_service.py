import prisma
import prisma.models
from pydantic import BaseModel


class DeleteEventResponse(BaseModel):
    """
    Indicates whether the event deletion was successful.
    """

    success: bool
    message: str


async def delete_event(id: str) -> DeleteEventResponse:
    """
    Endpoint for organizers to delete an event.

    This function attempts to delete an event from the database using its unique identifier.
    It returns an object indicating whether the deletion was successful and includes a descriptive message.

    Args:
        id (str): The unique identifier of the event to be deleted.

    Returns:
        DeleteEventResponse: An object indicating the outcome of the deletion attempt.

    Example:
        response = await delete_event("73f8fa83-8543-4d8e-96c2-12345abcde")
        if response.success:
            print(f"Event deletion successful: {response.message}")
        else:
            print(f"Event deletion failed: {response.message}")
    """
    try:
        event = await prisma.models.Event.prisma().delete(where={"id": id})
        if event:
            return DeleteEventResponse(
                success=True, message="Event successfully deleted."
            )
        else:
            return DeleteEventResponse(
                success=False, message="No event found with the provided ID."
            )
    except Exception as e:
        return DeleteEventResponse(
            success=False, message=f"An error occurred: {str(e)}"
        )
