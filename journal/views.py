from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView

from braces.views import LoginRequiredMixin

from .models import journal_entry
from .forms import JournalEntryForm


class JournalCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a journal entry.
    """
    template_name = 'journal/entry_create.html'
    model = journal_entry
    form_class = JournalEntryForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user.operator
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('journal_list', kwargs={'username': self.request.user.username})


class JournalDetailView(LoginRequiredMixin, DetailView):
    """
    View for details of a journal entry.
    """
    template_name = 'journal/entry_detail.html'
    model = journal_entry
    context_object_name = 'entry'


class JournalListView(LoginRequiredMixin, ListView):
    """
    View a list of recent journal entries.
    """
    template_name = 'journal/entry_list.html'
    model = journal_entry
    context_object_name = 'entries'

    def get_queryset(self):
        return journal_entry.objects.filter(author=self.request.user).order_by('-date')
