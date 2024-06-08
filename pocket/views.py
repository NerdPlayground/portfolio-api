from datetime import date,datetime
    
def get_date_object(date_string):
    date_format="%Y-%m-%d"
    return datetime.strptime(date_string,date_format).date()

def project_status(request):
    ongoing=request.data.get('ongoing')
    if ongoing: return (True,None)
    today=date.today()
    end_date=get_date_object(request.data.get('end_date'))
    return (True,None) if end_date>today else (False,end_date)