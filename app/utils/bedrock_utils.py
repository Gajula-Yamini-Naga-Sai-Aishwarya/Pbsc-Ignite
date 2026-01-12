# app/utils/bedrock_utils.py
"""AWS Bedrock utilities for Claude Sonnet 4 integration"""

import os
import json
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

class BedrockClient:
    """AWS Bedrock client for Claude Sonnet 4"""
    
    def __init__(self):
        """Initialize Bedrock client"""
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        # Initialize boto3 client
        try:
            self.client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region,
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key
            )
            self.available = True
            print("✅ AWS Bedrock client initialized successfully")
        except Exception as e:
            print(f"⚠️ AWS Bedrock client initialization failed: {str(e)}")
            self.available = False
            self.client = None
    
    def invoke_claude(self, prompt, max_tokens=4096, temperature=0.7, system_prompt=None):
        """
        Invoke Claude Sonnet 4 via AWS Bedrock
        
        Args:
            prompt: User prompt/message
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
            system_prompt: Optional system prompt
            
        Returns:
            Generated text response
        """
        if not self.available:
            raise Exception("AWS Bedrock client not available. Check your credentials.")
        
        # Model ID for Claude Sonnet 4
        model_id = "anthropic.claude-sonnet-4-20250514-v1:0"
        
        # Prepare the request body
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": temperature
        }
        
        # Add system prompt if provided
        if system_prompt:
            body["system"] = system_prompt
        
        try:
            # Invoke the model
            response = self.client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract the text from the response
            if 'content' in response_body and len(response_body['content']) > 0:
                return response_body['content'][0]['text']
            else:
                return response_body.get('completion', '')
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"❌ Bedrock API Error [{error_code}]: {error_message}")
            raise Exception(f"Bedrock API Error: {error_message}")
        except Exception as e:
            print(f"❌ Unexpected error invoking Claude: {str(e)}")
            raise

    def generate_tutoring_response(self, student_question, context=""):
        """
        Generate personalized tutoring response
        
        Args:
            student_question: The student's question
            context: Additional context (learning materials, etc.)
            
        Returns:
            Tutoring response
        """
        system_prompt = """You are LEO, an expert AI tutor specializing in personalized learning.
Your role is to:
1. Provide clear, detailed explanations
2. Break down complex concepts into simple steps
3. Use examples and analogies to aid understanding
4. Encourage critical thinking with thoughtful questions
5. Adapt your teaching style to the student's needs

Be patient, encouraging, and focus on helping students truly understand concepts."""

        prompt = f"""Student Question: {student_question}

{f"Context: {context}" if context else ""}

Provide a comprehensive, helpful response that aids the student's learning."""

        return self.invoke_claude(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
            temperature=0.7
        )

    def generate_career_advice(self, user_profile, career_goal, specific_question=""):
        """
        Generate career coaching advice
        
        Args:
            user_profile: User's profile information
            career_goal: Target career goal
            specific_question: Optional specific question
            
        Returns:
            Career advice response
        """
        system_prompt = """You are a professional career coach with expertise in technology careers.
Your role is to:
1. Provide actionable career development advice
2. Suggest concrete steps for skill development
3. Offer industry insights and trends
4. Help identify growth opportunities
5. Guide professional networking strategies

Be professional, insightful, and focused on helping individuals achieve their career goals."""

        prompt = f"""User Profile: {json.dumps(user_profile, indent=2)}
Career Goal: {career_goal}
{f"Specific Question: {specific_question}" if specific_question else ""}

Provide professional career guidance tailored to this individual's goals and background."""

        return self.invoke_claude(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
            temperature=0.7
        )

    def generate_assessment_feedback(self, submission, assessment_criteria):
        """
        Generate detailed assessment feedback
        
        Args:
            submission: Student's submission (code, answers, etc.)
            assessment_criteria: Grading criteria
            
        Returns:
            Detailed feedback and scoring
        """
        system_prompt = """You are an expert educator providing constructive assessment feedback.
Your role is to:
1. Evaluate submissions objectively
2. Provide specific, actionable feedback
3. Highlight both strengths and areas for improvement
4. Suggest concrete steps for enhancement
5. Encourage continued learning

Be fair, thorough, and constructive in your assessments."""

        prompt = f"""Submission:
{submission}

Assessment Criteria:
{assessment_criteria}

Provide detailed feedback including:
1. Overall evaluation
2. Specific strengths
3. Areas for improvement
4. Actionable recommendations
5. Suggested score/grade"""

        return self.invoke_claude(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=2048,
            temperature=0.5
        )


# Global instance
bedrock_client = BedrockClient()


def get_bedrock_client():
    """Get the global Bedrock client instance"""
    return bedrock_client


def invoke_claude_for_tutoring(question, context=""):
    """Convenience function for tutoring"""
    return bedrock_client.generate_tutoring_response(question, context)


def invoke_claude_for_career(user_profile, career_goal, question=""):
    """Convenience function for career coaching"""
    return bedrock_client.generate_career_advice(user_profile, career_goal, question)


def invoke_claude_for_assessment(submission, criteria):
    """Convenience function for assessments"""
    return bedrock_client.generate_assessment_feedback(submission, criteria)
