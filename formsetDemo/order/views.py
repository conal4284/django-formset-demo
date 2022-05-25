from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from order.models import Order, OrderParticulars
from order.forms import OrderForm, OrderParticularsFormset
from django.utils import timezone


# Create your views here.
class OrderCreate(CreateView):
    model = Order
    template_name = 'order/order_form.html'
    form_class = OrderForm
    success_url = '/order/list/'
    object = None

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        particulars_form = OrderParticularsFormset()
        return self.render_to_response(self.get_context_data(form=form, particulars_form=particulars_form,))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        particulars_form = OrderParticularsFormset(self.request.POST, instance=form.instance)
        if form.is_valid() and particulars_form.is_valid():
            return self.form_valid(form, particulars_form)
        else:
            print(form.errors)
            return self.form_invalid(form, particulars_form)
    
    def form_valid(self, form, particulars_form):
        """
        Called if all forms are valid. Creates Order instance along with the
        associated OrderParticulars instances then redirects to success url
        Args:
            form: Order Form
            particulars_form: Order Particulars Form

        Returns: an HttpResponse to success url

        """
        self.object = form.save(commit=False)
        # pre-processing for Order instance here...
        self.object.created_by = str(self.request.user)
        self.object.created_at = timezone.now()
        self.object.save()

        # saving OrderParticulars Instances
        particulars = particulars_form.save(commit=False)
        for p in particulars:
            #  change the OrderParticulars instance values here
            #  p.some_field = some_value
            p.created_by = str(self.request.user)
            p.created_at = timezone.now()
            p.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, particulars_form):
        return self.render_to_response(self.get_context_data(form=form, particulars_form=particulars_form))

class OrderUpdate(UpdateView):
    model = Order
    template_name = 'order/order_form.html'
    form_class = OrderForm
    success_url = '/order/list/'
    
    def get_object(self, queryset=None):
        self.object = super(OrderUpdate, self).get_object()
        return self.object

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        particulars_form = OrderParticularsFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=OrderForm(instance=self.object), particulars_form=particulars_form,))
    
    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_object()
        form = OrderForm(data=self.request.POST, files=self.request.FILES, instance=self.object)
        particulars_form = OrderParticularsFormset(data=self.request.POST, instance=self.object)
        if form.is_valid() and particulars_form.is_valid():
            return self.form_valid(form, particulars_form)
        else:
            print(form.errors)
            return self.form_invalid(form, particulars_form)
    
    def form_valid(self, form, particulars_form):
        """
        Called if all forms are valid. Creates Order instance along with the
        associated OrderParticulars instances then redirects to success url
        Args:
            form: Order Form
            particulars_form: Order Particulars Form

        Returns: an HttpResponse to success url

        """
        self.object = form.save()
        # pre-processing for Order instance here...
        self.object.updated_by = str(self.request.user)
        self.object.updated_at = timezone.now()
        self.object.save()

        # saving OrderParticulars Instances
        particulars = particulars_form.save(commit=False)
        for p in particulars:
            #  change the OrderParticulars instance values here
            #  p.some_field = some_value
            p.particulars = self.object
            p.updated_by = str(self.request.user)
            p.updated_at = timezone.now()
            p.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, particulars_form):
        return self.render_to_response(self.get_context_data(form=form, particulars_form=particulars_form))

    
class OrderList(ListView):
    model = Order