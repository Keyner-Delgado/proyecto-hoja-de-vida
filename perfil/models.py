from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class DatosPersonales(models.Model):
    SEXO_CHOICES = [('H', 'Hombre'), ('M', 'Mujer')]

    idperfil = models.AutoField(primary_key=True)
    descripcionperfil = models.CharField(max_length=200, null=True, blank=True, verbose_name="Descripción del Perfil")
    perfilactivo = models.IntegerField(
    default=1,
    choices=[(1, '1 (Activo)'), (0, '0 (Inactivo)')], # Crea un menú desplegable con los números
    validators=[
        MinValueValidator(0),
        MaxValueValidator(1)
    ],
    verbose_name="Estado del Perfil"    
    )    
    apellidos = models.CharField(max_length=60, verbose_name="Apellidos")
    nombres = models.CharField(max_length=60, verbose_name="Nombres")
    nacionalidad = models.CharField(max_length=20, null=True, blank=True, verbose_name="Nacionalidad")
    lugarnacimiento = models.CharField(max_length=60, null=True, blank=True, verbose_name="Lugar de Nacimiento")
    fechanacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    numerocedula = models.CharField(max_length=10, unique=True, verbose_name="Nº de Cédula")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    estadocivil = models.CharField(max_length=50, null=True, blank=True, verbose_name="Estado Civil")
    licenciaconducir = models.CharField(max_length=6, null=True, blank=True, verbose_name="Licencia de Conducir")
    telefonoconvencional = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono Convencional")
    telefonofijo = models.CharField(max_length=15, null=True, blank=True, verbose_name="Teléfono Fijo")
    direcciontrabajo = models.CharField(max_length=50, null=True, blank=True, verbose_name="Dirección de Trabajo")
    direcciondomiciliaria = models.CharField(max_length=50, null=True, blank=True, verbose_name="Dirección Domiciliaria")
    sitioweb = models.CharField(max_length=150, null=True, blank=True, verbose_name="Sitio Web")
    correo = models.EmailField(max_length=100, unique=True, verbose_name="Correo Electrónico")
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True, verbose_name="Foto de Perfil")

    class Meta:
        verbose_name = "Dato Personal"
        verbose_name_plural = "1. Datos Personales"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    idexperiencialaboral = models.AutoField(primary_key=True)
    idperfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, db_column='idperfilconqueestaactivo', verbose_name="Perfil")
    cargodesempenado = models.CharField(max_length=250, verbose_name="Cargo Desempeñado")
    nombrempresa = models.CharField(max_length=50, verbose_name="Nombre de la Empresa")
    lugarempresa = models.CharField(max_length=50, verbose_name="Ciudad/Lugar")
    emailempresa = models.EmailField(max_length=100, verbose_name="Email de la Empresa")
    sitiowebempresa = models.CharField(max_length=150, null=True, blank=True, verbose_name="Web de la Empresa")
    nombrecontactoempresarial = models.CharField(max_length=100, verbose_name="Nombre de Contacto")
    telefonocontactoempresarial = models.CharField(max_length=60, verbose_name="Teléfono de Contacto")
    fechainiciogestion = models.DateField(verbose_name="Fecha de Inicio")
    fechafingestion = models.DateField(null=True, blank=True, verbose_name="Fecha de Fin")
    descripcionfunciones = models.CharField(max_length=250, verbose_name="Descripción de Funciones")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en la Web")
    rutacertificado = models.FileField(
        upload_to='certificados/experiencia/', 
        null=True, 
        blank=True, 
        verbose_name="Subir Certificado Laboral"
    )
    # Opción de enlace (Google Drive / Web)
    url_certificado_externo = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="Link del Certificado"
    )
    class Meta:
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "2. Experiencia Laboral"

class CursosRealizados(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)
    idperfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, db_column='idperfilconqueestaactivo', verbose_name="Perfil")
    nombrecurso = models.CharField(max_length=100, verbose_name="Nombre del Curso")
    fechainicio = models.DateField(verbose_name="Fecha Inicio")
    fechafin = models.DateField(verbose_name="Fecha Fin")
    totalhoras = models.IntegerField(verbose_name="Total de Horas")
    descripcioncurso = models.CharField(max_length=250, verbose_name="Descripción")
    entidadpatrocinadora = models.CharField(max_length=100, verbose_name="Entidad Patrocinadora")
    nombrecontactoauspicia = models.CharField(max_length=100, verbose_name="Contacto Auspiciante")
    telefonocontactoauspicia = models.CharField(max_length=60, verbose_name="Teléfono Contacto")
    emailempresapatrocinadora = models.EmailField(max_length=60, verbose_name="Email Empresa")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Activo en Web")
    rutacertificado = models.FileField(
        upload_to='certificados/', 
        null=True, 
        blank=True, 
        verbose_name="Subir Certificado"
    )
    # Nuevo campo para link externo
    url_certificado_externo = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="Link del Certificado"
    )
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "3. Cursos Realizados"

