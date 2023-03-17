from django.urls import path, re_path
from crud_tienda.views import IndexView
from . import views
from .views import AdministradorView,AdministradorVestList,AdministradorCalzList,AdministradorAcceList,AdministradorSuplList, CalzadoLista, AccesoriosLista, SuplementosLista, VestimentaLista, AccesoriosDetalle, AccesorioCreate,AccesorioUpdate, AccesorioDelete, SuplementosDetalle,SuplementoCreate, SuplementoUpdate, SuplementoDelete, CalzadoDetalle, CalzadoCreate, CalzadoUpdate, CalzadoDelete, VestimentaDetalle, VestimentaCreate, VestimentaUpdate, VestimentaDelete #, VestimentaCreateTalle
from django.conf import settings

urlpatterns = [
    path('', IndexView.as_view() ,name="Home"),
    path('vestimenta/', VestimentaLista.as_view(),name='Vestimenta'),
    path('vestimenta/<str:filtro>/', VestimentaLista.as_view(),name='Vestimenta-filtro'),
    path('calzado/', CalzadoLista.as_view(),name='Calzado'),
    path('calzado/<str:filtro>/', CalzadoLista.as_view(),name='Calzado-filtro'),
    path('accesorios/', AccesoriosLista.as_view(),name='Accesorios'),
    path('accesorios/<str:filtro>/', AccesoriosLista.as_view(),name='Accesorios-filtro'),
    path('suplementos/', SuplementosLista.as_view(),name='Suplementos'),
    path('suplementos/<str:filtro>/', SuplementosLista.as_view(),name='Suplementos-filtro'),
    path('accesorios/<int:pk>', AccesoriosDetalle.as_view(), name="Accesorios-detalle"), 
    path('calzado/<int:pk>', CalzadoDetalle.as_view(), name="Calzado-detalle"),
    path('suplementos/<int:pk>', SuplementosDetalle.as_view(), name="Suplementos-detalle"), 
    path('vestimenta/<int:pk>', VestimentaDetalle.as_view(), name="Vestimenta-detalle"), 
    path('contacto/',views.contacto, name="Contacto"),
    # administrador
    path('administrador/', AdministradorView.as_view(), name="Administrador"),    
    path('administrador/Vestimenta/', AdministradorVestList.as_view(), name="Administrar_vestimenta"),
    path('administrador/Vestimenta/create/', VestimentaCreate.as_view(), name="Crear-vestimenta"),
    # path('administrador/Vestimenta/create/<int:pk>', VestimentaCreateTalle.as_view(), name="Crear-vestimenta-opciones"),
    path('administrador/Vestimenta/update/<int:pk>', VestimentaUpdate.as_view(), name="Actualizar-vestimenta"),
    path('administrador/Vestimenta/delete/<int:pk>', VestimentaDelete.as_view(), name="Borrar-vestimenta"),
    path('administrador/Calzado/', AdministradorCalzList.as_view(), name="Administrar_calzado"),
    path('administrador/Calzado/create/', CalzadoCreate.as_view(), name="Crear-calzado"),
    path('administrador/Calzado/update/<int:pk>', CalzadoUpdate.as_view(), name="Actualizar-calzado"),
    path('administrador/Calzado/delete/<int:pk>', CalzadoDelete.as_view(), name="Borrar-calzado"),
    path('administrador/Accesorios/', AdministradorAcceList.as_view(), name="Administrar_accesorios"),
    path('administrador/Accesorios/create/', AccesorioCreate.as_view(), name="Crear-accesorio"),
    path('administrador/Accesorios/update/<int:pk>', AccesorioUpdate.as_view(), name="Actualizar-accesorio"),
    path('administrador/Accesorios/delete/<int:pk>', AccesorioDelete.as_view(), name="Borrar-accesorio"),
    path('administrador/Suplementos/', AdministradorSuplList.as_view(), name="Administrar_suplementos"),
    path('administrador/Suplementos/create/', SuplementoCreate.as_view(), name="Crear-suplemento"),
    path('administrador/Suplementos/update/<int:pk>', SuplementoUpdate.as_view(), name="Actualizar-suplemento"),
    path('administrador/Suplementos/delete/<int:pk>', SuplementoDelete.as_view(), name="Borrar-suplemento"),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)