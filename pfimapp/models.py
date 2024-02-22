from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from .validators import validate_min_length_correo,validate_min_length_and_letters, validate_password,validate_numeric_length,validate_min_numeric_length,validate_past_date
from django.utils.translation import gettext_lazy as _

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

# Es1 = 'A'
# Es2 = 'I'
# ESTADO_OFERTA = [
#     (Es1, 'Activo'),
#     (Es2, 'Inactivo')
# ]

class EstadoCivil(models.Model):

    nombre = models.CharField(max_length=50)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "02 - Estado Civil"

class Sede(models.Model):

    nombre = models.CharField(max_length=50)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)  
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "04 - Sede"

class Maestria(models.Model):

    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)   
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)

    class Meta:
        verbose_name_plural = "11 - Maestrias"

class TipoDocumento(models.Model):

    nombre = models.CharField(max_length=50)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "01 - Tipo de Documentos"

class UsuarioManager(BaseUserManager):

    def create_user(self, email, primerNombre, apellidoPaterno, segundoNombre, apellidoMaterno,numeroUbigeoNacimiento, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not primerNombre:
            raise ValueError('El usuario debe tener un primer nombre')
        if not segundoNombre:
            raise ValueError('El usuario debe tener un segundo nombre')        
        if not apellidoPaterno:
            raise ValueError('El usuario debe tener un apellido paterno')
        if not apellidoMaterno:
            raise ValueError('El usuario debe tener un apellido materno')

        user = self.model(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            numeroUbigeoNacimiento=numeroUbigeoNacimiento,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, primerNombre, segundoNombre,apellidoPaterno,apellidoMaterno,numeroUbigeoNacimiento, password):
        user = self.create_user(
            email=self.normalize_email(email),
            primerNombre=primerNombre,
            segundoNombre=segundoNombre,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            numeroUbigeoNacimiento=numeroUbigeoNacimiento,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    password = models.CharField(max_length=128, validators=[validate_password])
    email = models.EmailField(max_length=50, unique=True, validators=[validate_min_length_correo(8)], error_messages={'unique': 'Este correo electrónico ya está en uso.'})
    nacionalidad = models.CharField(max_length=20, validators=[validate_min_length_and_letters(5)])
    tipoDocumento = models.ForeignKey(TipoDocumento, null=True, on_delete=models.SET_NULL)
    numeroDocumento = models.CharField(max_length=12, unique=True, error_messages={'unique': 'Este número de documento ya está en uso.'})
    numeroUbigeoNacimiento = models.CharField(max_length=6, validators=[validate_numeric_length(6)], help_text=_("Ingrese un número de 6 dígitos."))
    direccion = models.CharField(max_length=50)
    primerNombre = models.CharField(max_length=50,validators=[validate_min_length_and_letters(3)])
    segundoNombre = models.CharField(max_length=50, validators=[validate_min_length_and_letters(3)],null=True, blank=True)
    apellidoPaterno = models.CharField(max_length=50, validators=[validate_min_length_and_letters(3)])
    apellidoMaterno = models.CharField(max_length=50, validators=[validate_min_length_and_letters(3)])    
    estadoCivil = models.ForeignKey(EstadoCivil, null=True, on_delete=models.SET_NULL)
    correoUNI = models.EmailField(max_length=50, validators=[validate_min_length_correo(8)], unique=True)    
    telefono = models.CharField(max_length=15, validators=[validate_min_numeric_length(7)])
    fechaNacimiento = models.DateField(validators=[validate_past_date], help_text="Formato: AAAA-MM-DD")
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)     
  
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primerNombre', 'segundoNombre','apellidoPaterno','apellidoMaterno','numeroUbigeoNacimiento']

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()
        
    def nombre_completos(self):
        if self.segundoNombre:
            return "{} {} {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre, self.segundoNombre)
        else:
            return "{} {} {}".format(self.apellidoPaterno, self.apellidoMaterno, self.primerNombre)

    def get_max_length(self):
        if self.tipoDocumento:
            document_type = self.tipoDocumento.nombre
            if document_type == 'DOCUMENTO NACIONAL DE IDENTIDAD':
                return 8
            elif document_type == 'CARNET DE EXTRANJERIA' or document_type == 'PASAPORTE':
                return 12
        return 12  # Longitud máxima por defecto
    
    def clean(self):
        super().clean()
        if self.tipoDocumento:
            if self.tipoDocumento.nombre == 'DOCUMENTO NACIONAL DE IDENTIDAD' and len(self.numeroDocumento) != 8:
                raise ValidationError('El número de documento debe tener 8 caracteres para DNI.')
            elif self.tipoDocumento.nombre in ['CARNET DE EXTRANJERIA', 'PASAPORTE'] and len(self.numeroDocumento) < 12:
                raise ValidationError('El número de documento debe tener menos de 12 caracteres para carné de extranjería o pasaporte.')

    def __str__(self):
        return self.nombre_completos()
  
    class Meta:
        verbose_name_plural = "03 - Usuarios"

class EstadoBoletaP(models.Model):

    nombre = models.CharField(max_length=50)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "07 - Estados Boletas Pagos"


class ConceptoPago(models.Model):

    nombre = models.CharField(max_length=50)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "06 - Conceptos de Pagos"

class EstadoAcademico(models.Model):

    nombre = models.CharField(max_length=50)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name_plural = "08 - Estados Academico"

class Periodo(models.Model):

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.codigo

    class Meta:
        unique_together = ['codigo']
        verbose_name_plural = "05 - Periodos"

class Alumno(models.Model):

    usuario = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    periodoDeIngreso = models.ForeignKey(Periodo, null=True, blank=True, on_delete=models.SET_NULL)
    codigoUniPreGrado = models.CharField(max_length=10, null=True, blank=True)
    codigoAlumPFIM = models.CharField(max_length=15, null=True, blank=True)
    estadoAcademico = models.ForeignKey(EstadoAcademico, null=True, on_delete=models.SET_NULL)
    sede = models.ForeignKey(Sede, null=True, on_delete=models.SET_NULL)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)
    
    def nombre_completo(self):
        if self.usuario and self.usuario.segundoNombre:
            return "{} {} {} {}-{}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.usuario.segundoNombre, self.maestria.codigo)
        elif self.usuario:
            return "{} {} {}-{}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.maestria.codigo)
        else:
            return "Nombre no disponible"
       
    def clean(self):
        print("Validación de clean en el modelo Alumno...")
        # Validación de unicidad basada en el campo eliminado
        if self.pk is None:  # Solo para nuevos registros
            if Alumno.objects.filter(usuario=self.usuario, maestria=self.maestria, eliminado=True).exists():
                print("Permitiendo la creación de un nuevo registro.")
                return  # Permitir la creación incluso si existe un registro eliminado
            elif Alumno.objects.filter(usuario=self.usuario, maestria=self.maestria, eliminado=False).exists():
                raise ValidationError('Ya existe un alumno activo con la misma combinación de usuario y maestría.')
        else:
            print("No se está ejecutando la validación para un nuevo registro.")


    def save(self, *args, **kwargs):
        
        # Ejecutar la validación antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()
        
    def __str__(self):
        return self.nombre_completo()

    class Meta:
        unique_together = ['usuario', 'maestria']
        verbose_name_plural = "09 - Alumnos"

