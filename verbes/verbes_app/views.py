from random import sample
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from verbes_app.functions import get_results, verify_answer
from verbes_app.models import Verbe, Table, UserTable, UserProfile, UserVerbe
from verbes_app.forms import TableForm, VerbeForm


def verbe_list(request):

    return render(request,
        "verbes_app/verbe_list.html",
        )

@login_required
def reset_all(request):
    user_profile = UserProfile.objects.get(user=request.user)
    verbes = UserVerbe.objects.filter(user_profile=user_profile)
    if request.method == 'POST':
        if 'envoyer' in request.POST:
            for verbe in verbes.filter(done=True):
                verbe.done = False
                verbe.success = False
                verbe.save()
        return redirect('verbe-list')

    return render(request,
        'verbes_app/reset_all.html')

def table_detail(request, table_id):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        table = user_profile.tables.get(id=table_id)
        user_table = UserTable.objects.filter(user_profile=user_profile, table=table)
    else:
        table = Table.objects.get(id=table_id)
        user_table = table.verbes.all()

    return render(request,
        "verbes_app/table_detail.html",
        {"table": table, "user_table": user_table})

def table_list(request):
    
    return render(request,
        "verbes_app/table_list.html",
        )

@login_required
def table_create(request):
    # creates a json dict of object Verbe with selected fields
    verbes = serializers.serialize('json', Verbe.objects.all())
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        # Button envoyer
        if 'envoyer' in request.POST:
            form = TableForm(request.POST)
            if form.is_valid():
                table = form.save()
                user_profile.tables.add(table)
                return redirect('table-detail', table.id)
        # Button annuler
        else:
            return redirect('table-list')
    else:
        form = TableForm()

    return render(request,
        'verbes_app/table_create.html',
        {'form': form, 'verbes': verbes})

@login_required
def table_update(request, table_id):
    # creates a json dict of object Verbe with selected fields
    verbes = serializers.serialize('json', Verbe.objects.all())
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

@login_required
def table_delete(request, table_id):
    table = Table.objects.get(id=table_id)
    if request.method == 'POST':
        if 'envoyer' in request.POST:
            table.delete()

        return redirect('table-list')

    return render(request,
        'verbes_app/table_delete.html',
        {'table': table})

@login_required
def table_reset(request, table_id):
    user_profile = UserProfile.objects.get(user=request.user)
    table = Table.objects.get(id=table_id)
    user_tables = UserTable.objects.filter(user_profile=user_profile, table=table)
    if request.method == 'POST':
        if 'envoyer' in request.POST:
            for user_table in user_tables.filter(done=True):
                user_table.done = False
                user_table.success = False
                user_table.save()
        return redirect('table-detail', table_id)

    return render(request,
        'verbes_app/table_reset.html',
        {'table': table})

@login_required
def exercise(request, table_id):
    user = UserProfile.objects.get(user=request.user)
    table = user.tables.get(id=table_id)
    # gets 10 random items of table.verbes
    verbes_list = list(table.verbes.all())
    verbes = sample(verbes_list,
        10 if len(verbes_list) >= 10 else len(verbes_list))
    # creates list of verbes id
    # used in the hidden input to get it in request.POST
    verbes_id = [verbe.id for verbe in verbes]
    form = VerbeForm()

    return render(request,
        "verbes_app/exercise.html",
        {"table": table, "verbes": verbes, "form": form, 
        'verbes_id': verbes_id})

@login_required
def exercise_result(request, table_id):
    user = UserProfile.objects.get(user=request.user)
    table = user.tables.get(id=table_id)
    # creates the dictionary of results
    results = get_results(request, table, user)
    # gets the correction (dict of booleans)
    correction = verify_answer(results)
    # modifies done and success attributes of UserTable object
    # and modifies done and success attributes of UserVerbe object
    # saves the modification in the db
    for i, user_table in enumerate(results['verbes']):
        # get the UserVerbe object
        verbe = UserVerbe.objects.get(verbe=user_table.verbe, user_profile=user)
        # modifies the UserTable object done attribute
        user_table.done = True
        # modifies the UserVerbe object done attribute
        verbe.done = True
        user_table.success = correction[i][3]
        verbe.success = correction[i][3]
        user_table.save()
        verbe.save()

    return render(request,
        "verbes_app/exercise_result.html",
        {'results': results, 'correction': correction,
         'table_id': table_id, 'table': table})
