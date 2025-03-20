import os
from .database import db
from werkzeug.utils import secure_filename
from .services.inference import run_inference
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required
from .models import Image, Patient, User, Report, Clinic


main_bp = Blueprint('main', __name__)

# Define Upload Folder
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- Authentication & Authorization ---
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth.html')

@main_bp.route('/logout')
def logout():
    return redirect(url_for('main.index'))

# --- Home Page (Landing Page) ---
@main_bp.route('/')
def index():
    return render_template('index.html')

# --- Clinic Registration Page ---
@main_bp.route('/clinic-registration', methods=['GET', 'POST'])
def clinic_registration():
    return render_template('clinic_registration.html')

# --- Dashboard (Clinician/Admin) ---
@main_bp.route('/dashboard')
@jwt_required()
def dashboard():
    return render_template('dashboard.html')

# --- Patient Management Page ---
@main_bp.route('/patients', methods=['GET', 'POST'])
@jwt_required()
def patients():
    return render_template('patients.html')

# --- Image Upload & Processing Page ---
@main_bp.route('/upload', methods=['GET', 'POST'])
@jwt_required()
def upload_image():
    return render_template('upload.html')

# --- Melanoma Detection Result Page ---
@main_bp.route('/results/<int:image_id>')
@jwt_required()
def results(image_id):
    image = Image.query.get(image_id)
    return render_template('results.html', image=image)

# --- Report Generation Page ---
@main_bp.route('/reports', methods=['GET'])
@jwt_required()
def reports():
    return render_template('reports.html')

# --- System Logs & Audit Trail Page (Admin) ---
@main_bp.route('/logs', methods=['GET'])
@jwt_required()
def logs():
    return render_template('logs.html')

# --- Settings & Account Management Page ---
@main_bp.route('/settings', methods=['GET', 'POST'])
@jwt_required()
def settings():
    return render_template('settings.html')

# --- About & FAQs Page ---
@main_bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- User Authentication ---
@main_bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.user_id)
        return jsonify(access_token=token)
    return jsonify({"message": "Invalid credentials"}), 401

@main_bp.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# --- Upload Image API ---
@main_bp.route('/api/upload', methods=['POST'])
@jwt_required()
def api_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    patient_id = request.form.get('patient_id')

    if not patient_id:
        return jsonify({"error": "Patient ID is required"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Run AI model
        diagnosis = run_inference(file_path)

        # Store metadata
        new_image = Image(filename=filename, file_path=file_path, patient_id=patient_id)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            "filename": filename,
            "file_path": file_path,
            "diagnosis": diagnosis
        }), 201

    return jsonify({"error": "Invalid file format"}), 400

# --- Generate Reports API ---
@main_bp.route('/api/reports/<int:patient_id>', methods=['GET'])
@jwt_required()
def api_generate_report(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    reports = Report.query.filter_by(patient_id=patient_id).all()
    report_data = [{"report_id": r.report_id, "prediction_result": r.prediction_result, "generated_on": r.generated_on} for r in reports]

    return jsonify(report_data)

@main_bp.route('/api/clinic-register', methods=['POST'])
def register_clinic():
    data = request.json
    clinic_name = data.get('clinic_name')
    clinic_address = data.get('clinic_address')
    contact_number = data.get('contact_number')
    email = data.get('email')  # For notification

    if not clinic_name or not clinic_address or not contact_number or not email:
        return jsonify({"error": "Missing required fields"}), 400

    # Send clinic data to Node.js AI verification service
    node_url = "http://localhost:3000/api/verify-clinic"
    response = requests.post(node_url, json={
        "clinic_name": clinic_name,
        "clinic_address": clinic_address,
        "contact_number": contact_number,
        "email": email
    })

    return response.json(), response.status_code  # Forward response from Node.js to the frontend