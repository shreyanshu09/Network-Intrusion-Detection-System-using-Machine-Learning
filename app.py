# # from flask import Flask, render_template, jsonify, request
# # import subprocess
# # import pandas as pd
# # from capture_traffic import capture_traffic
# # from classify_traffic import classify_traffic, load_model

# # app = Flask(__name__)

# # @app.route('/')
# # def index():
# #     return render_template('mainhtml.html')

# # @app.route('/capture', methods=['POST'])
# # def capture():
# #     try:
# #         capture_duration = 60  # Capture for 60 seconds
# #         output_file = "captured_traffic.csv"
# #         capture_traffic(capture_duration, output_file)
# #         return jsonify({"status": "success", "message": "Traffic captured successfully"})
# #     except Exception as e:
# #         return jsonify({"status": "error", "message": str(e)})

# # @app.route('/analyze', methods=['POST'])
# # def analyze():
# #     try:
# #         model = load_model('traffic_model.pkl')
# #         classified_traffic = classify_traffic(model, 'captured_traffic.csv')
# #         results = classified_traffic['prediction'].value_counts().to_dict()
# #         return jsonify({"status": "success", "results": results})
# #     except Exception as e:
# #         return jsonify({"status": "error", "message": str(e)})

# # if __name__ == '__main__':
# #     app.run(debug=True)
# from flask import Flask, render_template, jsonify, request, send_from_directory
# import os
# from capture_traffic import capture_traffic
# from classify_traffic import classify_traffic, load_model

# app = Flask(__name__)#, template_folder='templates', static_folder='static')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/mainhtml.html')
# def ids():
#     return render_template('mainhtml.html')

# @app.route('/capture', methods=['POST'])
# def capture():
#     try:
#         capture_duration = 60  # Capture for 60 seconds
#         output_file = "captured_traffic.csv"
#         capture_traffic(capture_duration, output_file)
#         return jsonify({"status": "success", "message": "Traffic captured successfully"})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         model = load_model('traffic_model.pkl')
#         classified_traffic = classify_traffic(model, 'captured_traffic.csv')
#         results = classified_traffic['prediction'].value_counts().to_dict()
#         # Get the last non-empty value in the 'prediction' column
#         last_prediction = classified_traffic['prediction'].iloc[-1]
#         return jsonify({"status": "success", "results": results, "last_prediction": last_prediction})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
from capture_traffic import capture_traffic
from classify_traffic import classify_traffic, load_model

app = Flask(__name__)#, template_folder='project/templates', static_folder='project/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mainhtml.html')
def ids():
    return render_template('mainhtml.html')

@app.route('/capture', methods=['POST'])
def capture():
    try:
        capture_duration = 60  # Capture for 60 seconds
        output_file = "captured_traffic.csv"
        capture_traffic(capture_duration, output_file)
        return jsonify({"status": "success", "message": "Traffic captured successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        model = load_model('traffic_model.pkl')
        results, last_prediction = classify_traffic(model, 'captured_traffic.csv')
        return jsonify({"status": "success", "results": results, "last_prediction": last_prediction})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)