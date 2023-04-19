from recipes_app.config.mysqlconnection import connectToMySQL

from recipes_app.models.users_model import User

from flask import flash

from recipes_app import DATABASE

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under = int(data['under'])
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    # Create recipe
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes
            (name, description, instructions, date, under, user_id)
            VALUES
            (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under)s, %(user_id)s)
        """

        return connectToMySQL(DATABASE).query_db(query, data)

    # Validate new recipe
    @classmethod 
    def validate_recipe(cls, data):
        is_valid = True

        # Name validation
        if len(data['name']) < 1:
            flash("Name cannot be blank")
            is_valid = False
        
        # Description validation 
        if len(data['description']) < 1:
            flash("Description cannot be blank")
            is_valid = False
        
        # Instructions validation
        if len(data['instructions']) < 1:
            flash("Instructions cannot be blank")
            is_valid = False
        
        # Date cooked validation
        if data['date'] == "":
            flash("Date cannot be blank")
            is_valid = False
        
        return is_valid

    # Get all recipes with user attached
    @classmethod
    def get_all_recipes(cls):
        query = """
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []

        if results:
            for row in results:
                new_recipe = cls(row)

                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }

                recipe_creator = User(user_data)

                new_recipe.user = recipe_creator

                recipes.append(new_recipe)

        return recipes

    # Get single recipe from id
    @classmethod 
    def get_one_recipe(cls, id):
        data = {
            'id' : id
        }

        query = """
            SELECT * FROM recipes WHERE id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return results[0]
        else:
            return False
        
    # Update recipe
    @classmethod 
    def update(cls, data):
        query = """
            UPDATE recipes SET 
            name = %(name)s, description = %(description)s, instructions = %(instructions)s, 
            date = %(date)s WHERE id = %(recipe_id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    # Get one recipe with user attached
    @classmethod 
    def get_one_with_user(cls, id):
        data = {
            'id' : id
        }

        query = """
            SELECT * FROM recipes 
            JOIN users ON recipes.user_id = users.id 
            WHERE recipes.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        recipes = []

        if results:
            for row in results:
                recipe = cls(row)

                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }

                recipe_creator = User(user_data)

                recipe.user = recipe_creator

                recipes.append(recipe)
        
        return recipes[0]

    # Delete recipe
    @classmethod 
    def delete(cls, id):
        data = {
            'id' : id
        }

        query = """
            DELETE FROM recipes WHERE id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)