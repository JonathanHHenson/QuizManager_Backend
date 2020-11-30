# Quiz Manager Backend

## Setup
### Python dependencies
- flask
- sqlalchemy
- flask_sqlalchemy
- marshmallow_sqlalchemy
- timeloop

### Building the Frontend
1. Clone the QuizManager_Frontend Repository
2. Follow the setup instructions for the Frontend
3. Create a static directory
4. Run `npm run build` inside the Frontend project
5. Copy the files in `frontend/build` to `backend/static`

### Setting up the Database
1. Setup a MySQL server
2. Ensure that the server is setup with SSL support (required for encryption)
3. Execute `schema.sql` to setup the database
4. Edit `database.cfg` to match the server settings for your MySql server

### Importing Users From CSV
1. Clone the QuizManager_ImportPasswords Repository
2. Follow the setup instructions
3. (optional) Edit `users.csv` to prepare users for import
4. Execute the `import_passwords.py` script

# Running the project
Once everything has been setup, execute the command: `python -m flask run`
