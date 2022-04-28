from django.shortcuts import render
<<<<<<< Updated upstream
from verbes_app.models import Verbe

=======
<<<<<<< Updated upstream

# Create your views here.
=======
from verbes_app.models import Verbe, Table

>>>>>>> Stashed changes

def verbe_list(request):
    verbes = Verbe.objects.all()
    return render(request,
        "verbes_app/verbe_list.html",
        {"verbes": verbes})
<<<<<<< Updated upstream
=======

def table_detail(request, table_id):
    table = Table.objects.get(id=table_id)
    return render(request,
        "verbes_app/table_detail.html",
        {"table": table})

def table_list(request):
    tables = Table.objects.all()
    return render(request,
        "verbes_app/table_list.html",
        {"tables": tables})
>>>>>>> Stashed changes
>>>>>>> Stashed changes
