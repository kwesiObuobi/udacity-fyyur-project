Fyyur Project - Udacity Nanodegree Project
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

This was a half-completed Udacity project from their ALX-T Full Stack Web Developer Nanodegree. My job was to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

## Tasks Completed
* :white_check_mark: Connected the application to a local database
* :white_check_mark: Set up normalized  models for the objects supported in the web app models section of `app.py` 
* :white_check_mark: Implemeted missing model properties and relationships using database migrations via Flask-Migrate. <br/>
* :white_check_mark: Implemented form submissions for creating new Venues, Artists, and Shows. Proper constraints were set to duplicate or nonsensical form submissions. Ensured form submissions could create proper new records in the database. <br/>
* :white_check_mark: Implemented the controllers for listing venues, artists, and shows. <br/>
* :white_check_mark: Implemented search functionality, powering the `search` endpoints which serve the application's search functionalities. <br/>
* :white_check_mark: Served venue and artist details pages, powering the `<venue|artist>/<id>` endpoints which power the details pages.


## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```
> **Note** - If we do not mention the specific version of a package, then the default latest stable package will be installed. 

### 2. Frontend Dependencies
You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`
* Congiguration variables are separated from the application, and stored in `config.py`. This is where the connection to the database is set and stored.

Instructions
-----


#### Data Handling with `Flask-WTF` Forms
The project uses the [Flask-WTF](https://flask-wtf.readthedocs.io/) interactive form builder library which provides useful functionalities such as form validation and error handling. The form builders are located in `form.py`, with the WTForms being instantiated in the `app.py` file. To manage the request from Flask-WTF form, each field from the form has a `data` attribute containing the value from user input. For example, to handle the `venue_id` data from the Venue form, you can use: `show = Show(venue_id=form.venue_id.data)`, instead of using `request.form['venue_id']`.



## Development Setup
1. **Download the project starter code locally**
```
git clone https://github.com/kwesiObuobi/udacity-fyyur-project.git
```

2. **Setup the database**
With postgres running, enter your bash terminal and create a database:
```
psql -U postgres
create database myfyyurdb
```

3. **Initialize and activate a virtualenv using:**
```
py -m pip install --upgrade pip
py -m pip install --user virtualenv
py -m venv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
or
env\Scripts\activate
```

4. **Install the dependencies:**
```
pip install -r requirements.txt
```

>**Note** - You might need to change your python interpreter to match the one in your virtual environment:
In VSCode, Go to `View` tab, then `Command Palette`, then `Python: Select Interpreter`. Then you select the interpreter in your virtual environment.


5. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_DEBUG=true
export FLASK_ENV=development # enables debug mode
flask run --reload
```

6. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

