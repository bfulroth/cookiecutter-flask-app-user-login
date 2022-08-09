## Welcome

Building a flask app with user registration and logins? Awesome! This cookiecutter's goal is to take the work out of creating a postgres user database as well as writing your own user related operations such as registration, login, update, and delete. Django has this built in so let's fix this for flask apps!

<hr>

**What is Flask?** Flask is a microframework for Python based on Werkzeug and Jinja2.

Project Structure
--------
### Screenshots

![Structure]('{{cookiecutter.project_slug}}/{{cookiecutter.app_slug}}/screenshots/Screen Shot 2022-08-08 at 3.43.15 PM.png')

### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/bfulroth/flask-app-cookiecutter.git
  $ cd flask-app-cookiecutter
  ```

2. Initialize and activate a conda virtual env:
  ```
  $ conda create -n ENV_NAME
  $ conda activate ENV_NAME
  $ conda install pip
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Configure database url and app secret key stored as variables in .env.  Make sure NOT to commit your .env file to git! 
See example .env file below.

![example_env_file]('{{cookiecutter.project_slug}}/{{cookiecutter.app_slug}}/screenshots/Screen Shot 2022-08-08 at 3.43.15 PM.png')

5. Configure your local test database.
   - For postgres:
      - [PostgreSQL](https://www.postgresql.org/): The World's Most Advanced Open Source Relational Database.
      - Follow the tutorials: [installation](https://www.postgresqltutorial.com/install-postgresql/) and [connection](https://www.postgresqltutorial.com/connect-to-postgresql-database/)
      - Download the latest version of Postgres from [EDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads), which includes: PostgresSQL Server, pgAdmin 4, Stack Builder, Command Line Tools 
        - OR, Mac, Linux and WSL should use [Homebrew](https://wiki.postgresql.org/wiki/Homebrew) for installation.
        - OR, another Mac alternative is to download [Postgres App](https://postgresapp.com/)
          
      - Confirm success: 
        - For EDB, by opening SQL Shell (psql), and entering: `SELECT version();`
        - For homebrew, in terminal: `psql postgres`
        - For Postgres App, open application.
   - PSQL commands:
     - List all databases: `\l`
     - List all schemas: `\dn`
     - List all tables: `\dt`
     - List all users: `\du`
     - Connect: `\c`
     - Quit: `\q`
   
   - Setup the DB
      - Open psql in terminal: `psql postgres`
      - psql: `CREATE DATABASE {{cookiecutter.db_name_slug}};`
      - psql: `\c {{cookiecutter.db_name_slug}};`
      - create a test row:
        - Navigate to models/table-schema.sql. Copy and paste INSERT command into terminal running postgres.
      - Confirm in psql: `SELECT * FROM {{cookiecutter.db_name_slug}};`.
   

6. Run the development server:
  ```
  $ flask run
  ```

7. Navigate to [http://localhost:5000](http://localhost:5000)
   
8. Develop your app by adding your python modules and flask routes.

9. Note: when adding a new package add the dependency to requirements.txt.
    - `pip install pipreqs`
    - `pipreqs --force .`


Deploying to Heroku
------

10. Signup for [Heroku](https://api.heroku.com/signup)
11. Login to Heroku and download the [Heroku Toolbelt](https://toolbelt.heroku.com/)
12. Once installed, open your command-line and run the following command - `heroku login`. Then follow the prompts:

  ```
  Enter your Heroku credentials.
  Email: michael@mherman.org
  Password (typing will be hidden):
  Could not find an existing public key.
  Would you like to generate one? [Yn]
  Generating new SSH public key.
  Uploading ssh public key /Users/michaelherman/.ssh/id_rsa.pub
  ```

13. Heroku recognizes the dependencies needed through a *requirements.txt* file. Create one using the following command: `pip freeze > requirements.txt`. Now, this will only create the dependencies from the libraries you installed using pip. If you used easy_install, you will need to add them directly to the file.

14. Create your app on Heroku:

  ```
  $ heroku create <name_it_if_you_want>
  ```

15. Deploy your code to Heroku:

  ```
  $ git push heroku master
  ```

15. View the app in your browser:

  ```
  $ heroku open
  ```

16. Having problems? Look at the Heroku error log:

  ```
  $ heroku logs
  ```

### Learn More

1. [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/python)
1. [Flask Documentation](http://flask.pocoo.org/docs/)
2. [Flask Extensions](http://flask.pocoo.org/extensions/)