class ReporteEconomico(models.Model):

    alumno = models.ForeignKey(Alumno, null=True, on_delete=models.SET_NULL)
    conceptoPago = models.ManyToManyField(ConceptoPago, through='ReporteEcoConceptoPago', blank=True,)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    class Meta:

        verbose_name_plural = "10 - Reportes Economicos"


class ReporteEcoConceptoPago(models.Model):

    reporteEconomico = models.ForeignKey(ReporteEconomico, null=True, on_delete=models.SET_NULL)
    conceptoPago = models.ForeignKey(ConceptoPago, null=True, on_delete=models.SET_NULL)
    periodo = models.ForeignKey(Periodo, null=True, on_delete=models.SET_NULL)
    monto = models.FloatField()
    numeroRecibo = models.CharField(max_length=100, null=True, blank=True)
    estadoBoletaPago = models.ForeignKey(EstadoBoletaP, null=True, on_delete=models.SET_NULL)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

class Curso(models.Model):

    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    credito = models.IntegerField()
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nombre)

    class Meta:
        verbose_name_plural = "12 - Cursos"

class Docente(models.Model):

    usuario = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def nombre_completo(self):        
        if self.usuario.segundoNombre:
            return "{} {} {} {}, {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.usuario.segundoNombre, self.maestria.codigo)
        else:
            return "{} {} {}, {}".format(self.usuario.apellidoPaterno, self.usuario.apellidoMaterno, self.usuario.primerNombre, self.maestria.codigo)
    
    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        unique_together = ['usuario', 'maestria']
        verbose_name_plural = "13 - Docentes"

