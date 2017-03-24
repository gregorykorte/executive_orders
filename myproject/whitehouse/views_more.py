class OrderPresidentView(ListView):

    #model = Order

    #president = Order.president

    template_name = 'whitehouse/order_list.html'

    def get_queryset(self):
        self.president = Order.objects.filter(President, last_name=self.args[0])
        return Order.objects.filter(president=self.president)

    #queryset = Order.objects.filter(potus_slug)


    return Order.objects.filter(president=self.president)



    #queryset = Order.objects.filter(last_name)

    def get_queryset(self):
        self.president = get_object_or_404(President, potus_slug=self)
        return Order.objects.filter(president=self)

    #def get_queryset(self):
    #    self.president = get_object_or_404(Order)
    #    return Order.objects.filter(president=self.president)


class OrderFilterView(ListView):

    model = Order

    template_name = 'whitehouse/order_list.html'

    def get_queryset(self):
        self.order_type = get_object_or_404(Order, name=self.order_type)
        return Order.objects.filter(ordertype=self.order_type)    

    def get_context_data(self):
        context = super(OrderListView, self).get_context_data()
        context['now'] = timezone.now()
        return context
    
