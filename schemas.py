# schemas.py
from pydantic import BaseModel, Field

class AnimationRequest(BaseModel):
    prompt: str = Field(
        ...,
        title="Animation Prompt",
        description="The user's description of the animation concept.",
        min_length=10,
        example="Create an animation explaining the Pythagorean theorem."
    )