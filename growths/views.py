from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
import time
import growths.models
import afm.models
from .filters import growth_filter, RelationalFilterView
import re
from growths.forms import growth_form, sample_form
from django.http import HttpResponseRedirect


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
    growth_class = growth_form
    sample_class = sample_form
    form_class = growth_form

    def get_context_data(self, **kwargs):
        context = super(create_growth, self).get_context_data(**kwargs)
#         if 'growth_form' not in context:
#             context['growth_form'] = self.growth_class(initial={'some_field': context['model'].some_field})
#         if 'sample_form' not in context:
#             context['sample_form'] = self.sample_class(initial={'another_field': context['model'].another_field})
#         return context

        if 'g_form' not in context:
            context['g_form'] = self.growth_class() # request=self.request)
        if 's_form' not in context:
            context['s_form'] = self.sample_class() # request=self.request)
        return context

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

    def post(self, request, *args, **kwargs):
        # get the user instance
        self.growth_object = None
        self.sample_object = None
        self.object = None
        # determine which form is being submitted
        # uses the name of the form's submit button
        if 's_form' in request.POST:
            # get the primary form
#uncomment
#             sample_class = self.sample_class
#             sample_form_name = 's_form'
            form_class = self.sample_class
            form = self.get_form(form_class)
            form_name = 's_form'
        if 'g_form' in request.POST:
            # get the secondary form
#uncomment
#             growth_class = self.growth_class
#             growth_form_name = 'g_form'
            form_class = self.growth_class
            form = self.get_form(form_class)
            form_name = 'g_form'
         # get the form
#uncomment
#         growth_form = self.get_form(growth_class)
#         sample_form = self.get_form(sample_class)

# uncomment        #form = [growth_form, sample_form]
#uncomment
#         if sample_form.is_valid():
#             if growth_form.is_valid():
#                 return self.form_valid(form)
#             else:
#                 return self.form_invalid(**{form_name: growth_form})
#         else:
#             return self.form_invalid(**{form_name: sample_form})
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# uncomment
#     def form_valid(self, form):
#         self.growth_object = form[0].save()
#         self.sample_object = form[1].save()
#         return HttpResponseRedirect(self.get_success_url())

#uncomment
    def get_success_url(self):
        return ''
