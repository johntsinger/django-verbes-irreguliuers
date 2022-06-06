from verbes_app.models import Table

def tables(request):
    tables = Table.objects.all()
    return {'tables': tables}