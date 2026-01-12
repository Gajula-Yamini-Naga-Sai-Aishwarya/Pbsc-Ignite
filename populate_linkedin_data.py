"""
Populate LinkedIn Profile Data for Existing Users
Creates hardcoded/sample LinkedIn data for testing features
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "PBSC-Ignite-db")

# Sample LinkedIn data templates
LINKEDIN_PROFILES = [
    {
        "full_name": "Sarah Johnson",
        "headline": "Computer Science Student | Aspiring Software Engineer | Passionate about AI & Machine Learning",
        "location": "Palm Beach, FL",
        "profile_url": "https://www.linkedin.com/in/sarah-johnson-dev",
        "summary": "Motivated computer science student with a passion for creating innovative solutions through code. Currently focusing on full-stack development and machine learning applications.",
        "skills": [
            "Python", "JavaScript", "React", "Node.js", "Machine Learning",
            "Data Analysis", "SQL", "Git", "Problem Solving", "Team Collaboration"
        ],
        "education": [
            {
                "institution": "Palm Beach State College",
                "degree": "Associate in Science - Computer Science",
                "field_of_study": "Computer Science",
                "start_date": "2024-08",
                "end_date": "2026-05",
                "description": "GPA: 3.7 | Dean's List | Focus on Software Development and AI"
            }
        ],
        "experience": [
            {
                "title": "Student Developer",
                "company": "PBSC Tech Lab",
                "location": "Lake Worth, FL",
                "start_date": "2025-01",
                "end_date": None,
                "current": True,
                "description": "Developing web applications and assisting fellow students with coding challenges."
            }
        ],
        "certifications": [
            "Python for Data Science - Coursera",
            "Web Development Fundamentals - freeCodeCamp"
        ]
    },
    {
        "full_name": "Michael Chen",
        "headline": "Data Analytics Student | Business Intelligence Enthusiast | Future Data Scientist",
        "location": "Boca Raton, FL",
        "profile_url": "https://www.linkedin.com/in/michael-chen-data",
        "summary": "Data-driven problem solver pursuing a career in data analytics and business intelligence. Experienced in turning complex data into actionable insights.",
        "skills": [
            "Python", "SQL", "Excel", "Tableau", "Power BI",
            "Data Visualization", "Statistics", "R Programming", "Data Mining", "Critical Thinking"
        ],
        "education": [
            {
                "institution": "Palm Beach State College",
                "degree": "Associate in Arts - Data Analytics",
                "field_of_study": "Data Science",
                "start_date": "2023-08",
                "end_date": "2025-05",
                "description": "Focus on Statistical Analysis and Business Intelligence"
            }
        ],
        "experience": [
            {
                "title": "Data Analytics Intern",
                "company": "Local Business Solutions",
                "location": "Boca Raton, FL",
                "start_date": "2024-06",
                "end_date": "2024-12",
                "current": False,
                "description": "Analyzed customer data and created dashboards for business insights."
            }
        ],
        "certifications": [
            "Google Data Analytics Certificate",
            "SQL for Data Science - Coursera"
        ]
    },
    {
        "full_name": "Emily Rodriguez",
        "headline": "Cybersecurity Student | Information Security Advocate | Ethical Hacker in Training",
        "location": "West Palm Beach, FL",
        "profile_url": "https://www.linkedin.com/in/emily-rodriguez-cyber",
        "summary": "Passionate about protecting digital assets and learning the latest cybersecurity practices. Committed to making the internet a safer place.",
        "skills": [
            "Network Security", "Python", "Linux", "Penetration Testing",
            "Security Auditing", "Risk Assessment", "Encryption", "Firewalls", "Incident Response", "Compliance"
        ],
        "education": [
            {
                "institution": "Palm Beach State College",
                "degree": "Associate in Science - Cybersecurity",
                "field_of_study": "Information Security",
                "start_date": "2024-01",
                "end_date": "2026-05",
                "description": "Specializing in Network Security and Ethical Hacking"
            }
        ],
        "experience": [
            {
                "title": "IT Security Assistant",
                "company": "PBSC IT Department",
                "location": "Lake Worth, FL",
                "start_date": "2024-08",
                "end_date": None,
                "current": True,
                "description": "Assisting with security audits and helping maintain network security protocols."
            }
        ],
        "certifications": [
            "CompTIA Security+ (In Progress)",
            "Cybersecurity Fundamentals - Cisco"
        ]
    },
    {
        "full_name": "David Martinez",
        "headline": "UX/UI Design Student | Creative Problem Solver | Future Product Designer",
        "location": "Boynton Beach, FL",
        "profile_url": "https://www.linkedin.com/in/david-martinez-ux",
        "summary": "Creative designer passionate about creating user-centered digital experiences. Combining aesthetics with functionality to build intuitive interfaces.",
        "skills": [
            "Figma", "Adobe XD", "UI Design", "UX Research", "Prototyping",
            "User Testing", "Wireframing", "HTML/CSS", "Responsive Design", "Design Thinking"
        ],
        "education": [
            {
                "institution": "Palm Beach State College",
                "degree": "Associate in Arts - Digital Design",
                "field_of_study": "UX/UI Design",
                "start_date": "2023-08",
                "end_date": "2025-12",
                "description": "Focus on User Experience and Interface Design"
            }
        ],
        "experience": [
            {
                "title": "UX Design Intern",
                "company": "Creative Digital Agency",
                "location": "West Palm Beach, FL",
                "start_date": "2024-05",
                "end_date": "2024-08",
                "current": False,
                "description": "Created wireframes and prototypes for client projects. Conducted user research and usability testing."
            }
        ],
        "certifications": [
            "Google UX Design Certificate",
            "Figma Master Course - Udemy"
        ]
    },
    {
        "full_name": "Jessica Williams",
        "headline": "Software Engineering Student | Full-Stack Developer | Open Source Contributor",
        "location": "Delray Beach, FL",
        "profile_url": "https://www.linkedin.com/in/jessica-williams-dev",
        "summary": "Aspiring software engineer with hands-on experience in full-stack development. Enthusiastic about building scalable web applications and contributing to open-source projects.",
        "skills": [
            "JavaScript", "Python", "React", "Node.js", "MongoDB",
            "PostgreSQL", "REST APIs", "Docker", "Git", "Agile Methodologies"
        ],
        "education": [
            {
                "institution": "Palm Beach State College",
                "degree": "Associate in Science - Software Engineering",
                "field_of_study": "Computer Programming",
                "start_date": "2024-01",
                "end_date": "2026-05",
                "description": "GPA: 3.9 | President's List | Full-Stack Development Track"
            }
        ],
        "experience": [
            {
                "title": "Junior Web Developer",
                "company": "Tech Startup FL",
                "location": "Delray Beach, FL",
                "start_date": "2024-09",
                "end_date": None,
                "current": True,
                "description": "Building and maintaining web applications using React and Node.js. Collaborating with team using Agile methodologies."
            }
        ],
        "certifications": [
            "Full-Stack Web Development - freeCodeCamp",
            "MongoDB Developer Certification"
        ]
    }
]

def populate_linkedin_data():
    """Populate LinkedIn data for users in the database"""
    
    print("=" * 70)
    print("📊 POPULATING LINKEDIN DATA FOR USERS")
    print("=" * 70)
    
    try:
        # Connect to MongoDB
        print(f"\n📡 Connecting to MongoDB at {MONGO_URI}...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Test connection
        client.server_info()
        print(f"✅ Successfully connected to MongoDB")
        print(f"📊 Database: {DB_NAME}\n")
        
        # Get all users
        users = list(db.users.find({}))
        
        if not users:
            print("⚠️  No users found in database!")
            print("\n💡 Creating sample users with LinkedIn data...")
            
            # Create sample users
            sample_users = []
            for i, profile in enumerate(LINKEDIN_PROFILES):
                user_id = profile['full_name'].lower().replace(' ', '_')
                sample_user = {
                    "user_id": user_id,
                    "email": f"{user_id}@pbsc.edu",
                    "full_name": profile['full_name'],
                    "password": "$2b$12$KIX8Qb3Y5iNQ7kF8L1O9qO9Zm9Qb3Y5iNQ7kF8L1O9qO9Zm9Qb3Y5",  # hashed "password123"
                    "created_at": datetime.now().isoformat(),
                    "linkedin_data": profile,
                    "linkedin_connected": True,
                    "linkedin_account_id": f"linkedin_acc_{i+1000}",
                    "linkedin_profile_url": profile['profile_url'],
                    "auto_sharing_enabled": False,
                    "linkedin_last_updated": datetime.now().isoformat()
                }
                sample_users.append(sample_user)
            
            # Insert sample users
            result = db.users.insert_many(sample_users)
            print(f"✅ Created {len(result.inserted_ids)} sample users with LinkedIn data")
            users = sample_users
        
        else:
            print(f"📋 Found {len(users)} existing user(s) in database\n")
            
            # Update existing users with LinkedIn data
            updated_count = 0
            for i, user in enumerate(users):
                # Assign a LinkedIn profile (cycle through available profiles)
                profile = LINKEDIN_PROFILES[i % len(LINKEDIN_PROFILES)]
                
                # Update user with LinkedIn data
                update_data = {
                    "linkedin_data": profile,
                    "linkedin_connected": True,
                    "linkedin_account_id": f"linkedin_acc_{user.get('user_id', 'user')}_1000",
                    "linkedin_profile_url": profile['profile_url'],
                    "auto_sharing_enabled": False,
                    "linkedin_last_updated": datetime.now().isoformat()
                }
                
                db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": update_data}
                )
                updated_count += 1
                
                print(f"✅ Updated user: {user.get('user_id', user.get('email'))}")
                print(f"   LinkedIn Profile: {profile['full_name']}")
                print(f"   Headline: {profile['headline'][:60]}...")
                print()
            
            print(f"\n✅ Updated {updated_count} user(s) with LinkedIn data")
        
        # Verify the data
        print("\n" + "=" * 70)
        print("📊 VERIFICATION - Users with LinkedIn Data")
        print("=" * 70)
        
        users_with_linkedin = db.users.find({"linkedin_connected": True})
        count = 0
        for user in users_with_linkedin:
            count += 1
            linkedin_data = user.get('linkedin_data', {})
            print(f"\n{count}. User ID: {user.get('user_id', user.get('email'))}")
            print(f"   Name: {linkedin_data.get('full_name', 'N/A')}")
            print(f"   Headline: {linkedin_data.get('headline', 'N/A')[:70]}...")
            print(f"   Skills: {len(linkedin_data.get('skills', []))} skills")
            print(f"   Education: {len(linkedin_data.get('education', []))} entries")
            print(f"   Experience: {len(linkedin_data.get('experience', []))} entries")
        
        print("\n" + "=" * 70)
        print(f"✅ SUCCESS! {count} user(s) now have LinkedIn data")
        print("=" * 70)
        print("\n💡 You can now use this data for:")
        print("   - Career coaching features")
        print("   - Personalized recommendations")
        print("   - Chat/tutor interactions")
        print("   - Profile analysis")
        print("   - Skill gap analysis")
        print("\n🚀 Ready to test features with realistic LinkedIn data!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if client:
            client.close()
            print("\n🔌 Database connection closed")

if __name__ == "__main__":
    populate_linkedin_data()
