import re
from flask import Flask, request, jsonify
from tinydb import TinyDB


app = Flask(__name__)
db = TinyDB('database.json')

templates_test = [
    {'name': 'MyForm', 'user_name':'text', 'order_date': 'date'},
    {'name': 'OrderForm', 'lead_email': 'email', 'phone': 'phone'}
]
db.insert_multiple(templates_test)


def validate_date(date):
    validate = re.compile(r'\b(?:\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})\b')
    if validate.match(date):
        return date
    else:
        return False



def validate_email(email):
    validate = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    if validate.match(email):
        return True
    else:
        return False



def validate_phone(phone):
    validate = re.compile(r'\+\d{1,2} \d{3} \d{3} \d{2} \d{2}')
    if validate.match(phone):
        return True
    else:
        return False


def validate_text(text):
    validate = re.compile(r'^[A-Za-z0-9_,\s]+$')
    if validate.match(text):
        return True
    else:
        return False


def get_template(form_data):
    for template in db.all():
        template_fields = set(template.keys()) - {'name'}
        if template_fields.issubset(form_data.keys()):
            matching_fields = {key :template[key] for key in template_fields}
            if all(form_data[field] == matching_fields[field] for field in matching_fields):
                return template['name']
    return {field: get_field_type(form_data[field]) for field in form_data}

def get_field_type(value):
    if validate_date(value):
        return 'date'
    elif validate_phone(value):
        return 'phone'
    elif validate_email(value):
        return 'email'
    else:
        return 'text'


@app.route('/get_form', methods=['POST'])
def get_form():
    form_data = request.form.to_dict()
    result = get_template(form_data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)