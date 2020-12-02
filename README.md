## Project
Flask server used for the **Isoka Challenge** android application.  
Developpers:  
 - QUETIER Thomas  
 - RIBARDIÈRE Tom  
 - WALCAK Ladislas  

## Installation
 1. Create a venv `virtualenv -p python3.8 venv` and activate it
 2. Install dependencies `pip install -r requirements.txt`
 3. Create an .env file and store the the API key in API_KEY variable
 4. Initialise the database with `flask syncdb` 
 5. (Optionnal) Load test dataset `flask testmodel`
 6. Run the server !