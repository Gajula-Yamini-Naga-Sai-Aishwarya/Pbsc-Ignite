# COMPLETE OPTIMIZED career_coach.py - Cache processed profile data

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from markdown2 import Markdown
from app.utils.llm_utils import LEO_ai_response, fetch_linkedin_profile, fetch_github_projects
from app.utils.db_utils import get_db, get_user_by_id
import json
import time

# UPDATED: Import simple profile manager
from app.utils.simple_profile_manager import get_profile_summary_for_llm

# Initialize markdown converter
markdowner = Markdown()

# Career coach blueprint
career_coach_bp = Blueprint('career_coach_bp', __name__)

# 🚀 OPTIMIZED CACHE: LEO AI user data cache with processed profile
LEO_user_cache = {}
LEO_cache_timestamps = {}
LEO_CACHE_DURATION = 300  # 5 minutes

def process_user_profile_data(user_data):
    """🚀 Process user profile data once and cache it (heavy work done once)"""
    if not user_data:
        return {
            'name': 'Student',
            'headline': 'No headline available',
            'summary': 'No summary available',
            'geo': 'Location not specified',
            'certifications_str': 'None',
            'skills_str': 'None',
            'projects_str': 'None',
            'honors_str': 'None',
            'github_projects_str': 'None'
        }
    
    print("🔧 Processing user profile data for caching...")
    
    try:
        # Extract basic info
        name = f"{user_data.get('firstName', 'there')} {user_data.get('lastName', '')}".strip()
        headline = user_data.get("headline", "No headline available")
        summary = user_data.get("summary", "No summary available")
        geo = user_data.get("geo", {}).get("full", "Location not specified")
        github_username = user_data.get("github_username", None)
        
        # Process certifications
        certifications = user_data.get("certifications", [])
        certifications_str = []
        for cert in certifications:
            cert_name = cert.get("name", "Unnamed Certification")
            cert_authority = cert.get("authority", "Unknown Authority")
            cert_company = cert.get("company", {}).get("name", "Unknown Company")
            cert_time = f"{cert.get('start', {}).get('year', 'Unknown Start Year')} - {cert.get('end', {}).get('year', 'Unknown End Year')}"
            certifications_str.append(f"{cert_name} ({cert_authority} - {cert_company} - {cert_time})")
        
        certifications_str = ', '.join(certifications_str) if certifications_str else 'None'
        
        # Process honors
        honors = user_data.get("honors", [])
        honors_str = []
        for honor in honors:
            honor_title = honor.get("title", "Unknown Honor")
            honor_description = honor.get("description", "No description available")
            honor_issuer = honor.get("issuer", "Unknown Issuer")
            honor_time = f"{honor.get('issuedOn', {}).get('year', 'Unknown Year')}"
            honors_str.append(f"{honor_title} - {honor_description} (Issued by {honor_issuer} in {honor_time})")
        
        honors_str = ', '.join(honors_str) if honors_str else 'None'
        
        # Process skills
        skills = user_data.get("skills", [])
        skills_str = ', '.join([skill.get("name", "Unknown Skill") for skill in skills]) if skills else 'None'

        # Process projects
        projects = user_data.get("projects", {}).get("items", [])
        projects_str = ', '.join([proj.get("title", "Unknown Project") for proj in projects]) if projects else 'None'

        # Process GitHub projects (this is expensive, so cache it)
        github_projects_str = "None"
        if github_username:
            try:
                github_projects = fetch_github_projects(github_username)
                if isinstance(github_projects, list):
                    github_projects_str = ', '.join([f"{proj['title']}: {proj['description']}" for proj in github_projects])
                else:
                    github_projects_str = str(github_projects)
            except Exception as e:
                print(f"⚠️ GitHub projects error: {e}")
                github_projects_str = "GitHub data unavailable"
        
        processed_data = {
            'name': name,
            'headline': headline,
            'summary': summary,
            'geo': geo,
            'certifications_str': certifications_str,
            'skills_str': skills_str,
            'projects_str': projects_str,
            'honors_str': honors_str,
            'github_projects_str': github_projects_str
        }
        
        print(f"✅ Profile data processed: {len(str(processed_data))} chars")
        return processed_data
        
    except Exception as e:
        print(f"❌ Profile processing error: {e}")
        return {
            'name': 'Student',
            'headline': 'Profile processing error',
            'summary': 'Unable to process profile data',
            'geo': 'Location not specified',
            'certifications_str': 'None',
            'skills_str': 'None',
            'projects_str': 'None',
            'honors_str': 'None',
            'github_projects_str': 'None'
        }

