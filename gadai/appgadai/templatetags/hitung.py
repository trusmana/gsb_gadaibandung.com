'''
from django import template
register = template.Library()


@register.simple_tag
def ttl_noa_cair(plns):
    total = sum(d.get('noa_cair') for d in plns)
    return total

@register.simple_tag
def ttl_nilai_cair(plns):
    total = sum(d.get('nilai_cair') for d in plns)
    return total

@register.simple_tag
def ttl_noa_lunas(plns):
    total = sum(d.get('noa_lunas') for d in plns)
    return total

@register.simple_tag
def ttl_nilai_lunas(plns):
    total = sum(d.get('nilai_pelunasan') for d in plns)
    return total

@register.simple_tag
def ttl_noa_ayda_history(plns):
    total = sum(d.get('noa_ayda_history') for d in plns)
    return total

@register.simple_tag
def ttl_nilai_ayda_history(plns):
    total = sum(d.get('nilai_ayda_history') for d in plns)
    return total

@register.simple_tag
def ttl_noa_ayda_lunas(plns):
    total = sum(d.get('total_noa_ayda_lunas') for d in plns)
    return total

@register.simple_tag
def ttl_nilai_ayda_lunas(plns):
    total = sum(d.get('total_nilai_ayda_lunas') for d in plns)
    return total


@register.simple_tag
def ttl_noa_ayda(plns):
    total = sum(d.get('noa_ayda') for d in plns)
    return total

@register.simple_tag
def ttl_nilai_ayda(plns):
    total = sum(d.get('nilai_ayda') for d in plns)
    return total

@register.simple_tag
def ttl_nilai_jual_ayda(plns):
    total = sum(d.get('nilai_jual_ayda') for d in plns)
    return total

@register.simple_tag
def ttl_t_jasa(plns):
    total = sum(d.get('t_jasa') for d in plns)
    return total

@register.simple_tag#22222
def ttl_nilai_jasa_terlambat_plns(plns):
    total = sum(d.get('nilai_jasa_terlambat_plns') for d in plns)
    return total

@register.simple_tag
def ttl_t_denda(plns):
    total = sum(d.get('t_denda') for d in plns)
    return total

@register.simple_tag
def ttl_t_beasimpan(plns):
    total = sum(d.get('t_beasimpan') for d in plns)
    return total


@register.simple_tag
def ttl_t_adm(plns):
    total = sum(d.get('t_adm') for d in plns)
    return total

@register.simple_tag
def ttl_t_jual(plns):
    total = sum(d.get('t_jual') for d in plns)
    return total

@register.simple_tag
def ttl_t_akumulasi(plns):
    total = sum(d.get('t_akumulasi') for d in plns)
    return total

@register.simple_tag
def ttl_piutang(plns):
    total = sum(d.get('piutang') for d in plns)
    return total
'''
