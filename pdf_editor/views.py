import os

from django.shortcuts import render, redirect
from django.views.generic import View
from .models import PDFile, Images
from django.utils import timezone
from .forms import get_pdf_multiple, merge_form, get_pdf_single, rotation, delete_form, range_of_list, convert_setup
from django.views.generic.edit import FormView
from django.core.files import File
from django.core.files.storage import default_storage
from .editings import rotate, toZIP, delete, split, merge
from django.conf import settings
import random, string
from pdf2image import convert_from_path
import os
import PyPDF2
from PIL import Image


def create_random_str(size: int):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(size))


def get_file_name_without_extension(full_name):
    return os.path.splitext(full_name)[0]


def get_file_name_with_extension(full_name):
    return os.path.basename(full_name)


def get_only_file_name_without_extension(full_name):
    return get_file_name_without_extension(get_file_name_with_extension(full_name))


def save_thumbnails(pdfs):
    for pdf in pdfs:
        pages = convert_from_path(pdf.file.path)
        c = 0
        pdf_name = get_file_name_without_extension(pdf.file.path)
        for page in pages:
            _name = f"{pdf_name}_{c}.jpg"
            page.save(_name, 'JPEG')
            c += 1
            new_image = Images()
            new_image.image = _name
            new_image.save()
            pdf.images.add(new_image)
            pdf.save()


def get_images_and_orientations(pdf):
    images = []
    orientation = []
    for image in pdf.images.all():
        images.append(get_file_name_with_extension(image.image.path))
        orientation.append(get_orientation(image.image.path))
    return images, orientation


def get_first_image_and_orientation(pdf):
    images = []
    orientation = []
    for image in pdf.images.all():
        images.append(get_file_name_with_extension(image.image.path))
        orientation.append(get_orientation(image.image.path))
        break  # как тут по-другому сделать?
    return images[0], orientation[0]


def get_page_count(pdf) -> int:
    infile = PyPDF2.PdfFileReader(pdf.file.path)
    return infile.getNumPages()


def main(request):
    PDFile.objects.all().delete()
    return render(request, 'main.html')


class Merge(FormView):
    form_class = get_pdf_multiple
    template_name = 'merge.html'
    success_url = '/merge/setup'
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
                save_thumbnails([pdf])
                i += 1

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def get_orientation(filepath):
    with Image.open(filepath) as img:
        width, height = img.size
    if width > height:
        return 'L'
    return 'P'


class MergeSetup(View):
    def get(self, request):
        form = merge_form(initial={'order': 1})
        num_of_pdfs = PDFile.objects.all()

        first_images = []
        orientation = []
        for pdf in num_of_pdfs:
            _images, _orientation = get_first_image_and_orientation(pdf)
            first_images.append(_images)
            orientation.append(_orientation)

        num_and_image_and_orientation = zip(num_of_pdfs, first_images, orientation)
        data = {
            'form': form,
            'num_and_image_and_orientation': num_and_image_and_orientation,
        }
        return render(request, 'merge_setup.html', data)

    def post(self, request):
        files = PDFile.objects.all()
        num_of_pdfs = files
        form = merge_form(request.POST)
        nums = request.POST.getlist('order')  # последовательность
        merge_list = []
        files_list = files.order_by('id')
        i = 0
        if form.is_valid():
            for n in nums:
                merge_list.append([files_list[i].file.path, int(n)])
                i += 1
            out_path = f"{settings.MEDIA_URL_RESULTS}/merged_{create_random_str(10)}.pdf"
            merge.PDFmerge(merge_list, out_path)

        # data = {
        #     'form': form,
        #     'num_of_pdfs': num_of_pdfs,
        #     'files': files,
        # }
        return redirect(f"../../uploaded/results/{os.path.basename(out_path)}")


class Split(View):
    def get(self, request):
        form = get_pdf_single()
        return render(request, 'split.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        pdf = PDFile.objects.all().last()
        save_thumbnails([pdf])
        return redirect('setup/')


class SplitSetup(View):

    def get_pages_num(self, path):
        with open(path.file.path, 'rb') as file:
            a = PyPDF2.PdfFileReader(file)
            return a.getNumPages()

    def get(self, request):
        pdf = PDFile.objects.all().last()
        num_of_pages = self.get_pages_num(pdf)
        form = range_of_list(initial={'first': 1, 'last': num_of_pages})

        images, orientation = get_images_and_orientations(pdf)

        images_and_orientation = zip(images, orientation)

        data = {
            'form': form,
            'images_and_orientation': images_and_orientation,
        }
        return render(request, 'split_setup.html', data)

    def post(self, request):
        form = range_of_list(request.POST)
        first_list = request.POST.getlist('first')
        last_list = request.POST.getlist('last')
        split_ranges = []
        if form.is_valid():
            for i in range(len(first_list)):
                split_ranges.append([int(first_list[i]) - 1, int(last_list[i]) - 1])

        pdf = PDFile.objects.all().last()
        out_path = f"{settings.MEDIA_URL_RESULTS}/splited_{create_random_str(10)}.zip"
        split.PDFsplit(pdf.file.path, split_ranges, "pdf_{}.pdf", out_path)
        return redirect(f"../../uploaded/results/{os.path.basename(out_path)}")


class Rotate(View):
    def get(self, request):
        form = get_pdf_single()

        return render(request, 'rotate.html', {'form': form})

    def post(self, request):
        form = get_pdf_single(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        pdf = PDFile.objects.all().last()
        save_thumbnails([pdf])
        return redirect('setup/')


class RotateSetup(View):
    def get(self, request):
        form = rotation()
        return render(request, 'rotate_setup.html', {'form': form})

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
        pdf = PDFile.objects.all().last()
        save_thumbnails([pdf])
        return redirect('setup/')


class DeleteSetup(View):
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

        images, orientation = get_images_and_orientations(pdf)

        num_and_images_and_orientation = zip(list, images, orientation)
        data = {
            'form': form,
            'num_and_images_and_orientation': num_and_images_and_orientation,
        }
        return render(request, 'delete_setup.html', data)

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
        pdf = PDFile.objects.all().last()
        save_thumbnails([pdf])
        return redirect('setup/')


class ConvertSetup(View):
    def get(self, request):
        pdf = PDFile.objects.all().last()
        image, orientation = get_first_image_and_orientation(pdf)

        form = convert_setup(initial={'compresslevel': 5, 'name': f"{get_only_file_name_without_extension(pdf.file.path)}_jpgs.zip"})
        data = {
            'form': form,
            'image': image,
            'orientation': orientation,
            'file_name': get_file_name_with_extension(pdf.file.path),
            'page_count': get_page_count(pdf),
        }
        return render(request, 'convert_setup.html', data)


    def post(self, request):
        form = convert_setup(request.POST)
        if form.is_valid():
            result_name = request.POST.get('name')
            compresslevel = int(request.POST.get('compresslevel')) - 1

            pdf = PDFile.objects.all().last()
            out_path = f"{settings.MEDIA_URL_RESULTS}/{result_name}"
            toZIP.PDFtoZIP(pdf.file.path, "page_{}", out_path, compresslevel)

            data = {
                'result_url': f"../../uploaded/results/{result_name}",
            }
            return render(request, 'convert_ready.html', data)
