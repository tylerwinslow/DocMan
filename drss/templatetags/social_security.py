from django import template
register = template.Library()


@register.filter(name='social_security')
def social_security(value):
    if len(value) >= 4:
        formatted_social = "***-**-" + value[-4:]
    else:
        formatted_social = value
    return formatted_social