def get_cached_LEO_data(user_id):
    """Cache user data AND processed profile data for LEO AI"""
    current_time = time.time()
    
    # Check cache
    if (user_id in LEO_user_cache and 
        user_id in LEO_cache_timestamps and 
        current_time - LEO_cache_timestamps[user_id] < LEO_CACHE_DURATION):
        
        print(f"🚀 LEO cache HIT for: {user_id}")
        return LEO_user_cache[user_id]
    
    print(f"🔄 LEO cache MISS for: {user_id}")
    
    try:
        # Get all user data in one go
        user_record = get_user_by_id(user_id)
        if not user_record:
            return None
        
        # Try multiple field names for LinkedIn URL (backward compatibility)
        linkedin_url = (user_record.get('linkedin_profile_url') or 
                       user_record.get('linkedinProfile') or 
                       user_record.get('linkedin_url'))
        
        # Fetch LinkedIn data if URL exists
        if linkedin_url:
            fetch_result = fetch_linkedin_profile(linkedin_url, user_id)
            print(f"📡 LinkedIn fetch: {fetch_result.get('message', 'Done')}")
        
        # Get LinkedIn data from database
        db = get_db()
        
        # Try to get LinkedIn data from users collection first (where we populated it)
        user_data = user_record.get('linkedin_data') if user_record else None
        
        # If not found, try the separate linkedin_data collection (backward compatibility)
        if not user_data:
            students_collection = db.linkedin_data
            user_data = students_collection.find_one({"user_id": user_id})
        
        # Get profile summary
        try:
            profile_summary = get_profile_summary_for_llm(user_id, max_tokens=800)
            if not profile_summary:
                profile_summary = f"Career Goal: {user_record.get('career_goal', 'Professional Development')}"
        except Exception as e:
            print(f"⚠️ Profile summary error: {e}")
            profile_summary = f"Career Goal: {user_record.get('career_goal', 'Professional Development')}"
        
        # 🚀 NEW: Process and cache the formatted profile data (do this heavy work once)
        processed_profile = process_user_profile_data(user_data)
        
        # Cache the combined data
        cached_data = {
            'user_record': user_record,
            'user_data': user_data,
            'profile_summary': profile_summary,
            'linkedin_url': linkedin_url,
            'processed_profile': processed_profile,  # 🚀 Cache processed data!
            'cached_at': current_time
        }
        
        LEO_user_cache[user_id] = cached_data
        LEO_cache_timestamps[user_id] = current_time
        
        print(f"✅ LEO data cached with processed profile for: {user_id}")
        return cached_data
        
    except Exception as e:
        print(f"❌ LEO cache error: {e}")
        return None

def generate_fast_prompt(processed_profile, user_query, chat_history):
    """🚀 FAST: Generate prompt using cached processed profile data"""
    
    # Build the history string (this is the only processing we do each time)
    history_str = ""
    if chat_history:
        recent_history = chat_history[-5:]  # Only last 5 conversations for speed
        for entry in recent_history:
            if isinstance(entry, dict) and 'prompt' in entry:
                user_msg = entry.get('prompt', '')[:100]  # Limit length
                bot_msg = entry.get('raw_response', entry.get('response', ''))[:100]  # Limit length
                history_str += f"User: {user_msg}\nBot: {bot_msg}\n"
    
    # Use cached processed profile data (no processing needed!)
    prompt = f"""
    CAREER COACHING CONVERSATION:
    
    Student Profile:
    - Name: {processed_profile['name']}
    - Professional Headline: {processed_profile['headline']}
    - Professional Summary: {processed_profile['summary'][:200]}
    - Location: {processed_profile['geo']}
    - Certifications: {processed_profile['certifications_str'][:200]}
    - Skills: {processed_profile['skills_str'][:200]}
    - LinkedIn Projects: {processed_profile['projects_str'][:200]}
    - Honors & Awards: {processed_profile['honors_str'][:200]}
    - GitHub Projects: {processed_profile['github_projects_str'][:200]}

    Previous Chat History:
    {history_str}

    Current Student Question: "{user_query}"

    Please provide personalized career coaching advice considering:
    1. The student's background and skills
    2. Current industry trends and job market
    3. Specific career goals and aspirations
    4. Practical next steps and recommendations
    """
    return prompt

