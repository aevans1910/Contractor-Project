from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Contractor
dogs = db.dogs

app = Flask (__name__)

@app.route('/')
def dogs_index():
    """Show all dogs"""

    # dogs = [
    #     {'title': 'Small dogs', 'description': '1-25 lbs.'},
    #     {'title': 'Medium dogs', 'description': '26-40 lbs.'},
    #     {'title': 'Large dogs', 'description': '41-70 lbs.'},
    #     {'title': 'Very large dogs', 'description': '71-above lbs.'}
    # ]
    # for dog in dogs.find():
    #     print(dog['name'])
    return render_template('dogs_index.html', dogs=dogs.find())

@app.route('/dogs/new')
def dogs_new():
    """Create a new adoptable dog profile"""
    return render_template ('dogs_new.html', dog={}, title='New listing')

@app.route('/dogs', methods=['POST'])
def dogs_submit():
    """Submit a new adoptable dog listing"""
    dog = {
        'name': request.form.get('name'),
        'description':request.form.get('description'),
        'image': request.form.get('image')
    }
    dog_id = dogs.insert_one(dog).inserted_id
    return redirect(url_for('dogs_show', dog_id=dog_id))

@app.route('/dogs/<dog_id>')
def dogs_show(dog_id):
    """Show a single dog"""
    dog = dogs.find_one({'_id': ObjectId(dog_id)})
    return render_template('dogs_show.html', dog=dog)

@app.route('/dogs/<dog_id>/edit')
def dogs_edit(dog_id):
    """Show the edit form for a dog"""
    dog = dogs.find_one({'_id': ObjectId(dog_id)})
    return render_template('dogs_edit.html', dog=dog, title='Edit listing')

@app.route('/dogs/<dog_id>', methods=['POST'])
def dogs_update(dog_id):
    """Submit an edited listing"""
    updated_dog = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'image': request.form.get('image')
    }
    dogs.update_one(
        {'_id': ObjectId(dog_id)},
        {'$set': updated_dog}
    )
    return redirect(url_for('dogs_show', dog_id=dog_id))

if __name__ == '__main__':
    app.run(debug=True)