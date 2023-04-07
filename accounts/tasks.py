import os
from pathlib import Path

import pyotp
import qrcode
from decouple import config
from django.conf import settings

from STINBank.celery import app
from STINBank.utils.config import get_project_config
from accounts.models import User


@app.task
def generate_qr_code(user_id: int):
    user = User.objects.get(pk=user_id)
    uri = pyotp.totp.TOTP(config('TOTP_KEY')).provisioning_uri(
        name=user.username,
        issuer_name=get_project_config().name
    )
    Path(os.path.join(settings.MEDIA_ROOT, 'qr_codes')).mkdir(parents=True, exist_ok=True)
    qrcode.make(uri).save(os.path.join(settings.MEDIA_ROOT, 'qr_codes', f'{user.pk}.png'))
