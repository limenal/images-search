from django.shortcuts import render
from django.views import View
from .forms import SearchForm
from .services import search_image
# Create your views here.

class SearchImageView(View):
    async def get(self, request):
        return render(request, 'search_img/index.html', {'form': SearchForm()})
    
    async def post(self, request):
        form = SearchForm(request.POST)
        images = []
        if(form.is_valid()):
            images = await search_image(form.cleaned_data['query'], form.cleaned_data['count'])
            return render(request, 'search_img/index.html', {'form': SearchForm(), 'images': images})