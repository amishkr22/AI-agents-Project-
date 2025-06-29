from crewai import Crew, Task
from agents import (
    TechJobResearcher, 
    PersonalProfiler, 
    ResumeStrategist, 
    InterviewPreparer
)
from file_conversion import FileConverter

converter_instance  = FileConverter()
converter_instance.pdf_to_md(r"C:\Users\amish\Downloads\RESUME.pdf")

def create_crew_method():
    """Create crew using individual agent classes"""
    researcher = TechJobResearcher('./old_resume.md')
    profiler = PersonalProfiler('./old_resume.md')
    strategist = ResumeStrategist('./old_resume.md')
    interviewer = InterviewPreparer('./old_resume.md')
    
    research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher.get_agent(),
    async_execution=True
    )
    
    profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler.get_agent(),
    async_execution=True
    )

    resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="new_resume.md",
    context=[research_task, profile_task],
    agent=strategist.get_agent()
    )
    
    interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interviewer.get_agent()
    )
    
    crew = Crew(
        agents=[
            researcher.get_agent(),
            profiler.get_agent(),
            strategist.get_agent(),
            interviewer.get_agent()
        ],
        tasks=[research_task, profile_task, resume_strategy_task, interview_preparation_task],
        verbose=True
    )
    
    return crew


if __name__ == "__main__":
    crew = create_crew_method()
    
    job_application_inputs = {
    'job_posting_url': 'https://search.jobs.barclays/job/-/-/13015/81911683408?src=JB-12860',
    'github_url': 'https://github.com/amishkr22',
    'personal_writeup': """I am Amish Nayar, a passionate and driven Computer Science and Engineering undergraduate with a strong
                           focus on Machine Learning, Natural Language Processing, and Large Language Models. My hands-on
                           experience ranges from developing sophisticated AI-powered chatbots and RAG pipelines to fine-tuning
                           cutting-edge models like LLaMA and GEMMA."""
                           }
    
    result = crew.kickoff(inputs=job_application_inputs)
    print(result)