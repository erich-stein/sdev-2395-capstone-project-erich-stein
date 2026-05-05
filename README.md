# Recipe Book App

### SDEV-2395 Capstone Project By Erich Stein

An attempt at a full-stack web application for creating, storing, viewing, and editing recipes. Built with Flask, Vue.js, and MariaDB.

Not ready for deployment.

# Requirements

- Python 3.12
- Node.js 22.19
- MariaDB 10.11

# Backend

## Setup

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create .env file in base directory (same as config.py) and set 'user' and 'password' variables to your MariaDB user and password.

### Run

```sh
flask run
```

## Included SQL (Optional)

An sql file with a few recipes and an account with the username 'admin' and password 'dev' for testing.

- cd to project directory.
- Launch and login to MariaDB.
- Create a new database named recipeApp.
```sh
CREATE DATABASE recipeApp
```
- Exit the shell and then import the sql from normal command line.
```sh
mariadb -u username -p recipeApp < recipeApp.sql
```

```sh
flask db upgrade
```

# Frontend

## Setup

```sh
cd frontend
npm install
```

### Compile for Development

```sh
npm run dev
```

### Compile for Production

```sh
npm run build
```
