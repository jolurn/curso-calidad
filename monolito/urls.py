"""monolito URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pfimapp import views
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView

admin.site.site_header = 'Posgrado FIM UNI'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('adminLogin/', views.admin_login, name='admin_login'),
    path('docenteLogin/', views.docente_login, name='docente_login'),

    path('adminDashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reporte-calificaciones/', views.reporte_calificaciones, name='reporte_calificaciones'),
    # path('matricula/', views.matricula, name='matricula'),
    path('registro-pagos/', views.registro_pagos, name='registro_pagos'),
    path('obtener-alumnos-por-sede/', views.obtener_alumnos_por_sede, name='obtener_alumnos_por_sede'),
    path('obtener-alumnos-por-periodo/', views.obtener_alumnos_por_periodo, name='obtener_alumnos_por_periodo'),    
    path('generar_reporte_boleta_matricula/', views.generar_reporte_boleta_matricula, name='generar_reporte_boleta_matricula'),


    path('usuarios/editar/<int:pk>/', views.CustomUserUpdateView.as_view(), name='customuser_update'),
    path('matricula/<int:matricula_id>/', views.detalleMatricula, name='detalle_matricula'),
    path('reporteMatricula/', views.reporteMatricula, name='reporteMatricula'),  
    path('reporteAcademico/', views.reporteAcademico, name='reporteAcademico'),  
    path('reporteEconomico/', views.reporteEconomico, name='reporteEconomico'),  
    path('logout/', views.signout, name='logout'),
    path('logoutDocente/', views.signout, {'redirect_to': 'docente_login'}, name='logout_docente'),     
    path('logoutAdministrativo/', views.signout, {'redirect_to': 'admin_login'}, name='logout_administrativo'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('signin/', LoginView.as_view(template_name='signin.html'), name='signin'),
    
    path('generar-pdf/', views.generar_pdf, name='generar-pdf'),
    path('generar-pdf-admin/', views.generar_pdf_administrativo, name='generar_pdf_administrativo'),
    path('generar_pdf_pagos-admin/', views.generar_pdf_pagos, name='generar_pdf_pagos'),
    path('generar_pdf_boleta_matricula/', views.generar_pdf_boleta_matricula, name='generar_pdf_boleta_matricula'),

    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False)),
    
    path('guardar_calificaciones/', views.guardar_calificaciones, name='guardar_calificaciones'),

    path('editar_notas/<int:seccion_id>/', views.editar_notas, name='editar_notas'),    
    path('actualizar_calificacion/', views.actualizar_calificacion, name='actualizar_calificacion'),    
    path('cargar_calificaciones/', views.cargar_calificaciones, name='cargar_calificaciones'),
    path('obtener-maestrias-y-cursos/', views.obtener_maestrias_y_cursos, name='obtener_maestrias_y_cursos'),
   
]
