# Task Manager Application

This project is a task manager application that allows users to create profiles, manage repositories, and perform various email operations. The application is structured to provide a user-friendly interface for managing tasks efficiently.

## Project Structure

```
task-manager
├── src
│   ├── main.py               # Entry point for the application
│   ├── menu.py               # Menu display and user input handling
│   ├── profile.py            # User profile management
│   ├── repository.py         # Repository operations
│   ├── email_operations.py    # Email-related operations
│   └── utils
│       ├── error_logging.py   # Error logging functionality
│       └── file_handler.py     # File operations for user data and logs
├── data
│   ├── user_data.json        # Stores user profile information
│   └── error_logs.txt        # Contains logs of errors encountered
├── requirements.txt          # Lists project dependencies
└── README.md                 # Project documentation
```

## Features

- **Profile Creation**: Users can create a profile with a random name or from a specified file.
- **Repository Management**: Users can start a repository and select multiple tasks related to email management.
- **Email Operations**: The application allows users to manage their inbox, report emails, add to the whitelist, delete emails, and read random emails.
- **Error Logging**: Errors are logged with detailed messages and screenshots for troubleshooting.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd task-manager
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage Guidelines

- Run the application by executing `main.py`:
   ```
   python src/main.py
   ```
- Follow the on-screen menu to select tasks and manage your profiles and repositories.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.