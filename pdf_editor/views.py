from django.shortcuts import render, redirect
from django.views.generic import View
from .models import PDFile
from django.utils import timezone
from .forms import get_pdf_multiple, merge_form
from django.views.generic.edit import FormView
from django.core.files import File


def main(request):
    return render(request, 'main.html')


class Merge(FormView):
    # def get(self, request):
    #     if PDFile.objects.all().count == 0:
    #         form = get_pdf_multiple()
    #     else:
    #         num_of_files = PDFile.objects.all().count
    #         form = merge_form(num_of_files)
    #
    #     return render(request, 'merge.html')
    form_class = get_pdf_multiple
    template_name = 'merge.html'

    def post(self, request, *args, **kwargs):
        if PDFile.objects.all().count == 0:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            files = request.FILES.getlist('file')
            if form.is_valid():
                for f in files:
                    new_file = PDFile()
                    new_file.file = File(f)
                    new_file.save()
        else:
            num_of_files = PDFile.objects.all().count
            form = merge_form(num_of_files)
            # if form.is_valid():
            #     for f in files:
            #         ...  # Do something with each file.
            #     return self.form_valid(form)
            # else:
            #     return self.form_invalid(form)
        data = {
            'num_of_files': num_of_files,
            'form': form,
        }
        return render(request, 'merge.html', data)


class Split(View):
    def get(self, request):
        form = get_pdf()
        return render(request, 'split.html')

    def post(self, request):
        form = get_pdf()
        return render(request, 'split.html')


class Rotate(View):
    def get(self, request):
        form = get_pdf()
        return render(request, 'rotate.html')

    def post(self, request):
        form = get_pdf()
        return render(request, 'rotate.html')


class Delete(View):
    def get(self, request):
        form = get_pdf()
        return render(request, 'delete.html')

    def post(self, request):
        form = get_pdf()
        return render(request, 'delete.html')


class Convert(View):
    def get(self, request):
        form = get_pdf()
        return render(request, 'convert.html')

    def post(self, request):
        form = get_pdf()
        return render(request, 'convert.html')