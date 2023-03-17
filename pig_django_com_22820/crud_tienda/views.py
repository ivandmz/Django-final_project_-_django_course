from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect # a revisar y borrar

from crud_tienda.models import Vestimenta, Accesorio, Calzado, Suplemento, Opciones_calzado, Opciones_vestimenta, SEXO
from crud_tienda.forms import FormContacto, VestimentaForm, Opcion_vestimentaForm, VestimentaOpcionesFormset, CalzadoForm, CalzadoOpcionesFormset, AccesorioForm, SuplementoForm
from django.core.mail import EmailMessage
from pig_django_com_22820.settings import EMAIL_HOST_USER
from itertools import chain

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# from django.forms import inlineformset_factory # a revisar y borrar
from django.db import transaction


# Create your views here.

def pasar_a_dict(tuplaChoices):
        llaves = []
        for e in tuplaChoices:
            llaves.append(e[0])
        valores = []
        for e in tuplaChoices:
            valores.append(e[1])
        dict = {}
        for i in range(len(valores)):
            dict[llaves[i]]=valores[i]
        return dict

class IndexView(TemplateView):
    template_name = "crud_tienda/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        vestimentas = Vestimenta.objects.all().order_by('?')[:5]
        calzados = Calzado.objects.all().order_by('?')[:5]
        accesorios = Accesorio.objects.all().order_by('?')[:5]
        suplementos = Suplemento.objects.all().order_by('?')[:5]
        queryList = list(chain(vestimentas, calzados, accesorios, suplementos))
        context['object_list'] = queryList
        print(context)  # en produccion se va...
        return context

class AdministradorView(TemplateView):
    template_name = "administrador/administrador_menu.html"

# -------------------------------------------------------------------------------------

class VestimentaLista(ListView):
    model = Vestimenta
    template_name = 'crud_tienda/vestimenta.html'
    sexo = pasar_a_dict(SEXO)
    subcat_dict = pasar_a_dict(Vestimenta.SUBCATEGORIA)
    talles = pasar_a_dict(Opciones_vestimenta.TALLES)

    def get(self, request, *args, **kwargs):
        dict = request.GET
        print('-----------')
        print(dict)
        print('-----------')
        if dict:
            if dict['filtro'] in self.sexo.keys():
                object_list = Vestimenta.objects.filter(sexo=dict['filtro']).order_by('nombre')
                filtro = self.sexo[dict['filtro']]
            elif dict['filtro'] in self.subcat_dict.keys():
                object_list = Vestimenta.objects.filter(subcategoria=str(dict['filtro']))
                filtro = self.subcat_dict[dict['filtro']]
            elif dict['filtro'] in self.talles.keys():
                object_list = Vestimenta.objects.filter(opciones_vestimenta__talle=str(dict['filtro']))
                filtro = self.talles[dict['filtro']]
            return render(request, self.template_name, {"object_list": object_list, "filtro":filtro,"sexo":self.sexo, "talles": self.talles,"subcat_dict":self.subcat_dict})
        else:
            object_list = Vestimenta.objects.all().order_by('nombre')
        return render(request, self.template_name, {"object_list": object_list, "sexo":self.sexo, "talles": self.talles,"subcat_dict":self.subcat_dict})


class VestimentaDetalle(DetailView):
    model = Vestimenta
    template_name = 'crud_tienda/detalle.html'


class AdministradorVestList(ListView):
    model = Vestimenta
    template_name = "administrador/admin_vest_list.html"
    sexo = pasar_a_dict(SEXO)
    subcat_dict = pasar_a_dict(Vestimenta.SUBCATEGORIA)
    talles = pasar_a_dict(Opciones_vestimenta.TALLES)

    def get(self, request, *args, **kwargs):
        object_list = Vestimenta.objects.all().order_by('pk')
        return render(request, self.template_name, {"object_list": object_list, "sexo":self.sexo, "talles": self.talles,"subcat_dict":self.subcat_dict})