def convert_LEO_json_to_text(response):
    """Convert LEO's JSON response to natural text format with proper formatting"""
    try:
        # Check if response is JSON format
        response_str = str(response).strip()
        
        if response_str.startswith('{') and response_str.endswith('}'):
            print("⚠️ Detected JSON response, converting to text format...")
            
            try:
                json_data = json.loads(response_str)
                
                # Build natural text response with proper formatting
                text_response = ""
                
                # Start with greeting/message
                if 'message' in json_data:
                    text_response += json_data['message']
                    if 'content' in json_data:
                        text_response += " " + json_data['content']
                    text_response += "\n\n"
                elif 'content' in json_data:
                    text_response += json_data['content'] + "\n\n"
                
                # Add industry trends with proper formatting
                if 'currentIndustryTrends' in json_data and json_data['currentIndustryTrends']:
                    text_response += "**🔥 Current Industry Trends:**\n\n"
                    for i, trend in enumerate(json_data['currentIndustryTrends'], 1):
                        text_response += f"{i}. {trend}\n"
                    text_response += "\n"
                
                # Add actionable advice
                if 'actionableAdvice' in json_data and json_data['actionableAdvice']:
                    text_response += "**🎯 Actionable Advice:**\n\n"
                    for i, advice in enumerate(json_data['actionableAdvice'], 1):
                        text_response += f"{i}. {advice}\n"
                    text_response += "\n"
                
                # Add next steps
                if 'nextSteps' in json_data and json_data['nextSteps']:
                    text_response += "**🚀 Next Steps:**\n\n"
                    for i, step in enumerate(json_data['nextSteps'], 1):
                        text_response += f"{i}. {step}\n"
                    text_response += "\n"
                
                # Add encouragement
                if 'encouragement' in json_data:
                    text_response += json_data['encouragement'] + "\n\n"
                
                # Add sources
                if 'sources' in json_data:
                    text_response += "**Sources:** "
                    for i, source in enumerate(json_data['sources'][:5], 1):
                        text_response += f"[{i}] {source} "
                
                print(f"✅ Converted JSON to text: {len(text_response)} chars")
                return text_response.strip()
                
            except json.JSONDecodeError:
                print("❌ Failed to parse JSON, returning original")
                return response_str
        
        # If it's already text format, return as-is
        return response_str
        
    except Exception as e:
        print(f"❌ Response conversion error: {e}")
        return str(response)

