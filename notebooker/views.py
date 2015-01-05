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
from IPython.nbformat.current import read, write
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

class NotebookInteractive(FormView):
    template_name = 'notebooker/interactive_nb.html'
    form_class = NBCellEdit

    def get_form_kwargs(self):
        kwargs = super(NotebookInteractive, self).get_form_kwargs()
        user = str(self.request.user)
        if 'cell_count' not in kwargs:
            nb = json.load(open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(self.kwargs['notebook_name'] + '.ipynb')), 'r'))
            kwargs['cell_count'] = int(len(nb['worksheets'][0]['cells']))
        return kwargs

    def get_initial(self):
        initial = super(NotebookInteractive, self).get_initial()
        #cell_num = int(self.kwargs['cell'])
        user = str(self.request.user)
        nb = json.load(open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(self.kwargs['notebook_name'] + '.ipynb')), 'r'))
        for cell_num, i in enumerate(nb['worksheets'][0]['cells']):
            tmp = []
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
                initial['cell_{}'.format(cell_num)] = output.read()
                output.close
        return initial

    def get_context_data(self, **kwargs):
        filename = self.kwargs['notebook_name']
        user = str(self.request.user)
        e = HTMLExporter(config=Config({'HTMLExporter':{'default_template':'basic'}}))
        path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(filename + '.ipynb'))
        with open(path, 'r') as nb:
            notebook = json.loads(nb.read())
        if 'notebook_content' not in kwargs:
            cntnt = []
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
                    with open (tempfile.NamedTemporaryFile().name, 'wb+') as cleaned_output:
                        for i in e.from_file(output):
                            if 'defaultdict' not in str(i):
                                cleaned_output.write(i)
                        cleaned_output.flush()
                        cleaned_output.seek(0)
                        cntnt.append(cleaned_output.read())
                        cleaned_output.close()
                    output.close()
            kwargs['notebook_content'] = cntnt
        if 'comments' not in kwargs:
            tmp = []
            with open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, 'test.json'), 'r') as comment:
                comments = json.load(comment)
                for i in comments:
                    tmp.append(comments[i])
            kwargs['comments'] = tmp
        if 'cell_count' not in kwargs:
            nb = json.load(open(os.path.join(settings.MEDIA_ROOT, 'notebooks', user, str(self.kwargs['notebook_name'] + '.ipynb')), 'r'))
            kwargs['cell_count'] = range(int(len(nb['worksheets'][0]['cells'])))
        if 'notebook_name' not in kwargs:
            kwargs['notebook_name'] = 'Untitled0'
        return super(NotebookInteractive, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = str(self.request.user)
        #cell_num = int(form.cleaned_data['Submit'])

        #self.kwargs['notebook_name'] = 'Untitled0'
        filename = str(self.kwargs['notebook_name'] + '.ipynb')
        #cell_num = 0
        #cell_num = int(self.kwargs['cell'])
        nb_path = os.path.join(settings.MEDIA_ROOT, 'notebooks', user, filename)
        try:
            nb = json.load(open(nb_path, 'r'))

            cell_count = len(nb['worksheets'][0]['cells'])

            for i in range(cell_count):
                if 'upd_cell_{}'.format(int(i + 1)) in self.request.POST:
                    cell_num = int(i)
                elif 'upd_all' in self.request.POST:
                    pass

            if nb['worksheets'][0]['cells'][cell_num]['cell_type'] == 'code':
                nb['worksheets'][0]['cells'][cell_num]['input'] = form.cleaned_data['cell_{}'.format(cell_num)]
            elif nb['worksheets'][0]['cells'][cell_num]['cell_type'] == 'markdown':
                nb['worksheets'][0]['cells'][cell_num]['source'] = form.cleaned_data['cell_{}'.format(cell_num)]
            with open(nb_path, 'wb+') as output:
                try:
                    output.truncate()
                    output.seek(0)
                    json.dump(nb, output)
                    output.close()
                except Exception as e: print(e)
            nb = read(open(nb_path), 'json')
            r = NotebookRunner(nb)

            #r.run_notebook()
            #except Exception as e: print(e)
            #except NotebookError as e: print(e)
            #for i, cell in enumerate(r.iter_code_cells()):
            #    if i == cell_num:
            #        try:
            #            r.run_cell(cell, skip_exceptions=True)
            #        except NotebookError:
            #            if not skip_exceptions:
            #                raise
            #write(r.nb, open(nb_path, 'w'), 'json')
        except Exception as e: print(e)
        r.run_notebook()
        write(r.nb, open(nb_path, 'w'), 'json')

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
