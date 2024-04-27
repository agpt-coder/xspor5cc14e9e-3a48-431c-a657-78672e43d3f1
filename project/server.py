import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import project.authenticate_user_service
import project.create_event_service
import project.delete_event_service
import project.display_event_service
import project.edit_event_service
import project.edit_profile_service
import project.register_user_service
import project.search_events_service
import project.submit_feedback_service
import project.view_feedback_service
import project.view_profile_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="xspor",
    lifespan=lifespan,
    description="In the PHP MVC application, the global entry point is `index.php`, which initializes the whole application. This initialization involves loading `composer/autoload.php` for class autoloading, necessary for utilizing PHP classes without manual includes. The application's routing mechanism is handled by `routes.php`, which directs URL paths to their respective controllers based on the request. For example, the path `/event/display` routes to `CfeatureEventDisplay.php`, a controller that fetches event data through `MfeatureEvent.php` model and renders it via `vfeature_event_display.php` view. Similarly, the path `/event/upload` is managed by `CfeatureEventUpload.php`, which processes form submissions from `vfeature_event_form.php` view through the same model, `MfeatureEvent.php`. This model performs its database operations using `DaoFeatureEvent.php` for direct database interactions, while `DtoFeatureEvent.php` is used for clean data transmission between the controllers and models. The frontend dynamics, such as DOM manipulations and AJAX requests, are handled by JavaScript files `event_display.js` for display functionality and `event_form.js` for form interactions. All these components are styled cohesively using `style.css` to ensure a uniform appearance across different views.",
)


@app.post(
    "/user/register", response_model=project.register_user_service.RegisterUserResponse
)
async def api_post_register_user(
    email: str, password: str
) -> project.register_user_service.RegisterUserResponse | Response:
    """
    Endpoint for new users to create an account
    """
    try:
        res = await project.register_user_service.register_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile/view",
    response_model=project.view_profile_service.UserProfileResponse,
)
async def api_get_view_profile(
    user_id: str,
) -> project.view_profile_service.UserProfileResponse | Response:
    """
    Endpoint for users to view their profile
    """
    try:
        res = await project.view_profile_service.view_profile(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/submit",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    eventId: str, rating: int, content: str
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Endpoint for users to submit feedback on an event
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            eventId, rating, content
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/event/create", response_model=project.create_event_service.CreateEventResponse
)
async def api_post_create_event(
    title: str, description: str, date: datetime, location: str
) -> project.create_event_service.CreateEventResponse | Response:
    """
    Endpoint for organizers to create a new event
    """
    try:
        res = await project.create_event_service.create_event(
            title, description, date, location
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/feedback/view/{eventId}",
    response_model=project.view_feedback_service.FeedbackViewResponse,
)
async def api_get_view_feedback(
    eventId: str,
) -> project.view_feedback_service.FeedbackViewResponse | Response:
    """
    Endpoint for users to view feedback on an event
    """
    try:
        res = await project.view_feedback_service.view_feedback(eventId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/event/delete/{id}",
    response_model=project.delete_event_service.DeleteEventResponse,
)
async def api_delete_delete_event(
    id: str,
) -> project.delete_event_service.DeleteEventResponse | Response:
    """
    Endpoint for organizers to delete an event
    """
    try:
        res = await project.delete_event_service.delete_event(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/event/edit/{id}", response_model=project.edit_event_service.EditEventResponse
)
async def api_put_edit_event(
    id: str,
    title: Optional[str],
    description: Optional[str],
    date: Optional[datetime],
    location: Optional[str],
) -> project.edit_event_service.EditEventResponse | Response:
    """
    Endpoint allowing organizers to edit an existing event
    """
    try:
        res = await project.edit_event_service.edit_event(
            id, title, description, date, location
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/search/events", response_model=project.search_events_service.SearchEventsResponse
)
async def api_get_search_events(
    keywords: str, date: str, location: str, type: str
) -> project.search_events_service.SearchEventsResponse | Response:
    """
    Endpoint for users to search and filter events
    """
    try:
        res = await project.search_events_service.search_events(
            keywords, date, location, type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/edit",
    response_model=project.edit_profile_service.EditUserProfileResponse,
)
async def api_put_edit_profile(
    email: str, name: str, bio: Optional[str], avatar_url: Optional[str]
) -> project.edit_profile_service.EditUserProfileResponse | Response:
    """
    Endpoint for users to edit their profile
    """
    try:
        res = await project.edit_profile_service.edit_profile(
            email, name, bio, avatar_url
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/authenticate",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Endpoint for user login/authentication
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/event/display/{id}",
    response_model=project.display_event_service.DisplayEventResponse,
)
async def api_get_display_event(
    id: str,
) -> project.display_event_service.DisplayEventResponse | Response:
    """
    Endpoint to retrieve and display event details for attendees
    """
    try:
        res = await project.display_event_service.display_event(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
