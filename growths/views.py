import time

from django.shortcuts import render, render_to_response
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import growth, sample, readings, serial_number, recipe_layer, source
from .filters import growth_filter, RelationalFilterView
from .forms import growth_form, sample_form, p_form, split_form, readings_form, comments_form
from .forms import prerun_checklist_form, start_growth_form, prerun_growth_form, prerun_sources_form, postrun_checklist_form
import afm.models
import hall.models
from core.views import SessionHistoryMixin


class growth_list(SessionHistoryMixin, RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'growths/growth_filter.html'


class afm_compare(ListView):
    template_name = 'growths/afm_compare.html'

    def get_queryset(self):
        id_list = [int(id) for id in self.request.GET.getlist('afm')]
        objects = afm.models.afm.objects.filter(id__in=id_list)
        return objects


class GrowthDetailView(SessionHistoryMixin, DetailView):
    model = growth
    template_name = 'growths/growth_detail.html'
    slug_field = 'growth_number'
    context_object_name = 'growth'

    def get_context_data(self, **kwargs):
        context = super(GrowthDetailView, self).get_context_data(**kwargs)
        context['samples'] = sample.objects.filter(growth=context['object']).order_by('pocket')
        context['char_afm'] = afm.models.afm.objects.filter(growth=context['object']).order_by('sample__pocket', 'sample__piece', 'location', 'scan_number')
        context['char_hall'] = hall.models.hall.objects.filter(growth=context['object']).order_by('sample__pocket', 'sample__piece', 'date')
        return context


class SampleDetailView(SessionHistoryMixin, DetailView):
    model = sample
    template_name = 'growths/sample_detail.html'
    context_object_name = 'sample'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)

        parents = []
        obj = context['sample']
        while obj.parent != obj:
            parents.append(obj.parent)
            obj = obj.parent
        obj = context['sample']

        context['parents'] = parents[::-1]  # show in reverse order
        context['siblings'] = sample.objects.filter(growth=obj.growth).exclude(pk=obj.id).order_by('-growth__growth_number', 'pocket', 'piece')
        context['children'] = sample.objects.filter(parent=obj).exclude(pk=obj.id).order_by('-growth__growth_number', 'pocket', 'piece')

        context['char_afm'] = afm.models.afm.objects.filter(sample=context['object']).order_by('sample__pocket', 'sample__piece', 'location', 'scan_number')
        context['char_hall'] = hall.models.hall.objects.filter(sample=context['object']).order_by('sample__pocket', 'sample__piece', 'date')

        return context


class SampleFamilyDetailView(ListView):
    model = sample
    template_name = 'growths/sample_family_detail.html'
    context_object_name = 'samples'

    def get_context_data(self, **kwargs):
        growth_number = self.kwargs.get('growth', None)
        pocket = self.kwargs.get('pocket', None)
        context = super(SampleFamilyDetailView, self).get_context_data(**kwargs)
        context['samples'] = sample.objects.filter(growth__growth_number=growth_number)
        context['growth'] = growth.get_growth(growth_number)
        context['pocket'] = pocket
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
                print ("Here goes nothing")
                if new_s.substrate_serial.startswith('wbg_'):
                    print ("Success! It does start with 'wbg_'")
                    entireserial = new_s.substrate_serial
                    newserialnumber = ''
                    for x in range(4, len(entireserial)):
                        newserialnumber = newserialnumber + entireserial[x]
                    newserialnumber = int(newserialnumber)
                    sn = serial_number.objects.create(serial_number = newserialnumber)
                    sn.save
#                 new_s = sf.save(commit=False)
#                 new_s.growth = new_g
#                 new_s.save()
            # return HttpResponseRedirect(reverse('home'))
            return HttpResponseRedirect(reverse('growth_detail', args=[new_g.growth_number]))
    else:
        num_items = 0
        model = growth
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

        last = serial_number.objects.latest('id')
        lastnumber = last.serial_number
        nextserial = lastnumber + 1

        def generate_serial(sn):
            return ('wbg_' + str(sn))

        pf_1 = p_form(prefix="pf_1")
        pf_2 = p_form(prefix="pf_2")
        pf_3 = p_form(prefix="pf_3")
        pf_4 = p_form(prefix="pf_4")
        pf_5 = p_form(prefix="pf_5")
        pf_6 = p_form(prefix="pf_6")
        sform_1 = sample_form(instance=sample(), prefix="sform_1", initial={'substrate_serial': generate_serial(nextserial)})
        sform_2 = sample_form(instance=sample(), prefix="sform_2", initial={'substrate_serial': generate_serial(nextserial + 1)})
        sform_3 = sample_form(instance=sample(), prefix="sform_3", initial={'substrate_serial': generate_serial(nextserial + 2)})
        sform_4 = sample_form(instance=sample(), prefix="sform_4", initial={'substrate_serial': generate_serial(nextserial + 3)})
        sform_5 = sample_form(instance=sample(), prefix="sform_5", initial={'substrate_serial': generate_serial(nextserial + 4)})
        sform_6 = sample_form(instance=sample(), prefix="sform_6", initial={'substrate_serial': generate_serial(nextserial + 5)})

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
        model = sample
        print("split sample page accessed")
        sform = split_form(prefix='sform')
    return render(request, 'growths/split_sample.html', {'sform': sform})


