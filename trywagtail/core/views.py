from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from . import models


def home(request):
    return render(request, 'core/home.html', {
        'images': models.Image.objects.all(),
    })


def use_image(request, image_id):
    image = get_object_or_404(models.Image, id=image_id)

    if request.method == 'POST':
        container = image.create_container()
        container.start()

        return redirect(container.url())

    return render(request, 'core/use.html', {
        'image': image,
    })
