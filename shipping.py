import json
from urllib.request import Request, urlopen
import json
import interface as inter
import requests

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer sand_uQXMIPKfuVmebaIyOFTkEO6ziXpC0W3Gswd/MUkV0Xo=',
  'User-Agent': 'Mozilla/5.0'
}


def select_rate(origin_city, origin_state, origin_country, origin_zip,
                dest_city, dest_state, dest_country, dest_zip, tax_payer,
                insured, weight, height, width, length, category, currency,
                customs_val):
    values = """
  {{
    "origin_city": "{origin_city}",
    "origin_state": "{origin_state}",
    "origin_country_alpha2": "{origin_country}",
    "origin_postal_code": "{origin_zip}",
    "dest_city": "{dest_city}",
    "dest_state": "{dest_state}",
    "destination_country_alpha2": "{dest_country}",
    "destination_postal_code": "{dest_zip}",
    "taxes_duties_paid_by": "{tax_payer}",
    "is_insured": "{insured}",
    "items": [
      {{
        "actual_weight": {weight},
        "height": {height},
        "width": {width},
        "length": {length},
        "category": "{category}",
        "declared_currency": "{currency}",
        "declared_customs_value": {customs_val}
      }}
    ]
  }}
"""
    query = values.format(origin_city=origin_city, origin_state=origin_state,
                          origin_country=origin_country, origin_zip=origin_zip,
                          dest_city=dest_city, dest_state=dest_state,
                          dest_country=dest_country, dest_zip=dest_zip,
                          tax_payer=tax_payer, insured=insured, weight=weight,
                          height=height, width=width, length=length,
                          category=category, currency=currency,
                          customs_val=customs_val)
    updated_vals = query.encode('ascii')
    request = requests.post('https://api.easyship.com/rate/v1/rates',
                            data=updated_vals, headers=headers)
    return request.content


def create_shipment(userid, courierid, dest_name, dest_add1, dest_add2,
                    dest_city, dest_state, dest_zip, dest_country, dest_phone,
                    description, weight, height, width, length,
                    category, currency, customs_val, dest_email):
    vals = """
  {{
    "platform_name": "{platform}",
    "platform_order_number": "{order_num}",
    "selected_courier_id": "{courierid}",
    "destination_country_alpha2": "{dest_country}",
    "destination_city": "{dest_city}",
    "destination_postal_code": {dest_zip},
    "destination_state": "{dest_state}",
    "destination_name": "{dest_name}",
    "destination_address_line_1": "{dest_add1}",
    "destination_address_line_2": "{dest_add2}",
    "destination_phone_number": "{dest_phone}",
    "destination_email_address": "{dest_email}",
    "items": [
      {{
        "description": "{description}",
        "sku": "test",
        "actual_weight": {weight},
        "height": {height},
        "width": {width},
        "length": {length},
        "category": "{category}",
        "declared_currency": "{currency}",
        "declared_customs_value": {customs_val}
      }}
    ]
  }}
    """
    vals = vals.format(platform="Amazon", order_num="#1234",
                       dest_country=dest_country, dest_city=dest_city,
                       dest_state=dest_state, dest_name=dest_name,
                       dest_zip=dest_zip, dest_add1=dest_add1,
                       dest_add2=dest_add2, dest_phone=dest_phone,
                       dest_email=dest_email, description=description,
                       weight=weight, height=height, width=width,
                       length=length, category=category,
                       currency=currency, customs_val=customs_val,
                       courierid=courierid)
    updated_vals = vals.encode('ascii')
    try:
        request = requests.post('https://api.easyship.com/shipment/v1/shipments',
                                data=updated_vals, headers=headers)
    except requests.exceptions.HTTPError as e:
        return "Http Error: " + e
    except requests.exceptions.ConnectionError as f:
        return "Error Connecting:" + f
    except requests.exceptions.Timeout as g:
        return "Timeout Error:" + g
    except requests.exceptions.RequestException as h:
        return "Error: " + h
    except Exception as i:
        return "Error: " + i
    return request.content


def buy_labels(courier_id, shipment_id):
    vals = """
  {{
    "shipments": [
      {{
        "easyship_shipment_id": "{shipment_id}",
        "courier_id": "{courier_id}"
      }}
    ]
  }}
"""
    vals = vals.format(shipment_id=shipment_id, courier_id=courier_id)
    updated_vals = vals.encode('ascii')
    try:
        request = requests.post('https://api.easyship.com/label/v1/labels',
                                data=updated_vals, headers=headers)
    except requests.exceptions.HTTPError as e:
        return "Http Error: " + e
    except requests.exceptions.ConnectionError as f:
        return "Error Connecting:" + f
    except requests.exceptions.Timeout as g:
        return "Timeout Error:" + g
    except requests.exceptions.RequestException as h:
        return "Error: " + h
    resp = request.content
    package_vals = json.loads(resp.decode('utf8'))
    return package_vals['labels']
