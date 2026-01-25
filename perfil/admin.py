from django.contrib import admin
from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimientos, 
    CursosRealizados, ProductosAcademicos, ProductosLaborales, VentaGarage
)

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    list_display = ('idperfil', 'nombres', 'apellidos', 'numerocedula', 'correo', 'perfilactivo')
    search_fields = ('nombres', 'apellidos', 'numerocedula', 'correo')
    list_filter = ('sexo', 'nacionalidad', 'perfilactivo')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('foto_perfil', 'nombres', 'apellidos', 'numerocedula', 'correo', 'sexo', 'fechanacimiento')
        }),
        ('Ubicación y Contacto', {
            'fields': ('nacionalidad', 'lugarnacimiento', 'telefonoconvencional', 'telefonofijo', 'direcciondomiciliaria', 'sitioweb')
        }),
        ('Estado de Perfil', {
            'fields': ('descripcionperfil', 'perfilactivo', 'estadocivil', 'licenciaconducir', 'direcciontrabajo')
        }),
        # --- NUEVA SECCIÓN PARA LOS INTERRUPTORES ---
        ('Configuración de Visibilidad (WEB y PDF)', {
            'description': 'Controla qué secciones están activas globalmente en el sitio y en el modal del PDF.',
            'fields': (
                'ver_experiencia', 
                'ver_cursos', 
                'ver_reconocimientos', 
                'ver_productos_academicos', 
                'ver_productos_laborales', 
                'ver_garage'
            ),
        }),
    )

@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    list_display = ('cargodesempenado', 'nombrempresa', 'idperfil', 'fechainiciogestion')
    list_filter = ('nombrempresa', 'activarparaqueseveaenfront')
    search_fields = ('cargodesempenado', 'nombrempresa')

@admin.register(Reconocimientos)
class ReconocimientosAdmin(admin.ModelAdmin):
    list_display = ('tiporeconocimiento', 'descripcionreconocimiento', 'entidadpatrocinadora', 'idperfil')
    list_filter = ('tiporeconocimiento', 'activarparaqueseveaenfront')

@admin.register(CursosRealizados)
class CursosRealizadosAdmin(admin.ModelAdmin):
    list_display = ('nombrecurso', 'entidadpatrocinadora', 'totalhoras', 'idperfil')
    search_fields = ('nombrecurso', 'entidadpatrocinadora')

@admin.register(ProductosAcademicos)
class ProductosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('nombrerecurso', 'clasificador', 'idperfil')

@admin.register(ProductosLaborales)
class ProductosLaboralesAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'fechaproducto', 'idperfil')

@admin.register(VentaGarage)
class VentaGarageAdmin(admin.ModelAdmin):
    list_display = ('nombreproducto', 'valordelbien', 'estadoproducto', 'fechapublicacion', 'idperfil')
    list_filter = ('estadoproducto', 'activarparaqueseveaenfront')