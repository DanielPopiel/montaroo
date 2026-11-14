from mark import *
import os,subprocess
O='brand/logo'
def tile(simple, bgcol=INK, joey=SAND, sc=0.80, rx=28):
    tx=64-64*sc; ty=64-66*sc
    return (f'<rect width="128" height="128" rx="{rx}" fill="{bgcol}"/>'
            f'<g transform="translate({f(tx)} {f(ty)}) scale({sc})">'+mark_body(joey,OCH,INK,simple=simple)+'</g>')
os.makedirs(O+'/ikony',exist_ok=True)
open(O+'/ikony/favicon.svg','w').write(svg(tile(True,sc=0.86,rx=26),title='montaroo'))
open(O+'/ikony/ikona-aplikacji.svg','w').write(svg(tile(False),title='montaroo'))
open(O+'/ikony/ikona-aplikacji-mala.svg','w').write(svg(tile(True,sc=0.86,rx=24),title='montaroo'))
