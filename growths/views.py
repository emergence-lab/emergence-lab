from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
import time
import growths.models
import afm.models
from .filters import growth_filter, RelationalFilterView
import re


class growth_list(RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'growths/growth_filter.html'


class afm_compare(ListView):
    template_name = 'growths/afm_compare.html'

    def get_queryset(self):
        id_list = [int(id) for id in self.request.GET.getlist('afm')]
        objects = afm.models.afm.objects.filter(id__in=id_list)
        return objects


class growth_detail(DetailView):
    model = growths.models.growth
    template_name = 'growths/growth_detail.html'
    slug_field = 'growth_number'


class create_growth(CreateView):
    model = growths.models.growth
    template_name = 'growths/create_growth.html'
#     form_class = Form1
#     second_form_class = Form2
#
#     def get_context_data(self, **kwargs):
#         context = super(create_growth, self).get_context_data(**kwargs)
#         if 'form' not in context:
#             context['form'] = self.form_class(initial={'some_field': context['model'].some_field})
#         if 'form2' not in context:
#             context['form2'] = self.second_form_class(initial={'another_field': context['model'].another_field})
#         return context

    def get_initial(self):
        num_items = 0
        model = growths.models.growth
        query = model.objects.all()
        last = str(query[len(query)-1])
        last_int = ''
        for i in xrange (1,5):
            last_int += last[i]
        last_int = (int(last_int) + 1)
        last = ('g' + str(last_int))

        return { 'growth_number': last,
                 'date': time.strftime("%Y-%m-%d") }

#     def post(self, request, *args, **kwargs):
#         # get the user instance
#         self.object = self.get_object()
#         # determine which form is being submitted
#         # uses the name of the form's submit button
#         if 'form' in request.POST:
#             # get the primary form
#             form_class = self.get_form_class()
#             form_name = 'form'
#         else:
#             # get the secondary form
#             form_class = self.second_form_class
#             form_name = 'form2'
#          # get the form
#         form = self.get_form(form_class)
#          # validate
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(**{form_name: form})


    def get_success_url(self):
        return reverse('home')
