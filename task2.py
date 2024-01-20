import requests
from io import StringIO
from flask import Flask, request, jsonify
import pandas as pd
from task1 import calculate


app = Flask(import_name=__name__)


@app.route('/calculate_volatility', methods=['POST'])
def calculate_volatility():
    """
    Endpoint to calculate Daily and Annualized Volatility from a 
    CSV file or URl of a CSV file.

    Parameters:
    - csv_file: File (CSV) or form parameter for providing data.
    - csv_url: URL of the CSV file if not provided directly.

    Returns:
    JSON response containing Daily and Annualized Volatility.
    """

    try:
        # Check if 'csv_file' is in request files or form data
        if 'csv_file' in request.files:
            # Read CSV file
            file = request.files['csv_file']
            data = pd.read_csv(file)
        elif 'csv_url' in request.form:
            # Extract URl of CSV File
            csv_url = request.form['csv_url']
            # To work with sharepoint urls, append &download=1
            if "sharepoint" in csv_url:
                csv_url = csv_url + "&download=1"
            response = requests.get(url=csv_url)
            # Raise an exception for bad responses
            response.raise_for_status()
            # Use SringIO to create File Object (buffer) for read_csv
            data = pd.read_csv(filepath_or_buffer=StringIO(initial_value=response.text))
        else:
            return jsonify({"error": "Either 'csv_file' or 'csv_url' parameter is required."}), 400

        # Strip leading/trailing space in Col names
        data.columns = data.columns.str.strip()

        # Ensure the dataset has a 'Close' column
        if 'Close' not in data.columns:
            return jsonify({"error": "The dataset must contain a 'Close' column."}), 400

        daily_volatility, annualized_volatility = calculate(df=data)

        # Return results in JSON format
        result = {
            "Daily Volatility": daily_volatility,
            "Annualized Volatility": annualized_volatility
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
