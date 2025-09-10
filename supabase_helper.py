import os
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "manim-videos")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_video_to_supabase(video_path: str) -> str:
    """Upload video to Supabase storage and return public URL"""
    try:
        # Generate unique filename
        file_extension = video_path.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Read video file
        with open(video_path, "rb") as f:
            video_data = f.read()
        
        # Upload to Supabase - updated error handling
        try:
            result = supabase.storage.from_(SUPABASE_BUCKET).upload(
                unique_filename,
                video_data,
                file_options={"content-type": "video/mp4"}
            )
            
            # Check if upload was successful
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Upload failed: {result.error}")
            
        except Exception as upload_error:
            # Handle various types of upload errors
            raise Exception(f"Upload failed: {str(upload_error)}")
        
        # Get public URL
        try:
            public_url_response = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_filename)
            
            # The response might be a string or an object with a 'publicUrl' attribute
            if isinstance(public_url_response, str):
                public_url = public_url_response
            elif hasattr(public_url_response, 'publicUrl'):
                public_url = public_url_response.publicUrl
            else:
                # Fallback: construct URL manually
                public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{unique_filename}"
            
            return public_url
            
        except Exception as url_error:
            raise Exception(f"Failed to get public URL: {str(url_error)}")
        
    except Exception as e:
        raise Exception(f"Failed to upload video to Supabase: {str(e)}")

def delete_local_video(video_path: str):
    """Delete local video file after successful upload"""
    try:
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Deleted local file: {video_path}")
            
            # Also try to remove the parent directory if it's empty
            parent_dir = os.path.dirname(video_path)
            try:
                if os.path.exists(parent_dir) and not os.listdir(parent_dir):
                    os.rmdir(parent_dir)
                    print(f"Deleted empty directory: {parent_dir}")
            except OSError:
                pass  # Directory not empty, that's fine
    except Exception as e:
        print(f"Warning: Could not delete local file {video_path}: {e}")