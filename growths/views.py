from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
import time
import growths.models
from growths.models import growth, sample
import afm.models
from .filters import growth_filter, RelationalFilterView
import re
from growths.forms import growth_form, sample_form, p_form, split_form
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import random


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
    context_object_name = 'growthobject'

    def get_context_data(self, **kwargs):
        context = super(growth_detail, self).get_context_data(**kwargs)
        context["samples"] = sample.objects.filter(growth=self.get_object())
        return context


class sample_detail(DetailView):
    model = growths.models.sample
    template_name = 'growths/sample_detail.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        context = super(sample_detail, self).get_context_data(**kwargs)
        context["sample"] = self.get_object()
        parentlist = []
        nextobject = self.get_object()
        loopcounter = 0
        while nextobject.parent != nextobject:
            print (nextobject.parent)
            print (nextobject)
            parentlist.append(nextobject.parent)
            nextobject = nextobject.parent
            loopcounter = loopcounter + 1
            if loopcounter > 5:
                raise Exception("Whoa there pal. Hold your horses.")
        context["parents"] = parentlist
        siblings = sample.objects.filter(growth=(self.get_object()).growth)
        siblinglist = []
        for sibling in siblings:
            if sibling != self.get_object():
                siblinglist.append(sibling)
        context["siblings"] = siblinglist
        children = sample.objects.filter(parent=self.get_object())
        childlist = []
        for child in children:
            if child.parent != child:
                childlist.append(child)
        context["children"] = childlist
        return context


# class new_growth(View):
#     def post(self, request, *args, **kwargs):
#         gform = growth_form(request.POST)
#         sform = sample_form(request.POST)
#         if gform.is_valid() and sform.is_valid():
#             new_g = gform.save()
#             new_s = sform.save()
#             return HttpResponseRedirect('home')
#     def get(self, request, *args, **kwargs):
#         gform = growth_form()
#         sform = sample_form()
# #         context = super(new_growth, self).get_context_data(**kwargs)
#         if 'gform' not in context:
#             context['gform'] = self.gform() # request=self.request)
#         if 'sform' not in context:
#             context['sform'] = self.sform() # request=self.request)
#         return context
#
#     return render_to_response('growths/new_growth.html', {'growth_form': gform, 'sample_form': sform})

def create_growth(request):
    if request.method == "POST":
        gform = growth_form(request.POST, instance=growth())
        # sforms = [sample_form(request.POST, prefix=str(x), instnace=sample()) for x in range(0,6)]
        pf_1 = p_form(request.POST, prefix="pf_1")
        pf_2 = p_form(request.POST, prefix="pf_2")
        pf_3 = p_form(request.POST, prefix="pf_3")
        pf_4 = p_form(request.POST, prefix="pf_4")
        pf_5 = p_form(request.POST, prefix="pf_5")
        pf_6 = p_form(request.POST, prefix="pf_6")
        sform_1 = sample_form(request.POST, instance=sample(), prefix="sform_1")
        sform_2 = sample_form(request.POST, instance=sample(), prefix="sform_2")
        sform_3 = sample_form(request.POST, instance=sample(), prefix="sform_3")
        sform_4 = sample_form(request.POST, instance=sample(), prefix="sform_4")
        sform_5 = sample_form(request.POST, instance=sample(), prefix="sform_5")
        sform_6 = sample_form(request.POST, instance=sample(), prefix="sform_6")
        sforms_list = []
        sforms = [sform_1, sform_2, sform_3, sform_4, sform_5, sform_6]
        pforms = [pf_1, pf_2, pf_3, pf_4, pf_5, pf_6]
        for x in range(0, 6):
            if (pforms[x]).has_changed():
                print("The form has changed!!")
                sforms_list.append(sforms[x])
        if gform.is_valid() and all([sf.is_valid() for sf in sforms_list]):
            print ("validation success")
            new_g = gform.save()
            pocket = 0
            for sf in sforms_list:
                pocket = pocket + 1
                new_s = sf.save(growthid=new_g, pocketnum=pocket)
                new_s.save()