@method_decorator(staff_member_required, name='dispatch')
class VestimentaCreate(CreateView):
    # https://stackoverflow.com/questions/65596873/how-to-update-a-django-formset
    template_name = 'administrador/crear_vestimenta.html'
    form_class = VestimentaForm
    model = Vestimenta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['formset'] = VestimentaOpcionesFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VestimentaOpcionesFormset(instance=self.object)

        return context

    def form_valid(self, form): # para validar y salvar en DB
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic(): # si no guarda todo, no guarda nada
            self.object = form.save() # primero guardo el producto

            if formset.is_valid(): #valido opciones_vestimenta
                formset.instance = self.object
                formset.save() # luego guardo opciones_vestimenta

        return redirect('Administrar_vestimenta')


    #----------------------------------------------------------------------------------
    # # https://stackoverflow.com/questions/25321423/django-create-inline-forms-similar-to-django-admin
    # tira este error:
    #<tr><td colspan="2">
    #   <ul class="errorlist nonfield">
    #       <li>(Campo oculto TOTAL_FORMS) Este campo es obligatorio.</li>
    #       <li>(Campo oculto INITIAL_FORMS) Este campo es obligatorio.</li>
    #   </ul>
    # <input type="hidden" name="opciones-TOTAL_FORMS" id="id_opciones-TOTAL_FORMS">
    # <input type="hidden" name="opciones-INITIAL_FORMS" id="id_opciones-INITIAL_FORMS">
    # <input type="hidden" name="opciones-MIN_NUM_FORMS" id="id_opciones-MIN_NUM_FORMS">
    # <input type="hidden" name="opciones-MAX_NUM_FORMS" id="id_opciones-MAX_NUM_FORMS">
    # </td></tr>
    

    # model = Vestimenta
    # second_model = Opciones_vestimenta
    # # fields = ('nombre','precio','foto','info','subcategoria','sexo')
    # form_class = VestimentaForm
    # template_name = 'administrador/crear_vestimenta.html'
    # # data = f'{Vestimenta.objects.last().pk}'
    # # success_url = reverse_lazy('Crear-vestimenta-opciones', args=data) 
    # # success_url = f'{Vestimenta.objects.last().pk}'

    # VestimentaFormSet = inlineformset_factory(Vestimenta,Opciones_vestimenta, form=Opcion_vestimentaForm, extra=5)

    # def post(self, request, *args, **kwargs):
    #     vestimenta_form = self.form_class(request.POST,request.FILES,prefix='item') #(VestimentaForm)
    #     # opciones_formset = self.VestimentaFormSet(request.POST,prefix='opciones')
    #     # print(opciones_formset)
    #     if vestimenta_form.is_valid(): #and opciones_formset.is_valid():
    #         vestimenta = vestimenta_form.save()  # guardo primero el producto para tenerlo en opciones
    #         opciones_formset = self.VestimentaFormSet(request.POST,prefix='opciones',instance=vestimenta)  # uno el post de opciones con el producto creado
    #         print("-----------------------------------")
    #         print(opciones_formset)
    #         print("-----------------------------------")
    #         if opciones_formset.is_valid():
    #             # opciones_formset.is_valid()
    #             opciones_formset.save()
    #             return reverse_lazy('Administrar_vestimenta')
    #         else:
    #             return render(request, self.template_name, {
    #             'message'           : "Verifica los datos",
    #             'form'      : vestimenta_form,
    #             'opciones_formset'  : opciones_formset,
    #         })
    #     else:
    #         return render(request, self.template_name, {
    #             'message'           : "Verifica los datos",
    #             'form'      : vestimenta_form,
    #             'opciones_formset'  : opciones_formset,
    #         })
    
    # def get(self, request, *args, **kwargs):
    #     vestimenta_form = self.form_class(prefix='item') #(VestimentaForm)
    #     opciones_formset = inlineformset_factory(Vestimenta,Opciones_vestimenta,fields=('talle','stock'), extra=5)
    #     return render(request, self.template_name, {
    #         'form' :  vestimenta_form,
    #         'opciones_formset' : opciones_formset,
    #     })
    #----------------------------------------------------------------------------------


    # DE GABY
    # model = Vestimenta
    # # fields = ('nombre','precio','foto','info','subcategoria','sexo')
    # form_class = VestimentaForm
    # template_name = 'administrador/crear_vestimenta.html'
    # success_url = f'{Vestimenta.objects.last().pk}'

    # def get_context_data(self, **kwargs):
    #     data = super(VestimentaCreate, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         data['files'] = VestimentaForm(self.request.POST, self.request.FILES)
    #     else:
    #         data['files'] = VestimentaForm()
    #     return data


    # def get(self, request, *args, **kwargs):
    #     # form = self.form_class()
    #     return reverse_lazy(self.template_name,{'form_class':self.form_class}) #{'form_class':form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     return super().post(request, *args, **kwargs)

    # def get_success_url(self):
    #     return reverse_lazy('Home')

