from django.shortcuts import render
import os
from django.conf import settings
from django.views.generic import ListView, RedirectView, TemplateView, FormView
import tempfile
import json

from IPython.nbconvert.exporters.html import HTMLExporter
from IPython.config import Config


# Create your views here.

class NotebookList(TemplateView):
    template_name = 'notebooker/template_list.html'

    def get_context_data(self, **kwargs):
        user = str(self.request.user)
        tmp = []
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'notebooks', user)):
            if 'template_list' not in kwargs:
                for template in os.listdir(os.path.join(settings.MEDIA_ROOT, 'notebooks', user)):
                    if template.endswith('.ipynb'):
                        tmp.append({'name': template,
                                    'path': os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user, template),
                                    #'files': os.listdir(os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user)),
                                    #'comment': comment
                                    })
                kwargs['template_list'] = tmp
        return super(NotebookList, self).get_context_data(**kwargs)

class NotebookDemo(TemplateView):
    template_name = 'notebooker/demo_nb.html'

    def get_context_data(self, **kwargs):
        filename = kwargs['notebook_name']
        user = str(self.request.user)

        e = HTMLExporter(config=Config({'HTMLExporter':{'default_template':'basic'}}))
        path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(filename + '.ipynb'))
        if 'notebook_content' not in kwargs:

            #kwargs['notebook_content'] = str(e.from_filename(path))

            with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
            #with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, 'out1.html'), 'wb') as output:
                for i in e.from_filename(path):
                    if not str(i).startswith('defaultdict'):
                        output.write(i)
                output.flush()
                output.seek(0)
                kwargs['notebook_content'] = output.read()
                output.close()
        if 'comments' not in kwargs:
            tmp = []
            with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, 'test.json'), 'r') as comment:
                comments = json.load(comment)
                for i in comments:
                    tmp.append(comments[i])
            kwargs['comments'] = tmp
        return super(NotebookDemo, self).get_context_data(**kwargs)

class NotebookIntDemo(TemplateView):
    template_name = 'notebooker/demo_int_nb.html'

    def get_context_data(self, **kwargs):
        filename = kwargs['notebook_name']
        user = str(self.request.user)

        e = HTMLExporter(config=Config({'HTMLExporter':{'default_template':'basic'}}))
        path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(filename + '.ipynb'))
        with open(path, 'r') as nb:
            notebook = json.loads(nb.read())
        if 'notebook_content' not in kwargs:
            cntnt = []
            cleaned_cntnt = []
            #kwargs['notebook_content'] = str(e.from_filename(path))

            for cell in notebook['worksheets'][0]['cells']:
                with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
                    m = {}
                    t = []
                    t.append(cell)
                    m['cells'] = t
                    c = []
                    c.append(m)
                    p = {}
                    p['metadata'] = {}
                    p['nbformat'] = 3
                    p['worksheets'] = c
                    output.write(json.dumps(p))
                    output.seek(0)
                    #cntnt.append(e.from_file(output))
                    #for i in e.from_file(output):
                    #    if 'defaultdict' not in i:
                    #    cntnt.append(i)
                    with open (tempfile.NamedTemporaryFile().name, 'wb+') as cleaned_output:
                        for i in e.from_file(output):
                            if 'defaultdict' not in str(i):
                                cleaned_output.write(i)
                        cleaned_output.flush()
                        cleaned_output.seek(0)
                        cntnt.append(cleaned_output.read())
                        cleaned_output.close()

                    output.close()
            #for i in cntnt:
            #    if not str(i).startswith('defaultdict'):
            #        cleaned_cntnt.append(i)

        #        with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
        #        #with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, 'out1.html'), 'wb') as output:
        #
        #            for i in e.from_filename(path):
        #                if not str(i).startswith('defaultdict'):
        #                    output.write(i)
        #            output.flush()
        #            output.seek(0)
        #            kwargs['notebook_content'] = output.read()
        #            output.close()
            kwargs['notebook_content'] = cntnt
        if 'comments' not in kwargs:

            tmp = []
            with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, 'test.json'), 'r') as comment:
                comments = json.load(comment)
                for i in comments:
                    tmp.append(comments[i])
            kwargs['comments'] = tmp
        return super(NotebookIntDemo, self).get_context_data(**kwargs)
