import subprocess
import os
import json
from celery import shared_task
from time import sleep
from celery import Celery
from video.models import Video
import math

@shared_task
def video_encode(duration,video_id):
    try:
        sleep(duration)
        obj = Video.objects.filter(status='Pending',id=video_id).first()
        if obj:
            obj.status = 'Processing'
            obj.is_running = True
            obj.save()
            input_video_path = obj.video.path
            output_directory = os.path.join(os.path.dirname(input_video_path), 'hls_output')
            os.makedirs(output_directory, exist_ok=True)
            output_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '_hls.m3u8'
            audio_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '.mp3'
            output_audio = os.path.join(output_directory, audio_filename)
            output_hls_path = os.path.join(output_directory, output_filename)
            output_thumbnail_path = os.path.join(output_directory, os.path.splitext(os.path.basename(input_video_path))[0]+'thumbnail.jpg')

            # getting video duration/length

            command = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                
                input_video_path
            ]
            result = subprocess.run(command, shell=False,
                                    check=True, stdout=subprocess.PIPE)
            output_json = json.loads(result.stdout)

            video_length = None
            for stream in output_json['streams']:
                if stream['codec_type'] == 'video':
                    video_length = math.ceil(stream['duration'])
                    break

            if video_length is not None:
                obj.duration = video_length 
            

            # Use ffmpeg to create HLS segments
            cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-c:v', 'h264',
                '-c:a', 'aac',
                '-hls_time', '5',
                '-hls_list_size', '0',
                "-hls_base_url", "{{ dynamic_path }}/",
                "-movflags", "+faststart",
                '-y',
                output_hls_path
            ]


            subprocess.run(cmd, check=True)


            # generate thumbnail 
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', input_video_path,
                '-ss', '2', 
                '-vframes', '1',            
                '-q:v', '2',  
                '-y',               
                output_thumbnail_path
            ]
            subprocess.run(ffmpeg_cmd, check=True)


            # Update the Video object status to 'Processed' or something similar
            obj.hls = output_hls_path 
            obj.thumbnail = output_thumbnail_path
            obj.status = 'Completed'
            obj.is_running = False
            obj.save()

            print(f'HLS segments generated and saved at: {output_hls_path}')
        else:
            print('No video with status "Pending" found.')
        return True 

    except Exception as e:
        print(e)

        return False 
