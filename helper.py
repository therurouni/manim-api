import os
import uuid
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Gemini API Configuration ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Helper Functions for Gemini ---
def format_prompt_for_gemini(user_prompt: str) -> str:
    """Wraps the user's prompt with specific instructions for Manim code generation."""
    system_instruction = """
    You are an expert in Manim, the mathematical animation library for Python.
    Your task is to generate a single, complete, and runnable Python script that produces an animation to explain the concept in the most elegant way possible requested by the user in the user request prompt.

    IMPORTANT RULES:
    1.  The script must be a single block of code. Do not use explanations outside of the code block.
    2.  The script must import all necessary classes from `manim`, like `Scene`, `Create`, `Write`, `Circle`, `Square`, `Text`, `MathTex`, etc.
    3.  The script must define a single class that inherits from `manim.Scene`.
    4.  The class must contain a `construct(self)` method where the animation logic is defined.
    5.  Do not include any code to render the scene (e.g., `manim -pql my_scene.py MyScene`). Only provide the Python script itself.
    6.  The code should be well-commented to explain the animation steps.
    7.  AVOID using methods like `index_of_part()`, `index_of_part_by_tex()`, or complex MathTex manipulation that may fail.
    8.  Keep animations simple and robust - use basic animations like Create(), Write(), FadeIn(), FadeOut(), Transform().
    9.  When creating MathTex objects, keep them simple and avoid trying to access individual parts unless absolutely necessary.
    10. Test basic functionality first - focus on clear, working animations rather than complex visual effects.

    Here is the user's request:
    """
    return f"{system_instruction}\n---\nUSER REQUEST: \"{user_prompt}\"\n---"

def extract_python_code(response_text: str) -> str:
    if "```python" in response_text:
        return response_text.split("```python")[1].split("```")[0].strip()
    return response_text.strip()

def get_manim_code_from_gemini(prompt: str) -> str:
    print("Formatting prompt for Gemini...")
    formatted_prompt = format_prompt_for_gemini(prompt)

    print("Calling Gemini API...")
    response = model.generate_content(formatted_prompt)

    print("Extracting Python code from response...")
    manim_code = extract_python_code(response.text)
    return manim_code

# --- Manim Execution Function ---
def execute_manim_script(code: str) -> str:
    script_name = f"temp_manim_script_{uuid.uuid4()}"
    script_path = f"{script_name}.py"
    
    # Write script to current directory (not generated_scripts for Docker compatibility)
    with open(script_path, "w") as f:
        f.write(code)

    try:
        scene_name = code.split("class ")[1].split("(")[0].strip()
    except IndexError:
        if os.path.exists(script_path):
            os.remove(script_path)
        raise ValueError("Could not find a class definition in the generated script.")

    print(f"Rendering scene '{scene_name}' from '{script_path}'...")
    try:
        result = subprocess.run(
            ["manim", "-ql", script_path, scene_name],
            capture_output=True, text=True, check=True
        )
        print("Manim STDOUT:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Manim execution failed!")
        print("Manim STDERR:", e.stderr)
        if os.path.exists(script_path):
            os.remove(script_path)
        raise RuntimeError(f"Manim rendering failed: {e.stderr}")

    # The video will be in media/videos/{script_name}/480p15/{scene_name}.mp4
    video_path = f"media/videos/{script_name}/480p15/{scene_name}.mp4"
    
    # Clean up script file
    if os.path.exists(script_path):
        os.remove(script_path)
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Manim output video not found at expected path: {video_path}")
        
    return video_path