class ProductosAcademicos(models.Model):
    idproductoacademico = models.AutoField(primary_key=True)
    idperfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, db_column='idperfilconqueestaactivo', verbose_name="Perfil")
    nombrerecurso = models.CharField(max_length=100, verbose_name="Nombre del Recurso")
    clasificador = models.CharField(max_length=100, verbose_name="Tipo (Clasificador)")
    descripcion = models.CharField(max_length=250, verbose_name="Descripción")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en Web")

    class Meta:
        verbose_name = "Producto Académico"
        verbose_name_plural = "4. Productos Académicos"

class ProductosLaborales(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)
    idperfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, db_column='idperfilconqueestaactivo', verbose_name="Perfil")
    nombreproducto = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    fechaproducto = models.DateField(verbose_name="Fecha de Producto")
    descripcion = models.CharField(max_length=250, verbose_name="Descripción")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en Web")

    class Meta:
        verbose_name = "Producto Laboral"
        verbose_name_plural = "5. Productos Laborales"

class Reconocimientos(models.Model):
    TIPO_CHOICES = [('Académico', 'Académico'), ('Público', 'Público'), ('Privado', 'Privado')]
    idreconocimiento = models.AutoField(primary_key=True)
    idperfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, db_column='idperfilconqueestaactivo', verbose_name="Perfil")
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES, verbose_name="Tipo de reconocimiento")
    fechareconocimiento = models.DateField(verbose_name="Fecha del reconocimiento")
    descripcionreconocimiento = models.CharField(max_length=250, verbose_name="Descripción")
    entidadpatrocinadora = models.CharField(max_length=100, verbose_name="Entidad Patrocinadora")
    nombrecontactoauspicia = models.CharField(max_length=100, verbose_name="Nombre de Contacto")
    telefonocontactoauspicia = models.CharField(max_length=60, verbose_name="Teléfono Contacto")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en Web")
    rutacertificado = models.FileField(
        upload_to='reconocimientos/', 
        null=True, 
        blank=True, 
        verbose_name="Archivo del Reconocimiento"
    )
    # Nuevo campo para link externo
    url_certificado_externo = models.URLField(
        max_length=500, 
        null=True, 
        blank=True, 
        verbose_name="Link del Certificado"
    )
    class Meta:
        verbose_name = "Reconocimiento"
        verbose_name_plural = "6. Reconocimientos"

class VentaGarage(models.Model):
    ESTADO_CHOICES = [('Bueno', 'Bueno'), ('Regular', 'Regular')]
    idventagarage = models.AutoField(primary_key=True)
    idperfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, db_column='idperfilconqueestaactivo', verbose_name="Perfil")
    nombreproducto = models.CharField(max_length=100, verbose_name="Nombre del producto")
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES, verbose_name="Estado del producto")
    descripcion = models.CharField(max_length=250, verbose_name="Descripción")
    valordelbien = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Valor ($)")
    activarparaqueseveaenfront = models.BooleanField(default=True, verbose_name="Mostrar en Web")
    fotoproducto = models.ImageField(upload_to='garage/', null=True, blank=True, verbose_name="Foto del Producto")

    class Meta:
        verbose_name = "Artículo de Garage"
        verbose_name_plural = "7. Venta de Garage"

class ReporteUnificado(models.Model):
    TIPO_CHOICES = [
        ('CURSOS', 'Certificados de Cursos'),
        ('RECONOCIMIENTOS', 'Reconocimientos y Premios'),
    ]
    
    tipo = models.CharField(
        max_length=20, 
        choices=TIPO_CHOICES, 
        unique=True, 
        verbose_name="Categoría del Reporte"
    )
    archivo_pdf = models.FileField(
        upload_to='reportes_unificados/', 
        verbose_name="Archivo PDF Unificado"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última modificación"
    )

    class Meta:
        # Esto hace que aparezca como la opción 8 en tu panel
        verbose_name = "8. Reporte Unificado"
        verbose_name_plural = "8. Reportes Unificados"

    def __str__(self):
        return f"Reporte de {self.get_tipo_display()}"