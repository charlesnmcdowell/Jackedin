import os
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, ColorClip
from moviepy.audio.fx import AudioFadeOut
from moviepy.video.fx import FadeOut

def create_video(chapter_num, audio_file, image_file):
    print(f"Processing Chapter {chapter_num}...")
    
    if not os.path.exists(audio_file):
        print(f"Audio file not found: {audio_file}")
        return
    if not os.path.exists(image_file):
        print(f"Image file not found: {image_file}")
        return

    # Load audio
    audio = AudioFileClip(audio_file)
    
    # 1. Full Chapter Video (16:9 - 1920x1080)
    full_output = f"JackedIn_Chapter_{chapter_num}.mp4"
    if not os.path.exists(full_output):
        print(f"Creating full video for Chapter {chapter_num}...")
        black_bg = ColorClip(size=(1920, 1080), color=(0,0,0)).with_duration(audio.duration)
        img = ImageClip(image_file).resized(height=1080).with_duration(audio.duration)
        full_video = CompositeVideoClip([black_bg, img.with_position("center")], size=(1920, 1080))
        full_video = full_video.with_audio(audio)
        full_video.write_videofile(full_output, fps=10, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4)
    else:
        print(f"Full video for Chapter {chapter_num} already exists.")
    
    # 2. TikTok Snippet (9:16 - 1080x1920, 45 seconds)
    tiktok_output = f"JackedIn_TikTok_Snippet_Ch{chapter_num}.mp4"
    # Always recreate snippet if called to ensure fade-out is present, 
    # or rely on user to delete if they want update. 
    # Current request is specifically for Ch1, which we did manually.
    # But good to have the logic here for others.
    
    snippet_duration = 45
    if audio.duration > snippet_duration:
        # Check if we should recreate or skip. 
        # For now, let's skip if exists to avoid overwriting the one we just made manually unless deleted.
        if not os.path.exists(tiktok_output):
            print(f"Creating TikTok snippet for Chapter {chapter_num}...")
            audio_snippet = audio.subclipped(0, snippet_duration)
            audio_snippet = audio_snippet.with_effects([AudioFadeOut(5)])
            
            img_tiktok = ImageClip(image_file).resized(height=1920).with_duration(snippet_duration)
            w, h = img_tiktok.size
            x1 = (w - 1080) // 2
            x2 = x1 + 1080
            img_tiktok = img_tiktok.cropped(x1=x1, y1=0, x2=x2, y2=1920)
            
            # Apply fade out to video
            black_bg = ColorClip(size=(1080, 1920), color=(0,0,0)).with_duration(snippet_duration)
            img_tiktok = img_tiktok.with_effects([FadeOut(5)])
            final_clip = CompositeVideoClip([black_bg, img_tiktok])
            
            tiktok_video = final_clip.with_audio(audio_snippet)
            tiktok_video.write_videofile(tiktok_output, fps=10, codec="libx264", audio_codec="aac", preset="ultrafast", threads=4)
        else:
             print(f"TikTok snippet for Chapter {chapter_num} already exists.")
    else:
        print(f"Audio for Ch {chapter_num} too short for snippet.")

if __name__ == "__main__":
    chapters = [
        (1, "JackedIN_md_Chapter_1.mp3", "JackedIN_bookcover.png"),
        (2, "JackedIN_md_Chapter_2.mp3", "JackedIN_bookcover.png"),
        (3, "JackedIN_md_Chapter_3.mp3", "JackedIN_bookcover.png"),
    ]
    
    for ch_num, audio, img in chapters:
        try:
            create_video(ch_num, audio, img)
        except Exception as e:
            print(f"Error processing Chapter {ch_num}: {e}")