class readings_detail(SessionHistoryMixin, DetailView):
    model = growth
    template_name = 'growths/readings_detail.html'
    slug_field = 'growth_number'
    context_object_name = 'growth'

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(readings_detail, self).get_context_data(**kwargs)
        context["growth"] = self.get_object()
        context["readingslist"] = readings.objects.filter(growth=self.get_object())
        return context


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
                newgrowth = growth=self.get_object()
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


class recipe_detail(SessionHistoryMixin, DetailView):
    model = growth
    template_name = 'growths/recipe_detail.html'
    slug_field = 'growth_number'
    context_object_name = 'growth'

    def get_context_data(self, **kwargs):
        context = super(recipe_detail, self).get_context_data(**kwargs)
        context["recipes"] = recipe_layer.objects.filter(growth=self.get_object())
        return context


def create_growth_start(request):
    if request.method =="POST":
        print ("Now entering... The POST STAGE!!!")
        cgsform = start_growth_form(request.POST, prefix='cgsform')
        commentsform = comments_form(request.POST, prefix='commentsform')
        if cgsform.is_valid() and commentsform.is_valid():
            print ("It's valid!")
            comments = commentsform.cleaned_data['comment_field']
            cgsform.save(runcomments=comments)
            return HttpResponseRedirect(reverse('create_growth_prerun'))
    else:
        print ("GET request incoming")
        num_items = 0
        model = growth
        query = model.objects.all()
        last = str(query[len(query) - 1])
        last_int = ''
        for i in xrange(1, 5):
            last_int += last[i]
        last_int = (int(last_int) + 1)
        last = ('g' + str(last_int))
        currenttime = time.strftime("%Y-%m-%d")
        cgsform = start_growth_form(prefix='cgsform', initial={'growth_number': last, 'date': currenttime})
        commentsform = comments_form(prefix='commentsform')
    return render(request, 'growths/create_growth_start.html', {'cgsform': cgsform, 'commentsform': commentsform})


