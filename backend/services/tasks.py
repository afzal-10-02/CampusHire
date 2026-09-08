from services.celery import celery_app
from services.mail import send_email
from database.database import db
from database.models import Application,Student, Company, PlacementDrive, Admin
import io 
import csv
from flask import render_template
from datetime import datetime, timedelta


@celery_app.task
def user_export_applications(id, email):
    student = Student.query.filter_by(id = id).first()
    
    data = db.session.query(
    Student.id,
    Company.name,
    PlacementDrive.id.label("placement_id"),
    PlacementDrive.job_title,
    Application.status,
    Application.remarks,
    Application.application_date) \
    .join(Application, Application.student_id == Student.id) \
    .join(PlacementDrive, PlacementDrive.id == Application.drive_id) \
    .join(Company, Company.id == PlacementDrive.company_id)\
    .filter(Student.id == id) \
    .all()

    if not data:
        send_email(
            recipient=email,
            subject="Student Placement Record.",
            html_body=f"<p>Dear {student.full_name} there is no Placement Records Available </p>",
            attachment=None
        )


    csv_bytes = generate_csv(data)
    send_email(
            recipient=email,
            subject="Student Placement Record.",
            html_body=render_template("student_history.html" ,student_name = student.full_name),
            attachment={"filename" : "PlacementDrive.csv", "content_type": "text/csv", "data": csv_bytes}
        )



    
@celery_app.task
def monthly_report():
    admin = Admin.query.filter_by(id = 1).first()
    admin_email = admin.email

    today = datetime.now()
    first_day_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    end_date = first_day_current_month
    last_month_prime = first_day_current_month - timedelta(days=1)
    start_date = last_month_prime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    drives_count = PlacementDrive.query.filter(
        PlacementDrive.created_at >= start_date,
        PlacementDrive.created_at < end_date
    ).count()

    applied_count = Application.query.filter(
        Application.application_date >= start_date,
        Application.application_date < end_date
    ).count()

    selected_count = Application.query.filter(
        Application.status.ilike("shortlisted"),  # Handles case-insensitive string lookups
        Application.application_date >= start_date,
        Application.application_date < end_date
    ).count()

    month_label = start_date.strftime("%B %Y")
    current_date = today.strftime("%Y-%m-%d")

    send_email(
        recipient=admin_email,
        subject=f"Placement Portal Activity Report — {month_label}",
        html_body=render_template(
            "monthly_report.html",
            month_label=month_label,
            current_date=current_date,
            drives_count=drives_count,
            applied_count=applied_count,
            selected_count=selected_count
        )
    )


@celery_app.task
def task1():
    send_email("afzalmuz2005@gmail.com",  "hello" , "<h1>hii </h1>")


@celery_app.task
def daily_drive_reminder():
    current_time = datetime.now()

    active_drives = db.session.query(
        PlacementDrive.status,
        PlacementDrive.job_title,
        PlacementDrive.application_deadline,
        Company.name, 
    ).join(Company, PlacementDrive.company_id == Company.id) \
    .filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.application_deadline >= current_time
    ).all()



    if not active_drives:
        return "No active drives available today. Reminder skipped."


    students = Student.query.filter_by(status="active").all()
    if not students:
        return "No active students found in the database."


    drives_list = []

    for drive in active_drives:
        
        drives_list.append({
            "job_title": drive.job_title,
            "company": drive.name,
            "deadline": drive.application_deadline.strftime("%d %b %Y, %I:%M %p")
        })

    sent_count = 0
    for student in students:
        if student.email:
            html_content = render_template(
                "daily_remainder.html",
                student_name=student.full_name,
                drives=drives_list
            )
            
            send_email(
                recipient=student.email,
                subject="🔥 Active Placement Drives Alert — CampusHire",
                html_body=html_content
            )
            sent_count += 1

    return f"Daily active drives notification delivered to {sent_count} students."






def generate_csv(data) -> bytes:

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # Header row
    writer.writerow(["Drive ID", "Job Title", "Company", "Status", "Remarks", "Application Date"])

    for row in data:
        writer.writerow([
            row.placement_id,
            row.job_title,
            row.name,
            row.status,
            row.remarks,
            row.application_date.strftime("%Y-%m-%d") if row.application_date else ""
        ])

    return buffer.getvalue().encode("utf-8")



