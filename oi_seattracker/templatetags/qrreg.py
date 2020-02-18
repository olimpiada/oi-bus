from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
try:
    import lxml.etree.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import qrcode
import qrcode.image.svg

register = template.Library()

@register.simple_tag
def computer_qrcode(request):
    if not settings.DISPLAY_QR_CODES:
        return ''
    ip_addr = request.META['REMOTE_ADDR']
    qr = qrcode.QRCode(box_size=50, image_factory=qrcode.image.svg.SvgImage)
    qr.add_data(ip_addr)
    img = qr.make_image().get_image()
    svg = ET.tostring(img, encoding='unicode', method='html')
    return mark_safe(svg)

