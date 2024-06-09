from django.urls import reverse
from datetime import date,datetime
from allauth.account.adapter import DefaultAccountAdapter
    
def get_date_object(date_string):
    date_format="%Y-%m-%d"
    return datetime.strptime(date_string,date_format).date()

def project_status(request):
    ongoing=request.data.get('ongoing')
    if ongoing: return (True,None)
    today=date.today()
    end_date=get_date_object(request.data.get('end_date'))
    return (True,None) if end_date>today else (False,end_date)

class PortfolioAPIAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        confirm_email_url=reverse("account_confirm_email",kwargs={"key":context.get("key")})
        url_header=context.get("activate_url").split(confirm_email_url)[0]
        verification_url=f'{url_header}/{reverse("rest_verify_email")}'
        ctx={"verification_url":verification_url}
        ctx.update(context)
        return super().send_mail(template_prefix, email, ctx)