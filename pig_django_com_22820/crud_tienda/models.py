from django.db import models
from django.urls import reverse

# Create your models here.

SEXO = (
    ('M', 'Mujer'),
    ('H', 'Hombre'),
)

#Clase abstracta para cada categoría

class Item(models.Model):

    nombre = models.CharField(max_length=50, verbose_name='Producto')
    precio = models.FloatField()
    foto = models.ImageField(upload_to='productos', null=True,blank=True)
    info = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre

    class Meta:
        abstract = True

#Vestimenta y sus opciones

class Vestimenta(Item):

    SUBCATEGORIA = (
    ('RC', 'Remeras & Chombas'),
    ('BS', 'Bermudas & Shorts'),
    ('BC', 'Buzos & Camperas'),
    ('PC', 'Pantalones & Calzas'),
    )

    categoria = "Vestimenta"
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIA, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("mypage_detail", kwargs={"pk": self.pk})

class Opciones_vestimenta(models.Model):
    
    TALLES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    )

    talle = models.CharField(max_length=2, choices=TALLES, blank=True, null=True)
    stock = models.PositiveIntegerField()
    vestimenta = models.ForeignKey(Vestimenta, on_delete=models.CASCADE)

    def __str__(self):
        return ''

#Calzado y sus opciones

class Calzado(Item):

    categoria = "Calzado"
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True, null=True)

class Opciones_calzado(models.Model):
    
    TALLES = (
    ('34.5', '34.5(3.5 uk)'),
    ('35.5', '35.5(4 uk)'),
    ('36', '36(4.5 uk)'),
    ('38', '38(6 uk)'),
    ('39', '39(7 uk)'),
    ('40', '40(8 uk)'),
    ('41', '41(8.5 uk)'),
    ('41.5', '41.5(9 uk)'),
    ('42', '42(9.5 uk)'),
    ('43', '43(10 uk)'),
    ('44', '44(11 uk)'),
    ('45', '45(11.5 uk)'),
    )

    talle = models.CharField(max_length=4, choices=TALLES, blank=True, null=True)
    stock = models.PositiveIntegerField()
    calzado = models.ForeignKey(Calzado, null=False, blank=False, on_delete=models.CASCADE, related_name='calzado_relacionado')

    def __str__(self):
        return ''

#Suplementos y sus opciones

class Suplemento(Item):

    SUBCATEGORIA = (
        ('PR', 'Proteínas'),
        ('VT', 'Vitaminas'),
    )
    
    categoria = "Suplementos"
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIA, blank=True, null=True)
    stock = models.PositiveIntegerField()

#Accesorios y sus opciones

class Accesorio(Item):

    SUBCATEGORIA = (
    ('MO', 'Moda'),
    ('EN', 'Entrenamiento'),
    )

    categoria = "Accesorios"
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIA, blank=True, null=True)
    stock = models.PositiveIntegerField()
