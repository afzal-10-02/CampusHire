from flask import Blueprint, jsonify, request
from database.models import Company, PlacementDrive, Student, Application
from database.database import db
from controllers.auth import roles_required
from datetime import datetime
from flask_jwt_extended import get_jwt, get_jwt_identity
from services.cache import cache


admin = Blueprint('admin', __name__)




@admin.route("/approve-company/<int:id>", methods = ["PATCH"])
@roles_required('admin')
def approve_company(id):

    company = Company.query.filter_by(id= id).first()
    if not company:
        return jsonify({"status" : "error" , "message" : "No Company Found With given Id."})

    if company.status == "Approved":
        return jsonify({"status" : "error" , "message" : "Company Already Approved."})

    try:
        company.status = "Approved"
        db.session.commit()
            
    except Exception as e:
        print(e)
        return jsonify({"status" : "error" , "message" : "Internal Server Error. Try Again!"})

    return jsonify({"status" : "success" , "message" : "Company Approved."})



@admin.route("/reject-company/<int:id>" , methods = ["PATCH"])
@roles_required("admin")
def reject_company(id):

    company = Company.query.filter_by(id= id).first()
    if not company:
        return jsonify({"status" : "error" , "message" : "No Company Found With given Id."})

    if company.status == "Rejected":
        return jsonify({"status" : "error" , "message" : "Company Already Rejected."})

    try:
        company.status = "Rejected"
        db.session.commit()
            
    except Exception as e:
        print(e)
        return jsonify({"status" : "error" , "message" : "Internal Server Error. Try Again!"})

    return jsonify({"status" : "success" , "message" : "Company Rejected."})



@admin.route("/approve-drive/<int:id>" , methods = ["PUT"])
@roles_required('admin')
def approve_drive(id):
    drive = PlacementDrive.query.filter_by(id = id).first()

    if not drive:
        return jsonify({"status" : "error" , "message" : "No Drive Exits With Given Id."})

    if drive.status == "Approved":
        return jsonify({"status" : "error" , "message" : "The Given Drive is Already Approved."})

    try:
        drive.status = "Approved"
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"status" : "error" , "message" : "Internal Sever Error. Try Again!"})

    return jsonify({"status" : "success" , "message" : "Placement Drive Approved."})



@admin.route("/block-drive/<int:id>" , methods = ["PUT"])
@roles_required('admin')
def block_drive(id):
    drive = PlacementDrive.query.filter_by(id = id).first()

    if not drive:
        return jsonify({"status" : "error" , "message" : "No Drive Exits With Given Id."})

    if drive.status == "Rejected":
        return jsonify({"status" : "error" , "message" : "The Given Drive is Already Blocked."})

    try:
        drive.status = "Rejected"
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"status" : "error" , "message" : "Internal Sever Error. Try Again!"})

    return jsonify({"status" : "success" , "message" : "Placement Drive Blocked."})





@admin.route("/get-companies", methods=["GET"])
@roles_required('admin')
@cache.cached(timeout = 5)
def get_companies():

    
    companies = db.session.query(
            Company.id, 
            Company.name, 
        ).filter(Company.status == "Approved").all()

    approved = [{"id" : company.id , "name" : company.name} for company in companies]

    
    companies = db.session.query(
            Company.id, 
            Company.name, 
        ).filter(Company.status == "Pending").all()

    pending = [{"id" : company.id , "name" : company.name} for company in companies]


    companies = db.session.query(
            Company.id, 
            Company.name, 
        ).filter(Company.status == "Rejected").all()

    rejected = [{"id" : company.id , "name" : company.name} for company in companies]


    return jsonify({"status" : "success" , "message" : "Comapanies data successfully fetched." , "data" : {"approved" : approved , "pending" : pending, "rejected" : rejected }}), 200


