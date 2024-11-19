from flask import Flask, render_template, url_for, request, redirect, flash
from .modals import *
from .useful_function import *
from flask import current_app as app


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", defaults={"msg": ""}, methods=["GET", "POST"])
@app.route("/login/<msg>", methods=["GET", "POST"])
def login(msg):
    if request.method == "POST":
        user = request.form.get("user")
        usrname = request.form.get("usr_name")
        pwd = request.form.get("pass")
        if (
            user == "Admin"
            and Admin.query.filter_by(email=usrname, password=pwd).first()
        ):
            return redirect(url_for("adminDashboard"))
        elif user == "Professional":
            prof = Professional.query.filter_by(email=usrname, password=pwd).first()
            if prof:
                return redirect(url_for("professionalDashboard", id=prof.id))
            else:
                return render_template("login.html", msg="wrong credentials")
        elif user == "Customer":
            cust = Customer.query.filter_by(email=usrname, password=pwd).first()
            if cust:
                return redirect(url_for("customerDashboard", user=cust.name))
            else:
                return render_template("login.html", msg="wrong credentials")
        else:
            return render_template("login.html", msg="wrong credentials")
    return render_template("login.html", msg=msg)


@app.route("/<registerer>/register", methods=["GET", "POST"])
def register(registerer):
    if registerer == "professional":
        if request.method == "POST":
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            name = request.form.get("name")
            phone = request.form.get("phone")
            service = request.form.get("service")
            address = request.form.get("address")
            exp = request.form.get("exp")
            doc = request.form.get("doc")
            pin = request.form.get("pincode")
            usr = Professional.query.filter_by(email=email).first()
            if usr:
                return redirect(url_for("login", msg="this email is already in used"))
            else:
                user = Professional(
                    email=email,
                    password=pwd,
                    name=name,
                    phone=phone,
                    service_type=service,
                    experience=exp,
                    file_path=doc,
                    address=address,
                    pincode=pin
                )
                db.session.add(user)
                db.session.commit()
            return redirect(url_for("login", msg="sucessfully registered! now login"))
        services = Service.query.all()
        return render_template("professional_signup.html",services = services)
    else:
        if request.method == "POST":
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            name = request.form.get("name")
            phone = request.form.get('phone')
            address = request.form.get("address")
            pin = request.form.get("pin")
            usr = Customer.query.filter_by(email=email).first()
            if usr:
                return redirect(url_for("login", msg="this email is already in used"))
            else:
                user = Customer(
                    email=email, password=pwd, name=name, address=address, pincode=pin,phone = phone
                )
                db.session.add(user)
                db.session.commit()
            return redirect(url_for("login", msg="sucessfully registered! now login"))

        return render_template("customer_signup.html")


@app.route("/admin_dashboard")
def adminDashboard():
    sers = Service.query.all()
    ser_reqs = ServiceRequest.query.all()
    custmrs = Customer.query.all()
    profs = Professional.query.all()
    return render_template(
        "admin_dashboard.html",
        services=sers,
        service_requests=ser_reqs,
        customers=custmrs,
        professionals=profs,
    )


@app.route("/customer_dashboard/<user>")
def customerDashboard(user):
    cust = Customer.query.filter_by(name=user).first()
    ser = Service.query.all()
    ser_reqs = ServiceRequest.query.filter_by(customer_id=cust.id).all()
    return render_template(
        "customer_dashboard.html", customer=cust, services=ser, ser_reqs=ser_reqs
    )

@app.route('/professional_dashboard/<id>')
def professionalDashboard(id):
    prof = Professional.query.filter_by(id = id).first()
    ser_req = ServiceRequest.query.filter_by(professional_id=prof.id).all()
    return render_template('professional_dashboard.html', professional=prof, ser_req=ser_req)

@app.route("/dashboard/admin/search", methods=["GET", "POST"])
def search():
    search_query = request.args.get("search_query") or ""
    search_by = request.args.get("search_by") or ""
    if request.method == "POST":
        search_query = request.form.get("searched")
        search_by = request.form.get("search_by")
        return redirect(url_for('search',search_query=search_query,search_by=search_by))
    if search_by == "professionals":
        professionals = data_from_professional(search_query)
        return render_template("search.html", professionals=professionals, search_query=search_query, search_by=search_by)
    elif search_by == "service":
        services = data_from_service(search_query)
        return render_template("search.html", services=services, search_query=search_query, search_by=search_by)
    elif search_by == "customers":
        customers = data_from_customer(search_query)
        return render_template("search.html", customers=customers, search_query=search_query, search_by=search_by)
    elif search_by == "service-request":
        service_requests = data_from_servicerequest(search_query)
        return render_template("search.html", service_requests=service_requests, search_query=search_query, search_by=search_by)
    else:
        services = Service.query.all()
        return render_template(
            "search.html", search_by=search_by, search_query=search_query, services=services
        )


