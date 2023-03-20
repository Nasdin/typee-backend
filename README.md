# Typee Backend

Typee Backend is a FastAPI application that provides API endpoints for the Typee children's game frontend. The backend is responsible for handling the logic for word safety checks, generating explanations, stories, and facts for words, and managing images from Google Cloud Storage and data from Firebase.

## Deployment

The application is deployed to Google Cloud Run using Docker and is configured via a GitHub Actions CI/CD pipeline. The pipeline is triggered by a release with a git tag.

## Files and modules

Module/File	Purpose
Dockerfile	Defines the Docker container for the application.
LICENSE	Contains the terms and conditions of the software license for the project.
README.md	Provides documentation, instructions, and an overview of the project.
app/init.py	Initializes the Python package for the application.
app/api.py	Sets up the FastAPI application and includes the routers.
app/controllers	Contains the controllers that handle business logic.
app/controllers/gallery.py	Implements the logic related to the gallery functionality.
app/controllers/kid_word_encyclopedia.py	Implements the logic related to the kid word encyclopedia functionality.
app/controllers/safe_word.py	Implements the logic related to checking if a word is safe.
app/core/init.py	Initializes the Python package for the core components of the application.
app/core/config.py	Contains the application configuration settings.
app/models/init.py	Initializes the Python package for the data models.
app/models/word_data.py	Defines the WordData and WordInfo models for the application.
app/routers/init.py	Initializes the Python package for the routers.
app/routers/gallery_words.py	Implements the API routes for the gallery functionality.
app/routers/words.py	Implements the API routes for the safe words and kid word encyclopedia functionality.
app/services/init.py	Initializes the Python package for the services.
app/services/firebase.py	Implements the Firestore and Firebase authentication services.
app/services/google_search.py	Implements the service for Google search.
app/services/openai.py	Implements the service for the OpenAI GPT-4 API.
cloudbuild.yml	Contains the Google Cloud Build configuration for the project.
nginx.conf	Contains the configuration for the Nginx web server used in the Docker container.
requirements.txt	Lists the Python dependencies required for the project.
tests/init.py	Initializes the Python package for the tests.
tests/test_routers.py	Contains the test cases for the API routes.
tests/test_services	Contains the test cases for the various services.
tests/test_services/init.py	Initializes the Python package for the test_services.
tests/test_services/test_firebase.py	Contains test cases for the firebase service.
tests/test_services/test_google_search.py	Contains test cases for the google_search service.
tests/test_services/test_openai.py	Contains test cases for the openai service.
This table provides an overview of the project's structure and the purpose of each module/file.

## Getting Started

To start contributing to the Typee Backend, follow these steps:

1. Clone the repository:

git clone https://github.com/nasdin/typee-backend.git
cd typee-backend


2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate


3. Install the required dependencies:

pip install -r requirements.txt


4. Set up environment variables:
- Copy the `.env.example` file to `.env` and fill in the required values for each variable, such as your Firebase and OpenAI API keys, as well as your Google Cloud Storage bucket name and other required information.

5. Run the FastAPI application locally:

uvicorn app.api:app --reload


6. Access the FastAPI application:
The application should now be running at http://localhost:8000. You can also view the API documentation at http://localhost:8000/docs.

7. Run tests (optional):
To run the tests for the application, execute the following command:

pytest

## Contributing
After setting up the project locally, you can start making changes and improvements to the code. Create a new branch for each feature or bug fix, and then submit a pull request when your changes are ready for review.

Remember to follow best practices for Python and FastAPI development, and ensure that your code is well-documented and tested.

Happy coding!