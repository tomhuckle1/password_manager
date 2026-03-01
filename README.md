Production web app hosted on Render at: https://password-manager-3x2y.onrender.com/

# Local Setup Instructions

1. Extract the Project
Download and extract the project zip file to your machine.

------------------------------------------------------------

2. Open the Project in a Terminal

Navigate into the project directory.

Example:
cd password_manager

------------------------------------------------------------

3. Create a Virtual Environment

Create a Python virtual environment.

Windows:
python -m venv venv

Mac/Linux:
python3 -m venv venv

------------------------------------------------------------

4. Activate the Virtual Environment

Windows (PowerShell):
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

------------------------------------------------------------

5. Install Dependencies

Install all required Python packages.

pip install -r requirements.txt

------------------------------------------------------------

6. Create a .env File

Create a .env file in the project root directory.

Add the following variables:

SECRET_KEY=secret_key
ENCRYPTION_KEY=your_fernet_key_here

------------------------------------------------------------

7. Generate Encryption Key

Run the following Python command to generate a valid Fernet key:

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

Copy the output and paste it into the ENCRYPTION_KEY variable in the .env file.

------------------------------------------------------------

8. Run the Application

Start the Flask app:

python run.py

------------------------------------------------------------

9. Open the Application

Open your browser and navigate to:

http://127.0.0.1:5000

------------------------------------------------------------

10. Default Seeded Users

The application automatically seeds sample data when the database is empty.

Admin account:
Email: admin@example.com
Password: AdminPass123!

Regular user:
Email: user@example.com
Password: Password123!

10 passwords and 6 categories are seeded.

------------------------------------------------------------

Notes

- The application uses SQLite locally for development and Postegres for production
- The database file will be created automatically inside the instance/ folder.

------------------------------------------------------------

Running Tests

To run automated tests:

pytest -q

------------------------------------------------------------

Logging

Logging is set up for basic errors inside the instance/app.log file.

------------------------------------------------------------


Troubleshooting

If dependencies fail to install:

pip install --upgrade pip
pip install -r requirements.txt

If the virtual environment fails to activate, ensure Python is installed and available in your system PATH.