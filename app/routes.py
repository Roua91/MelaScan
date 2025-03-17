from flask import Flask, request, render_template, redirect, url_for, jsonify
from app import mongo
from app.models import insert_patient, create_patient  # Correct import


@app.route('/')
def index():
    return render_template('add_patient.html')  # Serve the HTML form

@app.route('/add_patient', methods=['POST'])
def add_patient():
    # Get data from the form
    patient_name = request.form.get('patient_name')
    patient_contact = request.form.get('patient_contact')
    date_of_birth = request.form.get('date_of_birth')
    clinic_id = request.form.get('clinic_id')

    # Create patient data (this can be enhanced to add other fields)
    patient_data = {
        "patient_name": patient_name,
        "patient_contact": patient_contact,
        "date_of_birth": date_of_birth,
        "clinic_id": clinic_id
    }

    # Insert the patient data into the MongoDB database
    patient_id = insert_patient(patient_data)

    # Return a response after successful insertion
    return jsonify(message="Patient added successfully", patient_id=patient_id), 201

@app.route('/get_patient_reports/<patient_id>', methods=['GET'])
def get_patient_reports(patient_id):
    # Fetch reports associated with a patient (if any)
    reports = find_reports_for_patient(patient_id)
    return jsonify(reports), 200
