from database.database import db 
from datetime import datetime, timezone 

from database.database import db
from datetime import datetime, timezone


#verified
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)


#verified
class Application(db.Model):
    __tablename__ = 'applications'
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='uix_student_drive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)

    application_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    status = db.Column(db.Enum('Applied', 'Shortlisted', 'Selected', 'Rejected'), default='Applied', nullable=False, index=True)
    
    
    remarks = db.Column(db.Text, nullable=True)


#verified
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(512), nullable=False)

    address = db.Column(db.String(100), nullable=True)

    status = db.Column(db.Enum('active', 'blocked'), default='active', nullable=False, index=True)


    # Eligibility Fields
    branch = db.Column(db.String(50), nullable=True)
    cgpa = db.Column(db.Float, nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    resume_link = db.Column(db.String(512), nullable=True)

    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)


#verified
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending', nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(100), nullable=True)


    #hr_details
    hr_name = db.Column(db.String(100), nullable=False)
    hr_phone_number = db.Column(db.String(20), nullable=False)
    hr_email = db.Column(db.String(120), nullable=False)

    # Relationships
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)



#verified
class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)

    # Eligibility Criteria
    eligible_branches = db.Column(db.String(255), nullable=False)  # e.g., "CSE, IT, ECE"
    min_cgpa = db.Column(db.Float, nullable=False)
    eligible_year = db.Column(db.Integer, nullable=False)

    application_deadline = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending', nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    applications = db.relationship('Application', backref='drive', lazy=True)
