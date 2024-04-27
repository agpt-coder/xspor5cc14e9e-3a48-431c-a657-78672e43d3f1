---
date: 2024-04-27T19:29:24.814556
author: AutoGPT <info@agpt.co>
---

# xspor

In the PHP MVC application, the global entry point is `index.php`, which initializes the whole application. This initialization involves loading `composer/autoload.php` for class autoloading, necessary for utilizing PHP classes without manual includes. The application's routing mechanism is handled by `routes.php`, which directs URL paths to their respective controllers based on the request. For example, the path `/event/display` routes to `CfeatureEventDisplay.php`, a controller that fetches event data through `MfeatureEvent.php` model and renders it via `vfeature_event_display.php` view. Similarly, the path `/event/upload` is managed by `CfeatureEventUpload.php`, which processes form submissions from `vfeature_event_form.php` view through the same model, `MfeatureEvent.php`. This model performs its database operations using `DaoFeatureEvent.php` for direct database interactions, while `DtoFeatureEvent.php` is used for clean data transmission between the controllers and models. The frontend dynamics, such as DOM manipulations and AJAX requests, are handled by JavaScript files `event_display.js` for display functionality and `event_form.js` for form interactions. All these components are styled cohesively using `style.css` to ensure a uniform appearance across different views.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'xspor'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
