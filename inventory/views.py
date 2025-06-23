from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto, Categoria, Proveedor
from django.contrib import messages
from django.views.generic import DeleteView
from django.http import JsonResponse
from django.http import FileResponse, Http404
from django.db.models import Q

# Función común para obtener proveedores y categorías
def obtener_proveedores_con_categorias_maquinaria():
    # Proveedores con tipo Maquinaria o Ambos
    proveedores = Proveedor.objects.filter(tipo_producto__in=[Proveedor.MAQUINARIA, Proveedor.AMBOS])
    proveedores_con_categorias = {}
    for proveedor in proveedores:
        if proveedor.tipo_producto == Proveedor.AMBOS:
            # Para proveedores 'Ambos' en PRODUCTOS:
            # Se muestran solo las categorías que NO contengan "repuesto" ni "lubricante"
            categorias = Categoria.objects.filter(
                productos__proveedor=proveedor
            ).exclude(
                Q(nombre__icontains="repuesto") | Q(nombre__icontains="lubricante")
            ).distinct()
        else:
            categorias = Categoria.objects.filter(productos__proveedor=proveedor).distinct()
        proveedores_con_categorias[proveedor] = categorias
    return proveedores_con_categorias

def obtener_proveedores_con_categorias_repuestos():
    # Proveedores con tipo Repuestos y Ambos
    proveedores = Proveedor.objects.filter(tipo_producto__in=[Proveedor.REPUESTOS_LUBRICANTES, Proveedor.AMBOS])
    proveedores_con_categorias = {}
    for proveedor in proveedores:
        if proveedor.tipo_producto == Proveedor.AMBOS:
            # Para proveedores 'Ambos' en REPUESTOS:
            # Se muestran solo las categorías que contengan "repuesto" o "lubricante"
            categorias = Categoria.objects.filter(
                productos__proveedor=proveedor
            ).filter(
                Q(nombre__icontains="repuesto") | Q(nombre__icontains="lubricante")
            ).distinct()
        else:
            categorias = Categoria.objects.filter(productos__proveedor=proveedor).distinct()
        proveedores_con_categorias[proveedor] = categorias
    return proveedores_con_categorias


def home(request):

    todos_proveedores = Proveedor.objects.all()

    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    context = {
        'todos_proveedores': todos_proveedores,
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos,
    }
    return render(request, 'inventario/index.html', context)

def pro_categorias_product(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/prov_categorias_pro.html', {
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
        })

def pro_categorias_rp(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/prov_categorias_rp.html', {
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
        })

def about(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/about.html', {
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
        })

def servi_postventa(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/servicio-postventa.html', {
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos,
        'name_contact': 'Servicio post-venta',
        'whatsapp_number': '51913949341'  # Número exclusivo para post-venta
        })

def contact(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/contact.html', {
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
        })

def shop_single(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/shop-single.html', {
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
        })

def shop(request, proveedor_id, categoria_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    # Filtrar productos que pertenezcan al proveedor y a la categoría indicada
    productos = Producto.objects.filter(proveedor=proveedor, categoria=categoria)

    sort_option = request.GET.get('sort', 'featured')
    if sort_option == 'az':
        productos = productos.order_by('nombre')
    elif sort_option == 'za':
        productos = productos.order_by('-nombre')

    # Paginación (9 productos por página)
    page = request.GET.get('page', 1)
    paginator = Paginator(productos, 9)  # 9 productos por página

    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)

    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/shop.html', {
        'proveedor': proveedor,
        'categoria': categoria, 
        'productos': productos_paginados,  # Pasamos los productos paginados
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos,
        'sort_option': sort_option,
    })


def productos_por_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    tipo = request.GET.get('tipo')
    
    # Filtramos productos directamente por el proveedor.
    productos = Producto.objects.filter(proveedor=proveedor)
    
    # Si se pasa el parámetro 'tipo' y el proveedor no es de ambos, validamos.
    if tipo and proveedor.tipo_producto != Proveedor.AMBOS and proveedor.tipo_producto != tipo:
        productos = Producto.objects.none()

    # Paginación (9 productos por página)
    page = request.GET.get('page', 1)
    paginator = Paginator(productos, 9)  # 9 productos por página

    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)
    
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/productos_proveedor.html', {
        'proveedor': proveedor,
        'productos': productos_paginados,  # Pasamos los productos paginados
        'tipo': tipo,
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
    })

