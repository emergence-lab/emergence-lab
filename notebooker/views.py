from django.shortcuts import render, HttpResponse, HttpResponseRedirect, render_to_response
from django.core.urlresolvers import reverse
import os
from django.conf import settings
from django.views.generic import ListView, RedirectView, TemplateView, FormView
import tempfile
import json

from IPython.nbconvert.exporters.html import HTMLExporter
from IPython.config import Config
from runipy.notebook_runner import NotebookRunner
from IPython.nbformat.current import read, write, reads_json
from .forms import NBCellEdit


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
                        tmp.append({'name': template.split('.ipynb')[0],
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

class NotebookInteractive(FormView):
    template_name = 'notebooker/interactive_nb.html'
    form_class = NBCellEdit

    def _set_ipython_variables(self, *args, **kwargs):
        self.nb_path = os.path.join(settings.MEDIA_ROOT,
                               'notebooks',
                               str(self.request.user),
                               str(self.kwargs['notebook_name'] + '.ipynb'))
        self.nb_name = self.kwargs['notebook_name']
        self.e = HTMLExporter(config=Config({'HTMLExporter':{'default_template':'basic'}}))
        self.nb = read(open(self.nb_path, 'rb'), 'json')
        self.cells = [ws.cells for ws in self.nb.worksheets]

    def get(self, request, *args, **kwargs):
        self._set_ipython_variables()
        return super(NotebookInteractive, self).get(request)

    def get_form_kwargs(self):
        kwargs = super(NotebookInteractive, self).get_form_kwargs()
        if 'cell_count' not in kwargs:
            kwargs['cell_count'] = int(len(self.cells[0]))
        return kwargs

    def get_initial(self):
        initial = super(NotebookInteractive, self).get_initial()
        for cell_num, i in enumerate(self.cells[0]):
            if i['cell_type'] == 'code': initial['cell_{}'.format(cell_num)] = i['input']
            elif i['cell_type'] == 'markdown': initial['cell_{}'.format(cell_num)] = i['source']
        return initial

    def get_context_data(self, **kwargs):
        if 'notebook_content' not in kwargs:
            nb_content = []
            for cell in self.cells[0]:
                #with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
                temp_nb = {
                    'metadata': {},
                    'nbformat': 3,
                    'worksheets': [{'cells': [cell]}]
                }
                for i in self.e.from_notebook_node(reads_json(json.dumps(temp_nb))):
                    if not 'defaultdict' in str(i):
                        nb_content.append(i)
            kwargs['notebook_content'] = nb_content
        if 'comments' not in kwargs:
            tmp = []
            with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', str(self.request.user), 'test.json'), 'r') as comment:
                comments = json.load(comment)
                for i in comments:
                    tmp.append(comments[i])
            kwargs['comments'] = tmp
        if 'cell_count' not in kwargs:
            kwargs['cell_count'] = int(len(self.cells[0]))
        if 'notebook_name' not in kwargs:
            kwargs['notebook_name'] = self.nb_name
        return super(NotebookInteractive, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self._set_ipython_variables()
        return super(NotebookInteractive, self).post(request)

    def form_valid(self, form):
        cell_count = int(len(self.cells[0]))
        for i in range(cell_count):
            if 'upd_cell_{}'.format(int(i + 1)) in self.request.POST:
                cell_num = int(i)
            elif 'upd_all' in self.request.POST:
                pass
        if self.cells[0][cell_num]['cell_type'] == 'code':
            self.cells[0][cell_num]['input'] = form.cleaned_data['cell_{}'.format(cell_num)]
        elif self.cells[0][cell_num]['cell_type'] == 'code':
            self.cells[0][cell_num]['source'] = form.cleaned_data['cell_{}'.format(cell_num)]
        r = NotebookRunner(self.nb)
        r.run_notebook()
        write(r.nb, open(self.nb_path, 'w'), 'json')
        return HttpResponseRedirect(reverse('notebook_int', kwargs = {'notebook_name': self.kwargs['notebook_name']}))

#class NotebookIntDemo(TemplateView):
#    template_name = 'notebooker/demo_int_nb.html'
#
#    def get_context_data(self, **kwargs):
#        filename = kwargs['notebook_name']
#        user = str(self.request.user)
#        e = HTMLExporter(config=Config({'HTMLExporter':{'default_template':'basic'}}))
#        path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(filename + '.ipynb'))
#        with open(path, 'r') as nb:
#            notebook = json.loads(nb.read())
#        if 'notebook_content' not in kwargs:
#            cntnt = []
#            for cell in notebook['worksheets'][0]['cells']:
#                with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
#                    m = {}
#                    t = []
#                    t.append(cell)
#                    m['cells'] = t
#                    c = []
#                    c.append(m)
#                    p = {}
#                    p['metadata'] = {}
#                    p['nbformat'] = 3
#                    p['worksheets'] = c
#                    output.write(json.dumps(p))
#                    output.seek(0)
#                    with open (tempfile.NamedTemporaryFile().name, 'wb+') as cleaned_output:
#                        for i in e.from_file(output):
#                            if 'defaultdict' not in str(i):
#                                cleaned_output.write(i)
#                        cleaned_output.flush()
#                        cleaned_output.seek(0)
#                        cntnt.append(cleaned_output.read())
#                        cleaned_output.close()
#                    output.close()
#            kwargs['notebook_content'] = cntnt
#        if 'comments' not in kwargs:
#            tmp = []
#            with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, 'test.json'), 'r') as comment:
#                comments = json.load(comment)
#                for i in comments:
#                    tmp.append(comments[i])
#            kwargs['comments'] = tmp
#        return super(NotebookIntDemo, self).get_context_data(**kwargs)

class CellEdit(FormView):
    template_name = 'notebooker/cell_edit_form.html'
    form_class = NBCellEdit
    success_url = '/ipython'
    def get_initial(self):
        initial = super(CellEdit, self).get_initial()
        cell_num = int(self.kwargs['cell'])
        user = str(self.request.user)
        nb = json.load(open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(self.kwargs['notebook_name'] + '.ipynb')), 'r'))
        if nb['worksheets'][0]['cells'][cell_num]['cell_type'] == 'code':
            tmp = nb['worksheets'][0]['cells'][cell_num]['input']
        elif nb['worksheets'][0]['cells'][cell_num]['cell_type'] == 'markdown':
            tmp = nb['worksheets'][0]['cells'][cell_num]['source']
        #initial['cell'] = nb['worksheets'][0]['cells'][cell_num]['input']
        with open(tempfile.NamedTemporaryFile().name, 'wb+') as output:
            for i in tmp:
                output.write(i)
            output.flush()
            output.seek(0)
            initial['cell'] = output.read()
            output.close
        return initial

    def form_valid(self, form):
        user = str(self.request.user)
        cell_num = int(self.kwargs['cell'])
        nb_path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(self.kwargs['notebook_name'] + '.ipynb'))
        nb = json.load(open(nb_path, 'r'))
        if nb['worksheets'][0]['cells'][cell_num]['cell_type'] == 'code':
            nb['worksheets'][0]['cells'][cell_num]['input'] = form.cleaned_data['cell']
        elif nb['worksheets'][0]['cells'][cell_num]['cell_type'] == 'markdown':
            nb['worksheets'][0]['cells'][cell_num]['source'] = form.cleaned_data['cell']
        with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(self.kwargs['notebook_name'] + '.ipynb')), 'wb+') as output:
            try:
                output.truncate()
                output.seek(0)
                json.dump(nb, output)
                output.close()
            except Exception as e: print(e)
        nb = read(open(nb_path), 'json')
        r = NotebookRunner(nb)
        for i, cell in enumerate(r.iter_code_cells()):
            if i == cell_num:
                try:
                    r.run_cell(cell)
                except NotebookError:
                    if not skip_exceptions:
                        raise
                #if progress_callback:
                #    progress_callback(i)
        #r.run_notebook(skip_exceptions=True)
        write(r.nb, open(nb_path, 'w'), 'json')
        return HttpResponseRedirect(reverse('notebook_int_demo', kwargs = {'notebook_name': self.kwargs['notebook_name']}))
