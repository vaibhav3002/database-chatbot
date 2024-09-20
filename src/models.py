from pydantic import BaseModel, Field


class QueryAnalysisOutput(BaseModel):
    extracted_query: str = Field(
        ..., description="The concrete query extracted from the conversation."
    )
    is_attack_detected: bool = Field(
        ...,
        description="Flag indicating whether an attack (e.g., SQL injection, Modifying tables etc.) was detected in the input.",
    )
    is_toxicity_detected: bool = Field(
        ...,
        description="Flag indicating whether any toxic language or harmful content was detected in the input.",
    )
