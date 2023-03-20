# Typee Backend

Typee Backend is a FastAPI application that provides API endpoints for the Typee children's game frontend. The backend is responsible for handling the logic for word safety checks, generating explanations, stories, and facts for words, and managing images from Google Cloud Storage and data from Firebase.

## Deployment

The application is deployed to Google Cloud Run using Docker and is configured via a GitHub Actions CI/CD pipeline. The pipeline is triggered by a release with a git tag.


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