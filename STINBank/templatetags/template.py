from django import template
from django.forms import Form, ChoiceField
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('includes/form.html')
def render_form(form: Form, field_wrap: bool = True, label: bool = True):
    return {
        'form': form,
        'field_wrap': field_wrap,
        'label': label
    }


@register.simple_tag()
def render_form_field(field):
    if isinstance(field.field, ChoiceField):
        return mark_safe(f'<div class="select">{field}</div>')
    else:
        return mark_safe(field)
