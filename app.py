from flask import Flask, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

@app.route('/api/rsi', methods=['GET'])
def get_rsi():
    try:
        # Read data from CSV file
        df = pd.read_csv('AAPL_1min_firstratedata.csv')  
        print("Columns in CSV:", df.columns.tolist())  # Print the columns to check their names
        
        # Convert 'close' column to numeric, coerce errors to NaN
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        
        # Calculate RSI
        df['RSI'] = calculate_rsi(df['close'])  # Pass the correct column
        rsi_values = df['RSI'].dropna().tolist()  # Convert to list and remove NaN values
        return jsonify(rsi_values)
    except Exception as e:
        print("Error:", e)  # Log the error in the console
        return jsonify({'error': str(e)}), 500

# Function to calculate the RSI
def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
# Route to serve index.html
@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