class DefinicionCalificacion(models.Model):
    nombre = models.CharField(max_length=50)
    porcentaje = models.IntegerField()
    seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)  # revisar si funciona
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tipos de Calificaciones"

class Seccion(models.Model):

    maestria = models.ForeignKey(Maestria, null=True, on_delete=models.SET_NULL)
    periodo = models.ForeignKey(Periodo, null=True, on_delete=models.SET_NULL)
    curso = models.ForeignKey(Curso, null=True, on_delete=models.SET_NULL)
    docente = models.ForeignKey(Docente, null=True, on_delete=models.SET_NULL)     
    aulaWeb = models.CharField(max_length=100, null=True, blank=True)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def nombre_completo(self):
        return "{} / {} {} {} / {} {} {}".format(self.periodo.codigo, self.maestria.codigo, self.curso.codigo, self.curso.nombre, self.docente.usuario.apellidoPaterno, self.docente.usuario.apellidoMaterno, self.docente.usuario.primerNombre)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "14 - Secciones"

class Matricula(models.Model):
    alumno = models.ForeignKey(Alumno, null=True, on_delete=models.SET_NULL)
    seccion = models.ManyToManyField(Seccion, through='DetalleMatricula', blank=True,)    
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    # def get_periodo(self):
    #     return self.seccion.first().periodo.codigo if self.seccion.exists() else None
    
    def nombre_completo(self):
        if self.alumno and self.alumno.usuario and self.alumno.usuario.segundoNombre:
            return "{} {} {} {}".format(
                self.alumno.usuario.apellidoPaterno,
                self.alumno.usuario.apellidoMaterno,
                self.alumno.usuario.primerNombre,
                self.alumno.usuario.segundoNombre,                    
            )
        elif self.alumno and self.alumno.usuario:
            return "{} {} {}".format(
                self.alumno.usuario.apellidoPaterno,
                self.alumno.usuario.apellidoMaterno,
                self.alumno.usuario.primerNombre,                    
            )
        else:
            return "Nombre no disponible"
        
    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()
        
    def __str__(self):        
        return self.nombre_completo()

    class Meta:
        verbose_name_plural = "15 - Matriculas"

class DetalleMatricula(models.Model):
    matricula = models.ForeignKey(Matricula, null=True, on_delete=models.SET_NULL) # revisar
    seccion = models.ForeignKey(Seccion, null=True, on_delete=models.SET_NULL) # revisar      
    retirado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    fechaRegistro = models.DateField(default=timezone.now)
    fechaModificado = models.DateField(null=True, blank=True, auto_now=True)    
    ipUsuario = models.CharField(null=True, default=s.getsockname()[0], blank=True, max_length=100)
    usuarioPosgradoFIM = models.CharField(null=True, blank=True, max_length=200)

    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()

    def __str__(self):
        
        curso = self.seccion.curso
        periodo = self.seccion.periodo
        alumno = self.matricula.alumno.usuario
        return f"{alumno.apellidoPaterno} {alumno.apellidoMaterno}, {curso}, {periodo}"
    
    # def calcular_nota_final(self):
        #calificaciones # referencia inversa
        # for calificacion
        # sumatoria ( calificacion.definicionCalificacion.porcentaje * calificacion.nota) /100
        #self.nota_final = resultasdo
        # pass

    class Meta:
        verbose_name_plural = "Detalle de Matriculas"

class Calificacion(models.Model):
    
    detalle_matricula = models.ForeignKey(DetalleMatricula, on_delete=models.CASCADE)
    definicionCalificacion = models.ForeignKey(DefinicionCalificacion, on_delete=models.CASCADE)
    nota = models.FloatField(null=True, blank=True)
    fecha_calificacion = models.DateField(default=timezone.now)
    eliminado = models.BooleanField(default=False)  # Campo para la eliminación suave
    
    def delete(self, *args, **kwargs):
        self.eliminado = True
        self.save()
    
    def __str__(self):        
        detalle_matricula = self.detalle_matricula
        alumno = detalle_matricula.matricula.alumno
        maestria = detalle_matricula.seccion.maestria
        curso = detalle_matricula.seccion.curso
        docente = detalle_matricula.seccion.docente
        return f"Calificación de {alumno} en {maestria} / {curso} / {docente} / Nota: {self.nota})"

    class Meta:
        verbose_name_plural = "Calificaciones"