from django import template

register = template.Library()

def number_format(number, decimals=2, dec_point=',', thousands_sep='.'):
    try:
        number = round(float(number), decimals)
    except ValueError:
    	return number
    except TypeError:
        return number
    neg = number < 0
    integer, fractional = str(abs(number)).split('.')
    m = len(integer) % 3
    if m:
        parts = [integer[:m]]
    else:
        parts = []
    
    parts.extend([integer[m+t:m+t+3] for t in xrange(0, len(integer[m:]), 3)])
    
    if decimals:
        return '%s%s%s%s' % (
            neg and '-' or '', 
            thousands_sep.join(parts), 
            dec_point, 
            fractional.ljust(decimals, '0')[:decimals]
        )
    else:
        return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

register.filter(number_format)

