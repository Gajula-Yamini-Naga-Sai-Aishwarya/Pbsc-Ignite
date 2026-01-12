"""
Check Database Data - Verify LinkedIn and Roadmap Storage
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "PBSC-Ignite-db")

def check_database():
    """Check what data is actually stored in the database"""
    
    print("=" * 80)
    print("🔍 DATABASE DATA VERIFICATION")
    print("=" * 80)
    
    try:
        # Connect to MongoDB
        print(f"\n📡 Connecting to MongoDB at {MONGO_URI}...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Test connection
        client.server_info()
        print(f"✅ Connected to Database: {DB_NAME}\n")
        
        # Check all collections
        print("=" * 80)
        print("📚 ALL COLLECTIONS IN DATABASE")
        print("=" * 80)
        collections = db.list_collection_names()
        for col in collections:
            count = db[col].count_documents({})
            print(f"  • {col}: {count} documents")
        
        # Check LinkedIn Data in Users Collection
        print("\n" + "=" * 80)
        print("👤 LINKEDIN DATA IN USERS COLLECTION")
        print("=" * 80)
        
        users = list(db.users.find({}))
        if not users:
            print("⚠️  No users found!")
        else:
            for i, user in enumerate(users, 1):
                print(f"\n--- User {i} ---")
                print(f"User ID: {user.get('user_id', 'N/A')}")
                print(f"Email: {user.get('email', 'N/A')}")
                
                # Check LinkedIn data
                linkedin_data = user.get('linkedin_data')
                if linkedin_data:
                    print(f"✅ HAS LINKEDIN DATA:")
                    print(f"   - Full Name: {linkedin_data.get('full_name', 'N/A')}")
                    print(f"   - Headline: {linkedin_data.get('headline', 'N/A')[:60]}...")
                    print(f"   - Skills: {len(linkedin_data.get('skills', []))} skills")
                    print(f"   - Education: {len(linkedin_data.get('education', []))} entries")
                    print(f"   - Experience: {len(linkedin_data.get('experience', []))} entries")
                    print(f"   - Location: {linkedin_data.get('location', 'N/A')}")
                else:
                    print(f"❌ NO LINKEDIN DATA")
                
                # Check LinkedIn connection info
                print(f"LinkedIn Connected: {user.get('linkedin_connected', False)}")
                print(f"LinkedIn Account ID: {user.get('linkedin_account_id', 'N/A')}")
                print(f"Auto Sharing: {user.get('auto_sharing_enabled', False)}")
        
        # Check LinkedIn Profiles Collection (separate collection)
        print("\n" + "=" * 80)
        print("🔗 LINKEDIN_PROFILES COLLECTION (Separate)")
        print("=" * 80)
        
        linkedin_profiles = list(db.linkedin_profiles.find({}))
        if not linkedin_profiles:
            print("⚠️  No data in linkedin_profiles collection (data is in users collection)")
        else:
            print(f"Found {len(linkedin_profiles)} profiles in separate collection")
            for profile in linkedin_profiles:
                print(f"  - {profile.get('full_name', 'N/A')}")
        
        # Check Roadmaps Data
        print("\n" + "=" * 80)
        print("🗺️  ROADMAP DATA")
        print("=" * 80)
        
        # Check roadmaps in users collection
        print("\n📍 Roadmaps in USERS collection:")
        users_with_roadmap = list(db.users.find({"road_map": {"$exists": True}}))
        if not users_with_roadmap:
            print("❌ No roadmaps found in users collection")
        else:
            for user in users_with_roadmap:
                print(f"\n✅ User: {user.get('user_id', user.get('email'))}")
                roadmap = user.get('road_map')
                if roadmap:
                    # Check if roadmap is a string (JSON) or dict
                    if isinstance(roadmap, str):
                        print(f"   ⚠️  Roadmap is stored as STRING (needs parsing)")
                        print(f"   Length: {len(roadmap)} characters")
                        try:
                            roadmap_dict = json.loads(roadmap)
                            print(f"   Career Path: {roadmap_dict.get('career_path', 'N/A')}")
                            print(f"   Phases: {len(roadmap_dict.get('phases', []))}")
                            for phase in roadmap_dict.get('phases', []):
                                print(f"      - {phase.get('phase_name', 'N/A')}")
                        except:
                            print(f"   ❌ Cannot parse roadmap JSON")
                    elif isinstance(roadmap, dict):
                        print(f"   ✅ Roadmap is stored as DICT (proper format)")
                        print(f"   Career Path: {roadmap.get('career_path', 'N/A')}")
                        print(f"   Phases: {len(roadmap.get('phases', []))}")
                        for phase in roadmap.get('phases', []):
                            print(f"      - {phase.get('phase_name', 'N/A')}")
                    else:
                        print(f"   ❌ Unknown roadmap format: {type(roadmap)}")
                
        # Check separate roadmaps collection
        print("\n📍 Roadmaps in ROADMAPS collection:")
        roadmaps_collection = list(db.roadmaps.find({}))
        if not roadmaps_collection:
            print("❌ No roadmaps in separate roadmaps collection")
        else:
            print(f"✅ Found {len(roadmaps_collection)} roadmap(s)")
            for roadmap in roadmaps_collection:
                print(f"   User ID: {roadmap.get('user_id', 'N/A')}")
                print(f"   Career Path: {roadmap.get('career_path', 'N/A')}")
                print(f"   Created: {roadmap.get('created_at', 'N/A')}")
        
        # Check active_modules (learning plans)
        print("\n" + "=" * 80)
        print("📚 LEARNING PLANS / ACTIVE MODULES")
        print("=" * 80)
        
        users_with_modules = list(db.users.find({"active_modules": {"$exists": True}}))
        if not users_with_modules:
            print("❌ No active modules/learning plans found")
        else:
            for user in users_with_modules:
                print(f"\n✅ User: {user.get('user_id', user.get('email'))}")
                modules = user.get('active_modules', [])
                print(f"   Active Modules: {len(modules)}")
                for module in modules:
                    print(f"      - Phase: {module.get('phase_id', 'N/A')}")
                    print(f"        Has Learning Plan: {bool(module.get('learning_plan'))}")
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 SUMMARY")
        print("=" * 80)
        total_users = db.users.count_documents({})
        users_with_linkedin = db.users.count_documents({"linkedin_data": {"$exists": True}})
        users_with_roadmaps = db.users.count_documents({"road_map": {"$exists": True}})
        separate_roadmaps = db.roadmaps.count_documents({})
        
        print(f"Total Users: {total_users}")
        print(f"Users with LinkedIn Data: {users_with_linkedin}")
        print(f"Users with Roadmaps (in users): {users_with_roadmaps}")
        print(f"Roadmaps in separate collection: {separate_roadmaps}")
        
        print("\n💡 STORAGE LOCATIONS:")
        print(f"   ✓ LinkedIn Data: Stored in 'users' collection")
        print(f"   ✓ Roadmaps: {'users collection' if users_with_roadmaps > 0 else 'NOT STORED'}")
        if separate_roadmaps > 0:
            print(f"   ✓ Also in 'roadmaps' collection: {separate_roadmaps} documents")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if client:
            client.close()
            print("\n🔌 Database connection closed")

if __name__ == "__main__":
    check_database()
