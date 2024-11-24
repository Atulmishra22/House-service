from .modals import db, Admin, Professional, Customer, Service, ServiceRequest, Review
from werkzeug.utils import secure_filename
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import os


# search service by name
def search_service_name(name):
    services = Service.query.filter(Service.name.ilike(f"%{name}%")).all()
    return services


# search service by price
def search_service_price(price):
    services = Service.query.filter(Service.price.ilike(f"%{price}%")).all()
    return services


# search service by time
def search_service_time(time):
    services = Service.query.filter(Service.time_required.ilike(f"%{time}%")).all()
    return services


# search professional by name
def search_professional_name(name):
    professionals = Professional.query.filter(
        Professional.name.ilike(f"%{name}%")
    ).all()
    return professionals


# search professional by status
def search_professional_status(status):
    professionals = Professional.query.filter(
        Professional.status.ilike(f"%{status}%")
    ).all()
    return professionals


# search professional by address
def search_professional_address(address):
    professionals = Professional.query.filter(
        Professional.address.ilike(f"%{address}%")
    ).all()
    return professionals


# search professional by pincode
def search_professional_pincode(pincode):
    professionals = Professional.query.filter(
        Professional.pincode.ilike(f"%{pincode}%")
    ).all()
    return professionals


# search professional by service_type
def search_professional_service_type(service):
    professionals = Professional.query.filter(
        Professional.service_type.ilike(f"%{service}%")
    ).all()
    return professionals


# search customer by name
def search_customer_name(name):
    customers = Customer.query.filter(Customer.name.ilike(f"%{name}%")).all()
    return customers


# search customer by pincode
def search_customer_pincode(pincode):
    customers = Customer.query.filter(Customer.pincode.ilike(f"%{pincode}%")).all()
    return customers


# search customer by address
def search_customer_address(address):
    customers = Customer.query.filter(Customer.address.ilike(f"%{address}%")).all()
    return customers


# search customer by status
def search_customer_status(status):
    customers = Customer.query.filter(Customer.status.ilike(f"%{status}%")).all()
    return customers


# search customer by contact
def search_customer_contact(contact):
    customers = Customer.query.filter(Customer.phone.ilike(f"%{contact}%")).all()
    return customers


# search service_request by service name
def search_sr_servicename(name):
    service = Service.query.filter(Service.name.ilike(f"%{name}%")).first()
    service_requests = ServiceRequest.query.filter_by(service_id=service.id).all()
    return service_requests


def search_sr_professionalname(name):
    professional_id = Professional.query.filter(
        Professional.name.ilike(f"%{name}%")
    ).first()
    service_requests = ServiceRequest.query.filter_by(
        professional_id=professional_id
    ).all()
    return service_requests


def search_sr_customername(name):
    customer_id = Customer.query.filter(Customer.name.ilike(f"%{name}%")).first()
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    return service_requests


def search_sr_status(status):
    service_requests = ServiceRequest.query.filter(
        ServiceRequest.service_status.ilike(f"%{status}%")
    ).all()
    return service_requests


def data_from_service(param):
    name = search_service_name(param)
    price = search_service_price(param)
    time = search_service_time(param)
    if name:
        return name
    elif price:
        return price
    elif time:
        return time
    else:
        return []


def data_from_professional(param):
    name = search_professional_name(param)
    service = search_professional_service_type(param)
    address = search_professional_address(param)
    pin = search_professional_pincode(param)
    status = search_professional_status(param)
    if name:
        return name
    elif service:
        return service
    elif address:
        return address
    elif pin:
        return pin
    elif status:
        return status
    else:
        return []


def data_from_customer(param):
    name = search_customer_name(param)
    phone = search_customer_contact(param)
    status = search_customer_status(param)
    address = search_customer_address(param)
    pin = search_customer_pincode(param)
    if name:
        return name
    elif address:
        return address
    elif phone:
        return phone
    elif status:
        return status
    elif pin:
        return pin
    else:
        return []


def data_from_servicerequest(param):
    pname = search_sr_professionalname(param)
    sname = search_sr_servicename(param)
    cname = search_sr_customername(param)
    status = search_sr_status(param)
    if pname:
        return pname
    elif sname:
        return sname
    elif cname:
        return cname
    elif status:
        return status
    else:
        return []


