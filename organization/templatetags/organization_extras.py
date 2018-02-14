from django import template
from dateutil.parser import parse

register = template.Library()

@register.simple_tag
def field_name(model, field):
    '''
    Django template filter which returns the verbose name of an object's, model's or related manager's field.
    '''
    field_name = field

    if model:
        try:
            field_name = model._meta.get_field(field).verbose_name.title()
        except Exception as ex:
            print ex
            pass

    return field_name


@register.simple_tag
def parse_date(date):
    '''
    Django template filter which returns the verbose name of an object's, model's or related manager's field.
    '''
    if date:
        return parse(date)
    else:
        return None


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)
