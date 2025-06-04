from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Important for sessions

# Load models
catboost_model = joblib.load("models/catboost_model.pkl")
iso_forest = joblib.load("models/isolation_forest.pkl")
meta_model = joblib.load("models/meta_model.pkl")
lstm_model = load_model("models/lstm_model.keras")
scaler = joblib.load("models/scaler.pkl")

USERNAME = 'admin'
PASSWORD = 'admin123'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == USERNAME and pw == PASSWORD:
            session['username'] = user
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    result = None
    pred_cat = pred_if = pred_lstm = None
    result_class = ""

    if request.method == 'POST':
        input_line = request.form['input_line']
        try:
            features = np.array([list(map(float, input_line.strip().split(",")))])
            if features.shape[1] != 7:
                result = "Error: Expected 7 features."
                result_class = "error"
            else:
                features_scaled = scaler.transform(features)
                lstm_input = features_scaled.reshape((1, 1, 7))

                pred_cat = int(catboost_model.predict(features_scaled)[0])
                pred_if = 1 if iso_forest.predict(features_scaled)[0] == -1 else 0
                lstm_score = float(lstm_model.predict(lstm_input, verbose=0)[0][0])
                pred_lstm = int(lstm_score > 0.5)

                combined_preds = np.array([[pred_cat, pred_if, pred_lstm]])
                final_pred = int(meta_model.predict(combined_preds)[0])

                if final_pred == 1:
                    result = "Ransomware Activity Detected!"
                    result_class = "result-ransomware"
                else:
                    result = "System Log appears Benign."
                    result_class = "result-benign"
        except Exception as e:
            result = f"Error: {e}"
            result_class = "error"

    return render_template(
        'predict.html',
        result=result,
        result_class=result_class,
        pred_cat=pred_cat,
        pred_if=pred_if,
        pred_lstm=pred_lstm
    )

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
