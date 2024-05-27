[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/t1dqGhBU)
# MockStock
Created by
- Anthony Toloczko (Lead Developer)
- Joshua Hodges (Developer)
- Witten Joplin (Project Manager)
- Noah Clark (Developer)
- Nicholas Toloczko (Developer)


DEPLOYED URL: flask-uncw-mockstock.herokuapp.com

# Installation INSTRUCTIONS (Git Bash Windows)
NOTE: Ignore the parentheses when typing in the commands
- First go to the directory that you wish to copy to (cd 'your directory')
- ((ONLY DO THIS IF YOU DO NOT HAVE A CLONE ALREADY)) Clone the root (git clone 'root address on github')
- ((ONLY DO THIS IF YOU ALREADY HAVE A CLONE))Then you pull from our root (git pull 'root address on github')
- Then make your way into the directory of our root (cd 'csc450-sp23-project-team-2')
- Then go into the MockStock folder (cd 'MockStock')
- Now create the venv folder within it (python -m venv venv)
- Activate the venv folder (. venv/Scripts/activate)
- You'll be able to tell that it is activated by the (venv) appearing next to or above your command line
- install flask (pip install Flask)
- Now use the command (FLASK_APP=mockstock.py) to prep Flask to run the webpage
- Finally use the command (flask run) and the website should run
- You can test entering the URL that is given to see what the page looks like

# Installation INSTRUCTIONS (Git Bash Apple)
NOTE: Ignore the parentheses when typing in the commands
- First go to the directory that you wish to copy to (cd 'your directory')
- ((ONLY DO THIS IF YOU DO NOT HAVE A CLONE ALREADY)) Clone the root (git clone 'root address on github')
- ((ONLY DO THIS IF YOU ALREADY HAVE A CLONE))Then you pull from our root (git pull 'root address on github')
- Then make your way into the directory of our root (cd 'csc450-sp23-project-team-2')
- Then go into the MockStock folder (cd 'MockStock')
- Now create the venv folder within it (python3 -m venv venv)
- Activate the venv folder (. venv/bin/activate)
- You'll be able to tell that it is activated by the (venv) appearing next to or above your command line
- install flask (pip install Flask)
- Now use the command (FLASK_APP=mockstock.py) to prep Flask to run the webpage
- Finally use the command (flask run) and the website should run
- You can test entering the URL that is given to see what the page looks like

# Build Insructions
Technologies:
- Python (https://www.python.org/downloads/)
  - Python Install Guide (https://realpython.com/installing-python/)
- Application Configuration:
  - See the above installation instructions, they will help with setting up the Project
  Libraries:
  - pip install -r requirements.txt
- External Applications:
  - Selenium, follow the selenium guide below to set that up
  - Will add more about MySQL if we switch over, but at the moment we are using SQLite which has setup help below

# CONNECTIVITY WITH THE DATABASE:
First make sure you’ve activated your scripts (you’ll see the (venv) in your prompt window)
- (venv) $ flask db migrate – m “Example message here” (give a short but detailed description)

TO COMMIT CHANGES:
- (venv) $ flask db upgrade

BE CAREFUL: Flask databases are finicky, and there’s a strong chance you won’t be able to easily migrate if you alter any tables dramatically. The easiest workaround we’ve found is to delete the table and re-instate it. This next command will be your friend when working (and merging):
- (venv) $ flask db downgrade

This command undoes the most recent migration. 
The general idea is to try and make sure you (reasonably) have everything done that you need in a table before committing and merging it with the main branch. It’s much easier to downgrade and upgrade as needed that way – but the commands can still be utilized after merge.
ENSURE that the migrations folder in the project folder stays intact – this is where backups are contained.

TO ADD DATA TO THE DATABASE:
Ensure the relevant tables are included in the import section of MockStock.py (from app.models import User, Portfolio, Stock…etc)
- Open the python prompt (or place this within the code) and type commands along the following formats:
- x = User(email=example@gmail.com, profile_name = testuser, etc etc) (Fill in the relevant data)
- db.session.add(x)

The db.session.add line adds the user, or the object, to the database. To commit, you need another command:
- db.session.commit()

Be VERY careful about placement with the commit command. You don’t want to be committing frequently, and ill-considered placement of the commit could have potential disastrous consequences should any bugs arise. It’s extraordinarily recommended to only commit when necessary, so carefully consider when and where commit commands occur. 


# Component Responsibilities
- User Management - Noah Clark
- Trading System - Noah Clark
- Dashboard - Nicholas Toloczko
- Stock Visualization - Witten Joplin
- Search - Anthony Toloczko
- Database - Joshua Hodges

# Reccomended Selenium Setup
- Just merge wih main so that you can use my file and build off of the few example cases I put there (the timers are also for demonstration you can get rid of those if you want)

# Selenium Scratch Setup
NOTE: These were only tested in the python terminal in Pycharm
- First, create a new file outside of app (on the level of mockstock.py)
- Second, you will need to install flask testing (pip install Flask-Testing)
- You will also need to install Selenium (pip install selenium)
- Install the webdriver (pip install webdriver-manager)
- Then, you will then need to import your web driver which will depend on your preferred browser (this will change some of the functions depending on which one you use)
- Set up you imports so that they look like below
from flask_testing import TestCase
from flask import Flask
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager (This can be a different webdriver if you don't like edge, but I don't know how that will impact functionality)
from selenium.webdriver.common.by import By
import time
- After that you only need the basic code around your soon to be cases

class Tests(TestCase): (This can be named differently but)

	def create app
        ...
    
    def ...
        (test cases)
	
	def ...
        (test cases)

if __name__ == '__main__':
    unittest.main()


# Test Execution
- Start the webpage in Git so that the tests can access it
- Enter into the python terminal the name of your file (python <file name>) this will run all of the tests in the file