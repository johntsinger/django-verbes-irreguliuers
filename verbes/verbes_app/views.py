from random import sample
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from verbes_app.functions import get_results, verify_answer
from verbes_app.models import Verbe, Table, UserTable, UserProfile, UserVerbe
from verbes_app.forms import (TableForm, VerbeForm, ResetAllForm,
    ResetListForm, DeleteListForm)


def verbe_list(request):
    reset_all_form = ResetAllForm()
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        user_verbes = UserVerbe.objects.filter(user_profile=user_profile)
        user_tables = UserTable.objects.filter(user_profile=user_profile)
        if request.method == 'POST':
            if 'reset-all' in request.POST:
                user_verbes.filter(done=True).update(done=False, success=False)
                user_tables.filter(done=True).update(done=False, success=False)
            return redirect('verbe-list')

    return render(request,
        "verbes_app/verbe_list.html",
        {'reset_all_form': reset_all_form})

def table_detail(request, table_id):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        table = user_profile.tables.get(id=table_id)
        user_table = UserTable.objects.filter(user_profile=user_profile,
            table=table)
        reset_list_form = ResetListForm(user=request.user, table_id=table_id)
        delete_list_form = DeleteListForm(user=request.user, table_id=table_id)
        context = {"table": table, "user_table": user_table,
            'reset_list_form': reset_list_form,
            'delete_list_form': delete_list_form}
        if request.method == 'POST':
            if 'reset' in request.POST:
                user_table.filter(done=True).update(done=False, success=False)
                return redirect('table-detail', table_id)
            if 'delete' in request.POST:
                table.delete()
                return redirect('table-list')
    else:
        table = Table.objects.get(id=table_id)
        user_table = table.verbes.all()
        context = {"table": table, "user_table": user_table}

    return render(request,
        "verbes_app/table_detail.html",
        context)

def table_list(request):
    if request.method == 'POST':
        if 'delete' in request.POST:
            user_profile = UserProfile.objects.get(user=request.user)
            table_id = request.POST['table-id']
            table = user_profile.tables.get(id=table_id)
            table.delete()
            return redirect('table-list')
    else:
        delete_list_form = DeleteListForm()
    
    return render(request,
        "verbes_app/table_list.html",
        {'delete_list_form': delete_list_form})

@login_required
def table_create(request):
    # creates a json dict of object Verbe with selected fields
    user_profile = UserProfile.objects.get(user=request.user)
    # Added verbe field to sort verbes in SelectBoxModified.js necessary not
    # to have an index shift when assigning the success and unsuccess classes
    # if the UserVerbes objects inside UserProfile have been modified
    verbes = serializers.serialize('json',
        UserVerbe.objects.filter(user_profile=user_profile),
        fields=('verbe', 'done', 'success'))
    if request.method == "POST":
        # Button envoyer
        if 'envoyer' in request.POST:
            form = TableForm(request.POST)
            if form.is_valid():
                # Check if table's name is already used
                for table in user_profile.tables.all():
                    if form.cleaned_data['name'] in table.name:
                        messages.error(request,
                            'This name is already used ! Please choose another one.')
                        return render(request,
                            'verbes_app/table_create.html',
                            {'form': form, 'verbes': verbes})
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
    user_profile = UserProfile.objects.get(user=request.user)
    table = Table.objects.get(id=table_id)
    verbe_in_table = table.verbes.all()
    # Added verbe field to sort verbes in SelectBoxModified.js necessary not
    # to have an index shift when assigning the success and unsuccess classes
    # if the UserVerbes objects inside UserProfile have been modified
    verbes = serializers.serialize('json',
        UserVerbe.objects.filter(user_profile=user_profile),
        fields=('verbe', 'done', 'success')) # verbe' value is 1 to 282
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
        {'form': form, 'verbes': verbes, 'table': table})

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
        verbe = UserVerbe.objects.get(verbe=user_table.verbe,
            user_profile=user)
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
