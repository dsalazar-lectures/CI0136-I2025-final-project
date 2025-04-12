# Flask MVC Application

This is a minimal Flask web application that implements the MVC (Model-View-Controller) architecture pattern with the use of Blueprints.

## Setup Instructions

1. **Within ```.\CI0136-I2025-final-project``` directory, create a virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On Windows:

      ```bash
      venv\Scripts\activate
      ```

   - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

3. **Install the required dependencies:**

   ``` bash
   pip install -r requirements.txt
   ```

## Running the Application

### Open a terminal inside the `.\CI0136-I2025-final-project` folder

### You can run the server in debug mode with

``` bash
flask --app app run --debug
 * Serving Flask app 'hello'
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: nnn-nnn-nnn
```

> With the debug mode, the server will automatically reload your changes in the code.

If you trust the users in your network, you can tell your operating system to listen on all public IP by using:

``` bash
flask run --host=0.0.0.0
```

## Access the web app in your preferred browser

Type this URL:

> <http://127.0.0.1:5000>

## Usage

## Application Structure

- **Blueprints**: Blueprints are defined inside the `controllers` directory. Each blueprint encapsulates the routes, and handles interactions between logic and views. To interact with the modules from the controllers, and additional abstraction layer is added, called services, to keep the code organize and clean.

- **Registration**: Every blueprint must be registered in the `__init__.py` file of the `app` directory to be included in the application.
