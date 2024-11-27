from flask import Flask, request, jsonify, render_template
import pandas as pd
import json
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Initialize Flask app
app = Flask(__name__)

# Load data and model setup
data = pd.read_csv("C:\\Users\\mohit\\OneDrive\\Desktop\\dataset\\blood_report_diseases_with_suggestions.csv")

# Load yoga and diet plans from CSV
plans_df = pd.read_csv("C:\\Users\\mohit\\OneDrive\\Desktop\\dataset\\disease_yoga_diet_plans.csv")
disease_plans = {
    row['Disease']: {'yoga': row['Yoga'], 'diet': row['Diet']}
    for _, row in plans_df.iterrows()
}

# Encode gender
le_gender = LabelEncoder()
data['Gender'] = le_gender.fit_transform(data['Gender'])

# Features and target for training
features = ['Age', 'Gender', 'Hemoglobin', 'WBC', 'RBC', 'Blood_Sugar']
target = 'Disease'

# Splitting data
X = data[features]
y = data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Function to predict disease and suggestion
def predict_disease_and_suggestion(age, gender, hemoglobin, wbc, rbc, blood_sugar):
    gender_encoded = le_gender.transform([gender])[0]
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender_encoded],
        'Hemoglobin': [hemoglobin],
        'WBC': [wbc],
        'RBC': [rbc],
        'Blood_Sugar': [blood_sugar]
    })
    predicted_disease = model.predict(input_data)[0]
    suggestion = data.loc[data['Disease'] == predicted_disease, 'Suggestion'].values[0]

    # Get yoga and diet plans for the predicted disease
    yoga_plan = disease_plans.get(predicted_disease, {}).get('yoga', 'No specific yoga plan available.')
    diet_plan = disease_plans.get(predicted_disease, {}).get('diet', 'No specific diet plan available.')

    return predicted_disease, suggestion, yoga_plan, diet_plan

# Home route to display the form
@app.route('/')
def home():
    return render_template('index.html')

# Project description route
@app.route('/project_description')
def project_description():
    return render_template('project_description.html')

# Result route
@app.route('/result')
def result():
    # Example data to pass if needed
    disease = "Sample Disease"
    suggestion = "Sample Suggestion"
    yoga_plan = "Sample Yoga Plan"
    diet_plan = "Sample Diet Plan"
    
    return render_template('result.html', disease=disease, suggestion=suggestion, yoga_plan=yoga_plan, diet_plan=diet_plan)

# Route to handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from form
    age = int(request.form['age'])
    gender = request.form['gender']
    hemoglobin = float(request.form['hemoglobin'])
    wbc = float(request.form['wbc'])
    rbc = float(request.form['rbc'])
    blood_sugar = float(request.form['blood_sugar'])

    # Predict disease and suggestion
    disease, suggestion, yoga_plan, diet_plan = predict_disease_and_suggestion(age, gender, hemoglobin, wbc, rbc, blood_sugar)

    # Return the result on the web page
    return render_template('result.html', disease=disease, suggestion=suggestion, yoga_plan=yoga_plan, diet_plan=diet_plan)

# Contact route to display contact form
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Route to handle contact form submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json
    name = data['name']
    email = data['email']
    message = data['message']

    # Append the message to a file (or use a database if available)
    with open("messages.json", "a") as file:
        file.write(json.dumps({"name": name, "email": email, "message": message}) + "\n")

    return jsonify({"message": "Your message has been received. Thank you!"})

if __name__ == '__main__':
    app.run(debug=True)