#                 new_s = sf.save(commit=False)
#                 new_s.growth = new_g
#                 new_s.save()
            # return HttpResponseRedirect(reverse('home'))
            return HttpResponseRedirect(reverse('growth_detail', args=[new_g.growth_number]))
    else:
        num_items = 0
        model = growths.models.growth
        query = model.objects.all()
        last = str(query[len(query) - 1])
        last_int = ''
        for i in xrange(1, 5):
            last_int += last[i]
        last_int = (int(last_int) + 1)
        last = ('g' + str(last_int))
        currenttime = time.strftime("%Y-%m-%d")
        gform = growth_form(instance=growth(), initial={'growth_number': last, 'date': currenttime})

        # sform = [sample_form(prefix=str(x), instance=sample()) for x in range(0,6)]
        def generate_serial():
            return ('wbg_' + str(random.randint(100, 999)))
        pf_1 = p_form(prefix="pf_1")
        pf_2 = p_form(prefix="pf_2")
        pf_3 = p_form(prefix="pf_3")
        pf_4 = p_form(prefix="pf_4")
        pf_5 = p_form(prefix="pf_5")
        pf_6 = p_form(prefix="pf_6")
        sform_1 = sample_form(instance=sample(), prefix="sform_1", initial={'substrate_serial': generate_serial})
        sform_2 = sample_form(instance=sample(), prefix="sform_2", initial={'substrate_serial': generate_serial})
        sform_3 = sample_form(instance=sample(), prefix="sform_3", initial={'substrate_serial': generate_serial})
        sform_4 = sample_form(instance=sample(), prefix="sform_4", initial={'substrate_serial': generate_serial})
        sform_5 = sample_form(instance=sample(), prefix="sform_5", initial={'substrate_serial': generate_serial})
        sform_6 = sample_form(instance=sample(), prefix="sform_6", initial={'substrate_serial': generate_serial})

    return render(request, 'growths/create_growth.html',
                  {'gform': gform, 'sform_1': sform_1, 'sform_2': sform_2, 'sform_3': sform_3,
                   'sform_4': sform_4, 'sform_5': sform_5, 'sform_6': sform_6, 'pf_1': pf_1,
                   'pf_2': pf_2, 'pf_3': pf_3, 'pf_4': pf_4, 'pf_5': pf_5, 'pf_6': pf_6, })


def split_sample(request):
    if request.method == "POST":
        print ("entering POST stage.")
        sform = split_form(request.POST, prefix='sform')
        if sform.is_valid():
            numberofpieces = sform.cleaned_data['pieces']
            sampletosplit = sform.cleaned_data['parent']
            print (sampletosplit)
            serialnumber = sampletosplit.substrate_serial
            print ("serial number: " + serialnumber)
            allsamples = sample.objects.filter(substrate_serial=serialnumber)
            dictionarylist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                              'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            numberofsamples = len(allsamples)
            # raise Exception("I don't know what you did, but you sure screwed something up.")
            if numberofsamples == 1:
                print ("This is the first sample to split")
                sample.objects.filter(substrate_serial=serialnumber).update(piece=dictionarylist[numberofsamples - 1])
            else:
                print ('There are ' + str(numberofsamples) + ' samples that already exist')
            for i in range(0, numberofpieces - 1):
                newsplit = sample(growth=sampletosplit.growth, pocket=sampletosplit.pocket,
                                  parent=sampletosplit.parent, size=sampletosplit.size,
                                  location=sampletosplit.location,
                                  substrate_type=sampletosplit.substrate_type,
                                  substrate_serial=sampletosplit.substrate_serial,
                                  substrate_orientation=sampletosplit.substrate_orientation,
                                  substrate_miscut=sampletosplit.substrate_miscut,
                                  substrate_comment=sampletosplit.substrate_comment)
                newsplit.piece = dictionarylist[i + numberofsamples]
                print (newsplit)
                print (newsplit.piece)
                newsplit.save()
                if sampletosplit.parent == sampletosplit:
                    newsplit.parent = newsplit
                    newsplit.save()

            return HttpResponseRedirect(reverse('growth_detail', args=[sampletosplit.growth]))

