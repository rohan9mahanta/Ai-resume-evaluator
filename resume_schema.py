import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY was not found. Add GROQ_API_KEY=your_key to the .env file in this project folder.")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

job_description="""We are hiring an experienced Full-Stack Software Development Engineer to join our Tracking team in Hyderabad. This role focuses on building and scaling real-time tracking systems that serve hundreds of millions of customers worldwide. You will own complex technical problems end-to-end, drive architectural decisions, mentor junior engineers, and deliver features that directly improve how customers experience order visibility and delivery updates. This is a high-impact role where your work is visible to customers every single day.

Key job responsibilities
As an SDE2 on this team, you'll own end-to-end design and delivery of features across the full stack, mentor junior engineers, and drive technical decisions that directly impact customer experience at massive scale.



A day in the life
What You'll Do

- Design and build scalable full-stack services handling millions of requests per day

- Own features end-to-end — from system design through production deployment and monitoring

- Drive technical design discussions and author design documents

- Mentor SDE1 engineers through code reviews, pairing, and knowledge sharing

- Collaborate with product managers and UX designers to translate requirements into technical solutions

- Improve operational excellence — build monitoring, alerting, and automated recovery mechanisms

- Contribute to team roadmap and technical strategy

About the team
Our Tracking team is responsible for building the real-time order tracking and delivery progress experience for one of the world's largest e-commerce platforms. We power the page that customers visit most after placing an order — showing them exactly where their package is, when it will arrive, and what's happening at every step.

We operate at massive scale (millions of page views daily), work across the full stack (front-end UI, backend services, real-time data pipelines), and obsess over customer experience. Our team is collaborative, fast-moving, and deeply technical. We value engineers who take ownership, simplify complex problems, and care about the end-user experience.

Basic Qualifications
- 3+ years of non-internship professional software development experience
- 2+ years of non-internship design or architecture (design patterns, reliability and scaling) of new and existing systems experience
- Knowledge of professional software engineering & best practices for full software development life cycle, including coding standards, software architectures, code reviews, source control management, continuous deployments, testing, and operational excellence
- Experience in one or more relevant front-end frameworks such as React, Angular, etc.
- Experience designing, building, operating, and managing large-scale distributed systems or web services
- - Strong problem-solving skills with a focus on scalability and performance

Preferred Qualifications
- 3+ years of full software development life cycle, including coding standards, code reviews, source control management, build processes, testing, and operations experience
- Bachelor's degree in computer science or equivalent
- Knowledge of system performance, memory management, and parallel computing principles"""

class JobDescription(BaseModel):
    """Key job details used to compare candidates."""

    role: str
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    minimum_years_experience: float | None = None
    educations_requirements: list[str] = []
    responsibilities: list[str] = []




schema = JobDescription.model_json_schema()
system_prompt = f"""
You are an HR assistant. Extract only useful job requirements from the description.
Return the result as valid JSON matching this schema:
{schema}
"""
message_system = {
    "role": "system",
    "content": system_prompt,
}
message = {
    "role": "user",
    "content": job_description,
}

messages=[message_system,message]
response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format={"type": "json_object"},
)
ans=response.choices[0].message.content

import json 
#json.loads() converts the python string into json dictionary
data_file=json.loads(ans)   
jobD=JobDescription(**data_file)

print(jobD.role)
print(jobD.required_skills)
print(jobD.preferred_skills)
print(jobD.minimum_years_experience)
print(jobD.educations_requirements)
print(jobD.responsibilities)


