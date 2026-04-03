from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import URLMap, ClickStats
from .forms import URLForm

def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url_map = form.save(commit=False)
            url_map.created_by = request.META.get('REMOTE_ADDR')
            url_map.save()
            short_url = request.build_absolute_uri(f'/{url_map.short_code}')
            return render(request, 'Links/home.html', {
                'form': URLForm(),  # Reset form
                'short_url': short_url,
                'original_url': url_map.original_url
            })
    else:
        form = URLForm()
    
    return render(request, 'Links/home.html', {'form': form})

def redirect_original(request, short_code):
    url_map = get_object_or_404(URLMap, short_code=short_code, is_active=True)
    
    if url_map.is_expired():
        return HttpResponse("This link has expired.", status=410)
    
    ClickStats.objects.create(
        link=url_map,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER', '')
    )
    
    url_map.increment_click_count()
    return redirect(url_map.original_url)

def url_stats(request, short_code):
    url_map = get_object_or_404(URLMap, short_code=short_code)
    return render(request, 'Links/stats.html', {'url_map': url_map})