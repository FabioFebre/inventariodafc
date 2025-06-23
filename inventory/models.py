from django.db import models

class Proveedor(models.Model):
    """Modelo para los proveedores."""
    MAQUINARIA = 'maquinaria'
    REPUESTOS_LUBRICANTES = 'repuestos_lubricantes'
    AMBOS = 'ambos'

    TIPO_PRODUCTO_CHOICES = [
        (MAQUINARIA, 'Maquinaria'),
        (REPUESTOS_LUBRICANTES, 'Repuestos y Lubricantes'),
        (AMBOS, 'Ambos'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre del proveedor")
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)
    email = models.EmailField(verbose_name="Correo electrónico", blank=True, null=True)
    tipo_producto = models.CharField(
        max_length=30,
        choices=TIPO_PRODUCTO_CHOICES,
        default=MAQUINARIA,
        verbose_name="Tipo de Producto"
    )
    imagen = models.ImageField(
        upload_to='proveedores/',
        verbose_name="Imagen del proveedor",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    """Categorías globales, sin relación directa con proveedores."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField(
        verbose_name="Descripción",
        null=True,
        blank=True
    )
    
    color = models.CharField(
        max_length=100, 
        null=True,
        blank=True,
    )

    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT,
        related_name='productos',
        verbose_name="Categoría"
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE,
        related_name='productos',
        verbose_name="Proveedor",
        null=True,  # Temporalmente
        blank=True
    )
    modelo = models.CharField(max_length=100, verbose_name="Modelo", blank=True, null=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio",
        null=True,    # Permite valores nulos en la base de datos
        blank=True    # Permite dejar el campo vacío en formularios
    )
    especificaciones = models.TextField(verbose_name="Especificaciones", blank=True, null=True)
    def especificaciones_formateadas(self):
        return "\n".join(f"• {line}" for line in self.especificaciones.splitlines())

    imagen = models.ImageField(upload_to='imagenes/')
    brochure = models.FileField(
        upload_to='brochures/',
        verbose_name="Brochure PDF",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.proveedor.nombre}"


class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='imagenes_productos/')
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