@app.route('/customer_dashboard/<user>/search',methods = ['GET','POST'])
def customer_search(user):   #user take name input of customer as user
    customer = Customer.query.filter_by(name = user).first()
    search_query = request.args.get("search_query") or ""
    search_by = request.args.get("search_by") or ""
    if request.method == "POST":
        search_query = request.form.get("searched")
        search_by = request.form.get("search_by")
        return redirect(url_for('customer_search',search_query=search_query,search_by=search_by,user=user))
    #writing logic for search functionality
    

    return render_template('customer_search.html',customer = customer,search_query=search_query,search_by=search_by)

@app.route('/professional_dashboard/<user>/search',methods = ['GET','POST'])
def professional_search(user): #user take name input of professional as user
    search_query = request.args.get("search_query") or ""
    search_by = request.args.get("search_by") or ""
    if request.method == "POST":    
        search_query = request.form.get("searched")
        search_by = request.form.get("search_by")
        return redirect(url_for('professional_search',search_query=search_query,search_by=search_by,user =user))
    #writing logic for search functionality


    professional = Professional.query.filter_by(name = user).first()
    return render_template('professional_search.html',professional = professional,search_query=search_query,search_by=search_by)


@app.route("/logout")
def logout():
    return redirect(url_for("login", msg="logout successfull"))


@app.route("/admin/add_service", methods=["GET", "POST"])
def addService():
    if request.method == "POST":
        sname = request.form["sname"]
        sprice = request.form["price"]
        tr = request.form["t_required"]
        sdesc = request.form["sdesc"]
        sr = Service.query.filter_by(name=sname).first()
        if sr:
            return render_template("add_service.html", msg="service already exists")
        ser = Service(name=sname, price=sprice, time_required=tr, description=sdesc)
        db.session.add(ser)
        db.session.commit()
        return redirect(url_for("adminDashboard"))
    return render_template("add_service.html", msg="")


@app.route("/admin/<task>/service/<id>", methods=["GET", "POST"])
def del_mod_service(task, id):
    if task == "delete":
        ser = Service.query.filter_by(id=id).first()
        db.session.delete(ser)
        db.session.commit()
        return redirect(url_for("adminDashboard"))
    else:
        ser = Service.query.get_or_404(id)
        if request.method == "POST":
            ser.name = request.form["sname"]
            ser.price = request.form["price"]
            ser.time_required = request.form["t_required"]
            ser.description = request.form["sdesc"]
            db.session.commit()
            return redirect(url_for("adminDashboard"))

        return render_template("modify_service.html", ser=ser)


@app.route("/admin/show_detail/<item>/<id>")
def show_detail_admin(item, id):
    if item == "service":
        ser = Service.query.filter_by(id=id).first()
        return render_template("show_admin_detail.html", ser=ser, item=item)
    elif item == "service_request":
        serreq = ServiceRequest.query.filter_by(id=id).first()
        return render_template("show_admin_detail.html", serreq=serreq, item=item)

    elif item == "customer":
        cust = Customer.query.filter_by(id=id).first()
        return render_template("show_admin_detail.html", customer=cust, item=item)

    else:
        prof = Professional.query.filter_by(id=id).first()
        return render_template("show_admin_detail.html", prof=prof, item=item)

@app.route('/customer_dashboard/<user>/particular_service/<service_type>')
def particular_service(user, service_type):
    customer = search_customer_name(user)
    return render_template('particular_service.html',customer=customer,service_type=service_type)


@app.route("/view/<user>/profile/<id>", methods=["GET", "POST"])
def update_profile(user, id):
    if user == "customer":
        cust = Customer.query.get_or_404(id)
        if request.method == "POST":
            cust.name = request.form["name"]
            cust.email = request.form["email"]
            cust.password = request.form["pwd"]
            cust.address = request.form["address"]
            cust.pincode = request.form["pin"]
            db.session.commit()
            return redirect(url_for("customerDashboard", user=cust.name))
        return render_template("profile_info.html", customer=cust,user ='customer')
    else:
        prof = Professional.query.get_or_404(id)
        if request.method == "POST":
            prof.email = request.form["email"]
            prof.password = request.form["pwd"]
            prof.name = request.form["name"]
            prof.address = request.form["address"]
            prof.pincode = request.form["pincode"]
            prof.phone = request.form["phone"]
            prof.description = request.form["description"]
            db.session.commit()
            return redirect(url_for("professionalDashboard", id=prof.id))
        return render_template("profile_info.html", professional=prof,user ='professional')

@app.route('/admin/<user>/<id>/<status>')
def update_status_admin(user,id,status):
    update = status_changer_user(user=user,id=id,status=status)
    return redirect(url_for('adminDashboard'))

@app.route('/summary/<user>/<id>')
def summary(user,id):
    if user == 'customer':
        customer = Customer.query.filter_by(id=id).first()
        return render_template('summary_all.html',customer=customer,user = user)
    elif user == 'professional':
        professional = Professional.query.get_or_404(id)
        return render_template('summary_all.html',professional=professional,user=user)
    else:
        
        return render_template('summary_all.html',user=user)
