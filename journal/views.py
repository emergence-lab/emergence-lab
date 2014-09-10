from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView

from actstream import action
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
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('dashboard')
