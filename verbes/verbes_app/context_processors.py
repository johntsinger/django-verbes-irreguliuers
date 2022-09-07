from verbes_app.models import Table, UserProfile, Verbe, UserVerbe, UserTable


def tables(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        tables = user_profile.tables.all()
    else:
        tables = Table.objects.filter(default=True)
    
    return {'tables': tables}

def verbes(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        verbes = UserVerbe.objects.filter(user_profile=user_profile)
    else:
        verbes = Verbe.objects.all()
    
    return {'verbes': verbes}