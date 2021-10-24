import os

from django.shortcuts import render, redirect
from django.views.generic import View
from .models import PDFile
from django.utils import timezone
from .forms import get_pdf_multiple, merge_form, get_pdf_single, rotation, delete_form, range_of_list
from django.views.generic.edit import FormView
from django.core.files import File
from django.core.files.storage import default_storage
from .editings import rotate, toZIP, delete
from django.conf import settings
import random, string
from pdf2image import convert_from_path
import os
from PIL import Image
import PyPDF2



def create_random_str(size: int):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


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
        return redirect('next/')


class SplitNext(View):

    def get_pages_num(self, path):
        with open(path.file.path, 'rb') as file:
            a = PyPDF2.PdfFileReader(file)
            return a.getNumPages()

    def get(self, request):
        pdf = PDFile.objects.all().last()
        num_of_pages = self.get_pages_num(pdf)
        form = range_of_list(initial={'first': 1, 'last': num_of_pages})
        data = {
            'form': form,
        }
        return render(request, 'splitnext.html', data)

    def post(self, request):
        form = range_of_list(request.POST)
        first_list = request.POST.getlist('first')
        last_list = request.POST.getlist('last')
        split_ranges = []
        if form.is_valid():
            for i in range(len(first_list)):
                split_ranges.append([first_list[i], last_list[i]])
        print(split_ranges)
        return redirect('/')



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
            c = 0
            pages_to_delete = []
            for b in to_delete:
                if b == "true":
                    pages_to_delete.append(c)
                c += 1

            pdf = PDFile.objects.all().last()
            out_path = f"{settings.MEDIA_URL_RESULTS}/deleted_{create_random_str(10)}.pdf"

            print(pages_to_delete)
            delete.PDFdelete(pdf.file.path, pages_to_delete, out_path)
            return redirect(f"../../uploaded/results/{os.path.basename(out_path)}")


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