def productos_por_categoria_busqueda(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)

    filtro_proveedor = request.GET.get('proveedor_id')  # parámetro opcional para filtrar por proveedor

    if filtro_proveedor:
        try:
            filtro_proveedor = int(filtro_proveedor)
            productos = productos.filter(proveedor__id=filtro_proveedor)
        except ValueError:
            pass

    # Obtenemos los proveedores asociados a la categoría, para el filtro
    proveedores_categoria_ids = Producto.objects.filter(categoria=categoria).values_list('proveedor', flat=True).distinct()
    proveedores_categoria = Proveedor.objects.filter(id__in=proveedores_categoria_ids)

    # Paginación (9 productos por página)
    page = request.GET.get('page', 1)
    paginator = Paginator(productos, 9)  # 9 productos por página

    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)

    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    
    return render(request, 'inventario/productos_categoria_busqueda.html', {
        'categoria': categoria,
        'productos': productos_paginados,  # Pasamos los productos paginados
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos,
        'proveedores_categoria': proveedores_categoria,
        'filtro_proveedor': filtro_proveedor,
    })

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    # Obtener productos relacionados: misma categoría y mismo proveedor, excluyendo el producto actual
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria,
        proveedor=producto.proveedor
    ).exclude(id=id)[:10]  # Limita el número de productos a 10
    
    imagenes = producto.imagenes.all()  # Relación con el modelo ImagenProducto
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    return render(request, 'inventario/shop-single.html', {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'imagenes': imagenes,  # Agregar imágenes al contexto
        'proveedores_maquinaria': proveedores_maquinaria,
        'proveedores_repuestos': proveedores_repuestos
    })

def buscar_producto(request):
    proveedores_maquinaria = obtener_proveedores_con_categorias_maquinaria()
    proveedores_repuestos = obtener_proveedores_con_categorias_repuestos()
    query = request.GET.get('q', '').strip()

    if query:
        # Obtiene todos los productos que contengan el término de búsqueda
        productos = Producto.objects.filter(nombre__icontains=query)
        if productos.exists():
            return render(request, 'inventario/productos_busqueda.html', {
                'query': query,
                'productos': productos,
                'proveedores_maquinaria': proveedores_maquinaria,
                'proveedores_repuestos': proveedores_repuestos,
            })
        else:
            return render(request, 'inventario/producto_not_found.html', {
                'query': query,
                'proveedores_maquinaria': proveedores_maquinaria,
                'proveedores_repuestos': proveedores_repuestos
            })
    else:
        # Si no se ingresó ningún término, se puede redirigir a la página principal o mostrar un mensaje de error
        return render(request, 'inventario/producto_not_found.html', {
            'query': query,
            'proveedores_maquinaria': proveedores_maquinaria,
            'proveedores_repuestos': proveedores_repuestos
        })


def buscar_sugerencias(request):
    query = request.GET.get('q', '')
    productos = []
    proveedores = []
    categorias = []
    if query:
        # Se obtienen hasta 8 productos relacionados
        productos_qs = Producto.objects.filter(nombre__icontains=query)[:8]
        productos = list(productos_qs.values('id', 'nombre', 'imagen', 'marca'))
        
        # Se obtienen hasta 5 proveedores relacionados
        proveedores_qs = Proveedor.objects.filter(nombre__icontains=query)[:5]
        proveedores = list(proveedores_qs.values('id', 'nombre'))
        
        # Se obtienen hasta 5 categorías relacionadas
        categorias_qs = Categoria.objects.filter(nombre__icontains=query)[:5]
        categorias = list(categorias_qs.values('id', 'nombre'))
    
    return JsonResponse({
        'productos': productos,
        'proveedores': proveedores,
        'categorias': categorias,
    })

def descargar_brochure(request, id):
    producto = get_object_or_404(Producto, id=id)
    if producto.brochure:
        return FileResponse(producto.brochure.open(), as_attachment=False, content_type='application/pdf')
    else:
        raise Http404("El producto no tiene un brochure disponible.")