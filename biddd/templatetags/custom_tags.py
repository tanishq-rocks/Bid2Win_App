from django import template
from more_itertools import numeric_range
import math
register = template.Library()

@register.filter(name='truncate')
def truncate(n, decimal=0):
    multiplier = 10 ** decimal
    return str(int(n * multiplier) / multiplier)

# @register.filter(name='range')
# def range(end, increment):
#     return numeric_range(0.00, end, increment)

# @register.filter(name='range_trunc')
# def range_trunc(end, increment):
#     string = []
#     l = numeric_range(0.00, end, increment)
#     for i in l:
#         string.append(truncate(i, 2))
#     return string

@register.filter(name='range_trunc')
def range_trunc(end, increment):
    l=[]
    for i in [float(j) / 100 for j in range(0, 10000, 1)]:
        l.append(str(i))
    return l

@register.filter(name='bid_values')
def bid_values(l1):
    l2 = [] 
    for i in l1:
        l2.append(i['bid_value'])
    return l2

@register.filter(name='count')
def count(l, i):
    return l.count(i)

@register.filter(name='floatvalue')
def floatvalue(num):
    # return math.trunc(100*float(num))
    return round(100*float(num))

@register.filter(name='list')
def list(num):
    return list(num)