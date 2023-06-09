import os
from pathlib import Path

import qrcode
from django.conf import settings

from STINBank.celery import app
from accounts.models import User


@app.task
def generate_qr_code(user_id: int):
    user = User.objects.get(pk=user_id)
    Path(os.path.join(settings.MEDIA_ROOT, 'qr_codes')).mkdir(parents=True, exist_ok=True)
    qrcode.make(user.get_totp_uri()).save(os.path.join(settings.MEDIA_ROOT, 'qr_codes', f'{user.pk}.png'))
