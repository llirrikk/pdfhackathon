import os

from django.shortcuts import render, redirect
from django.views.generic import View
from .models import PDFile
from django.utils import timezone
from .forms import get_pdf_multiple, merge_form, get_pdf_single, rotation
from django.views.generic.edit import FormView
from django.core.files import File
from django.core.files.storage import default_storage
from .editings import rotate, toZIP
from django.conf import settings
import random, string


def create_random_str(size: int):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


def main(request):
    return render(request, 'main.html')


class Merge(FormView):
    form_class = get_pdf_multiple
    template_name = 'merge.html'
    success_url = '/merge/next'

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


class MergeNext(View):
    def get(self, request):
        form = merge_form()
        num_of_pdfs = PDFile.objects.all()
        data = {
            'form': form,
            'num_of_pdfs': num_of_pdfs
        }
        return render(request, 'mergenext.html', data)

    def post(self, request):
        num_of_pdfs = PDFile.objects.all()
        form = merge_form(request.POST)
        nums = request.POST.getlist('order')
        if form.is_valid():
            for n in nums:
                print(n)
        data = {
            'form': form,
            'num_of_pdfs': num_of_pdfs
        }
        return render(request, 'mergenext.html', data)


class Split(View):
    def get(self, request):
        form = get_pdf_single()
        return render(request, 'split.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'split.html', {'form': form})


class Rotate(View):
    def get(self, request):
        form = get_pdf_single()

        return render(request, 'rotate.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('next/')


class RotateNext(View):
    def get(self, request):
        form = rotation()
        return render(request, 'rotate.html', {'form': form})

    def post(self, request):
        form = rotation(request.POST)
        if form.is_valid():
            pdf = PDFile.objects.all().last()
            out_path = f"{settings.MEDIA_URL_RESULTS}/rotated_{create_random_str(10)}.pdf"
            rotate.PDFrotate(pdf.file.path, form.cleaned_data.get('angle'), out_path)

            return redirect(f"../../uploaded/results/{os.path.basename(out_path)}")




class Delete(View):
    def get(self, request):
        form = get_pdf_single()
        return render(request, 'delete.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'delete.html', {'form': form})


class Convert(View):
    def get(self, request):
        form = get_pdf_single()
        return render(request, 'convert.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('next/')


class ConvertNext(View):
    def get(self, request):
        pdf = PDFile.objects.all().last()
        out_path = f"{settings.MEDIA_URL_RESULTS}/zip_{create_random_str(10)}.zip"
        toZIP.PDFtoZIP(pdf.file.path, "page_{}", out_path)

        return redirect(f"../../uploaded/results/{os.path.basename(out_path)}")
