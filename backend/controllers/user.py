from flask import Blueprint, jsonify, request
from database.models import *
from database.database import db
from werkzeug.security import generate_password_hash
from sqlalchemy import null, or_
from controllers.auth import roles_required
from flask_jwt_extended import get_jwt_identity, get_jwt
from services.redis import redisclient
from services.cache import cache

user = Blueprint('user', __name__)


@user.route("/registration",  methods = ["POST"])
def registration():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    fullName = data.get('fullname')
    rollno = data.get('rollno')
    role = data.get('role')
    cgpa =  data.get('cgpa')
    branch = data.get('branch')
    graduation_year = data.get('graduationyear')


    if not email or not password or not role or not fullName or not rollno or not cgpa or not branch or not graduation_year:
        return jsonify({"status": "error", "message": "All fields are Required."}), 400
    
    if role != "student":
        return jsonify({"status": "error", "message": "Invalid role."}), 400
 

    user = Student.query.filter(or_(Student.email == email, Student.roll_number == rollno)).first()

    if user:
        return jsonify({"status": "error", "message": "Student already exists."}), 400
    
    if len(password) < 6:
        return jsonify({"status" : "error", "message" : "Strong Password Required."})
    
    new_user = Student(
        email= email,
        password= generate_password_hash(password),
        full_name= fullName,
        roll_number= rollno,
        branch = branch,
        cgpa= cgpa,
        graduation_year= graduation_year
    )


    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "An error occurred while registering the user."}), 500
    

    return jsonify({"status": "success", "message": "Registration successful."}), 201



@user.route("/get-profile", methods= ["GET"])
@roles_required("student")
@cache.cached(timeout=10)
def get_profile():
    student_email = get_jwt_identity()

    student = Student.query.filter_by(email = student_email).first()
    if not student:
        return jsonify({"status": "error", "message": "Student not found."}), 404

    data = {
        "id" : student.id,
        "full_name" : student.full_name,
        "status" : student.status,
        "email" : student.email,
        "roll_number" : student.roll_number,
        "address" : student.address,
        "branch" : student.branch,
        "cgpa" : student.cgpa,
        "graduation_year" : student.graduation_year,
        "resume_link" : student.resume_link
    }

    return jsonify({"status": "success", "data": data}), 200




@user.route("/update-profile", methods= ["PUT"])
@roles_required("student")
def update_profile():
    student_email = get_jwt_identity()

    data = request.get_json()
    field_name = data.get("name")
    value = data.get("data")
    print([field_name, value])

    if field_name not in ["cgpa" , "address", "resume_link"]:
        return jsonify({"status" : "error" , "message" : f"You can't Update {field_name}."})

    if field_name == "cgpa":
        value = float(value)
        if value > 10:
            return jsonify({"status" : "error" , "message" : "Enter a Valid cgpa"})

    student = Student.query.filter_by(email = student_email).first()
    if not student:
        return jsonify({"status" : "error", "message" : "Invalid Student Id."})
    
    setattr(student , field_name, value)

    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"status" :"error", "message" : "Internal Server Error. Try Again"})

    return jsonify({"status" :"success", "message" : f"{field_name} Updated Successfully."})


@user.route("/get-active-drives", methods= ["GET"])
@roles_required("student")
def get_drives():
    drives = db.session.query(
        PlacementDrive.id,
        PlacementDrive.job_title,
        PlacementDrive.created_at,
        PlacementDrive.application_deadline,
        Company.name
    ).join(Company, Company.id == PlacementDrive.company_id) \
    .filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.application_deadline > datetime.now()
    ).all()


    drives_list = [
        {
            "id": drive.id,
            "job_title": drive.job_title,
            "company_name" :drive.name,
            "application_deadline": drive.application_deadline.strftime('%Y-%m-%dT%H:%M') if drive.created_at else None
        } 
        for drive in drives
    ]

    return jsonify({"status" : "success", "data": drives_list})


@user.route("/get-drive/<int:id>" , methods = ['GET'])
@roles_required("student")
def user_get_drive(id):
    drive = PlacementDrive.query.filter_by(id = id).first()
    company_id = drive.company_id

    company = db.session.query(
        Company.name,
        Company.hr_email,
        Company.hr_name,
        Company.hr_phone_number
    ).filter(Company.id == company_id).first()

    data = {"id" : drive.id, "job_title" :drive.job_title , "job_description" : drive.job_description, "eligible_branches" : drive.eligible_branches, "min_cgpa" : drive.min_cgpa, "eligible_year" : drive.eligible_year, "application_deadline" :drive.application_deadline, "status" : drive.status, "hr_name" : company.hr_name, "hr_phone": company.hr_phone_number, "hr_email" : company.hr_email, "company_name" : company.name}

    return jsonify({"status" : "success" , "message" : "Data fetched Success..", "data" : data })



@user.route("/get-active-companies" , methods = ["GET"])
@roles_required("student")
def get_active_companies():

    companies = Company.query.filter_by(status="Approved").all()
    
    if not companies:
        return jsonify({"status" : "success" , "message" : "No Company Found"})

    data = [{"id" : company.id , "name" : company.name} for company in companies]

    return jsonify({ "status" :  "success" , "message" : "companies fetched Succesfully", "data" : data })



