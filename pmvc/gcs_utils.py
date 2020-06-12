import shastarainnews.settings as settings
from .models import GcsAccessToken
import datetime
import pytz

from google.auth.transport.requests import Request
from google.oauth2 import service_account


def refresh_gcs_creds():
    RW_SCOPE = 'https://www.googleapis.com/auth/devstorage.read_write'
    credentials = service_account.Credentials.from_service_account_file(settings.GS_CREDENTIALS)
    creds_with_scopes = credentials.with_scopes([RW_SCOPE])
    creds_with_scopes.refresh(Request())
    utc = pytz.UTC
    # Even though google reports the expiry date in UTC they don't have the UTC timezone info, so add it.
    token_expiry = creds_with_scopes.expiry.astimezone(utc)
    # Back up the expiry time by 5 seconds to give us a little buffer.
    token_expiry = token_expiry - datetime.timedelta(seconds=5)

    creds, created = GcsAccessToken.objects.get_or_create(pk=1)
    creds.access_token = creds_with_scopes.token
    creds.expiry = token_expiry
    creds.save()

    return creds


def get_access_token():
    creds_query = GcsAccessToken.objects.filter(pk=1)
    if creds_query.count() == 0:
        # This should only happen once. There is no database record. Refresh will create one.
        creds = refresh_gcs_creds()
    else:
        creds = creds_query[0]
        utc = pytz.UTC
        current_utc_time = datetime.datetime.now(utc)
        if current_utc_time > creds.expiry:
            creds = refresh_gcs_creds()

        # print("Token: " + creds.access_token)
        # print("Expiry: " + str(creds.expiry))

    return creds.access_token
