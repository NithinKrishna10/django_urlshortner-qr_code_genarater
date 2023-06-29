from django.shortcuts import render,redirect
import uuid
from django.http import HttpResponse,JsonResponse
from .models import Url
import requests
from bs4 import BeautifulSoup
import qrcode
from io import BytesIO
# Create your views here.

def index(request):
    return render(request,'index.html')
def go(request, pk):
    url_details = Url.objects.get(uuid=pk)
    return redirect(url_details.link)





# def create(request):
#     if request.method == 'POST':
#         link = request.POST['link']
#         uid = str(uuid.uuid4())[:5]
#         new_url = Url(link=link, uuid=uid)
#         new_url.save()
#         fetch_link_preview(new_url)  # Fetch link preview metadata
#         # Generate QR code
#         qr = qrcode.QRCode(
#             version=1,
#             box_size=10,
#             border=4
#         )
#         qr.add_data(link)
#         qr.make(fit=True)
#         qr_image = qr.make_image(fill='black', back_color='white')

#         # Save QR code image
#         qr_filename = f'{uid}_qr.png'
#         qr_path = f'/path/to/qr_codes/{qr_filename}'  # Replace with your desired path
#         qr_image.save(qr_path)
#         data = {
#             'uid': uid,
#             'title': new_url.title,
#             'description': new_url.description,
#             'image_url': new_url.image_url,
#             'qr_code_url': qr_path 
#         }

#         return JsonResponse(data)


import os

# ...

def create(request):
    if request.method == 'POST':
        link = request.POST['link']
        uid = str(uuid.uuid4())[:5]
        new_url = Url(link=link, uuid=uid)
        new_url.save()
        fetch_link_preview(new_url)  # Fetch link preview metadata
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(link)
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='white')
        qr_filename = f'{uid}_qr.png'
        # Save QR code image
        qr_directory = 'uploads'  # Replace with your desired directory path
        new_url.qr_code = qr_filename
        new_url.save()
        
        # Create the directory if it doesn't exist
        os.makedirs(qr_directory, exist_ok=True)
        qr_path = os.path.join(qr_directory, qr_filename)
        
        qr_image.save(qr_path)
        
        data = {
            'uid': uid,
            'title': new_url.title,
            'description': new_url.description,
            'image_url': new_url.image_url,
            'qr_code_url': qr_path 
        }

        return JsonResponse(data)



def fetch_link_preview(url_obj):
    response = requests.get(url_obj.link)
    soup = BeautifulSoup(response.content, 'html.parser')
    meta_tags = soup.find_all('meta')


    for tag in meta_tags:
        if 'property' in tag.attrs and tag.attrs['property'].lower() == 'og:title':
            url_obj.title = tag.attrs['content']
        elif 'name' in tag.attrs and tag.attrs['name'].lower() == 'description':
            url_obj.description = tag.attrs['content']
        elif 'property' in tag.attrs and tag.attrs['property'].lower() == 'og:image':
            url_obj.image_url = tag.attrs['content']

    url_obj.save()
