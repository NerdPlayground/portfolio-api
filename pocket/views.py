from datetime import date,datetime
    
def get_date_object(date_string):
    date_format="%Y-%m-%d"
    return datetime.strptime(date_string,date_format).date()

def project_status(request):
    end_date=request.data.get('end_date')
    if end_date=='': return (True,None)
    today=date.today()
    datestamp=get_date_object(end_date)
    return (True,None) if datestamp>today else (False,end_date)