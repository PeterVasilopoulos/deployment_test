from flask import render_template, request, redirect, session

from recipes_app.models.users_model import User

from recipes_app.models.recipes_model import Recipe

from recipes_app import app

# Default login page
@app.route('/')
def default():
    return render_template('login.html')

# All recipes page
@app.route('/recipes')
def all_recipes():
    if not 'uid' in session:
        return redirect('/')
    
    user = User.get_user_by_id(session['uid'])

    recipes = Recipe.get_all_recipes()

    return render_template('all_recipes.html', user = user, recipes = recipes)

# Login route
@app.route('/login', methods = ["POST"])
def login():
    logged_in_user = User.login(request.form)

    if logged_in_user:
        session['uid'] = logged_in_user.id
        return redirect('/recipes')
    else:
        return redirect('/')

# Register route
@app.route('/register', methods = ["POST"])
def register():
    validate_reg = User.register(request.form)

    if validate_reg:
        session['uid'] = User.create(request.form)
        return redirect('/recipes')
    else:
        return redirect('/')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')