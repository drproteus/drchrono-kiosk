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
