from django import template
import locale

#locale.setlocale(locale.LC_ALL, '')

register = template.Library()

def terbilang(value):
	value = int(value)
	bunyi = ""
	satuan = ("", "satu", "dua", "tiga", "empat", "lima", "enam","tujuh","delapan","sembilan","sepuluh", "sebelas")
	if value >= 0 and value < 12:
		bunyi = ' ' + satuan[value]
	if value >= 12 and value < 20:
		bunyi = terbilang(value%10) + ' belas'
	if value >= 20 and value < 100:
		bunyi = terbilang(value/10) + ' puluh' + terbilang(value%10)
	if value >= 100 and value < 200:
		bunyi = ' seratus' + terbilang(value - 100)
	if value >= 200 and value < 1000:
		bunyi = terbilang(value/100) + ' ratus' + terbilang(value%100)
	if value >= 1000 and value < 2000:
		bunyi = ' seribu' + terbilang(value - 1000)
	if value >= 2000 and value < 1000000:
		bunyi = terbilang(value / 1000) + ' ribu' + terbilang(value % 1000)
	if value >= 1000000 and value < 1000000000:
		bunyi = terbilang(value/1000000) + ' juta' + terbilang(value % 1000000)
	return bunyi

register.filter('terbilang', terbilang)

def currency(value):
	return locale.currency(value, grouping=True)

register.filter('currency', currency)

def number_tanpa_desimal(number, dec_point=',', thousands_sep='.'):
    try:
        number = round(float(number))
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
    return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

from django.utils.safestring import mark_safe


def minplus(value):
    esc = ''
    if value <= 0 :
        esc = value * - 1
        result = '<FONT COLOR=\"FF0000\">%s</FONT>' % number_tanpa_desimal(esc)
    if value > 0:
        esc = value
        result = '<FONT COLOR=\"#000000\">%s</FONT>' % number_tanpa_desimal(esc)
    return mark_safe(result)
register.filter('minplus', minplus)
