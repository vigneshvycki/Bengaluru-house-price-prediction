# app.py

from flask import Flask, render_template, request, jsonify
import util

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    util.load_saved_artifacts()
    locations = util.get_location_names()
    return render_template('app.html', locations=locations)

@app.route('/get', methods=['GET'])
def get_location_names():
    util.load_saved_artifacts()
    locations = util.get_location_names()
    response = jsonify({
        'locations': locations
    })
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    util.load_saved_artifacts()
    
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        keys = util.get_data_columns()

        # Prepare the JSON response
        prediction_result = {
            'estimated_price': estimated_price,
            'keys': keys
        }

        return render_template('app.html', locations=util.get_location_names(), prediction_result=prediction_result)
    except Exception as e:
        return render_template('app.html', locations=util.get_location_names(), error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
