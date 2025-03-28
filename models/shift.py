from database import db
from datetime import datetime

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    hours_worked = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    shift_type = db.Column(db.String(20), default='DAY')  # DAY or NIGHT
    location = db.Column(db.String(100), nullable=False)
    break_time = db.Column(db.Float, default=0.0)  # Break time in hours

    def __repr__(self):
        return f'<Shift {self.id} for Employee {self.employee_id}>'

    def calculate_total_hours(self):
        """Calculate total hours worked including break time"""
        return self.hours_worked - self.break_time if self.hours_worked > self.break_time else 0
