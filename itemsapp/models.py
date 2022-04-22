import secrets

import pdfkit
import qrcode
from django.conf import settings
from django.db import models
from rest_framework.exceptions import ParseError


class Item(models.Model):
    title = models.CharField(max_length=150, blank=True)
    price = models.IntegerField(blank=True, null=True)

    @classmethod
    def save_to_pdf(cls, rendered_template):
        filename = secrets.token_hex()
        server_filepath = str(settings.BASE_DIR / 'media' / f'{filename}.pdf')
        try:
            pdfkit.from_string(rendered_template, server_filepath)
        except Exception as e:
            raise ParseError(detail=e)
        return filename

    @classmethod
    def generate_qr_code(cls, request, filename):
        host_name = request.get_host()
        qr_code = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(f'http://{host_name}/media/{filename}.pdf')
        qr_code.make(fit=True)
        img = qr_code.make_image()
        return img
