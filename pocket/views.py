from django.urls import reverse
from django.conf import settings
from datetime import date,datetime
from django.http import HttpResponsePermanentRedirect
from allauth.account.adapter import DefaultAccountAdapter

def home(request):
    return HttpResponsePermanentRedirect(reverse("swagger-ui"))
    
def get_date_object(date_string):
    """
    Generates a date object.

    Parameters
    ----------
    date_string: str
        a string representing date in the format %Y-%m-%d.
    
    Returns
    -------
    datetime.date
        a date object derived from the date string.
    """

    date_format="%Y-%m-%d"
    return datetime.strptime(date_string,date_format).date()

def project_status(request):
    """
    Sets both ongoing and end date.

    Parameters
    ----------
    request

    Returns
    -------
    tuple of (bool,datetime.date)
        ongoing receives the boolean value,
        end_date receives the datetime.date object.
    """

    ongoing=request.data.get('ongoing')
    if ongoing: return (True,None)
    today=date.today()
    end_date=get_date_object(request.data.get('end_date'))
    return (True,None) if end_date>today else (False,end_date)

class PortfolioAPIAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        """
        Use dj_rest_auth email verification endpoint

        Updates the send_mail context variable to include it
        """

        confirm_email_url=reverse("account_confirm_email",kwargs={"key":context.get("key")})
        base_url=context.get("activate_url").split(confirm_email_url)[0]
        verification_url=f'{base_url}{reverse("rest_verify_email")}'
        ctx={
            "verification_url":verification_url,
            "expires_after":settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
        }
        ctx.update(context)
        return super().send_mail(template_prefix, email, ctx)