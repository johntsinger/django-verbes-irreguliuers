from django.shortcuts import render
from verbes_app.models import Verbe


def verbe_list(request):
    verbes = Verbe.objects.all()
    return render(request,
        "verbes_app/verbe_list.html",
        {"verbes": verbes})
