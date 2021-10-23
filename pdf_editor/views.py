from django.shortcuts import render, redirect
from django.views.generic import View
from .models import PDFile
from django.utils import timezone
from .forms import get_pdf_multiple, merge_form
from django.views.generic.edit import FormView
from django.core.files import File
from django.core.files.storage import default_storage


def main(request):
    return render(request, 'main.html')


class Merge(FormView):
    form_class = get_pdf_multiple
    template_name = 'merge.html'
    success_url = '#'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                file_instance = PDFile(file=f)
                file_instance.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class Split(View):
    def get(self, request):
        form = get_pdf_multiple()
        return render(request, 'split.html')

    def post(self, request):
        form = get_pdf_multiple(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'split.html', {'form': form})


class Rotate(View):
    def get(self, request):
        form = get_pdf_multiple()
        return render(request, 'rotate.html')

    def post(self, request):
        form = get_pdf_multiple(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'rotate.html', {'form': form})


class Delete(View):
    def get(self, request):
        form = get_pdf_multiple()
        return render(request, 'delete.html')

    def post(self, request):
        form = get_pdf_multiple(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'delete.html', {'form': form})


class Convert(View):
    def get(self, request):
        form = get_pdf_multiple()
        return render(request, 'convert.html')

    def post(self, request):
        form = get_pdf_multiple(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'convert.html', {'form': form})
