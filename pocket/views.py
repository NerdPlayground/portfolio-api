from datetime import date,datetime
from django.shortcuts import render

def project_status(request):
    end_date=request.POST.get('end_date')
    if end_date=='': return (True,None)
    date_format="%Y-%m-%d"
    today=date.today()
    datestamp=datetime.strptime(end_date,date_format).date()
    return (True,None) if datestamp>today else (False,end_date)