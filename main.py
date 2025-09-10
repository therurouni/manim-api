from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from schemas import AnimationRequest
from helper import get_manim_code_from_gemini, execute_manim_script
from supabase_helper import upload_video_to_supabase, delete_local_video

app = FastAPI()

# Mount static files (keeping for backward compatibility)
app.mount("/videos", StaticFiles(directory="media"), name="videos")

@app.post("/generate-video/")
async def create_animation_video(request: AnimationRequest):
    try:
        prompt = request.prompt
        manim_code = get_manim_code_from_gemini(prompt)
        print("Executing Manim script...")
        video_file_path = execute_manim_script(manim_code)
        print(f"Success! Video generated at: {video_file_path}")
        
        # Upload to Supabase
        print("Uploading video to Supabase...")
        supabase_url = await upload_video_to_supabase(video_file_path)
        print(f"Video uploaded to Supabase: {supabase_url}")
        
        # Clean up local file
        delete_local_video(video_file_path)
        print("Local video file cleaned up")
        
        return {
            "video_url": supabase_url,
            "message": "Video generated and uploaded successfully"
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Keep the local video endpoint for backward compatibility
@app.get("/video/{video_path:path}")
async def get_video(video_path: str):
    full_path = f"media/{video_path}"
    if os.path.exists(full_path):
        return FileResponse(full_path, media_type="video/mp4")
    return {"error": "Video not found"}