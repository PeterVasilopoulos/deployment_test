from recipes_app.config.mysqlconnection import connectToMySQL

from flask import flash

from recipes_app import DATABASE, BCRYPT

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Create user
    @classmethod 
    def create(cls, form):
        hash = BCRYPT.generate_password_hash(form['password'])

        data = {
            **form,
            'password' : hash
        }

        query = """
            INSERT INTO users
            (first_name, last_name, email, password)
            VALUES 
            (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    # Validate login
    @classmethod 
    def login(cls, form):
        found_user = cls.get_user_by_email(form['email'])

        if found_user:
            if BCRYPT.check_password_hash(found_user.password, form['password']):
                return found_user
            else: 
                flash("Invalid Login")
                return False
        else:
            flash("Invalid Login")
            return False
        

    # Get user by email
    @classmethod
    def get_user_by_email(cls, email):
        data = {
            'email' : email
        }

        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False

    # Validate registration
    @classmethod 
    def register(cls, form):
        is_valid = True 

        # First name validation
        if len(form['first_name']) < 2:
            flash("First name must be valid")
            is_valid = False
        
        # Last name validation
        if len(form['last_name']) < 2:
            flash("Last name must be valid")
            is_valid = False

        # Email validation
        if not EMAIL_REGEX.match(form['email']):
            flash("Email must be valid")
            is_valid = False
        
        find_user = cls.get_user_by_email(form['email'])
        if find_user:
            flash("Email already in use")
            is_valid = False

        # Password validation
        if form['password'] != form['confirm_password']:
            flash("Passwords must match")
            is_valid = False

        return is_valid

    # Get user by id
    @classmethod 
    def get_user_by_id(cls, id):
        data = {
            'id' : id
        }

        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False