from django.shortcuts import render
from records.models import Record
from django.views.generic import CreateView, ListView


class RecordCreateView(CreateView):
    model = Record
    fields = ['description', 'date', 'start','end'  ]

class RecordListView(ListView):
    model = Record
