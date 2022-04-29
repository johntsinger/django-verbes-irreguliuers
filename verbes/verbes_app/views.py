from django.shortcuts import render
from verbes_app.models import Verbe, Table
from verbes_app.forms import TableForm
from django.shortcuts import redirect


def verbe_list(request):
    verbes = Verbe.objects.all()
    return render(request,
        "verbes_app/verbe_list.html",
        {"verbes": verbes})

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

def table_create(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save()
            return redirect('table-detail', table.id)
    else:
        form = TableForm()

    return render(request,
        'verbes_app/table_create.html',
        {'form': form})