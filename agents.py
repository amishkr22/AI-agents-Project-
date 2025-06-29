from crewai import Agent, LLM
from crewai_tools import FileReadTool, ScrapeWebsiteTool, MDXSearchTool, SerperDevTool
import os
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    """Base class for all agents with common functionality"""
    
    def __init__(self, resume_path='./old_resume.md'):
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.read_resume = FileReadTool(file_path=resume_path)
        self.search_resume = MDXSearchTool(mdx=resume_path)
        
        self.llm = LLM(
            model=os.getenv("GEMINI_MODEL_NAME"),
            temperature=0.7,
        )

class TechJobResearcher(BaseAgent):
    
    def __init__(self, resume_path='./old_resume.md'):
        super().__init__(resume_path)
        self.agent = self._create_agent()
    
    def _create_agent(self):
        return Agent(
            role="Tech Job Researcher",
            goal="Make sure to do amazing analysis on "
                 "job posting to help job applicants",
            tools=[self.scrape_tool, self.search_tool],
            verbose=True,
            backstory=(
                "As a Job Researcher, your prowess in "
                "navigating and extracting critical "
                "information from job postings is unmatched."
                "Your skills help pinpoint the necessary "
                "qualifications and skills sought "
                "by employers, forming the foundation for "
                "effective application tailoring."
            ),
            llm=self.llm
        )
    
    def get_agent(self):
        return self.agent

class PersonalProfiler(BaseAgent):
    
    def __init__(self, resume_path='./old_resume.md'):
        super().__init__(resume_path)
        self.agent = self._create_agent()
    
    def _create_agent(self):
        return Agent(
            role="Personal Profiler for Engineers",
            goal="Do incredible research on job applicants "
                 "to help them stand out in the job market",
            tools=[self.scrape_tool, self.search_tool,
                   self.read_resume, self.search_resume],
            verbose=True,
            backstory=(
                "Equipped with analytical prowess, you dissect "
                "and synthesize information "
                "from diverse sources to craft comprehensive "
                "personal and professional profiles, laying the "
                "groundwork for personalized resume enhancements."
            ),
            llm=self.llm
        )
    
    def get_agent(self):
        return self.agent

class ResumeStrategist(BaseAgent):
    
    def __init__(self, resume_path='./old_resume.md'):
        super().__init__(resume_path)
        self.agent = self._create_agent()
    
    def _create_agent(self):
        return Agent(
            role="Resume Strategist for Engineers",
            goal="Find all the best ways to make a "
                 "resume stand out in the job market.",
            tools=[self.scrape_tool, self.search_tool,
                   self.read_resume, self.search_resume],
            verbose=True,
            backstory=(
                "With a strategic mind and an eye for detail, you "
                "excel at refining resumes to highlight the most "
                "relevant skills and experiences, ensuring they "
                "resonate perfectly with the job's requirements."
            ),
            llm=self.llm
        )
    
    def get_agent(self):
        return self.agent

class InterviewPreparer(BaseAgent):
    
    def __init__(self, resume_path='./old_resume.md'):
        super().__init__(resume_path)
        self.agent = self._create_agent()
    
    def _create_agent(self):
        return Agent(
            role="Engineering Interview Preparer",
            goal="Create interview questions and talking points "
                 "based on the resume and job requirements",
            tools=[self.scrape_tool, self.search_tool,
                   self.read_resume, self.search_resume],
            verbose=True,
            backstory=(
                "Your role is crucial in anticipating the dynamics of "
                "interviews. With your ability to formulate key questions "
                "and talking points, you prepare candidates for success, "
                "ensuring they can confidently address all aspects of the "
                "job they are applying for."
            ),
            llm=self.llm
        )
    
    def get_agent(self):
        return self.agent

class AgentFactory:
    
    def __init__(self, resume_path='./old_resume.md'):
        self.resume_path = resume_path
    
    def create_all_agents(self):
        """Create and return all agents"""
        researcher = TechJobResearcher(self.resume_path)
        profiler = PersonalProfiler(self.resume_path)
        strategist = ResumeStrategist(self.resume_path)
        interviewer = InterviewPreparer(self.resume_path)
        
        return {
            'researcher': researcher.get_agent(),
            'profiler': profiler.get_agent(),
            'strategist': strategist.get_agent(),
            'interviewer': interviewer.get_agent()
        }
    
    def create_agent(self, agent_type):
        agents = {
            'researcher': TechJobResearcher,
            'profiler': PersonalProfiler,
            'strategist': ResumeStrategist,
            'interviewer': InterviewPreparer
        }
        
        if agent_type not in agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agents[agent_type](self.resume_path).get_agent()