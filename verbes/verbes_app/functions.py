import json
from verbes_app.models import Verbe


def get_results(request):
    """Creates dictionary with the querydict send by request.POST"""
    results = {}
    exclude = ["csrfmiddlewaretoken", "done", "success"]
    # creates a dict with the request.POST
    for key, value in request.POST.items():
        if key == 'verbes_id':
            # converts the json string list to list
            verbes_id = json.loads(request.POST.get('verbes_id'))
            verbes = []
            # for id in list get the verbe 
            for verbe_id in verbes_id:
                verbe = Verbe.objects.get(id=verbe_id)
                verbes.append(verbe)
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
    # set correction's value to False if it doesn't match with the verb's value
    for i, verbe in enumerate(results['verbes']):
        if verbe.present != results['present'][i]:
            correction[i][0] = False
        # split the verb if it has two forms
        if '/' in verbe.preterit:
            preterit = verbe.preterit.split('/')
            if preterit[0] != results['preterit'][i] and \
                    preterit[1] != results['preterit'][i]:
                correction[i][1] = False
        else:
            if verbe.preterit != results['preterit'][i]:
                correction[i][1] = False
        if '/' in verbe.participe_passe:
            participe_passe = verbe.participe_passe.split('/')
            if participe_passe[0] != results['participe_passe'][i] and \
                    participe_passe[1] != results['participe_passe'][i]:
                correction[i][2] = False
        else:
            if verbe.participe_passe != results['participe_passe'][i]:
                correction[i][2] = False

        # append a 4th value to correction 
        # if correction has one False value set the value to False otherwise
        # set it to True
        correction[i].append(correction[i][0] and correction[i][1] and
                             correction[i][2])

    return correction
