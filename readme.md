# Project Setup Guide

## Required Python version
Python 3.12

## Create Virtual Environment

Start by creating a virtual environment to isolate your project dependencies. Run the following command:

```bash
pipenv shell
```
This will create a virtual environment named `seat_booking`.

Once activated, your terminal prompt should indicate the active virtual environment.

## Install Dependencies

Install project dependencies specified in the `pipfile` file:

```bash
pipenv install --dev
```
This ensures that your project has all the necessary packages installed.

## Create database
Create a database named `seat_booking`.
```bash
psql -U username
create database seat_booking;
```
These commands will create the database in postgresql.

## Run Migrations

Apply database migrations to set up the initial database schema:

```bash
python manage.py migrate
```

This command will create the necessary tables and structures defined in your Django project.

## Run Django Server

Start the Django development server with the following command:

```bash
python manage.py runserver
```

The server will start, and you can access your Django application by navigating to `http://localhost:8000` in your web browser.


## Run Test codes

```bash
pytest -v
```