@user.route("/apply-drive/<int:drive_id>" , methods=["GET"])
@roles_required("student")
def apply_drive(drive_id):
    email = get_jwt_identity()

    student = Student.query.filter_by(email = email).first()
    if not student:
        return jsonify({"status": "error", "message": "Student not found"})

    student_id  = student.id

    
    
    if student.status == "blocked":
        return jsonify({"status" : "error", "message": "You are Blocked, Meet the Admin"})
    

    if not student.resume_link or not student.cgpa or not student.branch or not student.graduation_year:
        return jsonify({"status" : "error" , "message" : "Update your Profile Before Applying.."})

    drive = PlacementDrive.query.filter_by(id = drive_id).first()

    if not drive:
        return jsonify({"status": "error", "message": "Drive not found"})

    if float(student.cgpa) <= float(drive.min_cgpa):
        return jsonify({"status" : "error", "message" : "You are not eligible for this Drive.."})


    application = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if application:
        return jsonify({"status": "error", "message": "You Already Applied to this Drive, Apply Other drives"})

    new_application = Application(
        student_id=student.id,
        drive_id=drive.id,
        application_date=datetime.now()
    )
    try:
        db.session.add(new_application)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "success", "message": "Internal Server Error, Try Again.."})


    return jsonify({"status": "success", "message": "Application submitted successfully"})


@user.route("/get-history", methods = ["GET"])
@roles_required("student")
def user_get_history():
    email = get_jwt_identity()

    student = Student.query.filter_by(email = email).first()
    id = student.id 

    history = db.session.query(
        Application.id.label('application_id'),
        Application.application_date,
        Application.status,
        Application.remarks,
        PlacementDrive.id.label('drive_id'),
        PlacementDrive.job_title,
        PlacementDrive.company_id,
        Company.name.label('company_name')
    ).join(PlacementDrive, Application.drive_id == PlacementDrive.id) \
    .join(Company, PlacementDrive.company_id == Company.id) \
    .filter(Application.student_id == id) \
    .all()

    data = [row._asdict() for row in history]

    return jsonify({"status" : "success", "message": "Data fetched Success" , "data" :data})


@user.route("/export-placement-records", methods = ["GET"])
@roles_required("student")
def export_placement_records():
    email = get_jwt_identity()

    student = Student.query.filter_by(email = email).first()
    id = student.id

    from services.tasks import user_export_applications, task1

    user_export_applications.delay(id, email)
    # task1.delay()

    return jsonify({"status" : "success", "message": "Report Generated Successfully, Check Your Mail.."})



@user.route("/get-company/<int:id>" , methods = ["GET"])
@roles_required("student")
def get_company(id):
    company = Company.query.filter_by(id = id).first()
    if not company.status == "Approved":
        return jsonify({"status" : "error" , "message" : "You are not Authorized to view this Company"})
    

    drives = db.session.query(
        PlacementDrive.id,
        PlacementDrive.job_title,
        PlacementDrive.status,
        PlacementDrive.application_deadline
    ).filter_by(company_id = id , status = "Approved").all()


    company_data = {"status" :company.status,  "name": company.name, "email" : company.email, "website" : company.website, "description" : company.description, "address" : company.address, "hr_name" : company.hr_name, "hr_phone" : company.hr_phone_number, "hr_email" : company.hr_email}
    active_drives = []


    for drive in drives:
        if drive.status == "Approved" and drive.application_deadline > datetime.now():
            active_drives.append({"id" : drive.id , "job_title" : drive.job_title, "status" : drive.status})
    

    return jsonify({"status" : "success" , "message" : "Company data fetched Successfully." , "data": {"companyData" : company_data, "active_drives" : active_drives}})


    


@user.route("/search" , methods = ["GET"])
@roles_required("admin", "student")
def search():
    claims = get_jwt()
    role = claims.get("role")
    q = request.args.get("q", "")

    if role == "admin":
        students = Student.query.filter(
            Student.full_name.ilike(f"%{q}%")
        ).limit(20).all()

        companies = Company.query.filter(
            Company.name.ilike(f"%{q}%")
        ).limit(20).all()

        drives = PlacementDrive.query.filter(
            PlacementDrive.job_title.ilike(f"%{q}%")
        ).limit(20).all()
        
        data = {"students" : [{"id" : student.id, "name" : student.full_name} for student in students] , "drives" :[{"id":drive.id, "job_title" : drive.job_title} for drive in drives], "companies" : [{"id": company.id, "name" :company.name} for company in companies]}
        return jsonify({"status" : "success" , "message" : "searched Resulted Fetched..", "data" :data, "role" : "admin"})

    
    if role == "student":
        current_time = datetime.now()

        # 1. Fetch only Approved Companies
        companies = Company.query\
            .filter(Company.name.ilike(f"%{q}%"), Company.status == "Approved")\
            .limit(20)\
            .all()

        # 2. Fetch Approved Drives whose deadline is in the future AND belong to Approved Companies
        drives = PlacementDrive.query\
            .join(Company, PlacementDrive.company_id == Company.id)\
            .filter(
                PlacementDrive.job_title.ilike(f"%{q}%"),
                PlacementDrive.status == "Approved",
                PlacementDrive.application_deadline >= current_time, # Deadline not passed
                Company.status == "Approved"                        # Company must be approved
            )\
            .limit(20)\
            .all()

        data = {
            "students": [], 
            "drives" : [{"id": d.id, "job_title" : d.job_title} for d in drives],  
            "companies" : [{"id": c.id, "name" : c.name} for c in companies]
        }

        return jsonify({"status" : "success" , "message" : "searched Resulted Fetched..", "data" :data, "role" : "student"})



    return jsonify({"status" : "success" , "message" : "No Data to Search"})