def status_changer_user(user, status, id):
    if user == "customer":
        cust = Customer.query.filter_by(id=id).first()
        if status != "Delete":
            cust.status = status
            if status == "Blocked":
                ser_req = ServiceRequest.query.filter_by(customer_id=id).all()
                for ser in ser_req:
                    if ser.service_status in ["accepted", "requested"]:
                        ser.service_status = "rejected"
        else:
            db.session.delete(cust)
        db.session.commit()

    else:
        prof = Professional.query.filter_by(id=id).first()
        if status != "Delete":
            prof.status = status
            if status == "Blocked":
                ser_req = ServiceRequest.query.filter_by(professional_id=id,service_status = 'accepted').all()
                for ser in ser_req:
                    ser.service_status = "rejected"
        else:
            db.session.delete(prof)
        db.session.commit()


def file_url(file, name):
    if file.filename:
        filename = secure_filename(file.filename)
        path = "./professional_verification/" + name + "_" + filename
        file.save(path)
        return path


# find service by professional service type
def search_service_profser(service_type):
    service = Service.query.filter(Service.name.ilike(f"%{service_type}%")).first()
    return service


def calculate_average_rating(professional):
    ratings = []
    for service_request in professional.service_requests:
        for review in service_request.reviews:
            ratings.append(review.rating)
    if ratings:
        return sum(ratings) / len(ratings)
    return 0


def search_professional(word):
    professionals = data_from_professional(word)
    professional_ratings = []
    for professional in professionals:
        if professional.status not in ["Blocked", "Rejected", "pending"]:
            service = search_service_profser(professional.service_type)
            average_rating = calculate_average_rating(professional)
            professional_ratings.append(
                {
                    "professional": professional,
                    "average_rating": average_rating,
                    "service": service,
                }
            )
    sorted_list = sorted(
        professional_ratings, key=lambda x: x["average_rating"], reverse=True
    )
    return sorted_list[:5]


def auto_reject_request(rid):
    request = ServiceRequest.query.get(rid)
    pid = request.professional_id
    rdate = request.date_of_request
    cdate = request.date_of_completion
    overlap_request = (
        db.session.query(ServiceRequest)
        .filter(
            ServiceRequest.professional_id == pid,
            ServiceRequest.id != rid,
            ServiceRequest.service_status.notin_(["rejected", "completed"]),
            db.or_(
                db.and_(
                    ServiceRequest.date_of_request < cdate,
                    ServiceRequest.date_of_completion > rdate,
                )
            ),
        )
        .all()
    )
    if overlap_request:
        for req in overlap_request:
            req.service_status = "rejected"
    db.session.commit()


def reject_new_request(request):
    pid = request.professional_id
    rdate = request.date_of_request
    cdate = request.date_of_completion
    overlap_request = (
        db.session.query(ServiceRequest)
        .filter(
            ServiceRequest.professional_id == pid,
            ServiceRequest.service_status == "accepted",
            db.or_(
                db.and_(
                    ServiceRequest.date_of_request < cdate,
                    ServiceRequest.date_of_completion > rdate,
                )
            ),
        )
        .all()
    )
    if overlap_request:
        request.service_status = "rejected"
    db.session.commit()



def professional_searchbar(professional_id, search_query, search_type):
    query = db.session.query(ServiceRequest, Customer).join(Customer).filter(
        ServiceRequest.professional_id == professional_id  
    )

    if search_type == 'address':
        query = query.filter(Customer.address.like(f'%{search_query}%'))
    
    elif search_type == 'pincode':
        query = query.filter(Customer.pincode == search_query)
    elif search_type == 'customer_name':
        query = query.filter(Customer.name.like(f'%{search_query}%'))
    results = query.all()

    ser_req_list = []
    for service_request, customer in results:
        ser_req_list.append({
            "service_request": service_request,
            "customer": customer,
        })
    
    return ser_req_list





