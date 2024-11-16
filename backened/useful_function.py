from .modals import Admin , Professional, Customer,Service,ServiceRequest,Review


# search service by name
def search_service_name(name):
    services = Service.query.filter(Service.name.ilike(f'%{name}%')).all()
    return services


#search service by price
def search_service_price(price):
    services = Service.query.filter(Service.price.ilike(f'%{price}%')).all()
    return services

#search service by time
def search_service_time(time):
    services = Service.query.filter(Service.time.ilike(f'%{time}%')).all()
    return services

#search professional by name
def search_professional_name(name):
    professionals = Professional.query.filter(Professional.name.ilike(f'%{name}%')).all()
    return professionals

#search professional by status
def search_professional_status(status):
    professionals = Professional.query.filter(Professional.status.ilike(f'%{status}%')).all()
    return professionals

#search professional by address
def search_professional_address(address):
    professionals = Professional.query.filter(Professional.address.ilike(f'%{address}%')).all()
    return professionals

#search professional by pincode
def search_professional_pincode(pincode):
    professionals = Professional.query.filter(Professional.pincode.ilike(f'%{pincode}%')).all()
    return professionals

#search professional by service_type
def search_professional_service_type(service_type):
    professionals = Professional.query.filter(Professional.service_type.ilike(f'%{service_type}%')).all
    return professionals

#search customer by name
def search_customer_name(name):
    customers = Customer.query.filter(Customer.name.ilike(f'%{name}%')).all()
    return customers

#search customer by pincode
def search_customer_pincode(pincode):
    customers = Customer.query.filter(Customer.pincode.ilike(f'%{pincode}%')).all()
    return customers

#search customer by address
def search_customer_address(address):
    customers = Customer.query.filter(Customer.address.ilike(f'%{address}%')).all()
    return customers

#search service_request by service name
def search_sr_servicename(name):
    service_id = Service.query.filter_by(name= name).first()
    service_requests = ServiceRequest.query.filter_by(service_id=service_id).all()
    return service_requests

def search_sr_professionalname(name):
    professional_id = Professional.query.filter_by(name= name).first()
    service_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()
    return service_requests

def search_sr_customername(name):
    customer_id = Customer.query.filter_by(name=name).first()
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    return service_requests

def search_sr_status(status):
    service_requests = ServiceRequest.query.filter_by(service_status=status).all()
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
        return None
    
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
        return None
    
def data_from_customer(param):
    name = search_customer_name(param)
    address = search_customer_address(param)
    pin = search_customer_pincode(param)
    if name:
        return name
    elif address:
        return address  
    elif pin:
        return pin
    else:
        return None
    
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
        return None
    
