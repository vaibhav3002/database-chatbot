# Database Chatbot

## Overview

This repository contains Streamlit based python application for chatting with your database.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.8+
- [Poetry](https://python-poetry.org/)
- wget
- OpenAI API key

or you can use the Docker for containerized deployment in which case you do not need the above pre-requisites except the openai api key

## Installation

### Using Poetry (Recommended for Development)

1. Clone the repository:

   ```sh
   git clone https://github.com/vaibhav3002/database-chatbot.git
   cd database-chatbot
   ```

2. Install dependencies using Poetry:

    ```sh
   poetry install
   ```

3. Set up your environment variables:

   ```sh
   cp .env.example .env
   ```

   Edit the `.env` file and set your `OPENAI_API_KEY`.

### Using Docker (Recommended for Production)

1. Clone the repository:

   ```sh
   git clone https://github.com/vaibhav3002/database-chatbot.git
   cd database-chatbot
   ```

2. Build the Docker image:

   ```sh
   docker build -t myapp:latest .
   ```

## Running the Application

### Using Poetry

Activate the virtual environment and run the Streamlit app:

```sh
./scripts/download_northwind_database.sh
poetry shell
streamlit run src/app.py
```

### Using Docker

Run the Docker container, ensuring to pass the environment variables:

```sh
docker run --env-file .env -p 8501:8501 myapp:latest
```

The application will be accessible at `http://localhost:8501`.

## Architecture Overview

This application follows a modern, modular architecture:

- `src/app.py`: The main entry point for the Streamlit application.
- `tests/`: Comprehensive unit and integration tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Limitations

- Need to handle external openai rate limits

## Security - Risks to be mitigated

- Data corruption:  Only provide with read only database connection parameters on production database with access to only tables and columns authorized for the chatbot
- Performance risk:  Suggestion is not use the actual production database but a data lake where data from production has been copied so as avoid throtling the actual production database
- Access risk: Implement user authentication to not to expose the underlying data

## Next Steps

The possible enhancements to the solution can be as follows:

### Overall

- Instead of using ready-made langchain agent, break it down to individual module so that they can be modified
- If operating costs are not a primary concern, ideally able to use multiple LLMs to generate answer to validate cross consistency
- Column Selector - In case of large databases where column description will exceed the context length, we can first use RAG to select the tables and columns
- Add feature to display charts in the chatbot.
- Add feature to propse auto completeion of user prompts

### Machine Learning

- Decompose the user query into sub-queries to handle complex queries
- Generate synthetic data for evaluation from the selected database of northwind
- Evaluation pipeline

### Software Engineering

- Transform it into REST API so that it can be integrated with an external frontend with user authentication
- Feedback Loop - For every answer, we should gather feedback whether it was correct or not
- Use prompt manager instead of hardcoding the prompt
- Use LLM monitoring tool like langfuse
- Use Async Database for scalability
