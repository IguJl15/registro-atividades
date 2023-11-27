
from records.models import Record
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    fields = ['description', 'date', 'start','end']


class RecordListView(LoginRequiredMixin, ListView):
    model = Record
