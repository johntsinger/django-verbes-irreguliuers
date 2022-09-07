import json
from verbes_app.models import Verbe, UserTable


def get_results(request, table, user):
    """Creates dictionary with the querydict send by request.POST"""
    results = {}
    exclude = ["csrfmiddlewaretoken", "done", "success"]
    # creates a dict with the request.POST
    for key, value in request.POST.items():
        if key == 'verbes_id':
            # converts the json string list to list
            verbes_id = json.loads(request.POST.get('verbes_id'))
            verbes = []
            for verbe_id in verbes_id:
                user_table = UserTable.objects.get(user_profile=user, verbe__id=verbe_id, table=table)
                verbes.append(user_table)
            results['verbes'] = verbes
        else:
            if key not in exclude:
                # getlist to gets all values send by the form
                # otherwise with get, get only the last
                result = request.POST.getlist(key)
                for i, value in enumerate(result):
                    if value:
                        result[i] = value.strip().lower()
                    else:
                        result[i] = '---'
                results[key] = result

    return results

def verify_answer(results):
    """Verify user answers"""
    # set default value True for each verbs tense for each verbs objects
    correction = [[True, True, True] for i in range(len(results['verbes']))]
    # set correction's value to False if it doesn't match with the verblist 
    # object's value
    for i, verbelist_object in enumerate(results['verbes']):
        if verbelist_object.verbe.present != results['present'][i]:
            correction[i][0] = False
        # split the verb if it has two forms
        if '/' in verbelist_object.verbe.preterit:
            preterit = verbelist_object.verbe.preterit.split('/')
            if preterit[0] != results['preterit'][i] and \
                    preterit[1] != results['preterit'][i]:
                correction[i][1] = False
        else:
            if verbelist_object.verbe.preterit != results['preterit'][i]:
                correction[i][1] = False
        if '/' in verbelist_object.verbe.participe_passe:
            participe_passe = verbelist_object.verbe.participe_passe.split('/')
            if participe_passe[0] != results['participe_passe'][i] and \
                    participe_passe[1] != results['participe_passe'][i]:
                correction[i][2] = False
        else:
            if verbelist_object.verbe.participe_passe != \
                    results['participe_passe'][i]:
                correction[i][2] = False

        # append a 4th value to correction 
        # if correction has one False value set the value to False otherwise
        # set it to True
        correction[i].append(correction[i][0] and correction[i][1] and
                             correction[i][2])

    return correction
