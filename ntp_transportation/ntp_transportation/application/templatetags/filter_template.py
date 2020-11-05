from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='get_train_travel')
@stringfilter
def get_train_travel(value):
    return value.split(";")[0].split("(")[1].split("_")[1]


@register.filter(name='get_city_from')
@stringfilter
def get_city_from(value):
    return value.split(";")[1]


@register.filter(name='get_city_to')
@stringfilter
def get_city_to(value):
    return value.split(";")[2][:-1]


@register.filter(name='get_load_parcel')
@stringfilter
def get_load_parcel(value):
    return value.split(";")[0].split("(")[1].split("_")[1]


@register.filter(name='get_train_load')
@stringfilter
def get_train_load(value):
    return value.split(";")[1].split("_")[1]


@register.filter(name='get_load_destination')
@stringfilter
def get_load_destination(value):
    return value.split(";")[2][:-1]



