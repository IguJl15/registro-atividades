
from records.models import Record
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin



class RecordCreateView(CreateView, LoginRequiredMixin):
    model = Record
    fields = ['description', 'date', 'start','end'  ]


class RecordListView(ListView, LoginRequiredMixin):
    model = Record
