from flask import Blueprint, request, jsonify
from database.models import Company, PlacementDrive, Student, Application
from database.database import db
from email_validator import validate_email, EmailNotValidError
from werkzeug.security import generate_password_hash
from datetime import datetime
from controllers.auth import roles_required
from flask_jwt_extended import get_jwt_identity
from services.cache import cache


company = Blueprint('company', __name__)

@company.route("/registration" , methods= ["POST"])
def companyRegistration():
    data = request.get_json()
    email= data.get('email')
    password = data.get('password')
    company_name = data.get('companyName')
    website = data.get('website')
    description = data.get('description')
    role = data.get('role')
    hr_name = data.get('hr_name')
    hr_email = data.get('hr_email')
    hr_phone_number = data.get('hr_phone_no')
    print(data)

    if role != 'company':
        return jsonify({"status" : "error", "message" : "Invalid role."})

    if not email or not password or not company_name:
        return jsonify({"status": "error", "message": "All fielde Required."}), 400
    
    if Company.query.filter_by(email=email).first():
        return jsonify({"status": "error", "message": "Company Already Exists."}), 400
    
    if not validate_email(email) or not validate_email(hr_email):
        return jsonify({"status": "error", "message": "Invalid Email."}), 400
    

    if len(password) < 6:
        return jsonify({"status" : "error" , "message" : "Strong Password Required."}), 400
    
    if len(hr_phone_number) != 10:
        return jsonify({"status" : "error" , "message" : "Enter a Valid Phone Number"}), 400

    hash_password = generate_password_hash(password)

    new_company = Company(
        email=email,
        password=hash_password,
        name=company_name,
        website=website,
        description=description,
        hr_name = hr_name,
        hr_email = hr_email,
        hr_phone_number = hr_phone_number  
    )
    
    try:
        db.session.add(new_company)
        db.session.commit()
        return jsonify({"status": "success" , "message": "Company registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"status": "error" , "message": "Server Error, Try Again..."}), 400


@company.route("/dashboard" ,methods = ["GET"])
@roles_required("company")
@cache.cached(timeout=5)
def Company_dashboard():
    company_email = get_jwt_identity()
    company = Company.query.filter_by(email = company_email).first()
    com_id = company.id

    drives = PlacementDrive.query.filter_by(company_id = com_id).all()

    drive_no = {"total_drive" : 0, "pending_drive" :0 , "completed_drive" : 0, "rejected_drive" : 0, "active_drive" : 0}

    for drive in drives:
        if drive.status == "Approved" and drive.application_deadline < datetime.now():
            drive_no['completed_drive'] += 1
        elif drive.status == 'Approved':
            drive_no["active_drive"] += 1
        elif drive.status == "Rejected":
            drive_no["rejected_drive"] += 1
        elif drive.status == 'Pending':
            drive_no['pending_drive'] += 1

        drive_no["total_drive"] += 1

    applications = db.session.query(
        Application.status
    ).join(PlacementDrive, PlacementDrive.id == Application.drive_id) \
     .filter(PlacementDrive.company_id == com_id).all()

    app_numbers = {"total_applied" : 0, "shortlisted" :0 , "rejected" : 0, "pending" : 0}

    for app in applications:
        if app.status == "Shortlisted":
            app_numbers["shortlisted"] += 1
        elif app.status == "Rejected":
            app_numbers["rejected"] += 1
        elif app.status == "Applied":
            app_numbers["pending"] += 1
            
        app_numbers["total_applied"] += 1

    return jsonify({"status" : "success", "message" : "Data fetched Success." , "data" : {"drive_numbers" : drive_no, "application_numbers" :app_numbers}})
    


@company.route("/update-profile" , methods = ["POST"])
@roles_required("company")
def compnay_profile_update():
    email = get_jwt_identity()
    data = request.get_json()
    field_name = data.get("field_name")
    value = data.get("value")
    if not data:
        return jsonify({"status" : "error",  "message" : "No Data fields Send."})

    if field_name in ["email" , "password", "status"]:
        return jsonify({"status" : "error" , "message" : f"You are not allowed to update {field_name}.."})

    company = Company.query.filter_by(email = email).first()

    if not company:
        return jsonify({"status" : "error" , "message" : f"Invalid company.."})
    
    try:
        setattr(company, field_name, value)
        db.session.commit()
        
        return jsonify({"status": "success", "message": f"Profile field '{field_name}' updated successfully."})

    except Exception as e:
        db.session.rollback()
        print(f"Profile Update Error: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to update profile field. Try again."}), 500


@company.route("/create-drive" , methods= ["POST"])
@roles_required("company")
def create_drive():
    data = request.get_json()

    email = get_jwt_identity()
    print(data)

    company = Company.query.filter_by(email = email).first()
    company_id = company.id

    job_title = data.get('job_title')
    job_description =  data.get('job_description')
    eligible_branches = data.get('eligible_branches')
    min_cgpa = data.get('min_cgpa')
    eligible_year = data.get('eligible_year')
    application_deadline = data.get('application_deadline')



    company_data = Company.query.filter_by(id = company_id).first()

    if not company_data:
        return jsonify({"status" : "error",  "message" : "Company Not Exits"}) , 404

    if company_data.status != "Approved":
        return jsonify({"status" : "error", "message" : "Wait for the Company Approval."}), 400


    if not job_title or not job_description or not eligible_branches or not min_cgpa or not eligible_year or not application_deadline:
        return jsonify({"status" : "error" , "message" : "All fields Required."}), 400
    

    if application_deadline:
        # Standardise the 'Z' format for python's parser
        cleaned_str = application_deadline.replace('Z', '+0000')
        application_deadline = datetime.strptime(cleaned_str, '%Y-%m-%dT%H:%M')
    else:
        application_deadline = None


    new_drive = PlacementDrive(
        company_id = company_id,
        job_title = job_title, 
        job_description = job_description,
        eligible_branches = eligible_branches,
        min_cgpa = min_cgpa,
        eligible_year = eligible_year,
        application_deadline = application_deadline,   
    )

    try:
        db.session.add(new_drive)
        db.session.commit()
        return jsonify({"status": "success" , "message": "Placement Drive registered successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"status": "error" , "message": "Server error try agian..."}), 400



@company.route("/get-dashboard"  , methods = ["GET"])
@roles_required("company")
def get_dashboard():
    company_email = get_jwt_identity()
    company = Company.query.filter_by(email = company_email).first()
    company_id = company.id

    drives = db.session.query(
        PlacementDrive.id,
        PlacementDrive.job_title,
        PlacementDrive.status
    ).filter(PlacementDrive.company_id == company_id).all()


    data = [{"id" : drive.id, "job_title" : drive.job_title, "status" : drive.status} for drive in drives]

    return jsonify({"status" : "success", "message" : "Data fetched Successfully", "data" :data})




@company.route("/update-profile" , methods = ["GET", "PUT"])
@roles_required("company")
def update_profile():
    email = get_jwt_identity()
    company = Company.query.filter_by(email = email).first()


    if request.method == "GET":
        data = {
            "id" : company.id,
            "name" : company.name,
            "description" : company.description,
            "email" : company.email,
            "status" : company.status,
            "address" : company.address,
            "hr_phone" : company.hr_phone_number,
            "hr_name" : company.hr_name,
            "hr_email" : company.hr_email,
            "website" : company.website,
        }

        return jsonify({"status" : "success",  "message" : "Data fetched Successfully", "data" : data})



    elif request.method == "PUT":
        data = request.get_json()
        field_name = data.get("name")
        value = data.get("data")

        if field_name not in ["hr_phone_number", "address" , "hr_name", "hr_email" ,"description", "website"]:
            return jsonify({"status" : "error" , "message" : "you cant Edit This..."})
        
        setattr(company, field_name, value)

        try:
            db.session.commit()
            return jsonify({"status" : "success" , "message" : f"{field_name} updated..."})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status" : "error" , "message" : "Intenal Server Error, Try Again..."})

    return jsonify({"status" : "error" , "message" : "Not a Valid Request.."})



@company.route("/get-student/<int:id>", methods = ["GET"])
@roles_required("company")
def get_student_details(id):
    student = Student.query.get(id)

    if not student:
        return jsonify({"status": "failed", "message": "Student not found"}), 404

    student_details = {
        "id": student.id,
        "full_name": student.full_name,
        "email": student.email,
        "roll_number": student.roll_number,
        "status": student.status,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "resume_link": student.resume_link,
        "address": student.address,
    }

    return jsonify({"status": "success","message": "data fetched Successfully." ,"data": student_details})


@company.route('/shortlist-student/<int:student_id>/<int:drive_id>',  methods = ["GET"])
@roles_required("company")
def shortlist_student(student_id, drive_id):
    email = get_jwt_identity()
    company = Company.query.filter_by(email = email).first()
    company_id = company.id

    if not company.status == "Approved":
        return jsonify({"status": "error", "message": "your Company is Blocked, Contact Adminstration..."}), 404


    application = db.session.query(
        Application.id,
        Application.student_id,
        Application.drive_id,
        PlacementDrive.company_id
    ).join(PlacementDrive, PlacementDrive.id == Application.drive_id) \
     .filter(
         Application.student_id == student_id,
         Application.drive_id == drive_id,
         PlacementDrive.company_id == company_id
     ).first()

    if not application:
        return jsonify({"status": "error", "message": "Application not found"}), 404

    try:
        applica = Application.query.get(application.id)
        applica.status = "Shortlisted"
        db.session.commit()
        return jsonify({"status": "success", "message": "Student shortlisted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Internal Server Error, Try Again..."})
    


@company.route('/reject-student/<int:student_id>/<int:drive_id>',  methods = ["GET"])
@roles_required("company")
def rejected_student(student_id, drive_id):
    email = get_jwt_identity()
    company = Company.query.filter_by(email = email).first()
    company_id = company.id

    if not company.status == "Approved":
        return jsonify({"status": "error", "message": "your Company is Blocked, Contact Adminstration..."}), 404


    application = db.session.query(
        Application.id,
        Application.student_id,
        Application.drive_id,
        PlacementDrive.company_id
    ).join(PlacementDrive, PlacementDrive.id == Application.drive_id) \
     .filter(
         Application.student_id == student_id,
         Application.drive_id == drive_id,
         PlacementDrive.company_id == company_id
     ).first()

    if not application:
        return jsonify({"status": "error", "message": "Application not found"}), 404

    try:
        applica = Application.query.get(application.id)
        applica.status = "Rejected"
        db.session.commit()
        return jsonify({"status": "success", "message": "Student Rejected"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Internal Server Error, Try Again..."})
    