def create_growth_prerun(request):
    if request.method == "POST":
        print ("Now entering... The POST STAGE!!!")
        pcform = prerun_checklist_form(request.POST, prefix='pcform')
        pgform = prerun_growth_form(request.POST, prefix='pgform')
        sourceform = prerun_sources_form(request.POST, prefix="sourceform")
        commentsform = comments_form(request.POST, prefix='commentsform')
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
        filledoutforms = 0
        for x in range(0, 6):
            if (pforms[x]).has_changed():
                filledoutforms = filledoutforms + 1
                print("The form has changed!!")
                sforms_list.append(sforms[x])
        print ("FILLED OUT FORMS RIGHT HERE " + str(filledoutforms))
        if  filledoutforms != 0 and pcform.is_valid() and pgform.is_valid() and sourceform.is_valid() and all([sf.is_valid() for sf in sforms_list]) and commentsform.is_valid():
            print ("PRERUN SUCCESS")
            newproject = pgform.cleaned_data['project']
            newinvestigation = pgform.cleaned_data['investigation']
            newplatter = pgform.cleaned_data['platter']
            newreactor = pgform.cleaned_data['reactor']
            newhas_gan = pgform.cleaned_data['has_gan']
            newhas_aln = pgform.cleaned_data['has_aln']
            newhas_inn = pgform.cleaned_data['has_inn']
            newhas_algan = pgform.cleaned_data['has_algan']
            newhas_ingan = pgform.cleaned_data['has_ingan']
            newhas_alingan = pgform.cleaned_data['has_alingan']
            newother_material = pgform.cleaned_data['other_material']
            neworientation = pgform.cleaned_data['orientation']
            newis_buffer = pgform.cleaned_data['is_buffer']
            newis_template = pgform.cleaned_data['is_template']
            newhas_superlattice = pgform.cleaned_data['has_superlattice']
            newhas_mqw = pgform.cleaned_data['has_mqw']
            newhas_graded = pgform.cleaned_data['has_graded']
            newhas_u = pgform.cleaned_data['has_u']
            newhas_p = pgform.cleaned_data['has_p']
            newhas_n = pgform.cleaned_data['has_n']
            lastgrowth = growth.objects.latest('id')
            lastgrowth = growth.objects.filter(growth_number=lastgrowth.growth_number)
            lastgrowth.update(project=newproject, platter=newplatter, reactor=newreactor,
                              run_comments=commentsform.cleaned_data['comment_field'],
                              has_gan=newhas_gan, has_aln=newhas_aln, has_inn=newhas_inn,
                              has_algan=newhas_algan, has_ingan=newhas_ingan, has_alingan=newhas_alingan,
                              other_material=newother_material, orientation=neworientation, is_template=newis_template,
                              is_buffer=newis_buffer, has_superlattice=newhas_superlattice, has_mqw=newhas_mqw,
                              has_graded=newhas_graded, has_n=newhas_n, has_p=newhas_p, has_u=newhas_u,)
            lastgrowth = growth.objects.latest('id')
            lastgrowth = growth.objects.filter(growth_number=lastgrowth.growth_number)
            pocket = 0
            for sf in sforms_list:
                pocket = pocket + 1
                new_s = sf.save(growthid=lastgrowth[0], pocketnum=pocket)
                new_s.save()
                print ("working on serial numbers")
                if new_s.substrate_serial.startswith('wbg_'):
                    print ("Success! It does start with 'wbg_'")
                    entireserial = new_s.substrate_serial
                    newserialnumber = ''
                    for x in range(4, len(entireserial)):
                        newserialnumber = newserialnumber + entireserial[x]
                    newserialnumber = int(newserialnumber)
                    sn = serial_number.objects.create(serial_number = newserialnumber)
                    sn.save()
            sourceform.save()
            return HttpResponseRedirect(reverse('create_growth_readings'))
        else:
            return render(request, 'growths/create_growth_prerun.html', {'pcform': pcform, 'pgform': pgform,
                    'sform_1': sform_1, 'sform_2': sform_2, 'sform_3': sform_3,
                   'sform_4': sform_4, 'sform_5': sform_5, 'sform_6': sform_6, 'pf_1': pf_1,
                   'pf_2': pf_2, 'pf_3': pf_3, 'pf_4': pf_4, 'pf_5': pf_5, 'pf_6': pf_6, 'sourceform': sourceform})

    else:
        print ("You are requesting information from this page (just so you know).")
        gentered= growth.objects.latest('id')
        pcform = prerun_checklist_form(prefix='pcform')
        pgform = prerun_growth_form(prefix='pgform', initial={'project': gentered.project,
                'investigation': gentered.investigation, 'platter': gentered.platter,
                'reactor': gentered.reactor})

        lastsource = source.objects.latest('id')
        lastsource = source.objects.filter(id=lastsource.id)
        lastsource = lastsource[0]
        newcp2mg = lastsource.cp2mg
        newtmin1 = lastsource.tmin1
        newtmin2 = lastsource.tmin2
        newtmga1 = lastsource.tmga1
        newtmga2 = lastsource.tmga2
        newtmal1 = lastsource.tmal1
        newtega1 = lastsource.tega1
        newnh3 = lastsource.nh3
        newsih4 = lastsource.sih4
        newdate_time = lastsource.date_time

        last = serial_number.objects.latest('id')
        lastnumber = last.serial_number
        nextserial = lastnumber + 1

        def generate_serial(sn):
            return ('wbg_' + str(sn))

        pf_1 = p_form(prefix="pf_1")
        pf_2 = p_form(prefix="pf_2")
        pf_3 = p_form(prefix="pf_3")
        pf_4 = p_form(prefix="pf_4")
        pf_5 = p_form(prefix="pf_5")
        pf_6 = p_form(prefix="pf_6")
        sform_1 = sample_form(instance=sample(), prefix="sform_1", initial={'substrate_serial': generate_serial(nextserial), 'location': ('Lab')})
        sform_2 = sample_form(instance=sample(), prefix="sform_2", initial={'substrate_serial': generate_serial(nextserial + 1), 'location': ('Lab')})
        sform_3 = sample_form(instance=sample(), prefix="sform_3", initial={'substrate_serial': generate_serial(nextserial + 2), 'location': ('Lab')})
        sform_4 = sample_form(instance=sample(), prefix="sform_4", initial={'substrate_serial': generate_serial(nextserial + 3), 'location': ('Lab')})
        sform_5 = sample_form(instance=sample(), prefix="sform_5", initial={'substrate_serial': generate_serial(nextserial + 4), 'location': ('Lab')})
        sform_6 = sample_form(instance=sample(), prefix="sform_6", initial={'substrate_serial': generate_serial(nextserial + 5), 'location': ('Lab')})
        sourceform = prerun_sources_form(prefix='sourceform', initial={'cp2mg': newcp2mg, 'tmin1': newtmin1,
                        'tmin2': newtmin2, 'tmga1': newtmga1, 'tmga2': newtmga2, 'tmal1': newtmal1,
                        'tega1': newtega1, 'nh3': newnh3, 'sih4': newsih4, 'date_time': newdate_time})
        commentsform = comments_form(prefix='commentsform', initial={'comment_field': gentered.run_comments})
    return render(request, 'growths/create_growth_prerun.html', {'pcform': pcform, 'pgform': pgform,
                    'sform_1': sform_1, 'sform_2': sform_2, 'sform_3': sform_3,
                   'sform_4': sform_4, 'sform_5': sform_5, 'sform_6': sform_6, 'pf_1': pf_1,
                   'pf_2': pf_2, 'pf_3': pf_3, 'pf_4': pf_4, 'pf_5': pf_5, 'pf_6': pf_6, 'sourceform': sourceform, 'commentsform': commentsform})


