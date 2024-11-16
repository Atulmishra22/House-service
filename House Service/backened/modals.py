from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Professional(db.Model):
    __tablename__ = "professional"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.Text, nullable=True)
    service_type = db.Column(db.String(120), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default="pending")
    service_requests = db.relationship(
        "ServiceRequest",
        backref="professional",
        lazy=True,
        cascade="all, delete-orphan",
    )


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    service_requests = db.relationship(
        "ServiceRequest", backref="customer", lazy=True, cascade="all, delete-orphan"
    )
    reviews = db.relationship(
        "Review", backref="customer", lazy=True, cascade="all, delete-orphan"
    )


class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_requests = db.relationship(
        "ServiceRequest", backref="service", lazy=True, cascade="all, delete-orphan"
    )


class ServiceRequest(db.Model):
    __tablename__ = "service_request"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    professional_id = db.Column(
        db.Integer, db.ForeignKey("professional.id"), nullable=False
    )
    date_of_request = db.Column(db.DateTime, default=datetime.now())
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(50), nullable=False, default="requested")
    remarks = db.Column(db.Text, nullable=True)
    reviews = db.relationship(
        "Review", backref="service_request", lazy=True, cascade="all, delete-orphan"
    )


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(
        db.Integer, db.ForeignKey("service_request.id"), nullable=False
    )
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
