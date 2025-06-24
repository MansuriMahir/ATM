# ATM Machine API

This project is a FastAPI application for managing ATM operations. It provides a set of API endpoints to interact with ATM functionalities such as account management and transaction processing.

## Project Structure

```
atm-machine-api/
├── src/
│   ├── main.py          # Entry point of the FastAPI application
│   ├── api/
│   │   └── routes.py    # API routes for ATM operations
│   ├── models/
│   │   └── account.py    # Data models for accounts
│   ├── services/
│   │   └── atm_service.py # Business logic for ATM operations
│   └── utils/
│       └── __init__.py   # Utility functions and constants
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd atm-machine-api
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn src.main:app --reload
   ```

## Usage

Once the application is running, you can access the API documentation at `http://127.0.0.1:8000/docs`. This will provide you with an interactive interface to test the available endpoints.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bugs.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.