@career_coach_bp.route('/your-career_coach-LEO011', methods=['POST', 'GET'])
def career_coach():
    if "user_id" not in session:
        return redirect(url_for("auth_bp.sign_in"))
    
    db = get_db()
    LEO_chat_history = db.career_coach
    
    if request.method == 'POST':
        user_id = session['user_id']
        user_query = request.form['userQuery']
        
        # Validate input
        if not user_query or not user_query.strip():
            flash("Please enter a message before sending.", "warning")
            return redirect(url_for('career_coach_bp.career_coach'))
        
        start_time = time.time()
        
        # 🚀 CACHED: Get all user data from cache
        cached_data = get_cached_LEO_data(user_id)
        if not cached_data:
            print(f"❌ No cached data found for user: {user_id}")
            flash("User data not found. Please update your profile with a career goal.", "warning")
            return redirect(url_for('main_bp.student_profile'))
        
        user_record = cached_data['user_record']
        user_data = cached_data['user_data']
        profile_summary = cached_data['profile_summary']
        linkedin_url = cached_data['linkedin_url']
        processed_profile = cached_data['processed_profile']  # 🚀 Get processed data from cache!
        
        print(f"⏱️ LEO user data retrieved: {time.time() - start_time:.2f}s")
        print(f"📊 LinkedIn URL: {linkedin_url}")
        print(f"📊 User Data: {bool(user_data)}")
        print(f"📊 Profile Summary: {profile_summary[:50]}...")
        
        # Check if we have LinkedIn data
        if not linkedin_url:
            print(f"⚠️ No LinkedIn URL found for user: {user_id}")
            flash("LinkedIn profile URL not found. Please add your LinkedIn profile in your student profile.", "warning")
            return redirect(url_for('main_bp.student_profile'))
        
        if not user_data:
            print(f"⚠️ No LinkedIn data found for user: {user_id}")
            flash("LinkedIn data not yet fetched. Please ensure your LinkedIn profile is public and try again.", "warning")
            return redirect(url_for('main_bp.student_profile'))

        try:
            # Get existing conversation (still need this from DB)
            conversation_start = time.time()
            existing_conversation = LEO_chat_history.find_one({"user_id": user_id})
            chat_history = existing_conversation.get("messages", []) if existing_conversation else []
            print(f"⏱️ Chat history retrieved: {time.time() - conversation_start:.2f}s")
            
            # 🚀 FAST: Generate prompt using cached processed profile data
            prompt_start = time.time()
            prompt = generate_fast_prompt(processed_profile, user_query, chat_history)
            print(f"⏱️ FAST prompt generated: {time.time() - prompt_start:.2f}s")
            
            # Get LEO's AI response (using cached profile!)
            LEO_start = time.time()
            print(f"🦁 LEO processing: {user_query[:50]}...")
            
            raw_response = LEO_ai_response(prompt, 1500, user_profile=profile_summary)
            
            LEO_time = time.time() - LEO_start
            print(f"⏱️ LEO AI response: {LEO_time:.2f}s")
            
            # Convert JSON response to text format if needed
            response = convert_LEO_json_to_text(raw_response)
            
            # Convert markdown response to HTML (preserve citations)
            html_response = markdowner.convert(response)

            # Store conversation
            db_start = time.time()
            if not existing_conversation:
                conversation_id = f"conv_{str(datetime.now().timestamp()).replace('.', '')}"
                new_conversation = {
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "messages": [
                        {
                            "prompt": user_query,
                            "response": html_response,
                            "raw_response": response,
                            "time": datetime.utcnow(),
                        },
                    ]
                }
                LEO_chat_history.insert_one(new_conversation)
                updated_messages = new_conversation["messages"]
            else:
                updated_messages = sorted(
                    [
                        {
                            "prompt": msg["prompt"], 
                            "response": msg.get("response", markdowner.convert(msg.get("raw_response", ""))),
                            "raw_response": msg.get("raw_response", ""),
                            "time": msg["time"]
                        }
                        for msg in existing_conversation["messages"]
                    ] + [{
                        "prompt": user_query, 
                        "response": html_response,
                        "raw_response": response,
                        "time": datetime.utcnow()
                    }],
                    key=lambda x: x["time"]
                )

                LEO_chat_history.update_one(
                    {"user_id": user_id},
                    {"$set": {"messages": updated_messages}}
                )
            
            print(f"⏱️ Database update: {time.time() - db_start:.2f}s")
            
            total_time = time.time() - start_time
            print(f"✅ LEO total response time: {total_time:.2f}s")

            return render_template(
                "career_coach.html", 
                messages=updated_messages
            )
            
        except Exception as e:
            print(f"❌ Career coach error: {e}")
            import traceback
            traceback.print_exc()
            flash("Sorry, I'm having some technical difficulties. Please try again later!", "error")
            return redirect(url_for('career_coach_bp.career_coach'))
    
    # GET request - show existing conversation or empty page
    else:
        user_id = session['user_id']
        existing_conversation = LEO_chat_history.find_one({"user_id": user_id})
        
        if existing_conversation:
            # Sort messages by time and ensure proper formatting
            messages = sorted(
                [
                    {
                        "prompt": msg["prompt"],
                        "response": msg.get("response", markdowner.convert(msg.get("raw_response", ""))),
                        "raw_response": msg.get("raw_response", ""),
                        "time": msg["time"]
                    }
                    for msg in existing_conversation["messages"]
                ],
                key=lambda x: x["time"]
            )
            return render_template("career_coach.html", messages=messages)
        else:
            return render_template("career_coach.html", messages=[])

@career_coach_bp.route('/clear-conversation', methods=['POST'])
def clear_conversation():
    """Clear the career coach conversation history"""
    if "user_id" not in session:
        return redirect(url_for("auth_bp.sign_in"))
    
    try:
        user_id = session['user_id']
        db = get_db()
        LEO_chat_history = db.career_coach
        
        result = LEO_chat_history.delete_one({"user_id": user_id})
        
        if result.deleted_count > 0:
            flash("Conversation history cleared successfully!", "success")
        else:
            flash("No conversation history found to clear.", "info")
            
    except Exception as e:
        print(f"❌ Clear conversation error: {e}")
        flash("Error clearing conversation history.", "error")
    
    return redirect(url_for('career_coach_bp.career_coach'))

print("🚀 Complete optimized LEO AI caching system loaded!")