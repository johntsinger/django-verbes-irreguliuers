from random import sample
from django.shortcuts import render
from django.shortcuts import redirect
from verbes_app.functions import get_results, verify_answer
from verbes_app.models import Verbe, Table
from verbes_app.forms import TableForm, VerbeForm


def verbe_list(request):
    verbes = Verbe.objects.all()
    verbes_tested = Verbe.objects.filter(done=True).count()
    verbes_success = Verbe.objects.filter(success=True).count()
    verbes_not_tested = verbes.count() - verbes_tested

    return render(request,
        "verbes_app/verbe_list.html",
        {"verbes": verbes, 'verbes_tested': verbes_tested,
         'verbes_success': verbes_success,
         'verbes_not_tested': verbes_not_tested})

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
        {'form': form})

def exercise(request, table_id):
    table = Table.objects.get(id=table_id)
    # gets 10 random items of table.verbes
    verbes_list = list(table.verbes.all())
    verbes = sample(verbes_list, 10)
    # creates list of verbes id, need to pass it to context to get it in request.POST
    verbes_id = [verbe.id for verbe in verbes]
    form = VerbeForm()
                 
    return render(request,
        "verbes_app/exercise.html",
        {"table": table, "verbes": verbes, "form": form, 
        'verbes_id': verbes_id})

def exercise_result(request, table_id): 
    results = get_results(request)
    correction = verify_answer(results)
    n = len(results['verbes'])

    for i, verbe in enumerate(results['verbes']):
        verbe.done = True
        verbe.success = correction[i][3]
        verbe.save()

    return render(request,
        "verbes_app/exercise_result.html",
        {'results': results, 'n': range(n), 'correction': correction})
