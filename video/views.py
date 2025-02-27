import os 
from django.shortcuts import render
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from video.models import Video
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


def serve_hls_playlist(request, video_id):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_playlist_path = video.hls

        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()

        base_url = request.build_absolute_uri('/') 
        serve_hls_segment_url = base_url +"serve_hls_segment/" +str(video_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)


        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)


def serve_hls_segment(request, video_id, segment_name):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_directory = os.path.join(os.path.dirname(video.video.path), 'hls_output')
        segment_path = os.path.join(hls_directory, segment_name)

        # Serve the HLS segment as a binary file response
        return FileResponse(open(segment_path, 'rb'))
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)


def hls_video_player(request, video_id):
    video = Video.objects.filter(slug=video_id).first()
    hls_playlist_url = reverse('serve_hls_playlist', args=[video.id])
    
    

    context = {
        'hls_url': hls_playlist_url,
        'video': video,
    }

    return render(request, 'video.html', context)



def all_videos(request):
    videos = Video.objects.filter(status='Completed')
    # paginator = Paginator(videos, 6)
    # page_number = request.GET.get('page')
    # page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'videos': videos,
        # 'page_obj': page_obj
    }

    return render(request, 'home.html', context)


def search_videos(request):
     if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        videos = Video.objects.filter(
            name__icontains=search_str, status='Completed') | Video.objects.filter(
            description__icontains=search_str, status='Completed') | Video.objects.filter(
            category__icontains=search_str, status='Completed')
        data = videos.values()
        return JsonResponse(list(data), safe=False)
     

def pagination(request):
    if request.method == 'GET':
        videos = Video.objects.filter(status='Completed')
        data = videos.values('category')
        return JsonResponse(list(data), safe=False)
    