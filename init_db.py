"""
Database Initialization Script for PBSC-Ignite Platform
This script creates all necessary MongoDB collections and indexes
"""

import os
import sys
from pymongo import MongoClient, ASCENDING, DESCENDING
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "PBSC-Ignite-db")

def initialize_database():
    """Initialize MongoDB database with collections and indexes"""
    
    print("=" * 60)
    print("PBSC-Ignite Database Initialization")
    print("=" * 60)
    
    try:
        # Connect to MongoDB
        print(f"\n📡 Connecting to MongoDB at {MONGO_URI}...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Test connection
        client.server_info()
        print(f"✅ Successfully connected to MongoDB")
        print(f"📊 Database: {DB_NAME}")
        
        # Collections to create
        collections = {
            'users': 'User accounts and profiles',
            'roadmaps': 'Personalized learning roadmaps',
            'assessments': 'User assessments and submissions',
            'chat_history': 'AI tutor conversation history',
            'career_coach_sessions': 'Career coaching sessions',
            'linkedin_profiles': 'Cached LinkedIn profile data',
            'progress_tracking': 'User learning progress',
            'resources': 'Learning resources and materials',
            'social_posts': 'LinkedIn post history',
            'achievements': 'User achievements and milestones'
        }
        
        print(f"\n📁 Creating collections...")
        existing_collections = db.list_collection_names()
        
        for collection_name, description in collections.items():
            if collection_name in existing_collections:
                print(f"  ✓ {collection_name} - already exists")
            else:
                db.create_collection(collection_name)
                print(f"  ✨ {collection_name} - created ({description})")
        
        # Create indexes for better performance
        print(f"\n🔍 Creating indexes...")
        
        # Users collection indexes
        db.users.create_index([("user_id", ASCENDING)], unique=True)
        db.users.create_index([("email", ASCENDING)], unique=True)
        print("  ✓ Users: user_id, email (unique)")
        
        # Roadmaps collection indexes
        db.roadmaps.create_index([("user_id", ASCENDING)])
        db.roadmaps.create_index([("created_at", DESCENDING)])
        print("  ✓ Roadmaps: user_id, created_at")
        
        # Assessments collection indexes
        db.assessments.create_index([("user_id", ASCENDING)])
        db.assessments.create_index([("assessment_type", ASCENDING)])
        db.assessments.create_index([("submitted_at", DESCENDING)])
        print("  ✓ Assessments: user_id, assessment_type, submitted_at")
        
        # Chat history indexes
        db.chat_history.create_index([("user_id", ASCENDING)])
        db.chat_history.create_index([("session_id", ASCENDING)])
        db.chat_history.create_index([("timestamp", DESCENDING)])
        print("  ✓ Chat History: user_id, session_id, timestamp")
        
        # Career coach sessions indexes
        db.career_coach_sessions.create_index([("user_id", ASCENDING)])
        db.career_coach_sessions.create_index([("created_at", DESCENDING)])
        print("  ✓ Career Coach: user_id, created_at")
        
        # LinkedIn profiles indexes
        db.linkedin_profiles.create_index([("user_id", ASCENDING)], unique=True)
        db.linkedin_profiles.create_index([("fetched_at", DESCENDING)])
        print("  ✓ LinkedIn Profiles: user_id (unique), fetched_at")
        
        # Progress tracking indexes
        db.progress_tracking.create_index([("user_id", ASCENDING)])
        db.progress_tracking.create_index([("phase_id", ASCENDING)])
        db.progress_tracking.create_index([("updated_at", DESCENDING)])
        print("  ✓ Progress Tracking: user_id, phase_id, updated_at")
        
        # Social posts indexes
        db.social_posts.create_index([("user_id", ASCENDING)])
        db.social_posts.create_index([("posted_at", DESCENDING)])
        print("  ✓ Social Posts: user_id, posted_at")
        
        # Achievements indexes
        db.achievements.create_index([("user_id", ASCENDING)])
        db.achievements.create_index([("achievement_type", ASCENDING)])
        db.achievements.create_index([("earned_at", DESCENDING)])
        print("  ✓ Achievements: user_id, achievement_type, earned_at")
        
        # Insert initial configuration document
        print(f"\n⚙️ Setting up configuration...")
        config = {
            "initialized_at": datetime.now().isoformat(),
            "version": "2.11",
            "database_name": DB_NAME,
            "collections_count": len(collections),
            "features": [
                "Personalized Learning Roadmaps",
                "AI Tutoring (LEO)",
                "Career Coaching",
                "Integrated Assessments",
                "LinkedIn Integration",
                "Progress Tracking"
            ]
        }
        
        db.config.replace_one(
            {"_id": "system_config"},
            {**config, "_id": "system_config"},
            upsert=True
        )
        print("  ✓ System configuration saved")
        
        # Database statistics
        print(f"\n📈 Database Statistics:")
        stats = db.command("dbstats")
        print(f"  • Collections: {stats.get('collections', 0)}")
        print(f"  • Data Size: {stats.get('dataSize', 0) / 1024:.2f} KB")
        print(f"  • Storage Size: {stats.get('storageSize', 0) / 1024:.2f} KB")
        
        print(f"\n{'=' * 60}")
        print("✅ Database initialization completed successfully!")
        print("=" * 60)
        print(f"\nYour database '{DB_NAME}' is ready to use.")
        print(f"You can now run the application with: python run.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {str(e)}")
        print(f"\nPlease check:")
        print(f"  1. MongoDB is running")
        print(f"  2. Connection string is correct: {MONGO_URI}")
        print(f"  3. You have necessary permissions")
        return False
    finally:
        if 'client' in locals():
            client.close()

def reset_database():
    """Reset database (drop all collections) - USE WITH CAUTION"""
    
    print("\n⚠️  WARNING: This will delete ALL data in the database!")
    confirmation = input(f"Type 'DELETE {DB_NAME}' to confirm: ")
    
    if confirmation != f"DELETE {DB_NAME}":
        print("❌ Operation cancelled.")
        return False
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        print(f"\n🗑️ Dropping database '{DB_NAME}'...")
        client.drop_database(DB_NAME)
        print("✅ Database dropped successfully")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error resetting database: {str(e)}")
        return False

def check_database_health():
    """Check database connection and health"""
    
    print("\n🏥 Checking Database Health...")
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.server_info()
        print("✅ MongoDB connection: OK")
        
        db = client[DB_NAME]
        
        # Check collections
        collections = db.list_collection_names()
        print(f"✅ Database '{DB_NAME}': {len(collections)} collections")
        
        # Check if initialized
        config = db.config.find_one({"_id": "system_config"})
        if config:
            print(f"✅ Database initialized: {config.get('initialized_at')}")
            print(f"✅ Version: {config.get('version')}")
        else:
            print("⚠️  Database not initialized. Run initialization first.")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Database health check failed: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PBSC-Ignite Database Management")
    parser.add_argument(
        'action',
        choices=['init', 'reset', 'check'],
        help='Action to perform: init (initialize), reset (delete all), check (health check)'
    )
    
    args = parser.parse_args()
    
    if args.action == 'init':
        initialize_database()
    elif args.action == 'reset':
        if reset_database():
            print("\nRe-initializing database...")
            initialize_database()
    elif args.action == 'check':
        check_database_health()
