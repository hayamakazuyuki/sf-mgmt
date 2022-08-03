from flask import session

def get_customer_id():
    userinfo = session['user']['userinfo']
    customer_id = userinfo.get('customer')

    return customer_id
