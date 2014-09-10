import time

from django.shortcuts import render, render_to_response
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView, FormView
from django.views.generic.edit import ProcessFormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from actstream import action

from core.models import operator
from .models import growth, sample, readings, serial_number, recipe_layer, source
from .filters import growth_filter, RelationalFilterView
from .forms import growth_form, sample_form, p_form, split_form, readings_form, comments_form, GrowthUpdateForm
from .forms import prerun_checklist_form, start_growth_form, prerun_growth_form, prerun_sources_form, postrun_checklist_form
import afm.models
import hall.models


class growth_list(RelationalFilterView):
    filterset_class = growth_filter
    template_name = 'growths/growth_filter.html'


class afm_compare(ListView):
    template_name = 'growths/afm_compare.html'

    def get_queryset(self):
        id_list = [int(id) for id in self.request.GET.getlist('afm')]
        objects = afm.models.afm.objects.filter(id__in=id_list)
        return objects


class GrowthDetailView(DetailView):
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


class GrowthUpdateView(UpdateView):
    """
    View to update information about a growth.
    """
    model = growth
    template_name = 'growths/growth_update.html'
    slug_field = 'growth_number'
    form_class = GrowthUpdateForm

    def get_initial(self):
        return {'run_comments': self.object.run_comments.rendered}

    def get_success_url(self):
        return reverse('growth_detail', args=(self.object.growth_number,))


class SampleDetailView(DetailView):
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
        context['samples'] = sample.objects.filter(growth__growth_number=growth_number, pocket=pocket).order_by('pocket', 'piece')
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


class SplitSampleView(FormView):
    form_class = split_form
    template_name = 'growths/split_sample.html'

    def get_form_kwargs(self):
        kwargs = super(SplitSampleView, self).get_form_kwargs()
        if self.request.method == 'GET' and 'sample' in self.request.GET:
            kwargs.update({
                'initial': {'parent': self.request.GET.get('sample')},
            })
        return kwargs

    def form_valid(self, form):
        num_pieces = form.cleaned_data['pieces']
        parent = form.cleaned_data['parent']
        piece_siblings = sample.get_piece_siblings(parent).order_by('-piece')
        if piece_siblings:
            last_letter = piece_siblings.first().piece
        else:
            last_letter = 'a'
            parent.piece = 'a'
            parent.save()
        for i in range(num_pieces - 1):
            last_letter = unichr(ord(last_letter) + 1)
            parent.pk = None
            parent.piece = last_letter
            parent.save()
        action.send(self.request.user.operator, verb='split sample', action_object=parent.growth, target=parent.growth.project, investigation=parent.growth.investigation_id)
        return HttpResponseRedirect(reverse('sample_family_detail', args=(parent.growth.growth_number, parent.pocket)))


