import requests
from bs4 import BeautifulSoup
import bs4
from django.shortcuts import render
from requests.compat import quote_plus
import numpy as np
from . import models



def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')


    res=requests.get("https://www.google.com/search?q="+search)

    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,'lxml')

    url_list=[]
    for a in soup.select(' a[href^="/url?q="]'):
        if 'accounts.google.com' in a['href']:
            continue
        s=a['href']
        offset=2
        start=s.find('q=')+ offset
        end=s.find('&sa=')
        url_list.append(s[start:end])
    
    final_postings=[]

    x = np.array(url_list) 
    unique_list=np.unique(x)

    
    post_url=unique_list[0]
    page=requests.get(post_url)
    page.raise_for_status()
    soup=bs4.BeautifulSoup(page.text,'lxml')

    title=soup.select('title')
    post_title=title[0].get_text()

    page=requests.get(unique_list[0])
    page.raise_for_status()
    soup=bs4.BeautifulSoup(page.text,'lxml')
    content=soup.select('p')
    post_content=""
    post_content_list=[]
    for x in content:
        post_content+=((x.get_text())+"\n")
        post_content_list.append(x.get_text())

    post_url=unique_list
    final_postings.append((post_title, post_url))
    models.Search.objects.create(search=search, content=post_content)

    stuff_for_frontend = {
            
        'search': search,
        'final_postings': final_postings,
        'content': post_content_list,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)