#             tempparent = sampletosplit
#             firstparent = sampletosplit.parent
#             numberofparents = 0
#             print ('beginning')
#             print (numberofpieces)
#             print (tempparent)
#             print (firstparent)
#             if tempparent.id == firstparent.id:
#                 print ('No Parent!')
#             else:
#                 print ("try something else. this loop isn't working")
#                 while firstparent.id is not tempparent.id:
#                     print ('in loop')
#                     numberofparents = numberofparents + 1
#                     firstparent = firstparent.parent
#                     print (numberofparents)
#                     print (firstparent)
#                     if numberofparents >= 10:
#                         break
#             print (numberofparents)
#             print (tempparent)
#             print (firstparent)

            # find all siblings so the amount of pieces can be determined
            # return HttpResponseRedirect(reverse(''))

    else:
        model = growths.models.sample
        print("split sample page accessed")
        sform = split_form(prefix='sform')
    return render(request, 'growths/split_sample.html', {'sform': sform})
# class create_growth(CreateView):
#     model = growths.models.growth
#     template_name = 'growths/create_growth.html'
#     growth_class = growth_form
#     sample_class = sample_form
#     form_class = growth_form
#
#     def get_context_data(self, **kwargs):
#         context = super(create_growth, self).get_context_data(**kwargs)
# #         if 'growth_form' not in context:
# #             context['growth_form'] = self.growth_class(initial={'some_field': context['model'].some_field})
# #         if 'sample_form' not in context:
# #             context['sample_form'] = self.sample_class(initial={'another_field': context['model'].another_field})
# #         return context
#
#         if 'g_form' not in context:
#             context['g_form'] = self.growth_class() # request=self.request)
#         if 's_form' not in context:
#             context['s_form'] = self.sample_class() # request=self.request)
#         return context
#
#     def get_initial(self):
#         num_items = 0
#         model = growths.models.growth
#         query = model.objects.all()
#         last = str(query[len(query)-1])
#         last_int = ''
#         for i in xrange (1,5):
#             last_int += last[i]
#         last_int = (int(last_int) + 1)
#         last = ('g' + str(last_int))
#
#         return { 'growth_number': last,
#                  'date': time.strftime("%Y-%m-%d") }
#
#     def post(self, request, *args, **kwargs):
#         # get the user instance
#         self.growth_object = None
#         self.sample_object = None
#         self.object = None
#         # determine which form is being submitted
#         # uses the name of the form's submit button
#         if 's_form' in request.POST:
#             # get the primary form
# #uncomment
# #             sample_class = self.sample_class
# #             sample_form_name = 's_form'
#             form_class = self.sample_class
#             form = self.get_form(form_class)
#             form_name = 's_form'
#         if 'g_form' in request.POST:
#             # get the secondary form
# #uncomment
# #             growth_class = self.growth_class
# #             growth_form_name = 'g_form'
#             form_class = self.growth_class
#             form = self.get_form(form_class)
#             form_name = 'g_form'
#          # get the form
# #uncomment
# #         growth_form = self.get_form(growth_class)
# #         sample_form = self.get_form(sample_class)
#
# # uncomment        #form = [growth_form, sample_form]
# #uncomment
# #         if sample_form.is_valid():
# #             if growth_form.is_valid():
# #                 return self.form_valid(form)
# #             else:
# #                 return self.form_invalid(**{form_name: growth_form})
# #         else:
# #             return self.form_invalid(**{form_name: sample_form})
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
# # uncomment
# #     def form_valid(self, form):
# #         self.growth_object = form[0].save()
# #         self.sample_object = form[1].save()
# #         return HttpResponseRedirect(self.get_success_url())
#
# #uncomment
#     def get_success_url(self):
#         return ''
