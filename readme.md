# INEGI Census Project

This project is a desktop application built with Python and PyQt5 designed to manage and visualize census data, specifically focused on the region of Coahuila. It utilizes the Model-View-Controller (MVC) architectural pattern and interacts with a MySQL database using SQLAlchemy. The system includes an intelligent assistant module for querying data via natural language.

## Features

* **MVC Architecture:** Separation of concerns between the user interface (Vista), business logic (Controlador), and data structure (Modelo).
* **User Authentication:** Secure login interface for administrators.
* **Database Management:** Full integration with MySQL for storing census data including municipalities, locations, housing, and inhabitants.
* **Data Visualization:** Dashboard for viewing catalog and census information.
* **AI Assistant:** A chat interface that allows users to ask questions about the census data, processed asynchronously to maintain UI responsiveness.
* **ORM Integration:** Uses SQLAlchemy for efficient database interactions and schema management.
* **Styling:** Custom QSS stylesheet support for interface customization.

## Prerequisites

* Python 3.8 or higher
* MySQL Server
* Pip (Python Package Manager)

## Installation

1. **Clone the repository:**
Download the project files to your local machine.
2. **Install dependencies:**
Install the required Python libraries using pip.
```bash
pip install PyQt5 sqlalchemy mysql-connector-python

```


3. **Database Configuration:**
Ensure you have a MySQL server running. You must create a file named `constants.py` in the root directory of the project to store your connection strings.
Create `constants.py` and add the following variables:
```python
# constants.py

# Format: mysql+mysqlconnector://user:password@host:port/database_name
DB_CONNECTION_STRING = "mysql+mysqlconnector://root:password@localhost:3306/inegi_proyecto"

# Connection string for the assistant module (if different)
ASSISTANT_CONNECTION_STRING = "mysql+mysqlconnector://root:password@localhost:3306/inegi_proyecto"

```


4. **Database Initialization:**
The application is designed to create the necessary tables automatically upon the first run via SQLAlchemy's `create_all` method found in `main.py`.
To populate the database with initial testing data, you can run the seed script:
```bash
python seed.py

```


For massive data seeding, a separate utility is available:
```bash
python seed_massive.py

```



## Usage

To start the application, execute the `main.py` file from the terminal:

```bash
python main.py

```

### Application Flow

1. **Login:** Enter valid administrator credentials to access the system.
2. **Dashboard:** Navigate through the different modules (Catalog, Census, Reports).
3. **Assistant:** Use the "Asistente" tab to type natural language questions regarding the census data (e.g., "How many inhabitants are in Saltillo?").

## Project Structure

* **main.py:** The entry point of the application. Handles database connection validation and initializes the main Qt application loop.
* **constants.py:** (User created) Stores sensitive configuration and connection strings.
* **stylesheet.qss:** Contains the CSS-like styling for the PyQt5 widgets.
* **controlador/:** Contains the logic for the application (Admin, Assistant, Catalog, Census).
* **modelo/:** Contains SQLAlchemy class definitions representing the database tables (Base, Habitante, Vivienda, etc.).
* **vista/:** Contains the UI files (Login, Dashboard, Widgets).
* **dao/:** Data Access Objects for handling specific database queries.

## Troubleshooting

* **Import Errors:** If you encounter errors regarding module imports, ensure you are running the script from the root directory of the project.
* **Database Connection Failed:** Verify that your MySQL server is running and that the credentials in `constants.py` are correct. The application will print a critical error to the console if it cannot connect.
* **Missing Styles:** If `stylesheet.qss` is missing, the application will default to the standard system style without crashing.