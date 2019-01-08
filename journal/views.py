# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic

from braces.views import LoginRequiredMixin

from .models import JournalEntry
from .forms import JournalEntryForm


class JournalCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a journal entry.
    """
    template_name = 'journal/entry_create.html'
    model = JournalEntry
    form_class = JournalEntryForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('journal_list',
                       kwargs={'username': self.request.user.username})


class JournalDetailView(LoginRequiredMixin, generic.DetailView):
    """
    View for details of a journal entry.
    """
    template_name = 'journal/entry_detail.html'
    model = JournalEntry
    context_object_name = 'entry'


class JournalListView(LoginRequiredMixin, generic.ListView):
    """
    View a list of recent journal entries.
    """
    template_name = 'journal/entry_list.html'
    model = JournalEntry
    context_object_name = 'entries'

    def get_queryset(self):
        return (JournalEntry.objects.filter(author=self.request.user)
                                    .order_by('-date'))