@admin.route("/get-drives" , methods= ["GET"] , defaults={"company_id": None})
@admin.route("/get-drives/<int:company_id>" , methods= ["GET"] )
@roles_required('admin' , 'company')
def get_drives(company_id):
    claims = get_jwt()
    role = claims.get("role")


    if role == "company":
        company_email = get_jwt_identity()
        c = Company.query.filter_by(email = company_email).first()
        company_id = c.id

    if company_id is None:
        drives = db.session.query(
            PlacementDrive.id.label("placement_id"),
            PlacementDrive.job_title,
            PlacementDrive.status,
            PlacementDrive.application_deadline,
            Company.name
        ).join(Company, PlacementDrive.company_id == Company.id).all()

    else:
        drives = db.session.query(
            PlacementDrive.id.label("placement_id"),
            PlacementDrive.job_title,
            PlacementDrive.status,
            PlacementDrive.application_deadline,
            Company.id.label("company_id"),
            Company.name
        ).join(Company, PlacementDrive.company_id == Company.id) \
        .filter(PlacementDrive.company_id == company_id) \
        .all()

    approvedDrives = []
    rejectedDrives = []
    pendingDrives = []
    completedDrives = []

    for drive in drives:
        if drive.status == "Approved" and drive.application_deadline < datetime.now():
            completedDrives.append({"id": drive.placement_id, "name": drive.job_title, "companyName": drive.name})
        elif drive.status == "Approved":
            approvedDrives.append({"id": drive.placement_id, "name": drive.job_title, "companyName": drive.name})    
        elif drive.status == "Rejected":
            rejectedDrives.append({"id": drive.placement_id, "name": drive.job_title, "companyName": drive.name}) 
        else:
            pendingDrives.append({"id": drive.placement_id, "name": drive.job_title, "companyName": drive.name})



    return jsonify({"status" : "success", "message" : "Placement Drives data fetched Successfully", "data" : {"approvedDrives" : approvedDrives, "pendingDrives" : pendingDrives, "completedDrives" : completedDrives, "rejectedDrives" : rejectedDrives }})



@admin.route("/get-overview" , methods = ["GET"])
@roles_required("admin")
@cache.cached(timeout = 2)
def get_overview():
    companies_query = db.session.query(
        Company.status
    ).all()

    companies = {"approved" : 0, "pending" : 0 , "rejected" : 0, "total" : 0}

    for company in companies_query:
        company_status = company.status.lower()
        companies[company_status] += 1
        companies["total"] += 1


    drives_query = db.session.query(
        PlacementDrive.status,
        PlacementDrive.application_deadline
    ).all()

    drives = {"total" : 0, "active": 0, "completed" : 0, "pending" : 0, "rejected" : 0}
    for drive in drives_query:
        if drive.status == "Approved" and drive.application_deadline < datetime.now():
            drives["completed"] += 1
        elif drive.status == "Approved":
            drives["active"] += 1
        elif drive.status == "Pending":
            drives["pending"] += 1
        else:
            drives["rejected"] += 1
        drives["total"] += 1


    students_query = db.session.query(
        Student.status
    ).all()

    students ={"total" : 0, "blocked" :0, "active" : 0}
    for student in students_query:
        student_status = student.status.lower()
        students[student_status] += 1
        students["total"] += 1
    
    
    return jsonify({"status" : "success", "message" : "fetched Data Successfully" , "data" : {"companies" : companies, "drives" : drives, "students" : students}})




@admin.route("/get-students" , methods = ["GET"] , defaults = {"student_id" :None})
@admin.route("/get-students/<int:student_id>" , methods= ["GET"] )
@roles_required("admin")
def get_students(student_id):

    if student_id:
        try:
            student = db.session.query(
                Student.id,
                Student.full_name, 
                Student.status,
                Student.email,
                Student.roll_number,
                Student.branch,
                Student.cgpa,
                Student.graduation_year,
                Student.resume_link,
                Student.address
            ).filter(Student.id == student_id).first()

            applications = db.session.query(
                Application.id,
                Application.student_id,
                Application.status,
                PlacementDrive.job_title,
            ).join(PlacementDrive, Application.drive_id == PlacementDrive.id) \
            .filter(Application.student_id == student_id).all()


        except Exception as e:
            return jsonify({"status" : "error" , "message" : "Internal Server Error." })
        


        student_data = student._asdict()

        application_data = [{"id" : application.id, "job_title" :application.job_title, "status": application.status} for application in applications] 

        return jsonify({"status" :"success" , "message" : "Students data fetched Successfully.", "data" : student_data, "appliedDrives" : application_data})
    
    else:
        try:
            students = db.session.query(
                Student.id,
                Student.full_name,
                Student.status
            ).all()
        except Exception as e:
            return jsonify({"status" : "error" , "message" : "Internal Server Error." })

        active = []
        blocked = []

        for student in students:
            if student.status == "active":
                active.append({"id" : student.id , "full_name" : student.full_name})
            else:
                blocked.append({"id" : student.id , "full_name" : student.full_name})


        return jsonify({"status" :"success" , "message" : "Students data fetched Successfully.", "data" : {"active" : active, "blocked" : blocked}})


