# chatbot-pytorch

This is a chatbot which works with pytorch<br>
It also saves wrong answers with predicted category in a text file named as 'exceptions.txt'.

## Setup

1.  **Create and activate a virtual environment:**

    For Windows:

    ```shell
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

    For macOS/Linux:

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies:**

    With the virtual environment activated, install the required packages from `requirements.txt`:

    ```shell
    pip install -r requirements.txt
    ```

3.  **Download NLTK data:**

    After installation, you need to download the 'punkt' tokenizer from NLTK. Run this command in your terminal:

    ```shell
    python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
    ```

NOTE: This json dataset is taken from the internet, credits to the creator

## Core Elements of the Chatbot

intents.json
A list of intents which includes function calls and arguments

vacation_spots.json
A list of vacation spots with data around their activities, and weather.

chatbot.py
The main core of the application. Determines which reply to display, and which function to call if any. Keeps up with the current session state as well as a list of vacations pulled from vacation_spots.json.

vacation_functions.py
Functions to tailor output based on user selection and the current session_state
