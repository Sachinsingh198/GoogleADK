from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel, Field
from google.adk import Agent
from typing import Literal


class Enquiry(BaseModel):
    name: str | None = Field(default=None, description="Student's full name, properly capitalized")
    email: str | None = Field(default=None, description="Email address of the student exactly as written")
    interested_in: list[Literal["GenAI", "Data Science", "MLOps", "Deep Learning", "Other"]] = Field(description="CampusX courses the student is interested in.")
    budget_inr: int | None = Field(default = None, ge=0, le=500000, description="Total budget in rupees as a plain number. Convert '15k' to 15000")

root_agent = Agent(
    model='gemini-3.5-flash',
    name='enquiry_agent',
    description='Extracts student enquiry details from a message.',
    instruction="Read the student's message and extract theri details."
        "If something is not mentioned, leave it empty. Never guess."
    ,
    output_schema=Enquiry,
    output_key="Enquiry"
)
