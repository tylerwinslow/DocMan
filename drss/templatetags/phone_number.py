import phonenumbers
from django import template
register = template.Library()


@register.filter(name='phone_number')
def phone_number(value):
    value = "+1" + value
    parsed_number = phonenumbers.parse(value, None)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    return formatted_number
