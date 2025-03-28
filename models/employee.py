from database import db
from datetime import datetime
import re
from werkzeug.security import generate_password_hash

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    position = db.Column(db.String(50), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    security_license = db.Column(db.String(50), nullable=False)
    license_expiry = db.Column(db.DateTime)
    clearance_level = db.Column(db.String(20), default='BASIC')
    employment_type = db.Column(db.String(20), default='FULL_TIME')
    emergency_contact = db.Column(db.String(100), nullable=False)
    emergency_phone = db.Column(db.String(20), nullable=False)
    bank_account = db.Column(db.String(50), nullable=False)
    bank_routing = db.Column(db.String(20), nullable=False)
    tax_id = db.Column(db.String(20))
    benefits_enrolled = db.Column(db.Boolean, default=False)
    uniform_size = db.Column(db.String(10))
    last_training_date = db.Column(db.DateTime)
    
    shifts = db.relationship('Shift', backref='employee', lazy=True)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def validate_bank_account(self):
        """Validate bank account format (digits only)"""
        return re.match(r'^\d+$', self.bank_account) is not None

    def validate_routing_number(self):
        """Validate routing number format (9 digits)"""
        return re.match(r'^\d{9}$', self.bank_routing) is not None

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_years_of_service(self):
        return (datetime.utcnow() - self.hire_date).days // 365

    def is_license_valid(self):
        return self.license_expiry > datetime.utcnow() if self.license_expiry else False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.get_full_name(),
            'position': self.position,
            'hourly_rate': self.hourly_rate,
            'hire_date': self.hire_date.isoformat(),
            'security_license': self.security_license,
            'clearance_level': self.clearance_level,
            'employment_type': self.employment_type,
            'bank_account_last4': self.bank_account[-4:],
            'is_active': self.is_active,
            'license_valid': self.is_license_valid()
        }
