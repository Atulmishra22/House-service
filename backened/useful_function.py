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
def search_sr_servicename(id):
    service_request = ServiceRequest.query.filter()