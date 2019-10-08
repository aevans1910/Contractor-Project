from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient

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
    return render_template ('dogs_new.html')

@app.route('/dogs', methods=['POST'])
def dogs_submit():
    """Submit a new adoptable dog listing"""
    dog = {
        'name': request.form.get('name'),
        'description':request.form.get('description'),
        'dog-image': request.form.get('dog-image')
    }
    dogs.insert_one(dog)
    return redirect(url_for('dogs_index'))

if __name__ == '__main__':
    app.run(debug=True)