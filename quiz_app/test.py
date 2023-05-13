from wtforms import Form, StringField, FieldList, FormField

class AddressForm(Form):
    street = StringField()
    city = StringField()
    state = StringField()

class MyForm(Form):
    addresses = FieldList(FormField(AddressForm))

# create an instance of the form
form = MyForm()

# create a list of dictionaries with data for the field list
my_data = [
    {'addresses-0-street': '123 Main St', 'addresses-0-city': 'Anytown', 'addresses-0-state': 'CA'},
    {'addresses-1-street': '456 Oak St', 'addresses-1-city': 'Otherville', 'addresses-1-state': 'NY'},
    {'addresses-2-street': '789 Elm St', 'addresses-2-city': 'Smallville', 'addresses-2-state': 'IL'}
]

# set the data for the field list on the form instance
# form.addresses.data = my_data

for d in form.addresses.entries:
    d = my_data
    print(d)
