"""Generate the client brochure for GitHub Pages, Django and PDF."""
import json
import re
import shutil
from html import escape as e
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'brochures/gallos-finos-peru/contenido.json').read_text(encoding='utf-8'))
PDF_NAME = 'benigno-ranilla-sistemas-gallos-finos-peru.pdf'
OUT = ROOT / 'output/pdf/revision-2' / PDF_NAME
OUT.parent.mkdir(parents=True, exist_ok=True)

cards = ''.join(f'''<article class="service"><span class="number">{s['number']}</span><h3>{e(s['title'])}</h3><p>{e(s['benefit'])}</p><ul>{''.join(f'<li>{e(i)}</li>' for i in s['items'])}</ul><div class="example"><strong>Así se vería en tu negocio</strong><p>{e(s['example'])}</p></div></article>''' for s in data['services'])
steps = ''.join(f'<li><span>0{i}</span><div><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></div></li>' for i, s in enumerate(data['delivery'], 1))
html = f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brochure para Gallos Finos Perú | Benigno Ranilla</title>
<meta name="description" content="Sistemas de ventas, almacén, ingresos y gastos por evento, control documental y desarrollo a medida para Gallos Finos Perú.">
<link rel="icon" href="static/images/brand-favicon.png"><link rel="stylesheet" href="static/css/brochure.css"></head>
<body><header><a class="brand" href="index.html"><img src="static/images/brand-logo.png" alt="Logo de Benigno Ranilla"><span>Benigno Ranilla<small>Arquitecto de aplicaciones</small></span></a><a class="back" href="index.html#brochure">Volver al portafolio ↗</a></header>
<main><section class="cover"><div class="cover-copy"><p class="eyebrow">BROCHURE DE SERVICIOS / 2026</p><p class="client">{e(data['client'])}</p><h1>Tu negocio,<br><em>conectado.</em></h1><h2>{e(data['subtitle'])}</h2><p>{e(data['intro'])}</p><div class="actions"><a class="button" href="static/brochures/{PDF_NAME}" download>Descargar brochure PDF ↓</a><a class="text-link" href="{data['contact']}" target="_blank" rel="noopener">Conversemos ↗</a></div></div>
<aside class="map" aria-label="Áreas que se pueden conectar"><p class="eyebrow">SISTEMAS PARA TU OPERACIÓN</p><div class="map-center">Tus negocios<small>Información para tomar decisiones</small></div><div class="map-grid"><div><b>01</b> Ventas<span>Caja · Cobros · Clientes</span></div><div><b>02</b> Almacén<span>Stock · Compras · Insumos</span></div><div><b>03</b> Eventos<span>Ingresos · Gastos · Balance</span></div><div><b>04</b> Documentos<span>Archivo · Permisos · Vencimientos</span></div></div><p class="map-note">Sistemas disponibles, adaptaciones y desarrollo a medida según tus prioridades.</p></aside></section>
<section class="context"><span class="eyebrow">EL PUNTO DE PARTIDA</span><h2>Tu web fue el primer paso. Sigamos con tus sistemas.</h2><p>{e(data['context'])}</p><a href="https://gallosfinosperu.com/" target="_blank" rel="noopener">Web desarrollada por nosotros: Gallos Finos Perú ↗</a></section>
<section class="solutions" id="soluciones"><div class="section-heading"><p class="eyebrow">SISTEMAS QUE PODEMOS IMPLEMENTAR CONTIGO</p><h2>De la venta al control.<br>Soluciones para toda tu operación.</h2></div><div class="service-grid">{cards}</div></section>
<section class="process"><div><p class="eyebrow">DE LA IDEA A LA OPERACIÓN</p><h2>Un proceso claro,<br>contigo en cada etapa.</h2><p>{e(data['start'])}</p><a class="text-link" href="index.html#portfolio">Explora mi experiencia web y móvil ↗</a></div><ol>{steps}</ol></section>
<section class="closing"><p class="eyebrow">EMPECEMOS POR LO QUE MÁS NECESITAS</p><h2>Tu próxima mejora<br>empieza con una conversación.</h2><p>Cuéntame qué necesitas organizar, vender o automatizar. Definimos una primera etapa con entregables claros.</p><a class="button" href="{data['contact']}" target="_blank" rel="noopener">Conversemos por WhatsApp ↗</a><p class="phone">+51 914 751 129 · Perú</p></section>
<p class="scope">{e(data['scope'])}</p></main><footer><span>Benigno Ranilla · Sistemas de gestión y desarrollo a medida</span><span>Preparado para Gallos Finos Perú · Octubre 2026</span></footer></body></html>'''
(ROOT / 'docs/brochure-gallos-finos-peru.html').write_text(html, encoding='utf-8')
template = re.sub(r'(href|src)="static/([^"]+)"', lambda m: m[1] + '="{% static \'' + m[2] + '\' %}"', html)
template = template.replace('href="index.html', 'href="/').replace('href="/#', 'href="/#')
(ROOT / 'benignoWeb/templates/brochure-gallos-finos-peru.html').write_text('{% load static %}\n' + template, encoding='utf-8')

# Fixed editorial pages keep the commercial brochure short and readable.
W, H = 595.28, 841.89
navy, blue, copper, ink, muted = map(HexColor, ['#102c48', '#0563bb', '#b77b4a', '#20354a', '#52677a'])
c = canvas.Canvas(str(OUT), pagesize=(W, H))
c.setTitle('Propuesta de servicios para Gallos Finos Perú | Benigno Ranilla')
c.setAuthor('Benigno Ranilla')

def para(text, x, top, width, size=11, color=ink, leading=None, bold=False):
    st = ParagraphStyle('body', fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=size, leading=leading or size*1.45, textColor=color)
    p = Paragraph(text, st)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, H-top-height)
    return top+height

def line(y):
    c.setStrokeColor(HexColor('#dbe5ef')); c.line(42,H-y,W-42,H-y)

def base(page, label):
    c.setFillColor(HexColor('#ffffff')); c.rect(0,0,W,H,fill=1,stroke=0)
    c.drawImage(ImageReader(str(ROOT/'docs/static/images/brand-logo.png')),42,H-75,70,38,mask='auto',preserveAspectRatio=True,anchor='c')
    para('Benigno Ranilla',126,40,260,13,navy,bold=True)
    para('Arquitecto de aplicaciones',126,61,260,9,muted)
    line(96)
    line(788)
    para('GALLOS FINOS PERÚ / PROPUESTA DE SERVICIOS',42,803,430,8,muted)
    para(f'{page:02}',523,803,35,9,blue,bold=True)
    para(label.upper(),42,119,500,9,copper,bold=True)

base(1,'Sistemas de gestión · Automatización · Integraciones')
para('Tu negocio,<br/><font color="#0563bb">conectado.</font>',42,163,510,52,navy,56,True)
para(data['subtitle'],44,304,480,21,navy,28,True)
para(data['intro'],44,389,478,13,muted,20)
c.setFillColor(HexColor('#eef5fb')); c.roundRect(42,H-684,511,155,14,fill=1,stroke=0)
para('PREPARADO PARA GALLOS FINOS PERÚ',62,549,460,9,blue,bold=True)
para(data['context'],62,580,465,12,ink,19)
para('Ventas  /  Almacén  /  Eventos  /  Documentos',44,719,505,11,navy,bold=True)
para('Benigno Ranilla · Perú · Octubre 2026',44,750,505,10,muted)
c.showPage()

for page, services, label in [(2,data['services'][:2],'Ventas y existencias'),(3,data['services'][2:4],'Control económico y documental'),(4,data['services'][4:6],'Restaurantes y sistemas a medida')]:
    base(page,label)
    top=161
    for s in services:
        para(s['number'],42,top,40,24,copper,bold=True)
        end=para(s['title'],94,top,455,22,navy,27,True)
        end=para(s['benefit'],94,end+12,440,12,blue,17)
        for item in s['items']:
            end=para('• '+e(item),94,end+10,438,11,ink,16)
        end=para('<b>Así se vería en tu negocio</b><br/>'+e(s['example']),94,end+16,438,10,muted,15)
        if end>(455 if top==161 else 777):
            raise ValueError(f'Page {page} overflow: {end}')
        if top==161: line(465)
        top=493
    c.showPage()

base(5,'Una primera etapa con entregables claros')
para('Construyamos lo que<br/>tu negocio necesita.',42,160,510,31,navy,38,True)
top=267
for i,s in enumerate(data['delivery'],1):
    para(f'0{i}',42,top,37,17,copper,bold=True)
    end=para(s['title'],91,top,460,13,navy,bold=True)
    top=para(s['text'],91,end+4,455,10.5,muted,15)+18
para(data['start'],42,top+2,510,11,ink,16)
c.setFillColor(navy); c.roundRect(42,111,511,88,12,fill=1,stroke=0)
para('Conversemos sobre tu primera etapa.',61,657,465,17,HexColor('#ffffff'),bold=True)
para('+51 914 751 129  ·  WhatsApp  ·  Perú',61,689,465,12,HexColor('#ffffff'))
c.linkURL(data['contact'],(42,111,553,199),relative=0)
para(data['scope'],42,741,510,7.5,muted,10)
c.showPage(); c.save()
for folder in ['docs/static/brochures','benignoWeb/static/brochures']:
    dest=ROOT/folder
    dest.mkdir(parents=True,exist_ok=True)
    shutil.copy2(OUT,dest/PDF_NAME)
print(f'Generated HTML, Django template and PDF: {OUT}')
