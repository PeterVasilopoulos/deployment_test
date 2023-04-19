from flask import render_template, request, redirect, session

from recipes_app.models.recipes_model import Recipe

from recipes_app.models.users_model import User

from recipes_app import app

# Create new recipe page
@app.route('/recipes/create')
def create_recipe():
    if not 'uid' in session:
        return redirect('/')
    
    return render_template('create_recipe.html')

# Store recipe in database route
@app.route('/recipes/store', methods = ['POST'])
def store_recipe():
    validate_rec = Recipe.validate_recipe(request.form)

    if validate_rec:
        Recipe.create(request.form)
        return redirect('/recipes')
    else:
        return redirect('/recipes/create')

# Edit recipe route
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not 'uid' in session:
        return redirect('/')

    recipe = Recipe.get_one_recipe(id)

    return render_template('edit_recipe.html', recipe = recipe)

# Store updated recipe route
@app.route('/recipes/update', methods = ['POST'])
def update_recipe():
    validate_rec = Recipe.validate_recipe(request.form)

    print("its working")

    if validate_rec:
        Recipe.update(request.form)
        return redirect('/recipes')
    else:
        return redirect(f'/recipes/edit/{request.form["recipe_id"]}')

# View single recipe route
@app.route('/recipes/view/<int:id>')
def view_recipe(id):
    user = User.get_user_by_id(session['uid'])

    recipe = Recipe.get_one_with_user(id)

    if recipe:
        return render_template('/view_recipe.html', user = user, recipe = recipe)
    else:
        return redirect('/recipes')

# Delete recipe route
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete(id)

    return redirect('/recipes')