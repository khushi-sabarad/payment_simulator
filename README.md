# Payment Gateway Simulator

This project is a simplified Payment Gateway Simulator built using Flask, SQLAlchemy, and cryptography. It provides a set of RESTful APIs to simulate payment authorization, capture, and refund processes.

## Features

* **Authorization:** Simulates the authorization of a payment transaction.
* **Capture:** Simulates the capture of an authorized transaction.
* **Refund:** Simulates the refund of a captured transaction.
* **Card Number Encryption:** Securely encrypts card numbers using Fernet cryptography.
* **Database Persistence:** Stores transaction data in a SQLite database.
* **API Testing:** Comprehensive test suite using PyTest to ensure API reliability.

## Technologies Used

* **Flask:** A lightweight web framework for building the API.
* **SQLAlchemy:** An SQL toolkit and ORM for database interaction.
* **Cryptography:** For secure card number encryption.
* **SQLite:** A lightweight, file-based database.
* **PyTest:** A testing framework for Python.
* **Postman:** Used for manual api testing.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [your-repository-url]
    cd payment_simulator
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate # On windows
    source venv/bin/activate # On linux or mac
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```
    The application will start running on `http://127.0.0.1:5000/`.

## API Endpoints

* **`POST /authorize`:**
    * Authorizes a payment transaction.
    * Request body:
        ```json
        {
            "card_number": "1234123412341234",
            "amount": 100
        }
        ```
    * Response:
        ```json
        {
            "status": "authorized" or "declined"
        }
        ```
* **`POST /capture`:**
    * Captures an authorized transaction.
    * Request body:
        ```json
        {
            "transaction_id": 1
        }
        ```
    * Response:
        ```json
        {
            "status": "captured"
        }
        ```
* **`POST /refund`:**
    * Refunds a captured transaction.
    * Request body:
        ```json
        {
            "transaction_id": 1
        }
        ```
    * Response:
        ```json
        {
            "status": "refunded"
        }
        ```

## Testing

* **Run the tests:**
    ```bash
    pytest
    ```
    This will execute the test suite in `test_app.py`.

## Database

* The application uses a SQLite database named `transactions.db` to store transaction data.
* The database schema includes the following columns:
    * `id`: Transaction ID (primary key).
    * `card_number_encrypted`: Encrypted card number.
    * `amount`: Transaction amount.
    * `status`: Transaction status (authorized, captured, refunded).
    * `timestamp`: Transaction timestamp.

## Security

* Card numbers are encrypted using Fernet cryptography to ensure secure storage.
* It is crucial to keep the encryption key secure in a real-world application.

## Postman

* Postman is used to manually test the API endpoints.
* Example Postman collections and environment files are not included in this repository.

## Notes

* This is a simplified payment gateway simulator for demonstration purposes.
* In a real-world payment gateway, you would need to implement more robust logic, including card validation, risk assessment, and integration with payment processors.
* The in memory database used by the tests ensures that the tests do not interact with the main transactions.db database.

## Future Improvements

* Implement card number validation.
* Add simulated risk scoring.
* Include more detailed error handling.
* Create a user interface for the simulator.
* Add more test cases.
* Create a better way to store the encryption key.

## Author

[Khushi Sabarad](https://www.linkedin.com/in/khushi-sabarad/)
