from service import auth_service
from model.delivery import Delivery
from model.delivery_state_history import DeliveryStateHistory
from repository import delivery_repository
from service import city_service, cap_service, courier_service, state_history_service, delivery_state_service
from secrets import token_urlsafe
import validator

def get_all(session):
    return delivery_repository.get_all(session)

def get_by_id(session, delivery_id):
    return delivery_repository.get_by_id(session, delivery_id)

def get_by_tracking_code(session, tracking_code):
    return delivery_repository.get_by_tracking_code(session, tracking_code)

def create(session, data, package_id):
    for field in ["recipient", "recipient_address", "recipient_city", "recipient_cap", "sender", "sender_address", "sender_city", "sender_cap"]:
        if field not in data:
            raise ValueError(f'Field "{field}" is required!')
    
    recipient = data["recipient"].strip()

    if not validator.check_string(recipient):
        raise ValueError("Invalid recipient!")

    recipient_address = data["recipient_address"].strip()

    if not validator.check_string(recipient_address):
        raise ValueError("Invalid address!")

    recipient_city = data["recipient_city"].strip()

    if city_service.get_by_istat(session, recipient_city) is None:
        raise ValueError("Invalid city!")

    recipient_cap = data["recipient_cap"].strip()
    found_recipient_cap = cap_service.get_by_city_and_cap(session, recipient_city, recipient_cap)
    
    if found_recipient_cap is None:
        raise ValueError("Invalid recipient cap!")

    sender = data["sender"].strip()

    if not validator.check_string(sender):
        raise ValueError("Invalid sender!")

    sender_address = data["sender_address"].strip()

    if not validator.check_string(sender_address):
        raise ValueError("Invalid sender address!")

    sender_city = data["sender_city"].strip()

    if city_service.get_by_istat(session, sender_city) is None:
        raise ValueError("Invalid city!")

    sender_cap = data["sender_cap"].strip()
    found_sender_cap = cap_service.get_by_city_and_cap(session, sender_city, sender_cap)

    if found_sender_cap is None:
        raise ValueError("Invalid sender cap!")

    # Find courier that's free
    all_couriers = courier_service.get_all(session)

    if len(all_couriers)==0:
        raise Exception("There are no registered couriers!")

    selected_courier = None

    for courier in all_couriers:
        print(len(courier.deliveries))
        if selected_courier==None or (count_opened_deliveries(courier.deliveries) < count_opened_deliveries(selected_courier.deliveries)):
            selected_courier = courier

    newDelivery = delivery_repository.create(session, Delivery(
        tracking_code = token_urlsafe(3).upper(),
        courier_id = selected_courier.id,
        package_id = package_id,
        
        sender_name = sender,
        sender_cap_id = found_sender_cap.id,
        sender_city_id = sender_city,
        sender_address = sender_address,

        recipient_name = recipient,
        recipient_cap_id = found_recipient_cap.id,
        recipient_city_id = recipient_city,
        recipient_address = recipient_address
    ))

    ordered_state = delivery_state_service.get_by_name(session, "Ordered")

    state_history_service.create(session, {
        "delivery_id": newDelivery.id,
        "state_id": ordered_state.id
    })

    return newDelivery

def count_opened_deliveries(deliveries):
    x = 0

    for delivery in deliveries:
        if not delivery.is_closed:
            x += 1
    
    return x

def delete(session, delivery):
    session.delete(delivery)
    session.commit()

def update(session, delivery):
    session.commit()
    return delivery