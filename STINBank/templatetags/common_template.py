from django import template
from django.core.paginator import Paginator
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


@register.inclusion_tag('includes/pagination/pagination_range.html')
def render_pagination_range(
        paginator: Paginator,
        page: int,
        one_each_side: int = 1,
        on_ends: int = 1,
        range_ellipsis: any = None
):
    page_range = paginator.get_elided_page_range(page, on_each_side=one_each_side, on_ends=on_ends)
    return {
        'page_range': [int(page) if str(page).isnumeric() else None for page in page_range],
        'current_page': page,
        'ellipsis': range_ellipsis if range_ellipsis else paginator.ELLIPSIS
    }
