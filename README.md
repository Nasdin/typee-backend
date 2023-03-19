# Typee Backend

Typee Backend is a FastAPI application that provides API endpoints for the Typee children's game frontend. The backend is responsible for handling the logic for word safety checks, generating explanations, stories, and facts for words, and managing images from Google Cloud Storage and data from Firebase.

## Deployment

The application is deployed to Google Cloud Run using Docker and is configured via a GitHub Actions CI/CD pipeline. The pipeline is triggered by a release with a git tag.

## Modules and Files

| Module/File                | Description                                                                                          |
|----------------------------|------------------------------------------------------------------------------------------------------|
| app/                       | Main application folder containing all the modules and files for the FastAPI application             |
| ├── __init__.py            | File containing app initialization, Firebase admin initialization, and router                       |
| ├── api.py                 | Main FastAPI application initialization                                                              |
| ├── api/                   | Folder containing FastAPI routers                                                                    |
| │   ├── __init__.py        | Empty __init__.py file for package initialization                                                   |
| │   ├── kid_word_encyclopedia.py | Router containing the API endpoint for kid_word_encyclopedia                                     |
| │   ├── safe_word.py       | Router containing the API endpoint for safe_word                                                     |
| ├── core/                  | Folder containing core configuration files                                                           |
| │   ├── __init__.py        | Empty __init__.py file for package initialization                                                   |
| ├── models/                | Folder containing Pydantic models used in the application                                            |
| │   ├── __init__.py        | Empty __init__.py file for package initialization                                                   |
| │   ├── word_data.py       | Pydantic model for word data                                                                         |
| ├── services/              | Folder containing service modules                                                                    |
| │   ├── __init__.py        | Empty __init__.py file for package initialization                                                   |
| │   ├── firebase.py        | Module containing the logic to interact with Google Firebase Firestore                               |
| │   ├── openai.py          | Module containing the logic to interact with OpenAI GPT-3 API                                        |
| │   ├── gcs.py             | Module containing the logic to interact with Google Cloud Storage                                    |
| │   ├── google_search.py   | Module containing the logic to interact with Google Search                                           |
| ├── tests/                 | Folder containing test files for the application                                                     |
| Dockerfile                 | Dockerfile to build the Docker image for the FastAPI application                                     |
| requirements.txt           | Python package requirements for the FastAPI application                                              |
| .github/                   | Folder containing GitHub configuration files                                                         |
| ├── workflows/             | Folder containing GitHub Actions workflows                                                           |
| │   ├── deploy.yml         | GitHub Actions CI/CD configuration for deploying the FastAPI application to Google Cloud Run          |

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