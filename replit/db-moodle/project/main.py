from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response, session, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
import os
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd
import csv
import xlwt
from io import BytesIO, StringIO
from functools import wraps

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db_session = Session()


##############LOGIN#########################################################

def check_auth(username, password):
    try:
        with open('secret.txt', 'r') as f:
            correct_login = f.read().strip()
        correct_username, correct_password = correct_login.split(':')
        return username == correct_username and password == correct_password
    except Exception as e:
        app.logger.error(f"Error reading secret file: {e}")
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password and check_auth(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return 'Вход выполнен!'
    
##############Vehicle#######################################################

class Vehicle(db.Model):
    __tablename__ = 'Транспорт'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    manufacture_year = db.Column(db.SmallInteger, nullable=False)
    start_year = db.Column(db.SmallInteger, nullable=False)

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    new_vehicle = Vehicle(
        number=data['number'],
        model=data['model'],
        manufacture_year=data['manufacture_year'],
        start_year=data['start_year']
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify({'message': 'Успешно сохранено'})

@app.route('/add_vehicle', methods=['GET'])
def add_vehicle_page():
    return render_template('add_vehicle.html')

@app.route('/edit_vehicle/<int:vehicle_id>', methods=['GET'])
def edit_vehicle_form(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template('edit_vehicle.html', vehicle=vehicle)

@app.route('/edit_vehicle/<int:vehicle_id>', methods=['POST'])
def update_vehicle(vehicle_id):
    data = request.form
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    try:
        vehicle.number = data['number']
        vehicle.model = data['model']
        vehicle.manufacture_year = int(data['manufacture_year'])
        vehicle.start_year = int(data['start_year'])
        db.session.commit()
        return redirect(url_for('get_vehicles'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating vehicle'}), 500

@app.route('/delete_vehicle/<int:vehicle_id>', methods=['GET'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('get_vehicles'))  

##############classes#######################################################

class Employee(db.Model):
    __tablename__ = 'Сотрудник'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    position = db.Column(db.Integer, db.ForeignKey('Должность.id'), nullable=False)
    rank = db.Column(db.Integer, db.ForeignKey('Звание.id'), nullable=False)

    certifications = db.relationship('Certification', backref='employee', lazy=True)
    training_sessions = db.relationship('TrainingSession', backref='employee', lazy=True)

class Position(db.Model):
    __tablename__ = 'Должность'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(255), nullable=False)

class Rank(db.Model):
    __tablename__ = 'Звание'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Certification(db.Model):
    __tablename__ = 'Аттестации'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('Сотрудник.id'), nullable=False)
    type = db.Column(db.Integer, db.ForeignKey('Виды_аттестации.id'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    no_attestation_reason = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)

class CertificationType(db.Model):
    __tablename__ = 'Виды_аттестации'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class TrainingSession(db.Model):
    __tablename__ = 'Занятия'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('Сотрудник.id'), nullable=False)
    exercise_type = db.Column(db.Integer, db.ForeignKey('Виды_занятий.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255), nullable=False)

class ExerciseType(db.Model):
    __tablename__ = 'Виды_занятий'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class TrainingReport(db.Model):
    __tablename__ = 'Отчет_по_занятиям'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    finish_date = db.Column(db.Date, nullable=False)
    count_plan = db.Column(db.SmallInteger, nullable=False)
    count_reason = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.Text, nullable=True)


@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session.get('username'))



##############employees####################################################

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    new_employee = Employee(
        last_name=data['last_name'],
        first_name=data['first_name'],
        middle_name=data.get('middle_name'),
        birthday=date.fromisoformat(data['birthday']),
        position=data['position'],
        rank=data['rank']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'message': 'Успешно сохранено'})

@app.route('/add_employee', methods=['GET'])
def add_employee_page():
    return render_template('add_employee.html')


@app.route('/edit_employee/<int:employee_id>', methods=['GET'])
def edit_employee_form(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('edit_employee.html', employee=employee)

@app.route('/edit_employee/<int:employee_id>', methods=['POST'])
def update_employee(employee_id):
    data = request.form
    employee = Employee.query.get_or_404(employee_id)
    app.logger.debug(f"Received data for update: {data}")
    try:
        employee.last_name = data['last_name']
        employee.first_name = data['first_name']
        employee.middle_name = data.get('middle_name')
        employee.birthday = date.fromisoformat(data['birthday'])
        employee.position = data['position']
        employee.rank = data['rank']
        db.session.commit()
        return redirect(url_for('get_employees'))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error updating employee: {e}")
        return jsonify({'message': 'Error updating employee'}), 500

@app.route('/delete_employee/<int:employee_id>', methods=['GET'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('get_employees'))

@app.route('/employees/download', methods=['GET'])
def download_employees():
    employees = Employee.query.all()

    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Employees')

    headers = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Должность', 'Звание']
    for col_num, header in enumerate(headers):
        sheet.write(0, col_num, header)

    for row_num, employee in enumerate(employees, start=1):
        sheet.write(row_num, 0, employee.id)
        sheet.write(row_num, 1, employee.last_name)
        sheet.write(row_num, 2, employee.first_name)
        sheet.write(row_num, 3, employee.middle_name)
        sheet.write(row_num, 4, employee.birthday.strftime('%Y-%m-%d'))
        sheet.write(row_num, 5, employee.position)
        sheet.write(row_num, 6, employee.rank)

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype='application/vnd.ms-excel', headers={'Content-Disposition': 'attachment;filename=employees.xls'})

##############certification################################################

@app.route('/certifications/list', methods=['GET'])
def list_certifications():
    certifications = Certification.query.all()
    return render_template('certifications.html', certifications=certifications)

@app.route('/certifications/edit/<int:certification_id>', methods=['GET'])
def edit_certification_form(certification_id):
    certification = Certification.query.get_or_404(certification_id)
    return render_template('edit_certification.html', certification=certification)

@app.route('/certifications/edit/<int:certification_id>', methods=['POST'])
def update_certification(certification_id):
    certification = Certification.query.get_or_404(certification_id)
    certification.employee_id = request.form['employee_id']
    certification.type = request.form['type']
    certification.status = 'status' in request.form
    certification.no_attestation_reason = request.form['no_attestation_reason']
    certification.date = date.fromisoformat(request.form['date'])
    db.session.commit()
    return redirect(url_for('list_certifications'))

@app.route('/add_certification', methods=['GET'])
def add_certification_page():
    return render_template('add_certification.html')

@app.route('/certifications', methods=['POST'])
def create_certification():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    new_certification = Certification(
        employee_id=data['employee_id'],
        type=data['type'],
        status=data['status'],
        no_attestation_reason=data.get('no_attestation_reason'),
        date=date.fromisoformat(data['date'])
    )
    db.session.add(new_certification)
    db.session.commit()
    return jsonify({'message': 'Certification added successfully'})

@app.route('/delete_certification/<int:certification_id>', methods=['GET'])
def delete_certification(certification_id):
    certification = Certification.query.get_or_404(certification_id)
    db.session.delete(certification)
    db.session.commit()
    return redirect(url_for('list_certifications'))

@app.route('/certification/download', methods=['GET'])
def download_certification():
    certifications = session.query(Certification).all()

    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Certifications')

    headers = ['ID', 'ID сотрудника', 'Вид аттестации', 'Статус', 'Причина отсутствия аттестации', 'Дата']
    for col_num, header in enumerate(headers):
        sheet.write(0, col_num, header)

    for row_num, certification in enumerate(certifications, start=1):
        sheet.write(row_num, 0, certification.id)
        sheet.write(row_num, 1, certification.employee_id)
        sheet.write(row_num, 2, certification.type)
        sheet.write(row_num, 3, "Пройдено" if certification.status else "Не пройдено")
        sheet.write(row_num, 4, certification.no_attestation_reason)
        sheet.write(row_num, 5, certification.date.strftime('%Y-%m-%d'))

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype='application/vnd.ms-excel', headers={'Content-Disposition': 'attachment;filename=certifications.xls'})

##############Dispatch#####################################################

class Dispatch(db.Model):
    __tablename__ = 'Выезды'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # в минутах
    lead_employee_id = db.Column(db.Integer, db.ForeignKey('Сотрудник.id'), nullable=False)
    rescued_count = db.Column(db.Integer, nullable=False, default=0)
    evacuated_count = db.Column(db.Integer, nullable=False, default=0)
    work_date = db.Column(db.Date, nullable=False)
    work_type = db.Column(db.String(100), nullable=False)
    work_address = db.Column(db.String(255), nullable=False)
    fire_rank = db.Column(db.Integer, nullable=False)

    lead_employee = db.relationship('Employee', backref=db.backref('dispatches', lazy=True))

@app.route('/dispatches', methods=['GET'])
def list_dispatches_page():
    dispatches = Dispatch.query.all()
    return render_template('dispatch.html', dispatches=dispatches)

@app.route('/dispatches', methods=['POST'])
def create_dispatch():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    new_dispatch = Dispatch(
        number=data['number'],
        duration=data['duration'],
        lead_employee_id=data['lead_employee_id'],
        rescued_count=data['rescued_count'],
        evacuated_count=data['evacuated_count'],
        work_date=date.fromisoformat(data['work_date']),
        work_type=data['work_type'],
        work_address=data['work_address'],
        fire_rank=data['fire_rank']
    )
    db.session.add(new_dispatch)
    db.session.commit()
    return jsonify({'message': 'Dispatch added successfully'})

@app.route('/add_dispatch', methods=['GET'])
def add_dispatch_page():
    return render_template('add_dispatch.html')

@app.route('/delete_dispatch/<int:dispatch_id>', methods=['GET'])
def delete_dispatch(dispatch_id):
    dispatch = Dispatch.query.get_or_404(dispatch_id)
    db.session.delete(dispatch)
    db.session.commit()
    return redirect(url_for('list_dispatches_page'))

@app.route('/dispatch/download', methods=['GET'])
def download_dispatch():
    dispatches = Dispatch.query.all()

    output = io.BytesIO()
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Dispatch')

    headers = ['ID', 'Номер', 'Продолжительноть (в минутах)', 'ID сотрудника', 'Кол-во спасенных', 'Кол-во эвакуированных', 'Дата работы', 'Тип работы', 'Адрес места работы', 'Ранг пожара', 'Действия']

    for col_num, header in enumerate(headers):
        sheet.write(0, col_num, header)

    for row_num, dispatch in enumerate(dispatches, start=1):
        sheet.write(row_num, 0, dispatch.id)
        sheet.write(row_num, 1, dispatch.number)
        sheet.write(row_num, 2, dispatch.duration)
        sheet.write(row_num, 3, dispatch.lead_employee_id)
        sheet.write(row_num, 4, dispatch.rescued_count)
        sheet.write(row_num, 5, dispatch.evacuated_count)
        sheet.write(row_num, 6, dispatch.work_date)
        sheet.write(row_num, 7, dispatch.work_type)
        sheet.write(row_num, 8, dispatch.work_address)
        sheet.write(row_num, 9, dispatch.fire_rank)

    workbook.save(output)
    output.seek(0)

    return Response(output, mimetype='application/vnd.ms-excel', headers={'Content-Disposition': 'attachment;filename=dispatches.xls'})

@app.route('/edit_dispatch/<int:dispatch_id>', methods=['GET'])
def edit_dispatch_form(dispatch_id):
    dispatch = Dispatch.query.get_or_404(dispatch_id)
    return render_template('edit_dispatch.html', dispatch=dispatch)

@app.route('/edit_dispatch/<int:dispatch_id>', methods=['POST'])
def update_dispatch(dispatch_id):
    data = request.form
    dispatch = Dispatch.query.get_or_404(dispatch_id)
    app.logger.debug(f"Received data for update: {data}")
    try:
        dispatch.number = data['number']
        dispatch.duration = data['duration']
        dispatch.lead_employee_id = data['lead_employee_id']
        dispatch.rescued_count = data['rescued_count']
        dispatch.evacuated_count = data['evacuated_count']
        dispatch.work_date = date.fromisoformat(data['work_date'])
        dispatch.work_type = data['work_type']
        dispatch.work_address = data['work_address']
        dispatch.fire_rank = data['fire_rank']
        db.session.commit()
        return redirect(url_for('get_dispatches'))
    except Exception as e:
        db.session.rollback()
        return redirect(url_for('list_dispatches_page'))

###########################################################################

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
