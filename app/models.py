from app import db
from datetime import datetime

# ✅ Define Customer first
class Customer(db.Model):
    __tablename__ = 'customers'  # optional, but explicit
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    street = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Customer {self.name}>'
    
# ✅ Now define Job second
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    job_date = db.Column(db.Date)
    service_type = db.Column(db.String(100))
    status = db.Column(db.String(50))
    price = db.Column(db.Float)
    notes = db.Column(db.Text)

    customer = db.relationship('Customer', backref=db.backref('jobs', lazy=True))

    def __repr__(self):
        return f'<Job {self.service_type} for Customer {self.customer_id}>'