from django.shortcuts import render,redirect
import requests
from bs4 import BeautifulSoup
from .models import link as Link
from django.contrib import messages

# Create your views here.

def scrape(request):
    if request.method=='POST':
        url=request.POST.get('search-link')

        if not url or None:
            messages.warning(request,"Not the right url")
            return redirect('/')

        try:

            page=requests.get(url)
            soup_obj=BeautifulSoup(page.text,'html.parser')


            for link in soup_obj.find_all('a'):
                link_address=link.get('href')
                link_text=link.string
                Link.objects.create(address=link_address,name=link_text)
            return redirect('/')
        
        
        except Exception as e:
            messages.warning(request,f"An error occured {e}")
            return redirect('/')

        

    else:

        link_set=Link.objects.all()    
        return render(request,'index.html',{'link_set':link_set})

def delete(request):
    Link.objects.all().delete()
    return redirect('/')