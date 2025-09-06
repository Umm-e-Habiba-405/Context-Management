
from agents import Agent, Runner, function_tool, RunContextWrapper,trace
import asyncio
from pydantic import BaseModel
from connection import config
import rich


# Student profile model
class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int


# Tool to access student profile from context
@function_tool
async def student_profile(wrapper: RunContextWrapper[StudentProfile]):
    """
    Returns the student profile from the provided context.
    """
    return wrapper.context


# Student profile object
student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

# Student Agent with improved instructions
student_agent = Agent(
    name="Student Agent",
    instructions=(
        "You are a helpful student assistant. "
        "You have access to a student's profile containing the student ID , name, current semester, and total courses. "
        "Always answer using the provided profile context. "
        "If the user asks about multiple details, provide them clearly in one response without adding extra information."
    ),
    tools=[student_profile]
)


# Main function to run the agent
async def main():
    with trace("student agent"):
       result = await Runner.run(
        student_agent,
        """
  "What is my student ID?"
"Please tell me my name and current semester."
"How many courses am I enrolled in?"
"Give me all my student details."
"Which semester am I currently studying in?"
"Tell me my name and total number of courses."
"What's the ID and semester of this student?"
Can you tell me my current semester and how many courses I have?""",
        run_config=config,
        context=student  # Local context
    )
    rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

