from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Job, Customer
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def list_customers():
    search = request.args.get('q')
    if search:
        customers = Customer.query.filter(Customer.name.ilike(f"%{search}%")).all()
    else:
        customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET','POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        new_customer = Customer(
            name=name, email=email, phone=phone,
            street=street, city=city, state=state, zipcode=zipcode
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('list_customers'))
    return render_template('add_customer.html')

@app.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        db.session.commit()
        return redirect(url_for('list_customers'))

    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/<int:customer_id>/delete', methods=['GET'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('list_customers'))

@app.route('/jobs')
def list_jobs():
    jobs = Job.query.all()
    return render_template('jobs/jobs.html', jobs=jobs)

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        service_type = request.form.get('service_type')
        job_date = request.form.get('job_date')  # 👈 Update here
        status = request.form.get('status')
        price = request.form.get('price')
        notes = request.form.get('notes')

        print("DEBUG: job_date =", job_date)
        print("DEBUG: full request.form =", request.form)

        job = Job(
            customer_id=customer_id,
            service_type=service_type,
            job_date=datetime.strptime(job_date, '%Y-%m-%d'),
            status=status,
            price=float(price) if price else None,
            notes=notes
        )
        db.session.add(job)
        db.session.commit()
        if not job_date:
            return "Error: job_date is missing from the form submission", 400
        return redirect(url_for('list_jobs'))

    customers = Customer.query.all()
    return render_template('jobs/add_job.html', customers=customers)


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    customers = Customer.query.all()

    if request.method == 'POST':
        job.customer_id = request.form.get('customer_id')
        job.service_type = request.form.get('service_type')
        job.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        job.status = request.form.get('status')
        db.session.commit()
        return redirect(url_for('list_jobs'))

    return render_template('jobs/edit_job.html', job=job, customers=customers)

@app.route('/jobs/delete/<int:job_id>')
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('list_jobs'))

