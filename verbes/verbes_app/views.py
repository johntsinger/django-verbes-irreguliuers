from random import sample
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from verbes_app.functions import get_results, verify_answer
from verbes_app.models import Verbe, Table
from verbes_app.forms import TableForm, VerbeForm


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
    # creates a json dict of object Verbe with selected fields
    verbes = serializers.serialize('json', Verbe.objects.all(),
        fields=('done', 'success'))
    if request.method == "POST":
        # Button envoyer
        if 'envoyer' in request.POST:
            form = TableForm(request.POST)
            if form.is_valid():
                table = form.save()
                return redirect('table-detail', table.id)
        # Button annuler
        else:
            return redirect('table-list')
    else:
        form = TableForm()

    return render(request,
        'verbes_app/table_create.html',
        {'form': form, 'verbes': verbes})

def table_update(request, table_id):
    # creates a json dict of object Verbe with selected fields
    verbes = serializers.serialize('json', Verbe.objects.all(),
        fields=('done', 'success'))
    table = Table.objects.get(id=table_id)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if 'envoyer' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('table-detail', table.id)
        else:
            return redirect('table-list')
    else:
        form = TableForm(instance=table)  

    return render(request,
        'verbes_app/table_update.html',
        {'form': form, 'verbes': verbes})

def table_delete(request, table_id):
    table = Table.objects.get(id=table_id)
    if request.method == 'POST':
        if 'supprimer' in request.POST:
            table.delete()
            return redirect('table-list')
        else:
            return redirect('table-list')

    return render(request,
        'verbes_app/table_delete.html',
        {'table': table})

def exercise(request, table_id):
    table = Table.objects.get(id=table_id)
    # gets 10 random items of table.verbes
    verbes_list = list(table.verbes.all())
    verbes = sample(verbes_list, 10 if len(verbes_list) >= 10 else len(verbes_list))
    # creates list of verbes id
    # used in the hidden input to get it in request.POST
    verbes_id = [verbe.id for verbe in verbes]
    form = VerbeForm()
                 
    return render(request,
        "verbes_app/exercise.html",
        {"table": table, "verbes": verbes, "form": form, 
        'verbes_id': verbes_id})

def exercise_result(request, table_id):
    # creates the dictionary of results
    results = get_results(request)
    # gets the correction (dict of booleans)
    correction = verify_answer(results)
    # set n to pass it to the context to creates a range object
    # needed to creates 10 rows in the template
    n = len(results['verbes'])

    # modifies done and success attributes of verb object
    # saves the modification in the db
    for i, verbe in enumerate(results['verbes']):
        verbe.done = True
        verbe.success = correction[i][3]
        verbe.save()

    return render(request,
        "verbes_app/exercise_result.html",
        {'results': results, 'n': range(n), 'correction': correction,
         'table_id': table_id})
