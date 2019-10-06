from flask import Flask, render_template

app = Flask (__name__)

@app.route('/')
def dogs_index():
    """Show all dogs"""

    dogs = [
        {'title': 'Small dogs', 'description': '1-25 lbs.'},
        {'title': 'Medium dogs', 'description': '26-40 lbs.'},
        {'title': 'Large dogs', 'description': '41-70 lbs.'},
        {'title': 'Very large dogs', 'description': '71-above lbs.'}
    ]

    return render_template('dogs_index.html', dogs=dogs)

if __name__ == '__main__':
    app.run(debug=True)