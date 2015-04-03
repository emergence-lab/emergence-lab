# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import math
import os

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from braces.views import LoginRequiredMixin
import nanoscope
from PIL import Image, ImageDraw, ImageFont
import six

from afm.models import AFMFile, AFMScan
from core.models import DataFile, Process
from core.forms import DropzoneForm
from core.views import ActionReloadView


class AFMList(LoginRequiredMixin, ListView):
    """
    List the most recent afm data
    """
    model = AFMScan
    template_name = 'afm/afm_list.html'
    paginate_by = 25


class AFMDetail(LoginRequiredMixin, DetailView):
    """
    Detail view of the afm model.
    """
    model = AFMScan
    template_name = 'afm/afm_detail.html'
    context_object_name = 'afm'
    lookup_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_context_data(self, **kwargs):
        context = super(AFMDetail, self).get_context_data(**kwargs)
        context['dataset'] = self.object.datafiles.get_queryset().instance_of(AFMFile)
        return context


class AFMCreate(LoginRequiredMixin, CreateView):
    """
    View for creation of new afm data.
    """
    model = AFMScan
    template_name = 'afm/afm_create.html'
    fields = ('comment',)

    def get_success_url(self):
        return reverse('afm_detail', args=(self.object.uuid,))


class AFMUpdate(LoginRequiredMixin, UpdateView):
    """
    View for updating afm data.
    """
    model = AFMScan
    template_name = 'afm/afm_update.html'
    context_object_name = 'afm'
    lookup_url_kwarg = 'uuid'
    fields = ('comment',)

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_success_url(self):
        return reverse('afm_detail', args=(self.object.uuid,))


class AFMDelete(LoginRequiredMixin, DeleteView):
    """
    View for deleting afm data
    """
    model = AFMScan
    template_name = 'afm/afm_delete.html'
    context_object_name = 'afm'
    lookup_url_kwarg = 'uuid'

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()

        assert self.lookup_url_kwarg in self.kwargs, (
            'Expected view {} to be called with a URL keyword argument '
            'named "{}". Fix your URL conf.'.format(self.__class__.__name__,
                                                    self.lookup_url_kwarg))
        uuid = Process.strip_uuid(self.kwargs[self.lookup_url_kwarg])
        return get_object_or_404(Process, uuid_full__startswith=uuid)

    def get_success_url(self):
        return reverse('afm_list')


class AFMFileUpload(LoginRequiredMixin, CreateView):
    """
    Add files to an existing afm process
    """
    model = AFMFile
    template_name = 'afm/afm_upload.html'
    form_class = DropzoneForm

    def get_context_data(self, **kwargs):
        context = super(AFMFileUpload, self).get_context_data(**kwargs)
        context['process'] = self.kwargs['uuid']
        return context

    def process_image(self, scan, filename, scan_number):
        image = Image.fromarray(scan.colorize())

        processed_image = Image.new(image.mode, (654, 580), 'white')
        processed_image.paste(image,
                              (20, 20, image.size[0] + 20, image.size[1] + 20))

        calibri = ImageFont.truetype(
            os.path.join(settings.STATIC_ROOT, 'afm', 'fonts', 'calibrib.ttf'),
            20)
        draw = ImageDraw.Draw(processed_image)

        scale_image = Image.open(
            os.path.join(settings.STATIC_ROOT, 'afm', 'img', 'scale_12.png'))
        processed_image.paste(scale_image,
                             (28 + image.size[0],
                              30,
                              28 + image.size[0] + scale_image.size[0],
                              30 + scale_image.size[1]))
        if scan.type == 'Height':
            unit = 'nm'
        else:
            unit = 'V'
            print(scan.sensitivity, scan.magnify, scan.scale)
        draw.text(
            (28 + image.size[0] + scale_image.size[0] + 7, 25 ),
            '{0:.1f} {1}'.format(scan.height_scale, unit), 'black', calibri)
        draw.text(
            (28 + image.size[0] + scale_image.size[0] + 7, 20 + scale_image.size[1]),
            '0.0 {}'.format(unit), 'black', calibri)


        zrange_str = 'Z-Range: {0:.2f} nm'.format(scan.zrange)
        rms_str = 'RMS: {0:.2f} nm'.format(scan.rms)
        size_str = 'Area: {0} \u03bcm X {0} \u03bcm'.format(math.sqrt(scan.scan_area))

        draw.text((20, 25 + image.size[1]), filename, 'black', calibri)
        draw.text(
            (20 + image.size[0] - calibri.getsize(size_str)[0], 25 + image.size[1]),
            size_str, 'black', calibri)
        if scan.type == 'Height':
            draw.text(
                (20, 50 + image.size[1]), zrange_str, 'black', calibri)
            draw.text(
                (20 + image.size[0] - calibri.getsize(rms_str)[0], 50 + image.size[1]),
                rms_str, 'black', calibri)
        else:
            type_str = '{} AFM'.format(scan.type)
            draw.text(
                (20 + image.size[0] - calibri.getsize(type_str)[0], 50 + image.size[1]),
                type_str, 'black', calibri)

        tempio = six.StringIO()
        processed_image.save(tempio, format='PNG')
        return InMemoryUploadedFile(
            tempio, field_name=None, name=filename + '.png',
            content_type='image/png', size=tempio.len, charset=None)

    def form_valid(self, form):
        process = Process.objects.get(
            uuid_full__startswith=Process.strip_uuid(self.kwargs['uuid']))

        image = self.request.FILES['file']
        scan_number = int(os.path.splitext(image.name)[-1][1:])
        raw = six.BytesIO(image.read())
        raw.mode = 'b'
        scan = nanoscope.read(raw, encoding='cp1252')
        for img in scan:
            img.process()

            with transaction.atomic():
                obj = AFMFile.objects.create(data=image,
                                             content_type='application/octet-stream',
                                             rms=img.rms,
                                             zrange=img.zrange,
                                             size=img.scan_area,
                                             image_type=img.type,
                                             scan_number=scan_number)
                obj.processes.add(process)

                img_file = AFMFile.objects.create(
                    data=self.process_image(img, image.name, scan_number),
                    content_type='image/png',
                    state='extracted',
                    rms=img.rms,
                    zrange=img.zrange,
                    size=img.scan_area,
                    image_type=img.type,
                    scan_number=scan_number)
                img_file.processes.add(process)

        return JsonResponse({'status': 'success'})


class AFMRemoveFileActionReloadView(LoginRequiredMixin, ActionReloadView):

    def perform_action(self, request, *args, **kwargs):
        process = Process.objects.get(uuid_full__startswith=Process.strip_uuid(self.kwargs['uuid']))
        datafile = DataFile.objects.get(pk=self.kwargs['id'])
        datafile.processes.remove(process)
        if not datafile.processes.all().exists():
            datafile.delete()

    def get(self, request, *args, **kwargs):
        self.perform_action(request, *args, **kwargs)
        return super(ActionReloadView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('afm_detail', args=(self.kwargs['uuid'],))
