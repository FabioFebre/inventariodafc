from django.urls import path
from . import views 
from .views import buscar_producto, buscar_sugerencias, productos_por_proveedor

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop-single/', views.shop_single, name='shop-single'),
    path('shop/<int:proveedor_id>/<int:categoria_id>/', views.shop, name='shop'),
    path('servicio-postventa/', views.servi_postventa, name='servicio-postventa'),
    path('buscar/', buscar_producto, name='buscar_producto'),

    path('buscar-sugerencias/', buscar_sugerencias, name='buscar_sugerencias'),  # Nueva ruta

    path('proveedor/<int:proveedor_id>/', productos_por_proveedor, name='productos_por_proveedor'),
    
    path('busqueda/categoria/<int:categoria_id>/', views.productos_por_categoria_busqueda, name='productos_por_categoria_busqueda'),

    path('shopd/<int:id>/', views.detalle_producto, name='detalle_producto'),  # Nueva ruta para producto detalle
    path('producto/<int:id>/brochure/', views.descargar_brochure, name='descargar_brochure'),
    path('prov_categorias_produc/', views.pro_categorias_product, name='prov_categorias_produc'),
    path('prov_categorias_rp/', views.pro_categorias_rp, name='prov_categorias_rp')
]
