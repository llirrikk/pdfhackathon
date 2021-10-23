from django.shortcuts import render, redirect
from django.views.generic import View
from .models import PDFile
from django.utils import timezone
from .forms import get_pdf_multiple, merge_form, get_pdf_single, delete_form
from django.views.generic.edit import FormView
from django.core.files import File
from django.core.files.storage import default_storage
from pdf2image import convert_from_path
import os
from PIL import Image
import PyPDF2


def main(request):
    return render(request, 'main.html')


class Merge(FormView):
    def PDFtoImages(pdf, output_nameN):
        def get_file_name_without_extension(full_name):
            return os.path.splitext(output_nameN)[0]

        pages = convert_from_path(pdf)
        pdf_name_without_extension = get_file_name_without_extension(output_nameN)

        output_names = []
        images = []
        c = 0
        for page in pages:
            _name = f'../media/images/{pdf_name_without_extension.format(c)}.jpg'
            output_names.append(_name)
            page.save(_name, 'JPEG')

            _i = Image.open(_name)
            images.append(_i)
            c += 1
        return images


    form_class = get_pdf_multiple
    template_name = 'merge.html'
    success_url = '/merge/next'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        i = 0
        if form.is_valid():
            for f in files:
                file_instance = PDFile(file=f, number=i)
                file_instance.save()

                pdf = PDFile.objects.all().last()

                pages = convert_from_path(pdf)
                c = 0
                for page in pages:
                    _name = f'../media/images/{pdf}_{c}.jpg'
                    page.save(_name, 'JPEG')
                    c += 1

                i += 1

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MergeNext(View):
    def get(self, request):
        form = merge_form()
        num_of_pdfs = PDFile.objects.all()
        data = {
            'form': form,
            'num_of_pdfs': num_of_pdfs,
        }
        return render(request, 'mergenext.html', data)

    def post(self, request):
        files = PDFile.objects.all()
        num_of_pdfs = PDFile.objects.all()
        form = merge_form(request.POST)
        nums = request.POST.getlist('order')  # последовательность
        if form.is_valid():
            for n in nums:
                print(n)
        data = {
            'form': form,
            'num_of_pdfs': num_of_pdfs,
            'files': files,
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
        return render(request, 'rotate.html', {'form': form})


class Delete(View):
    def get(self, request):
        form = get_pdf_single()
        return render(request, 'delete.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('next/')


class DeleteNext(View):
    def get_pages_num(self, path):
        with open(path.file.path, 'rb') as file:
            a = PyPDF2.PdfFileReader(file)
            return a.getNumPages()


    def get(self, request):
        form = delete_form(initial={'to_delete': False})
        pdf = PDFile.objects.all().last()
        num_of_pages = self.get_pages_num(pdf)
        list = []
        for i in range(num_of_pages):
            list.append(i)
        data = {
            'form': form,
            'num_of_pages': list,
        }
        return render(request, 'deletenext.html', data)

    def post(self, request):
        form = delete_form(request.POST)
        to_delete = request.POST.getlist('to_delete')
        if form.is_valid():
            for i in to_delete:
                print(i, " <<<")
        return render(request, 'deletenext.html', {'form': form})


class Convert(View):
    def get(self, request):
        form = get_pdf_single()
        return render(request, 'convert.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, 'convert.html', {'form': form})