class create_growth_readings(SingleObjectMixin, TemplateView):
    context_object_name = 'growth'
    queryset = growth.objects.all()
    template_name = 'growths/create_growth_readings.html'

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(create_growth_readings, self).get_context_data(**kwargs)
        lastgrowth = growth.objects.latest('id')
        lastgrowth = growth.objects.filter(growth_number=lastgrowth.growth_number)
        lastgrowth = lastgrowth[0]
        commentsform = comments_form(prefix='commentsform', initial={'comment_field': lastgrowth.run_comments})
        context["commentscontext"] = commentsform
        context["growth"] = lastgrowth
        allreadings = readings.objects.filter(growth=lastgrowth)
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
        lastgrowth = growth.objects.latest('id')
        lastgrowth = growth.objects.filter(growth_number=lastgrowth.growth_number)
        commentsform = comments_form(request.POST, prefix='commentsform')
        if commentsform.is_valid():
            newcomments = commentsform.cleaned_data['comment_field']
            lastgrowth.update(run_comments=newcomments)
        lastgrowth = lastgrowth[0]
        numberofreadings = len(readings.objects.filter(growth=lastgrowth))
        print (numberofreadings)
        for x in range(0, numberofreadings):
            print("inside for loop")
            print(x)
            rform = readings_form(request.POST, prefix=('reading' + str(x+1)))
            if rform.is_valid():
                print ("rform is valid")
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
                thisreading = readings.objects.filter(growth=lastgrowth, layer=newlayer)
                thisreading.update(layer=newlayer, layer_desc=newlayer_desc,
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
        return HttpResponseRedirect(reverse('create_growth_readings'))


def create_growth_postrun(request):
    if request.method == "POST":
        print ("post request")
        prcform = postrun_checklist_form(request.POST, prefix='prcform')
        prsform = prerun_sources_form(request.POST, prefix='prsform')
        commentsform = comments_form(request.POST, prefix='commentsform')
        if prcform.is_valid() and prsform.is_valid() and commentsform.is_valid():
            print ("successful validation. Now let's do something.")
            lastgrowth = growth.objects.latest('id')
            lastgrowth = growth.objects.filter(id=lastgrowth.id)
            lastgrowth.update(run_comments=commentsform.cleaned_data['comment_field'])
            prsform.save()
            lastgrowth = lastgrowth[0]
            return HttpResponseRedirect(reverse('growth_detail', args=[lastgrowth]))
    else:
        print ("get request")
        lastsource = source.objects.latest('id')
        lastsource = source.objects.filter(id=lastsource.id)
        lastsource = lastsource[0]
        lastgrowth = growth.objects.latest('id')
        lastgrowth = growth.objects.filter(id=lastgrowth.id)
        lastgrowth = lastgrowth[0]
        newcp2mg = lastsource.cp2mg
        newtmin1 = lastsource.tmin1
        newtmin2 = lastsource.tmin2
        newtmga1 = lastsource.tmga1
        newtmga2 = lastsource.tmga2
        newtmal1 = lastsource.tmal1
        newtega1 = lastsource.tega1
        newnh3 = lastsource.nh3
        newsih4 = lastsource.sih4
        newdate_time = lastsource.date_time
        prcform = postrun_checklist_form(prefix='prcform')
        commentsform = comments_form(prefix='commentsform', initial={'comment_field': lastgrowth.run_comments})
        prsform = prerun_sources_form(prefix='prsform', initial={'cp2mg': newcp2mg, 'tmin1': newtmin1,
                        'tmin2': newtmin2, 'tmga1': newtmga1, 'tmga2': newtmga2, 'tmal1': newtmal1,
                        'tega1': newtega1, 'nh3': newnh3, 'sih4': newsih4, 'date_time': newdate_time})
    return render(request, 'growths/create_growth_postrun.html', {'prcform': prcform, 'prsform': prsform, 'commentsform': commentsform})