@admin.route("/block-student/<int:id>" , methods = ["PUT"])
@roles_required("admin")
def block_student(id):
    student = Student.query.filter_by(id=id).first()

    if not student:
            return jsonify({"status": "error", "message": "Student not found."}), 404

    try:
        student.status = "blocked"

        db.session.commit()
        return jsonify({"status" : "success" , "message" : "Student Blocked Successfully..."})

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"status" : "error" , "message" : "Internal Server Error, try Again..."})



@admin.route("/get-company/<int:id>", methods = ["GET"])
@roles_required("admin")
def getCompany(id):

    company = Company.query.filter_by(id = id).first()

    drives = db.session.query(
        PlacementDrive.id,
        PlacementDrive.job_title,
        PlacementDrive.status,
        PlacementDrive.application_deadline
    ).filter_by(company_id = id).all()

    company_data = {"status" :company.status,  "name": company.name, "email" : company.email, "website" : company.website, "description" : company.description, "address" : company.address, "hr_name" : company.hr_name, "hr_phone" : company.hr_phone_number, "hr_email" : company.hr_email}
    drive_data = {"active": [], "completed" : [], "pending" : [], "rejected" : []}

    for drive in drives:
        if drive.status == "Approved" and drive.application_deadline < datetime.now():
            drive_data["completed"].append({"id" : drive.id , "job_title" : drive.job_title, "status" : drive.status})
        elif drive.status == "Approved":
            drive_data["active"].append({"id" : drive.id , "job_title" : drive.job_title, "status" : drive.status})
        elif drive.status == "Pending":
            drive_data["pending"].append({"id" : drive.id , "job_title" : drive.job_title, "status" : drive.status})
        else:
            drive_data["rejected"].append({"id" : drive.id , "job_title" : drive.job_title, "status" : drive.status})
                


    return jsonify({"status" : "success" , "message" : "Company data fetched Successfully." , "data": {"companyData" : company_data, "placementData" : drive_data}})


@admin.route("/get-drive-details/<int:drive_id>" , methods = ["GET"])
@roles_required("admin", "company")
def get_drive_details(drive_id):
    claims = get_jwt()
    role = claims.get("role")
    
    drive = PlacementDrive.query.filter_by(id = drive_id).first()


    if role == "company":
        company_email = get_jwt_identity()
        company = Company.query.filter_by(email = company_email).first()
        company_id = company.id

        if drive.company_id != company_id:
            return jsonify({"status" : "error" , "message" : "Unauthorize access.."})
        
    students = db.session.query(
        Application.id,
        Application.student_id,
        Application.status,
        Application.drive_id,
        Student.full_name,
        Student.roll_number,
        Student.id
    ).join(Student, Application.student_id == Student.id) \
    .filter(Application.drive_id == drive_id) \
    .all()

    drive_details = {"id" : drive.id, "job_title" : drive.job_title, "job_description" : drive.job_description, "min_cgpa" :drive.min_cgpa, "eligible_year" : drive.eligible_year, "status" : drive.status, "application_deadline" :drive.application_deadline}
    applied_students = {"applied" : [], "shortlisted" : [] , "rejected" : []}
    numbers = {"total" : 0, "shortlisted" : 0 , "rejected" : 0, "pending" : 0}

    for student in students:
        if student.status == "Shortlisted":
            applied_students["shortlisted"].append({"name" : student.full_name, "roll_no" : student.roll_number, "id" : student.id})
            numbers["shortlisted"] += 1
        elif student.status == "Rejected":
            applied_students["rejected"].append({"name" : student.full_name, "roll_no" : student.roll_number, "id" : student.id})
            numbers["rejected"] += 1
        else:
            applied_students["applied"].append({"name" : student.full_name, "roll_no" : student.roll_number, "id" : student.id})
            numbers["pending"] += 1
        
        numbers['total'] += 1




    return jsonify({"status" : "success" , "message" : "data fetched Successfully", "drive_details" :drive_details, "applied_students" : applied_students , "numbers" : numbers})

