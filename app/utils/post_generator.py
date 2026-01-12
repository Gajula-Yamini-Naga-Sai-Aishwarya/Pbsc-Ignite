# app/utils/post_generator.py
"""AI-powered LinkedIn post generation for progress sharing"""

import os
import json
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class PostGenerator:
    """Generate AI-powered LinkedIn posts for achievements and milestones"""
    
    def __init__(self):
        """Initialize post generator with Groq client"""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.groq_api_key) if self.groq_api_key else None
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"
        self.available = bool(self.client)
        
        if self.available:
            print("✅ Post Generator initialized successfully")
        else:
            print("⚠️ Groq API not configured. Post generation will use templates.")
    
    def generate_milestone_post(self, user_name, milestone_data, tone="professional"):
        """
        Generate a LinkedIn post for a learning milestone
        
        Args:
            user_name: User's name
            milestone_data: Dict with milestone information
            tone: Post tone (professional, casual, excited)
            
        Returns:
            Generated post content
        """
        if not self.available:
            return self._generate_template_post(user_name, milestone_data)
        
        prompt = f"""Generate a compelling LinkedIn post for {user_name} who just achieved the following milestone:

Achievement: {milestone_data.get('achievement', 'Completed a learning module')}
Career Goal: {milestone_data.get('career_goal', 'Career development')}
Skills Learned: {', '.join(milestone_data.get('skills', []))}
Duration: {milestone_data.get('duration', 'Recently')}

Tone: {tone}

The post should:
1. Be engaging and authentic (150-200 words)
2. Highlight the achievement and skills gained
3. Show enthusiasm and growth mindset
4. Include relevant hashtags (3-5)
5. Encourage professional connections
6. NOT use emojis excessively

Format: Just the post text, ready to publish."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional LinkedIn content creator who writes engaging, authentic posts for career development and learning achievements."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=400
            )
            
            post_content = response.choices[0].message.content.strip()
            return post_content
            
        except Exception as e:
            print(f"❌ Error generating post with AI: {str(e)}")
            return self._generate_template_post(user_name, milestone_data)
    
    def generate_project_completion_post(self, user_name, project_data):
        """
        Generate a post for project completion
        
        Args:
            user_name: User's name
            project_data: Dict with project information
            
        Returns:
            Generated post content
        """
        if not self.available:
            return self._generate_project_template(user_name, project_data)
        
        prompt = f"""Generate a LinkedIn post for {user_name} who completed a project:

Project: {project_data.get('project_name', 'Learning Project')}
Technologies Used: {', '.join(project_data.get('technologies', []))}
Key Achievements: {project_data.get('achievements', 'Successfully completed')}
Learning Outcomes: {project_data.get('learnings', 'Valuable skills gained')}

The post should:
1. Showcase technical skills and growth
2. Be specific about what was built/learned
3. Demonstrate problem-solving abilities
4. Include relevant tech hashtags
5. Be approximately 200 words

Format: Just the post text, ready to publish."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional LinkedIn content creator specializing in tech and project achievements."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=450
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error generating project post: {str(e)}")
            return self._generate_project_template(user_name, project_data)
    
    def generate_skill_update_post(self, user_name, skill_data):
        """
        Generate a post for new skill acquisition
        
        Args:
            user_name: User's name
            skill_data: Dict with skill information
            
        Returns:
            Generated post content
        """
        skills = skill_data.get('skills', [])
        skill_list = ', '.join(skills) if isinstance(skills, list) else skills
        
        if not self.available:
            return f"""Excited to share that I've been expanding my skillset! 🚀

I've recently learned {skill_list}, which aligns with my goal of {skill_data.get('career_goal', 'professional growth')}.

Key takeaways:
• Hands-on practice with real-world applications
• Problem-solving in {skill_data.get('domain', 'my field')}
• Building practical expertise

Always learning, always growing! 💡

#ProfessionalDevelopment #SkillBuilding #ContinuousLearning #CareerGrowth"""
        
        prompt = f"""Generate a LinkedIn post for {user_name} who learned new skills:

New Skills: {skill_list}
Career Goal: {skill_data.get('career_goal', 'Professional development')}
Application: {skill_data.get('application', 'Real-world projects')}
Next Steps: {skill_data.get('next_steps', 'Continuing to learn')}

Create an engaging post (150-180 words) that shows enthusiasm for learning and professional growth.
Include 3-4 relevant hashtags."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a LinkedIn content creator focused on skill development and career growth."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=350
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error generating skill post: {str(e)}")
            return self._generate_template_post(user_name, skill_data)
    
    def generate_assessment_completion_post(self, user_name, assessment_data):
        """
        Generate a post for assessment completion
        
        Args:
            user_name: User's name
            assessment_data: Dict with assessment information
            
        Returns:
            Generated post content
        """
        score = assessment_data.get('score', 'successfully')
        assessment_type = assessment_data.get('type', 'Assessment')
        
        return f"""Proud to share that I've completed the {assessment_type}! ✅

Score: {score}
Focus Areas: {', '.join(assessment_data.get('topics', ['Multiple topics']))}

This assessment challenged me to:
• Apply theoretical knowledge to practical scenarios
• Demonstrate problem-solving skills
• Showcase technical expertise

Each assessment is a step forward in my journey toward {assessment_data.get('career_goal', 'career excellence')}.

#LearningJourney #SkillValidation #ProfessionalGrowth #CareerDevelopment"""
    
    def _generate_template_post(self, user_name, data):
        """Generate a template-based post when AI is unavailable"""
        achievement = data.get('achievement', 'completed a learning milestone')
        skills = ', '.join(data.get('skills', ['valuable skills']))
        
        return f"""Excited to share my recent progress! 🎯

I've {achievement} as part of my journey toward {data.get('career_goal', 'career excellence')}.

Key skills developed: {skills}

This experience has reinforced my commitment to continuous learning and professional growth.

#LearningJourney #ProfessionalDevelopment #SkillBuilding #CareerGrowth"""
    
    def _generate_project_template(self, user_name, project_data):
        """Generate a template-based project post"""
        project_name = project_data.get('project_name', 'a new project')
        technologies = ', '.join(project_data.get('technologies', ['various technologies']))
        
        return f"""Thrilled to announce the completion of {project_name}! 🚀

Technologies used: {technologies}

Key achievements:
• Built practical solutions to real-world problems
• Strengthened technical skills through hands-on development
• Gained valuable experience in {project_data.get('domain', 'software development')}

Every project is a learning opportunity and a step forward in my career journey.

#ProjectCompletion #TechSkills #SoftwareDevelopment #BuildInPublic"""


# Global instance
post_generator = PostGenerator()


def generate_milestone_post(user_name, milestone_data, tone="professional"):
    """Convenience function to generate milestone post"""
    return post_generator.generate_milestone_post(user_name, milestone_data, tone)


def generate_project_post(user_name, project_data):
    """Convenience function to generate project post"""
    return post_generator.generate_project_completion_post(user_name, project_data)


def generate_skill_post(user_name, skill_data):
    """Convenience function to generate skill update post"""
    return post_generator.generate_skill_update_post(user_name, skill_data)


def generate_assessment_post(user_name, assessment_data):
    """Convenience function to generate assessment post"""
    return post_generator.generate_assessment_completion_post(user_name, assessment_data)
