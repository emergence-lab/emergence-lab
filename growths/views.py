from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView
import time
import growths.models
from growths.models import growth, sample, readings
import afm.models
from .filters import growth_filter, RelationalFilterView
import re
from growths.forms import growth_form, sample_form, p_form, split_form, readings_form
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

    else:
        model = growths.models.sample
        print("split sample page accessed")
        sform = split_form(prefix='sform')
    return render(request, 'growths/split_sample.html', {'sform': sform})


class update_readings(SingleObjectMixin, TemplateView):
    context_object_name = 'growth'
    queryset = growth.objects.all()
    slug_field = 'growth_number'
    template_name = 'growths/update_readings.html'

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(update_readings, self).get_context_data(**kwargs)
        context["growth"] = self.get_object()
        allreadings = readings.objects.filter(growth=self.get_object())
        context["readings"] = allreadings
        formlist = []
        numberofreadings = 0
        for reading in allreadings:
            numberofreadings = numberofreadings + 1
            rform = readings_form(instance=readings(), prefix=('reading' + str(numberofreadings)),
                                  initial={'growth': reading.growth,
                'layer': reading.layer, 'layer_desc': reading.layer_desc,
                'pyro_out': reading.pyro_out, 'pyro_in': reading.pyro_in, 'tc_out': reading.tc_out,
                'tc_in': reading.tc_in, 'motor_rpm': reading.motor_rpm, 'gc_pressure': reading.gc_pressure,
                'gc_position': reading.gc_position, 'voltage_in': reading.voltage_in,
                'voltage_out': reading.voltage_out, 'current_in': reading.current_in,
                'current_out': reading.current_out, 'top_vp_flow': reading.top_vp_flow,
                'hydride_inner': reading.hydride_inner, 'hydride_outer': reading.hydride_outer,
                'alkyl_flow_inner': reading.alkyl_flow_inner, 'alkyl_push_inner': reading.alkyl_push_inner,
                'alkyl_flow_middle': reading.alkyl_flow_middle, 'alkyl_push_middle': reading.alkyl_push_middle,
                'alkyl_flow_outer': reading.alkyl_flow_outer, 'alkyl_push_outer': reading.alkyl_push_outer,
                'n2_flow': reading.n2_flow, 'h2_flow': reading.h2_flow, 'nh3_flow': reading.nh3_flow,
                'hydride_pressure': reading.hydride_pressure, 'tmga1_flow': reading.tmga1_flow,
                'tmga1_pressure': reading.tmga1_pressure, 'tmga2_flow': reading.tmga2_flow,
                'tmga2_pressure': reading.tmga2_pressure, 'tega2_flow': reading.tega2_flow,
                'tega2_pressure': reading.tega2_pressure, 'tmin1_flow': reading.tmin1_flow,
                'tmin1_pressure': reading.tmin1_pressure, 'tmal1_flow': reading.tmal1_flow,
                'tmal1_pressure': reading.tmal1_pressure, 'cp2mg_flow': reading.cp2mg_flow,
                'cp2mg_pressure': reading.cp2mg_pressure, 'cp2mg_dilution': reading.cp2mg_dilution,
                'silane_flow': reading.silane_flow, 'silane_dilution': reading.silane_dilution,
                'silane_mix': reading.silane_mix, 'silane_pressure': reading.silane_pressure})
            formlist.append(rform)
        context["readingslist"] = formlist
        return context
    def post(self, request, **kwargs):
        print ("IS THIS POST TEST WORKING? YES. YES IT IS.")
        numberofreadings = len(readings.objects.filter(growth=self.get_object()))
        print (numberofreadings)
        for x in range(0, numberofreadings):
            print("inside for loop")
            print(x)
            rform = readings_form(request.POST, prefix=('reading' + str(x+1)))
            if rform.is_valid():
                print ("rform is valid")
                newgrowth = rform.cleaned_data['growth']
                newlayer = rform.cleaned_data['layer']
                newlayer_desc = rform.cleaned_data['layer_desc']
                newpyro_out = rform.cleaned_data['pyro_out']
                newpyro_in = rform.cleaned_data['pyro_in']
                newtc_out = rform.cleaned_data['tc_out']
                newtc_in = rform.cleaned_data['tc_in']
                newmotor_rpm = rform.cleaned_data['motor_rpm']
                newgc_pressure = rform.cleaned_data['gc_pressure']
                newgc_position = rform.cleaned_data['gc_position']
                newvoltage_in = rform.cleaned_data['voltage_in']
                newvoltage_out = rform.cleaned_data['voltage_out']
                newcurrent_in = rform.cleaned_data['current_in']
                newcurrent_out = rform.cleaned_data['current_out']
                newtop_vp_flow = rform.cleaned_data['top_vp_flow']
                newhydride_inner = rform.cleaned_data['hydride_inner']
                newhydride_outer = rform.cleaned_data['hydride_outer']
                newalkyl_flow_inner = rform.cleaned_data['alkyl_flow_inner']
                newalkyl_push_inner = rform.cleaned_data['alkyl_push_inner']
                newalkyl_flow_middle = rform.cleaned_data['alkyl_flow_middle']
                newalkyl_push_middle = rform.cleaned_data['alkyl_push_middle']
                newalkyl_flow_outer = rform.cleaned_data['alkyl_flow_outer']
                newalkyl_push_outer = rform.cleaned_data['alkyl_push_outer']
                newn2_flow = rform.cleaned_data['n2_flow']
                newh2_flow = rform.cleaned_data['h2_flow']
                newnh3_flow = rform.cleaned_data['nh3_flow']
                newhydride_pressure = rform.cleaned_data['hydride_pressure']
                newtmga1_flow = rform.cleaned_data['tmga1_flow']
                newtmga1_pressure = rform.cleaned_data['tmga1_pressure']
                newtmga2_flow = rform.cleaned_data['tmga2_flow']
                newtmga2_pressure = rform.cleaned_data['tmga2_pressure']
                newtega2_flow = rform.cleaned_data['tega2_flow']
                newtega2_pressure = rform.cleaned_data['tega2_pressure']
                newtmin1_flow = rform.cleaned_data['tmin1_flow']
                newtmin1_pressure = rform.cleaned_data['tmin1_pressure']
                newtmal1_flow = rform.cleaned_data['tmal1_flow']
                newtmal1_pressure = rform.cleaned_data['tmal1_pressure']
                newcp2mg_flow = rform.cleaned_data['cp2mg_flow']
                newcp2mg_pressure = rform.cleaned_data['cp2mg_pressure']
                newcp2mg_dilution = rform.cleaned_data['cp2mg_dilution']
                newsilane_flow = rform.cleaned_data['silane_flow']
                newsilane_dilution = rform.cleaned_data['silane_dilution']
                newsilane_mix = rform.cleaned_data['silane_mix']
                newsilane_pressure = rform.cleaned_data['silane_pressure']
                print("LAYER DESCRIPTION:")
                print (newlayer_desc)
                thisreading = readings.objects.filter(growth=newgrowth, layer=newlayer)
                thisreading.update(growth=newgrowth, layer = newlayer, layer_desc=newlayer_desc,
                                   pyro_out=newpyro_out, pyro_in=newpyro_in, tc_out=newtc_out,
                                   tc_in=newtc_in, motor_rpm=newmotor_rpm, gc_pressure=newgc_pressure,
                                   gc_position=newgc_position, voltage_in=newvoltage_in, voltage_out=newvoltage_out,
                                   current_in=newcurrent_in, current_out=newcurrent_out, top_vp_flow=newtop_vp_flow,
                                   hydride_inner=newhydride_inner, hydride_outer=newhydride_outer,
                                   alkyl_flow_inner=newalkyl_flow_inner, alkyl_push_inner=newalkyl_push_inner,
                                   alkyl_flow_middle=newalkyl_flow_middle, alkyl_push_middle=newalkyl_push_middle,
                                   alkyl_flow_outer=newalkyl_flow_outer, alkyl_push_outer=newalkyl_push_outer,
                                   n2_flow=newn2_flow, h2_flow=newh2_flow, nh3_flow=newnh3_flow, hydride_pressure=newhydride_pressure,
                                   tmga1_flow=newtmga1_flow, tmga1_pressure=newtmga1_pressure, tmga2_flow=newtmga2_flow,
                                   tmga2_pressure=newtmga2_pressure, tega2_flow=newtega2_flow, tega2_pressure=newtega2_pressure,
                                   tmin1_flow=newtmin1_flow, tmin1_pressure=newtmin1_pressure, tmal1_flow=newtmal1_flow,
                                   tmal1_pressure=newtmal1_pressure, cp2mg_flow=newcp2mg_flow, cp2mg_pressure=newcp2mg_pressure,
                                   cp2mg_dilution=newcp2mg_dilution, silane_flow=newsilane_flow, silane_dilution=newsilane_dilution,
                                   silane_mix=newsilane_mix, silane_pressure=newsilane_pressure)
        return HttpResponseRedirect(reverse('update_readings', args=[self.get_object()]))











#     def post(request):
#         print ("POST")
#     def get(request, self, *args, **kwargs):
#         print ("GET")
#         model = growths.models.readings
#         rform = readings_form(prefix='rform')
#         return render(request, 'growths/update_readings.html', {'rform': rform})
# , initial={'growth_number': self.get_object()}




# class update_readings(UpdateView):
#     model = growths.models.readings
#     template_name = 'growths/update_readings.html'
#     form_class = readings_form
#
#     def get_context_data(self, **kwargs):
#         context = super(sample_detail, self).get_context_data(**kwargs)
#         readingobjects = readings.objects.all()
#         lastreading = readingobjects[len(readingobjects)]
#         lastreadings = readings.objects.filter(growth=lastreading.growth)
#         context["readings"] = lastreadings