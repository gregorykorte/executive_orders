from django.shortcuts import get_object_or_404 #render
#from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count
from models import Order, President, OrderType

# Create your views here.

class OrderListView(ListView):
    
    model = Order

    queryset = Order.objects.order_by('-sign_date')
    context_object_name = 'order_list'

class OrderDetailView(DetailView):

    model = Order
    queryset = Order.objects.all()
    context_object_name = 'order_detail'

class OrderPresidentView(ListView):

    def get_queryset(self):
        self.president = get_object_or_404(President, potus_slug=self.args[0])
        President.objects.annotate(Count('order__order_type'))
        return Order.objects.filter(president=self.president)

class OrderTypeView(ListView):

    template_name = 'whitehouse/order_list_by_type.html'

    def get_queryset(self):
        self.order_type = get_object_or_404(OrderType, short_type=self.args[0])
        return Order.objects.filter(order_type=self.order_type)
        context_object_name = 'order_list_by_type'

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

# end views
