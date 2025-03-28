from flask import Blueprint, jsonify, request
from models.employee import Employee
from models.shift import Shift
from services.pay_calculator import PayCalculator
from datetime import datetime, timedelta
from database import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/employees')
def list_employees():
    employees = Employee.query.filter_by(is_active=True).all()
    return jsonify([e.to_dict() for e in employees])

@main_bp.route('/employees/<int:employee_id>')
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify(employee.to_dict())

@main_bp.route('/shifts', methods=['GET', 'POST'])
def manage_shifts():
    if request.method == 'POST':
        data = request.get_json()
        try:
            shift = Shift(
                employee_id=data['employee_id'],
                start_time=datetime.fromisoformat(data['start_time']),
                end_time=datetime.fromisoformat(data['end_time']),
                hours_worked=float(data['hours_worked']),
                date=datetime.fromisoformat(data['date']).date(),
                shift_type=data.get('shift_type', 'DAY'),
                location=data['location'],
                break_time=float(data.get('break_time', 0.0))
            )
            db.session.add(shift)
            db.session.commit()
            return jsonify({'message': 'Shift created successfully', 'id': shift.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # GET request
    employee_id = request.args.get('employee_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Shift.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if start_date:
        query = query.filter(Shift.date >= datetime.fromisoformat(start_date).date())
    if end_date:
        query = query.filter(Shift.date <= datetime.fromisoformat(end_date).date())
    
    shifts = query.all()
    return jsonify([{
        'id': s.id,
        'employee_id': s.employee_id,
        'date': s.date.isoformat(),
        'start_time': s.start_time.isoformat(),
        'end_time': s.end_time.isoformat(),
        'hours_worked': s.hours_worked,
        'effective_hours': s.calculate_total_hours(),
        'shift_type': s.shift_type,
        'location': s.location
    } for s in shifts])

@main_bp.route('/payroll/<int:employee_id>')
def generate_payroll(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    calculator = PayCalculator()
    period_end = datetime.utcnow().date()
    period_start = period_end - timedelta(days=14)

    gross_pay = calculator.calculate_gross_pay(employee, period_start, period_end)
    net_pay = calculator.calculate_net_pay(gross_pay)

    return jsonify({
        'employee': employee.to_dict(),
        'period': f"{period_start} to {period_end}",
        'gross_pay': round(gross_pay, 2),
        'tax': round(gross_pay * calculator.tax_rate, 2),
        'net_pay': round(net_pay, 2),
        'currency': 'USD'
    })