# @method_decorator(staff_member_required, name='dispatch')
# class VestimentaCreateTalle(SingleObjectMixin, FormView):

#     model = Opciones_vestimenta
#     template_name = 'administrador/crear_vestimenta_opciones.html'
#     success_url = reverse_lazy('Administrar_vestimenta')

    # # ivan
    # model = Opciones_vestimenta
    # template_name = 'administrador/crear_vestimenta_opciones.html'
    # success_url = reverse_lazy('Administrar_vestimenta')

    
    # model = Vestimenta
    # template_name = 'administrador/crear_vestimenta_opciones.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Vestimenta.objects.filter(pk=self.kwargs['pk']))
    #     return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Vestimenta.objects.filter(pk=self.kwargs['pk']))
    #     return super().post(request, *args, **kwargs)

    # def get_form(self, form_class=None):
    #     return VestimentaOpcionesFormset(**self.get_form_kwargs(), instance=self.object)

    # def form_valid(self, form):
    #     form.save()

    #     return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse('crud_tienda:Home')
    


@method_decorator(staff_member_required, name='dispatch')
class VestimentaUpdate(UpdateView):
    model = Vestimenta
    # fields = ('nombre','precio','foto','info','subcategoria','sexo')
    form_class = VestimentaForm
    template_name = 'administrador/editar_vestimenta.html'
    success_url = reverse_lazy('Administrar_vestimenta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        if self.request.method == 'POST':
            context['formset'] = VestimentaOpcionesFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VestimentaOpcionesFormset(instance=self.object)

        return context


    def form_valid(self, form): # para validar y salvar en DB
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic(): # si no guarda todo, no guarda nada
            self.object = form.save() # primero guardo el producto

            if formset.is_valid(): #valido opciones_vestimenta
                formset.instance = self.object
                formset.save() # luego guardo opciones_vestimenta

    
    
    
    # if request.method == 'POST':
    #     form = MyForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()

    # def post(self, request, *args, **kwargs):
    #     vestimenta = self.model.objects.get(id=args)
    #     form = self.form_class(request.POST, request.FILES, instance=vestimenta)
    #     print(form)
    #     return super().post(request, *args, **kwargs)

@method_decorator(staff_member_required, name='dispatch')
class VestimentaDelete(DeleteView):
    model = Vestimenta
    template_name = 'administrador/producto_confirm_delete.html'
    success_url = reverse_lazy('Administrar_vestimenta')

# -------------------------------------------------------------------------------------

class CalzadoLista(ListView):
    model = Calzado
    template_name = "crud_tienda/calzado.html"
    sexo = pasar_a_dict(SEXO)
    talles = pasar_a_dict(Opciones_calzado.TALLES)
    
    def get(self, request, *args, **kwargs):
        dict = request.GET
        print(dict)
        if dict:
            if dict['filtro'] in self.sexo.keys():
                object_list = Calzado.objects.filter(sexo=dict['filtro']).order_by('nombre')
                filtro = self.sexo[dict['filtro']]
            elif dict['filtro'] in self.talles.keys():
                object_list = Calzado.objects.filter(opciones_calzado__talle=str(dict['filtro']))
                filtro = self.talles[dict['filtro']]
            return render(request, self.template_name, {"object_list": object_list, "filtro":filtro, "sexo":self.sexo, "talles": self.talles})
        else:
            object_list = Calzado.objects.all().order_by('nombre')
        return render(request, self.template_name, {"object_list": object_list, "sexo":self.sexo, "talles": self.talles})

class CalzadoDetalle(DetailView):
    model = Calzado
    template_name = 'crud_tienda/detalle.html'


class AdministradorCalzList(ListView):
    model = Calzado
    template_name = "administrador/admin_calz_list.html"
    sexo = pasar_a_dict(SEXO)
    talles = pasar_a_dict(Opciones_calzado.TALLES)

    def get(self, request, *args, **kwargs):
        object_list = Calzado.objects.all().order_by('pk')
        return render(request, self.template_name, {"object_list": object_list, "sexo":self.sexo, "talles": self.talles})



@method_decorator(staff_member_required, name='dispatch')
class CalzadoCreate(CreateView):
    model = Calzado
    # fields = ('nombre','precio','foto','info','sexo')
    form_class = CalzadoForm
    template_name = 'administrador/crear_calzado.html'
    success_url = f'{Calzado.objects.last().pk}'


@method_decorator(staff_member_required, name='dispatch')
class CalzadoCreateTalle(SingleObjectMixin, FormView):

    model = Calzado
    template_name = 'administrador/crear_calzado_opciones.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Calzado.objects.filter(pk=self.kwargs['pk']))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Calzado.objects.filter(pk=self.kwargs['pk']))
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return CalzadoOpcionesFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crud_tienda:Home')
    


@method_decorator(staff_member_required, name='dispatch')
class CalzadoUpdate(UpdateView):
    model = Calzado
    # fields = ('nombre','precio','foto','info','sexo')
    form_class = CalzadoForm
    template_name = 'administrador/editar_calzado.html'
    success_url = reverse_lazy('Administrar_calzado')

@method_decorator(staff_member_required, name='dispatch')
class CalzadoDelete(DeleteView):
    model = Calzado
    template_name = 'administrador/producto_confirm_delete.html'
    success_url = reverse_lazy('Administrar_calzado')


# -------------------------------------------------------------------------------------

class AccesoriosLista(ListView):
    model = Accesorio
    template_name = 'crud_tienda/accesorios.html'
    subcat_dict = pasar_a_dict(Accesorio.SUBCATEGORIA)

    def get(self, request, *args, **kwargs):
        dict = request.GET
        filtro = ""
        print('-----------')
        print(dict)
        print('-----------')
        if dict:
            if dict['filtro'] in self.subcat_dict.keys():
                object_list = Accesorio.objects.filter(subcategoria=str(dict['filtro']))
                filtro = self.subcat_dict[dict['filtro']]
        else:
            object_list = Accesorio.objects.all().order_by('nombre')
        return render(request, self.template_name, {"object_list": object_list,"filtro":filtro, "subcat_dict":self.subcat_dict})

class AccesoriosDetalle(DetailView):
    model = Accesorio
    template_name = 'crud_tienda/detalle.html'


class AdministradorAcceList(ListView):
    model = Accesorio
    template_name = "administrador/admin_acce_list.html"
    subcat_dict = pasar_a_dict(Accesorio.SUBCATEGORIA)

    def get(self, request, *args, **kwargs):
        object_list = Accesorio.objects.all().order_by('pk')
        return render(request, self.template_name, {"object_list": object_list, "subcat_dict":self.subcat_dict})


@method_decorator(staff_member_required, name='dispatch')
class AccesorioCreate(CreateView):
    model = Accesorio
    # fields = ('nombre','precio','foto','info','subcategoria','stock')
    form_class = AccesorioForm
    template_name = 'administrador/crear_accesorio.html'
    success_url = reverse_lazy('Administrar_accesorios')

@method_decorator(staff_member_required, name='dispatch')
class AccesorioUpdate(UpdateView):
    model = Accesorio
    # fields = ('nombre','precio','foto','info','subcategoria','stock')
    form_class = AccesorioForm
    template_name = 'administrador/editar_accesorio.html'
    success_url = reverse_lazy('Administrar_accesorios')

@method_decorator(staff_member_required, name='dispatch')
class AccesorioDelete(DeleteView):
    model = Accesorio
    template_name = 'administrador/producto_confirm_delete.html'
    success_url = reverse_lazy('Administrar_accesorios')

# -------------------------------------------------------------------------------------

class SuplementosLista(ListView):
    model = Suplemento
    template_name = 'crud_tienda/suplementos.html'
    subcat_dict = pasar_a_dict(Suplemento.SUBCATEGORIA)

    def get(self, request, *args, **kwargs):
        dict = request.GET
        filtro = ""
        print('-----------')
        print(dict)
        print('-----------')
        if dict:
            if dict['filtro'] in self.subcat_dict.keys():
                object_list = Suplemento.objects.filter(subcategoria=str(dict['filtro']))
                filtro = self.subcat_dict[dict['filtro']]
        else:
            object_list = Suplemento.objects.all().order_by('nombre')
        return render(request, self.template_name, {"object_list": object_list,"filtro":filtro, "subcat_dict":self.subcat_dict})

class SuplementosDetalle(DetailView):
    model = Suplemento
    template_name = 'crud_tienda/detalle.html'


class AdministradorSuplList(ListView):
    model = Suplemento
    template_name = "administrador/admin_supl_list.html"
    subcat_dict = pasar_a_dict(Suplemento.SUBCATEGORIA)

    def get(self, request, *args, **kwargs):
        object_list = Suplemento.objects.all().order_by('pk')
        return render(request, self.template_name, {"object_list": object_list, "subcat_dict":self.subcat_dict})


@method_decorator(staff_member_required, name='dispatch')
class SuplementoCreate(CreateView):
    model = Suplemento
    # fields = ('nombre','precio','foto','info','subcategoria','stock')
    form_class = SuplementoForm
    template_name = 'administrador/crear_suplemento.html'
    success_url = reverse_lazy('Administrar_suplementos')

@method_decorator(staff_member_required, name='dispatch')
class SuplementoUpdate(UpdateView):
    model = Suplemento
    # fields = ('nombre','precio','foto','info','subcategoria','stock')
    form_class = SuplementoForm
    template_name = 'administrador/editar_suplemento.html'
    success_url = reverse_lazy('Administrar_suplementos')

@method_decorator(staff_member_required, name='dispatch')
class SuplementoDelete(DeleteView):
    model = Suplemento
    template_name = 'administrador/producto_confirm_delete.html'
    success_url = reverse_lazy('Administrar_suplementos')

# -------------------------------------------------------------------------------------






# Vistas basadas en funciones:

# def calzado(request):
#     talles = (
#     ('34.5'),
#     ('35.5'),
#     ('36'),
#     ('38'),
#     ('39'),
#     ('40'),
#     ('41'),
#     ('41.5'),
#     ('42'),
#     ('43'),
#     ('44'),
#     ('45'),
#     )

#     if request.method == 'POST':
#         talle = request.POST['talle']
#     else:
#         dict = request.GET
#         print("--------------")
#         print(dict)
#         print("--------------")
#         if dict:
#             if dict['filtro'] == 'M' or dict['filtro'] == 'H':
#                 object_list = Calzado.objects.filter(sexo=dict['filtro']).order_by('nombre')
#             elif dict['filtro'] != None:
#                 object_list = Calzado.objects.filter(opciones_calzado__talle=str(dict['filtro']))
#         else:
#             object_list = Calzado.objects.all().order_by('nombre')
#     return render(request, "crud_tienda/calzado.html", {"object_list": object_list,"talles":talles})



# def vestimenta(request):
#     if request.method == 'POST':
#         categoria = request.POST['categoria']
#         talle = request.POST['talle']
#     else:
#         productos = Vestimenta.objects.all().order_by('nombre')
#     return render(request, "crud_tienda/vestimenta.html", {"productos": productos})


# def accesorios(request):
#     if request.method == 'POST':
#         categoria = request.POST['categoria']
#     else:
#         productos = Accesorio.objects.all().order_by('nombre')
#     return render(request, "crud_tienda/accesorios.html", {"productos": productos})


# def suplementos(request):
#     if request.method == 'POST':
#         categoria = request.POST['categoria']
#     else:
#         categoria = "Sumplementos"
#         productos = Suplemento.objects.all().order_by('nombre')
#     return render(request, "crud_tienda/suplementos.html", {"productos": productos, "categoria": categoria})


def contacto(request):
    """formulario de contacto"""
    contact = FormContacto()
    if request.method == 'POST':
        contact = FormContacto(request.POST)
        nombre = request.POST['nombre']
        mail = request.POST['mail']
        mensaje = request.POST['mensaje']
        if contact.is_valid():
            # enviamos el email
            email = EmailMessage(
                "Tienda: Nuevo mensaje",                            # Asunto
                f"De {nombre} <{mail}>\n\nEscribió:\n\n{mensaje}",  # Cuerpo
                EMAIL_HOST_USER,                                    # Email de origen
                # Email donde llega la respuesta
                ['ivandariomunioz@gmail.com'],
                # responder a...
                reply_to=[mail]
            )
            print(email)
            try:
                email.send()
                return redirect('Home')
            except:
                # aca habría que crear una excepcion o mensaje de error propio y que continúe
                raise ValueError("Ocurrió un error...")
    else:
        return render(request, "crud_tienda/contacto.html", {"contact": contact})