class readings_detail(DetailView):
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
                'pyro_out': reading.pyro_out, 'pyro_in': reading.pyro_in, 'ecp_temp': reading.ecp_temp, 'tc_out': reading.tc_out,
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
        numberofreadings = len(readings.objects.filter(growth=self.get_object()))
        print (numberofreadings)
        for x in range(0, numberofreadings):
            rform = readings_form(request.POST, prefix=('reading' + str(x+1)))
            if rform.is_valid():
                newgrowth = growth=self.get_object()
                newlayer = rform.cleaned_data['layer']
                newlayer_desc = rform.cleaned_data['layer_desc']
                newpyro_out = rform.cleaned_data['pyro_out']
                newpyro_in = rform.cleaned_data['pyro_in']
                newecp_temp = rform.cleaned_data['ecp_temp']
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
                thisreading = readings.objects.filter(growth=newgrowth, layer=newlayer)
                thisreading.update(growth=newgrowth, layer = newlayer, layer_desc=newlayer_desc,
                                   pyro_out=newpyro_out, pyro_in=newpyro_in, ecp_temp=newecp_temp, tc_out=newtc_out,
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


class recipe_detail(DetailView):
    model = growth
    template_name = 'growths/recipe_detail.html'
    slug_field = 'growth_number'
    context_object_name = 'growth'

    def get_context_data(self, **kwargs):
        context = super(recipe_detail, self).get_context_data(**kwargs)
        context["recipes"] = recipe_layer.objects.filter(growth=self.get_object())
        return context


class CreateGrowthStartView(TemplateView):
    template_name = 'growths/create_growth_start.html'

    def post(self, request, *args, **kwargs):
        cgsform = start_growth_form(request.POST, prefix='cgsform')
        commentsform = comments_form(request.POST, prefix='commentsform')
        if cgsform.is_valid() and commentsform.is_valid():
            comments = commentsform.cleaned_data['comment_field']
            cgsform.save(runcomments=comments)
            return HttpResponseRedirect(reverse('create_growth_prerun'))
        else:
            return render(request, self.template_name,
                          {'cgsform': cgsform, 'commentsform': commentsform})

    def get_context_data(self, **kwargs):
        context = super(CreateGrowthStartView, self).get_context_data(**kwargs)
        try:
            last_growth = growth.objects.latest('growth_number').growth_number
            next_growth = 'g{0}'.format(int(last_growth[1:]) + 1)
        except:
            next_growth = 'g1000'
        currenttime = time.strftime('%Y-%m-%d')
        context['cgsform'] = start_growth_form(prefix='cgsform',
                                               initial={
                                                   'growth_number': next_growth,
                                                   'date': currenttime,
                                                   'reactor': 'd180',
                                                   'operator': operator.objects.get(user=self.request.user),
                                               })
        context['commentsform'] = comments_form(prefix='commentsform')
        return context


class CreateGrowthPrerunView(TemplateView):
    template_name = 'growths/create_growth_prerun.html'

    def post(self, request, *args, **kwargs):
        lastgrowth = growth.objects.latest('growth_number')
        pcform = prerun_checklist_form(request.POST, prefix='pcform')
        pgform = prerun_growth_form(request.POST, prefix='pgform', instance=lastgrowth)
        sourceform = prerun_sources_form(request.POST, prefix="sourceform")
        commentsform = comments_form(request.POST, prefix='commentsform')
        saved_forms = {}
        sample_forms = []
        for i in range(1, 7):
            pf = p_form(request.POST, prefix='pf_{0}'.format(i))
            saved_forms['pf_{0}'.format(i)] = pf
            sf = sample_form(request.POST, instance=sample(), prefix='sform_{0}'.format(i))
            saved_forms['sform_{0}'.format(i)] = sf
            if pf.has_changed():
                sample_forms.append(sf)
        if sample_forms and pcform.is_valid() and pgform.is_valid() and sourceform.is_valid() and all([sf.is_valid() for sf in sample_forms]) and commentsform.is_valid():
            
            lastgrowth = pgform.save()
            for i, sform in enumerate(sample_forms):
                pocket = i + 1
                new_sample = sform.save(growth=lastgrowth, pocket=pocket)
            return HttpResponseRedirect(reverse('create_growth_readings'))
        else:  # form did not validate
            saved_forms.update({
                'pcform': pcform,
                'pgform': pgform,
                'sourceform': sourceform,
                'commentsform': commentsform
            })
            return render(request, self.template_name, saved_forms)

    def get_context_data(self, **kwargs):
        context = super(CreateGrowthPrerunView, self).get_context_data(**kwargs)
        last_growth = growth.objects.latest('growth_number')
        context['pcform'] = prerun_checklist_form(prefix='pcform')
        context['pgform'] = prerun_growth_form(prefix='pgform',
                                               initial={
                                                   'project': last_growth.project,
                                                   'investigation': last_growth.investigation,
                                                   'platter': last_growth.platter,
                                                   'reactor': last_growth.reactor,
                                               })
        try:
            last_sources = source.objects.latest('date_time')
            context['sourceform'] = prerun_sources_form(instance=last_sources, prefix='sourceform')
        except:
            context['sourceform'] = prerun_sources_form(prefix='sourceform')
        context['commentsform'] = comments_form(prefix='commentsform',
                                                initial={'comment_field': last_growth.run_comments})
        for i in range(1, 7):
            context['pf_{0}'.format(i)] = p_form(prefix='pf_{0}'.format(i))
            context['sform_{0}'.format(i)] = sample_form(prefix='sform_{0}'.format(i), instance=sample(),
                                                         initial={'substrate_serial': 'wbg_{0}'.format(serial_number.generate_serial()),
                                                                  'location': 'Lab'})
        return context


class create_growth_readings(SingleObjectMixin, TemplateView):
    context_object_name = 'growth'
    queryset = growth.objects.all()
    template_name = 'growths/create_growth_readings.html'

    def get_context_data(self, **kwargs):
        self.object = None
        context = super(create_growth_readings, self).get_context_data(**kwargs)
        lastgrowth = growth.objects.latest('growth_number')
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
                'pyro_out': reading.pyro_out, 'pyro_in': reading.pyro_in, 'ecp_temp': reading.ecp_temp, 'tc_out': reading.tc_out,
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
        lastgrowth = growth.objects.latest('growth_number')
        commentsform = comments_form(request.POST, prefix='commentsform')
        if commentsform.is_valid():
            newcomments = commentsform.cleaned_data['comment_field']
            lastgrowth.update(run_comments=newcomments)
        lastgrowth = lastgrowth[0]
        numberofreadings = len(readings.objects.filter(growth=lastgrowth))
        print (numberofreadings)
        for x in range(0, numberofreadings):
            rform = readings_form(request.POST, prefix=('reading' + str(x+1)))
            if rform.is_valid():
                newlayer = rform.cleaned_data['layer']
                newlayer_desc = rform.cleaned_data['layer_desc']
                newpyro_out = rform.cleaned_data['pyro_out']
                newpyro_in = rform.cleaned_data['pyro_in']
                newecp_temp = rform.cleaned_data['ecp_temp']
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
                thisreading = readings.objects.filter(growth=lastgrowth, layer=newlayer)
                thisreading.update(layer=newlayer, layer_desc=newlayer_desc,
                                   pyro_out=newpyro_out, pyro_in=newpyro_in, ecp_temp=newecp_temp, tc_out=newtc_out,
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
        prcform = postrun_checklist_form(request.POST, prefix='prcform')
        prsform = prerun_sources_form(request.POST, prefix='prsform')
        commentsform = comments_form(request.POST, prefix='commentsform')
        if prcform.is_valid() and prsform.is_valid() and commentsform.is_valid():
            print ("successful validation. Now let's do something.")
            lastgrowth = growth.objects.latest('growth_number')
            lastgrowth.update(run_comments=commentsform.cleaned_data['comment_field'])
            prsform.save()
            action.send(request.user.operator, verb='completed growth', action_object=lastgrowth, target=lastgrowth.project, investigation=lastgrowth.investigation_id)
            return HttpResponseRedirect(reverse('growth_detail', args=[lastgrowth]))
    else:
        lastgrowth = growth.objects.latest('growth_number')
        prcform = postrun_checklist_form(prefix='prcform')
        commentsform = comments_form(prefix='commentsform', initial={'comment_field': lastgrowth.run_comments})
        try:
            last_sources = source.objects.latest('date_time')
            prsform = prerun_sources_form(instance=last_sources, prefix='prsform')
        except:
            prsform = prerun_sources_form(prefix='prsform')
    return render(request, 'growths/create_growth_postrun.html', {'prcform': prcform, 'prsform': prsform, 'commentsform': commentsform})

