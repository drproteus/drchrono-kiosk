from django import template

register = template.Library()

@register.filter
def time_format(t):
    try:
        t = t.split('T')[-1]
        hour, minute, seconds = t.split(':')[:3]
        meridian = 'AM'
        if int(hour) > 12:
            hour = int(hour) % 12
            meridian = 'PM'
        elif int(hour) == 0:
            hour = 12
        elif int(hour) == 12:
            meridian = 'PM'
        hour = str(int(hour))
    except Exception, e:
        print e
        return None
    return "{} {}".format(":".join([hour, minute]), meridian)

@register.filter
def initial(name):
    name = name[0:1]
    if name:
        return name + '.'
    return ''

@register.filter
def stringify_date(date):
    return date.strftime("%A %B %d, %Y")

@register.filter
def stringify_time(date):
    pass

@register.filter
def time_to_seconds(date):
    return (date.hour * 60 * 60) + (date.minute * 60) + (date.second)
