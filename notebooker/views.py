from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.urlresolvers import reverse
import os
from django.conf import settings
from django.views.generic import TemplateView
import json

from IPython.nbconvert.exporters.html import HTMLExporter
from IPython.config import Config
from .runipy_extender import NotebookRunner
from IPython.nbformat import read, write, reads


class EmbeddedNotebook(TemplateView):
    template_name = 'notebooker/embedded.html'


class NotebookList(TemplateView):
    template_name = 'notebooker/template_list.html'

    def get_context_data(self, **kwargs):
        user = str(self.request.user)
        tmp = []
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, 'notebooks', user)):
            if 'template_list' not in kwargs:
                for template in os.listdir(os.path.join(settings.MEDIA_ROOT, 'notebooks', user)):
                    if template.endswith('.ipynb'):
                        tmp.append({'name': template.split('.ipynb')[0],
                                    #'path': os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user, template),
                                    'jupyter_url': '{0}/user/{1}/notebooks/{2}'.format(settings.JUPYTERHUB_URL, user, template)
                                    #'files': os.listdir(os.path.join(settings.MEDIA_ROOT, 'simulations', 'templates', user)),
                                    #'comment': comment
                                    })
                kwargs['template_list'] = tmp
        return super(NotebookList, self).get_context_data(**kwargs)

class NotebookViewer(TemplateView):
    template_name = 'notebooker/nb_viewer.html'

    def get_context_data(self, **kwargs):
        filename = kwargs['notebook_name']
        user = str(self.request.user)

        e = HTMLExporter(config=Config({'HTMLExporter':{'default_template':'basic'}}))
        path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(filename + '.ipynb'))
        if 'notebook_content' not in kwargs:
            with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
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
        return super(NotebookViewer, self).get_context_data(**kwargs)
