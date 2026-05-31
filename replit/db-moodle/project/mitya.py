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

###########################################################################

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
