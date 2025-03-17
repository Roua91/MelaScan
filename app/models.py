#Database models (User, Admin, AnalysisResult)
from datetime import datetime
from bson import ObjectId
from app import mongo

# Users Collection
def create_user(data):
    """Create a new user."""
    user = {
        "username": data["username"],
        "password": data["password"],  # Password should be hashed before storing
        "role": data["role"],  # 'doctor', 'local_admin', 'global_admin'
        "clinic_id": ObjectId(data["clinic_id"])  # Reference to Clinic collection
    }
    return user

def insert_user(data):
    user = create_user(data)
    mongo.db.users.insert_one(user)
    return str(user["_id"])

# Doctors Collection
def create_doctor(data):
    """Create a new doctor."""
    doctor = {
        "user_id": ObjectId(data["user_id"]),  # Reference to Users collection
        "clinic_id": ObjectId(data["clinic_id"]),  # Reference to Clinics collection
        "specialization": data["specialization"]
    }
    return doctor

def insert_doctor(data):
    doctor = create_doctor(data)
    mongo.db.doctors.insert_one(doctor)
    return str(doctor["_id"])

# LocalAdmins Collection
def create_local_admin(data):
    """Create a new local admin."""
    local_admin = {
        "user_id": ObjectId(data["user_id"]),  # Reference to Users collection
        "clinic_id": ObjectId(data["clinic_id"])  # Reference to Clinics collection
    }
    return local_admin

def insert_local_admin(data):
    local_admin = create_local_admin(data)
    mongo.db.local_admins.insert_one(local_admin)
    return str(local_admin["_id"])

# GlobalAdmins Collection
def create_global_admin(data):
    """Create a new global admin."""
    global_admin = {
        "user_id": ObjectId(data["user_id"]),  # Reference to Users collection
    }
    return global_admin

def insert_global_admin(data):
    global_admin = create_global_admin(data)
    mongo.db.global_admins.insert_one(global_admin)
    return str(global_admin["_id"])

# Clinics Collection
def create_clinic(data):
    """Create a new clinic."""
    clinic = {
        "clinic_name": data["clinic_name"],
        "clinic_address": data["clinic_address"],
        "contact_number": data["contact_number"],
        "local_admins": [ObjectId(admin) for admin in data["local_admins"]],  # List of LocalAdmin references
        "global_admins": [ObjectId(admin) for admin in data["global_admins"]],  # List of GlobalAdmin references
        "doctors": [ObjectId(doctor) for doctor in data["doctors"]]  # List of Doctor references
    }
    return clinic

def insert_clinic(data):
    clinic = create_clinic(data)
    mongo.db.clinics.insert_one(clinic)
    return str(clinic["_id"])

# Patients Collection
# Create a patient
def create_patient(data):
    """Create a new patient."""
    patient = {
        "patient_name": data["patient_name"],
        "patient_contact": data["patient_contact"],
        "date_of_birth": data["date_of_birth"],
        "clinic_id": ObjectId(data["clinic_id"]),  # Reference to Clinics collection
    }
    return patient

# Insert the patient into the database
def insert_patient(data):
    patient = create_patient(data)
    mongo.db.patients.insert_one(patient)
    return str(patient["_id"])

# Reports Collection
def create_report(data, patient_id, image_id):
    """Create a new report."""
    report = {
        "patient_id": ObjectId(patient_id),  # Reference to Patients collection
        "image_id": ObjectId(image_id),  # Reference to Images collection
        "prediction_result": data["prediction_result"],
        "generated_on": datetime.utcnow()
    }
    return report

def insert_report(data, patient_id, image_id):
    report = create_report(data, patient_id, image_id)
    mongo.db.reports.insert_one(report)
    return str(report["_id"])

# Images Collection
def create_image(data, patient_id):
    """Create a new image."""
    image = {
        "patient_id": ObjectId(patient_id),  # Reference to Patients collection
        "filename": data["filename"],
        "upload_date": datetime.utcnow(),
        "file_path": data["file_path"]
    }
    return image

def insert_image(data, patient_id):
    image = create_image(data, patient_id)
    mongo.db.images.insert_one(image)
    return str(image["_id"])

# Patient Access Control Collection
def create_patient_access(data):
    """Create a new patient access control record."""
    patient_access = {
        "patient_id": ObjectId(data["patient_id"]),  # Reference to Patients collection
        "clinic_id": ObjectId(data["clinic_id"])  # Reference to Clinics collection
    }
    return patient_access

def insert_patient_access(data):
    patient_access = create_patient_access(data)
    mongo.db.patient_access.insert_one(patient_access)
    return str(patient_access["_id"])

# Example function to find all reports for a given patient
def find_reports_for_patient(patient_id):
    reports = mongo.db.reports.find({"patient_id": ObjectId(patient_id)})
    result = []
    for report in reports:
        report["_id"] = str(report["_id"])  # Convert ObjectId to string for easy handling
        result.append(report)
    return result

# Example function to find all images for a given patient
def find_images_for_patient(patient_id):
    images = mongo.db.images.find({"patient_id": ObjectId(patient_id)})
    result = []
    for image in images:
        image["_id"] = str(image["_id"])  # Convert ObjectId to string for easy handling
        result.append(image)
    return result