# matplotlib function
def service_request_graph(id, user):
    if user == "admin":
        received_count = ServiceRequest.query.count()
        accepted_count = ServiceRequest.query.filter_by(
            service_status="accepted"
        ).count()
        rejected_count = ServiceRequest.query.filter_by(
            service_status="rejected"
        ).count()
        Completed_count = ServiceRequest.query.filter_by(
            service_status="closed"
        ).count()
    elif user == "professional":
        received_count = ServiceRequest.query.filter_by(professional_id=id).count()
        accepted_count = ServiceRequest.query.filter_by(
            professional_id=id, service_status="accepted"
        ).count()
        rejected_count = ServiceRequest.query.filter_by(
            professional_id=id, service_status="rejected"
        ).count()
        Completed_count = ServiceRequest.query.filter_by(
            professional_id=id, service_status="closed"
        ).count()
    elif user == "customer":
        received_count = ServiceRequest.query.filter_by(customer_id=id).count()
        accepted_count = ServiceRequest.query.filter_by(
            customer_id=id, service_status="accepted"
        ).count()
        rejected_count = ServiceRequest.query.filter_by(
            customer_id=id, service_status="rejected"
        ).count()
        Completed_count = ServiceRequest.query.filter_by(
            customer_id=id, service_status="closed"
        ).count()
    else:
        return []
    categories = ["All Request", "Accepted","Completed" ,"Rejected"]
    counts = [received_count, accepted_count, Completed_count ,rejected_count]

    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color=["blue", "green","orange" ,"red"])
    plt.title("Service Request Graph")
    plt.xlabel("Status")
    plt.ylabel("Count")

    fldr = os.path.join("static", "images", user)
    if not os.path.exists(fldr):
        os.makedirs(fldr)

    img_name = f"{id}_service_request.jpeg"
    img_path = os.path.join(fldr, img_name)
    plt.savefig(img_path)
    plt.clf()
    plt.close()
    return img_name


def users_graph():
    profs = Professional.query.count()
    custs = Customer.query.count()
    x_axis = ["Professionals", "Customers"]
    y_axis = [profs, custs]
    plt.figure(figsize=(10, 6))
    plt.bar(x_axis, y_axis, color=["blue", "green"])
    plt.title("Users")
    plt.xlabel("Type")
    plt.ylabel("Count")
    img_name = "users.png"
    path = os.path.join("static", "images", "admin", img_name)
    plt.savefig(path)
    plt.clf()
    plt.close()
    return img_name


def rating_for_admin():
    ratings = db.session.query(Review.rating).all()
    if ratings:
        rating_list = [rating[0] for rating in ratings]
        if not rating_list:
            return 0
        rating_sum = sum(rating_list)
        rating = rating_sum / len(rating_list)
        return rating
    else:
        return 0


def prepare_pie_chart_data(average_rating):
    if average_rating:
        proportions = [average_rating, 5 - average_rating]
        labels = ["Average Rating", "Remaining to 5"]
        colors = ["gold", "lightgrey"]
        return proportions, labels, colors
    else:
        # zero case handle
        proportions = [1]  # Full circle representing zero rating
        labels = ["No Ratings"]
        colors = ["lightgrey"]
        return proportions, labels, colors



def create_pie_chart(proportions, labels, colors, user, id):
    if proportions and labels and colors:
        plt.figure(figsize=(8, 8))
        plt.pie(
            proportions, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140
        )
        plt.title("Average Rating Distribution")
        plt.axis("equal")
        if user == "admin":
            img_name = 'rating_chart.png'
            path = os.path.join("static", "images", "admin", img_name)
        elif user == "professional":
            img_name = f"{id}_rating_charg.jpeg"
            path = os.path.join("static",'images' ,"professional", img_name)
        plt.savefig(path)
        plt.clf()
        plt.close()
        return img_name
    else:
        return ''


def rating_graph_admin():
    avg_r = rating_for_admin()
    proportions, label, color = prepare_pie_chart_data(avg_r)
    name = create_pie_chart(proportions, label, color, "admin", 1)
    return name


def prof_rating_graph(professional):
    avg_r = calculate_average_rating(professional)
    proportions, label, color = prepare_pie_chart_data(avg_r)
    name = create_pie_chart(proportions, label, color, "professional", professional.id)
    return name
