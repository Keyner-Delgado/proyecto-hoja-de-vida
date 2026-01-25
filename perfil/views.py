import os
import io
import requests
from django.conf import settings
from django.contrib.staticfiles import finders
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pypdf import PdfWriter 
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import (
    DatosPersonales, ExperienciaLaboral, CursosRealizados, 
    Reconocimientos, ProductosAcademicos, ProductosLaborales, 
    VentaGarage
)

def link_callback(uri, rel):
    if uri.startswith('http'):
        return uri
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        s_url = settings.STATIC_URL
        s_root = settings.STATIC_ROOT
        m_url = settings.MEDIA_URL
        m_root = settings.MEDIA_ROOT
        if uri.startswith(m_url):
            path = os.path.join(m_root, uri.replace(m_url, ""))
        elif uri.startswith(s_url):
            path = os.path.join(s_root, uri.replace(s_url, ""))
        else:
            return uri
    return path

def crear_caratula(texto):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 32)
    can.drawCentredString(300, 500, texto.upper())
    can.save()
    packet.seek(0)
    return packet

# --- VISTAS DEL SITIO WEB ---

def home(request):
    try:
        perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
        if not perfil:
            perfil = DatosPersonales.objects.first()
        
        if not perfil:
            return HttpResponse("No hay perfiles creados. Por favor agrega uno en el Admin.")
            
        return render(request, 'home.html', {'perfil': perfil})
    except Exception as e:
        return HttpResponse(f"Error crítico en Home: {e}")

def experiencia(request):
    perfil = DatosPersonales.objects.first()
    items = ExperienciaLaboral.objects.filter(idperfil=perfil)
    return render(request, 'experiencia.html', {'perfil': perfil, 'items': items})

def cursos(request):
    perfil = DatosPersonales.objects.first()
    items = CursosRealizados.objects.filter(idperfil=perfil)
    return render(request, 'cursos.html', {'perfil': perfil, 'items': items})

def reconocimientos(request):
    perfil = DatosPersonales.objects.first()
    items = Reconocimientos.objects.filter(idperfil=perfil)
    return render(request, 'reconocimientos.html', {'perfil': perfil, 'items': items})

def productos_academicos(request):
    perfil = DatosPersonales.objects.first()
    items = ProductosAcademicos.objects.filter(idperfil=perfil)
    return render(request, 'productos_academicos.html', {'perfil': perfil, 'items': items})

def productos_laborales(request):
    perfil = DatosPersonales.objects.first()
    items = ProductosLaborales.objects.filter(idperfil=perfil)
    return render(request, 'productos_laborales.html', {'perfil': perfil, 'items': items})

def garage(request):
    perfil = DatosPersonales.objects.first()
    items = VentaGarage.objects.filter(idperfil=perfil)
    return render(request, 'garage.html', {'perfil': perfil, 'items': items})

# --- VISTA PARA GENERAR EL PDF (CORREGIDA) ---

def pdf_datos_personales(request):
    # 1. Obtener Perfil
    perfil = DatosPersonales.objects.filter(perfilactivo=1).first()
    if not perfil:
        perfil = get_object_or_404(DatosPersonales)

    # 2. Captura de parámetros SIN valores por defecto
    # Si el switch está apagado, request.GET.get devuelve None.
    # La comparación None == 'on' resulta en False.
    incluir_exp = request.GET.get('exp') == 'on'
    incluir_cur = request.GET.get('cur') == 'on'
    incluir_rec = request.GET.get('rec') == 'on'
    incluir_aca = request.GET.get('aca') == 'on'
    incluir_lab = request.GET.get('lab') == 'on'
    incluir_gar = request.GET.get('gar') == 'on'

    # 3. Consultas Condicionales (Si la variable es False, la lista queda vacía [])
    experiencias = ExperienciaLaboral.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_exp else []
    productos_academicos = ProductosAcademicos.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_aca else []
    productos_laborales = ProductosLaborales.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_lab else []
    cursos_objs = CursosRealizados.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_cur else []
    reconocimientos_objs = Reconocimientos.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_rec else []
    articulos_garage = VentaGarage.objects.filter(idperfil=perfil, activarparaqueseveaenfront=True) if incluir_gar else []
    
    # 4. Renderizado del Template HTML
    template = get_template('reportes/pdf_personales.html')
    context = {
        'perfil': perfil,
        'items': experiencias,
        'productos': productos_academicos,
        'productos_laborales': productos_laborales,
        'cursos': cursos_objs,
        'reconocimientos': reconocimientos_objs,
        'garage': articulos_garage,
    }
    html = template.render(context)
    
    # 5. Generación del PDF Base
    buffer_cv_base = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer_cv_base, link_callback=link_callback)
    
    if pisa_status.err:
        return HttpResponse('Error al generar el cuerpo del PDF', status=500)
    
    writer = PdfWriter()
    buffer_cv_base.seek(0)
    writer.append(buffer_cv_base)

    # 6. Anexar Certificados (Solo si la sección fue incluida y existen archivos)
    if incluir_cur:
        cursos_con_pdf = [c for c in cursos_objs if c.rutacertificado]
        if cursos_con_pdf:
            writer.append(crear_caratula("Certificados de Cursos"))
            for curso in cursos_con_pdf:
                try:
                    response = requests.get(curso.rutacertificado.url, timeout=10)
                    if response.status_code == 200:
                        writer.append(io.BytesIO(response.content))
                except:
                    pass

    if incluir_rec:
        reco_con_pdf = [r for r in reconocimientos_objs if r.rutacertificado]
        if reco_con_pdf:
            writer.append(crear_caratula("Reconocimientos"))
            for reco in reco_con_pdf:
                try:
                    response = requests.get(reco.rutacertificado.url, timeout=10)
                    if response.status_code == 200:
                        writer.append(io.BytesIO(response.content))
                except:
                    pass

    # 7. Respuesta Final
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="CV_{perfil.apellidos}.pdf"'
    writer.write(response)
    writer.close()
    
    return response