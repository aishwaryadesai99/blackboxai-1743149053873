from datetime import datetime, timedelta
from models.employee import Employee
from models.shift import Shift
from config import Config

class PayCalculator:
    def __init__(self):
        self.overtime_rate = Config.OVERTIME_RATE
        self.holiday_rate = Config.HOLIDAY_RATE
        self.tax_rate = Config.TAX_RATE

    def calculate_regular_pay(self, employee, hours, shift_type='DAY'):
        base_rate = employee.hourly_rate
        # Apply night shift differential (20% more)
        if shift_type == 'NIGHT':
            base_rate *= 1.2
        return base_rate * hours

    def calculate_overtime_pay(self, employee, hours, shift_type='DAY'):
        base_rate = employee.hourly_rate
        # Apply night shift differential to overtime too
        if shift_type == 'NIGHT':
            base_rate *= 1.2
        return base_rate * self.overtime_rate * hours

    def calculate_holiday_pay(self, employee, hours, shift_type='DAY'):
        base_rate = employee.hourly_rate
        # Apply night shift differential to holiday pay
        if shift_type == 'NIGHT':
            base_rate *= 1.2
        return base_rate * self.holiday_rate * hours

    def calculate_gross_pay(self, employee, period_start, period_end):
        from app import create_app
        app = create_app()
        with app.app_context():
            print(f"Calculating gross pay for employee {employee.id} from {period_start} to {period_end}")
            shifts = Shift.query.filter(
                Shift.employee_id == employee.id,
                Shift.date >= period_start,
                Shift.date <= period_end
            ).all()
            print(f"Found {len(shifts)} shifts in period")

            total_pay = 0.0
            for shift in shifts:
                effective_hours = shift.calculate_total_hours()
                print(f"Processing shift: {shift.date} - {effective_hours} effective hours (Type: {shift.shift_type}, Location: {shift.location})")

                if shift.date.weekday() >= 5:  # Weekend
                    pay = self.calculate_holiday_pay(employee, effective_hours, shift.shift_type)
                    print(f"Weekend shift - holiday pay: {pay}")
                    total_pay += pay
                elif effective_hours > 8:  # Overtime
                    regular_hours = 8
                    overtime_hours = effective_hours - 8
                    regular_pay = self.calculate_regular_pay(employee, regular_hours, shift.shift_type)
                    overtime_pay = self.calculate_overtime_pay(employee, overtime_hours, shift.shift_type)
                    print(f"Overtime shift - regular: {regular_pay}, overtime: {overtime_pay}")
                    total_pay += regular_pay + overtime_pay
                else:
                    pay = self.calculate_regular_pay(employee, effective_hours, shift.shift_type)
                    print(f"Regular shift - pay: {pay}")
                    total_pay += pay

            print(f"Total gross pay: {total_pay}")
            return total_pay

    def calculate_net_pay(self, gross_pay):
        tax = gross_pay * self.tax_rate
        return gross_pay - tax