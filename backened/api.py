from .modals import db, Admin, Professional, Customer
from flask_restful import Api, Resource
from flask import request, jsonify

api = Api()


class AdminApi(Resource):

    def get(self):
        admins = Admin.query.all()
        admin_list = [
            {"admin_id": admin.id, "email": admin.email, "password": admin.password}
            for admin in admins
        ]
        return admin_list, 200

    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400
        if Admin.query.filter_by(email=email).first():
            return {"message": "Admin already exists"}, 409

        admin = Admin(email=email, password=password)
        db.session.add(admin)
        db.session.commit()
        return {"message": "Admin created successfully"}, 201

    def put(self, id):
        admin = Admin.query.get(id)
        if not admin:
            return {"message": "Admin not found"}, 404
        data = request.get_json()
        admin.email = data.get("email", admin.email)
        admin.password = data.get("password", admin.password)
        db.session.commit()
        return {"message": "Admin updated successfully"}, 200

    def delete(self, id):
        admin = Admin.query.get(id)
        if not admin:
            return {"message": "Admin not found"}, 404
        db.session.delete(admin)
        db.session.commit()
        return {"message": "Admin deleted successfully"}, 200


class ProfessionalApi(Resource):
    def get(self):
        profs = Professional.query.all()
        profs_list = [
            {
                "id": prof.id,
                "name": prof.name,
                "email": prof.email,
                "pwd": prof.password,
                "service": prof.service_type,
                "address": prof.address,
                "pincode": prof.pincode,
                "phone": prof.phone,
                "desc": prof.description,
                "file_path": prof.file_path,
                "exp": prof.experience,
                "status": prof.status,
            }
            for prof in profs
        ]
        return profs_list, 200

    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("pwd")
        experience = data.get("exp")
        service_type = data.get("service")
        address = data.get("address")
        pincode = data.get("pincode")
        phone = data.get("phone")
        description = data.get("desc")
        file_path = data.get("file_path")

        prof_exist = Professional.query.filter_by(email=email).first()
        if prof_exist:
            return {"message": "Professional already exists"}, 409

        prof = Professional(
            name=name,
            email=email,
            password=password,
            service_type=service_type,
            address=address,
            pincode=pincode,
            phone=phone,
            description=description,
            file_path=file_path,
            experience=experience,
        )
        db.session.add(prof)
        db.session.commit()
        return {"message": "Professional added successfully"}, 201

    def put(self, id):
        prof = Professional.query.get(id)
        if prof:
            data = request.get_json()
            prof.name = data.get("name")
            prof.email = data.get("email")
            prof.password = data.get("pwd")
            prof.service_type = data.get("service")
            prof.address = data.get("address")
            prof.pincode = data.get("pincode")
            prof.phone = data.get("phone")
            prof.description = data.get("desc")
            prof.file_path = data.get("file_path")
            prof.experience = data.get("exp")
            db.session.commit()
            return {"message": "Professional updated successfully"}, 200
        else:
            return {"message": "Professional not found"}, 404

    def delete(self, id):
        prof = Professional.query.get(id)
        if prof:
            db.session.delete(prof)
            db.session.commit()
            return {"message": "Professional deleted successfully"}, 200
        else:
            return {"message": "Professional not found"}, 404


class SearchProfessional(Resource):
    def get(self, id):
        prof = Professional.query.get(id)
        if prof:
            return {
                "id": prof.id,
                "name": prof.name,
                "email": prof.email,
                "pwd": prof.password,
                "service": prof.service_type,
                "address": prof.address,
                "pincode": prof.pincode,
                "phone": prof.phone,
                "desc": prof.description,
                "file_path": prof.file_path,
                "exp": prof.experience,
                "status": prof.status,
            }, 200
        return {"message": "Professional not found"}, 404


class CustomerApi(Resource):
    def get(self):
        customers = Customer.query.all()
        customers_list = [
            {
                "id": c.id,
                "email": c.email,
                "pwd": c.password,
                "name": c.name,
                "phone": c.phone,
                "address": c.address,
                "pincode": c.pincode,
                "status": c.status,
            }
            for c in customers
        ]
        return customers_list, 200

    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        pwd = data.get("pwd")
        phone = data.get("phone")
        address = data.get("address")
        pincode = data.get("pincode")
        if Customer.query.filter_by(email=email).first():
            return {"message": "Customer already exists"}, 409
        else:
            customer = Customer(
                name=name,
                email=email,
                password=pwd,
                phone=phone,
                address=address,
                pincode=pincode,
            )
            db.session.add(customer)
            db.session.commit()
            return {"message": "Customer created successfully"}, 201

    def put(self, id):
        customer = Customer.query.get(id)
        if customer:
            data = request.get_json()
            customer.name = data.get("name")
            customer.email = data.get("email")
            customer.password = data.get("pwd")
            customer.phone = data.get("phone")
            customer.address = data.get("address")
            customer.pincode = data.get("pincode")
            db.session.commit()
            return {"message": "Customer updated successfully"}, 200
        else:
            return {"message": "Customer not found"}, 404

    def delete(self, id):
        customer = Customer.query.get(id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return {"message": "Customer deleted successfully"}, 200
        else:
            return {"message": "Customer not found"}, 404


api.add_resource(AdminApi, "/api/admins", "/api/admins/<int:id>")
api.add_resource(ProfessionalApi, "/api/professionals", "/api/professionals/<int:id>")
api.add_resource(SearchProfessional, "/api/search_professional/<int:id>")
api.add_resource(CustomerApi, "/api/customer", "/api/customer/<int:id>")
