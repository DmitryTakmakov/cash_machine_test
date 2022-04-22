import io

from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView

from itemsapp.models import Item
from itemsapp.serializers import ReceiptSerializer


class CreateReceiptView(APIView):
    template = 'receipt.html'

    def post(self, request):
        incoming_data = ReceiptSerializer(data=request.data)
        if not incoming_data.is_valid(raise_exception=True):
            return ParseError(incoming_data.errors)
        else:
            requested_ids = request.data.get('items')
            if not len(requested_ids):
                raise ParseError(detail='no IDs provided')
            items = Item.objects.in_bulk(requested_ids)
            context = {
                'items': [],
                'total': 0,
                'created': 0
            }
            for value in items.values():
                context['items'].append({
                    'title': value.title,
                    'quantity': 1,
                    'price': value.price
                })
                context['total'] += value.price
            context['created'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            template = get_template(self.template)
            rendered = template.render(context)
            file = Item.save_to_pdf(rendered)
            buffer = io.BytesIO()
            qr_code = Item.generate_qr_code(request, file)
            qr_code.save(buffer)
            response = HttpResponse(buffer.getbuffer())
            response.status_code = status.HTTP_201_CREATED
            response['Content-Type'] = "image/png"
            response['Cache-Control'] = "max-age=0"
            return response
