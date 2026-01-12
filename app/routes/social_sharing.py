# app/routes/social_sharing.py
"""Social sharing routes for LinkedIn integration"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.utils.db_utils import get_user_by_id, db
from app.utils.post_generator import (
    generate_milestone_post,
    generate_project_post,
    generate_skill_post,
    generate_assessment_post
)
from app.utils.unipile_integration import (
    get_unipile_client,
    post_to_linkedin_via_unipile
)
from datetime import datetime
import json

# Social sharing blueprint
social_sharing_bp = Blueprint('social_sharing_bp', __name__, url_prefix='/social')

@social_sharing_bp.route("/share")
def share_page():
    """Social sharing dashboard page"""
    if "user_id" not in session:
        flash("Please log in to access social sharing features.", "warning")
        return redirect(url_for("auth_bp.sign_in"))
    
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth_bp.sign_in"))
    
    # Get user's recent achievements
    achievements = list(db.achievements.find({"user_id": user_id}).sort("earned_at", -1).limit(10))
    
    # Get post history
    post_history = list(db.social_posts.find({"user_id": user_id}).sort("posted_at", -1).limit(20))
    
    # Check LinkedIn connection status
    linkedin_profile = db.linkedin_profiles.find_one({"user_id": user_id})
    linkedin_connected = bool(linkedin_profile and linkedin_profile.get("account_id"))
    
    return render_template(
        "social_sharing.html",
        user=user,
        achievements=achievements,
        post_history=post_history,
        linkedin_connected=linkedin_connected
    )

@social_sharing_bp.route("/generate_post", methods=["POST"])
def generate_post():
    """Generate a LinkedIn post based on achievement/milestone"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        data = request.get_json()
        post_type = data.get("type", "milestone")
        
        user_name = user.get("name", "User")
        
        # Generate post based on type
        if post_type == "milestone":
            post_content = generate_milestone_post(
                user_name=user_name,
                milestone_data={
                    "achievement": data.get("achievement", "Completed a learning milestone"),
                    "career_goal": user.get("career_goal", "Career development"),
                    "skills": data.get("skills", []),
                    "duration": data.get("duration", "Recently")
                },
                tone=data.get("tone", "professional")
            )
        
        elif post_type == "project":
            post_content = generate_project_post(
                user_name=user_name,
                project_data={
                    "project_name": data.get("project_name", "Learning Project"),
                    "technologies": data.get("technologies", []),
                    "achievements": data.get("achievements", ""),
                    "learnings": data.get("learnings", ""),
                    "domain": data.get("domain", "software development")
                }
            )
        
        elif post_type == "skill":
            post_content = generate_skill_post(
                user_name=user_name,
                skill_data={
                    "skills": data.get("skills", []),
                    "career_goal": user.get("career_goal", "Professional development"),
                    "application": data.get("application", "Real-world projects"),
                    "next_steps": data.get("next_steps", "Continuing to learn"),
                    "domain": data.get("domain", "technology")
                }
            )
        
        elif post_type == "assessment":
            post_content = generate_assessment_post(
                user_name=user_name,
                assessment_data={
                    "type": data.get("assessment_type", "Assessment"),
                    "score": data.get("score", "successfully"),
                    "topics": data.get("topics", []),
                    "career_goal": user.get("career_goal", "career excellence")
                }
            )
        
        else:
            return jsonify({"error": "Invalid post type"}), 400
        
        # Store draft post
        draft_id = db.social_posts.insert_one({
            "user_id": user_id,
            "post_content": post_content,
            "post_type": post_type,
            "status": "draft",
            "metadata": data,
            "created_at": datetime.now().isoformat()
        }).inserted_id
        
        return jsonify({
            "success": True,
            "post_content": post_content,
            "draft_id": str(draft_id)
        })
    
    except Exception as e:
        print(f"❌ Error generating post: {str(e)}")
        return jsonify({"error": str(e)}), 500

@social_sharing_bp.route("/post_to_linkedin", methods=["POST"])
def post_to_linkedin():
    """Post content to LinkedIn via Unipile"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session["user_id"]
    
    try:
        data = request.get_json()
        post_content = data.get("post_content", "")
        draft_id = data.get("draft_id")
        
        if not post_content:
            return jsonify({"error": "Post content is required"}), 400
        
        # Get LinkedIn account info
        linkedin_profile = db.linkedin_profiles.find_one({"user_id": user_id})
        
        if not linkedin_profile or not linkedin_profile.get("account_id"):
            return jsonify({
                "error": "LinkedIn account not connected. Please connect your account first."
            }), 400
        
        account_id = linkedin_profile["account_id"]
        
        # Post to LinkedIn via Unipile
        unipile_client = get_unipile_client()
        result = post_to_linkedin_via_unipile(
            account_id=account_id,
            content=post_content,
            media=data.get("media")
        )
        
        if result.get("success"):
            # Update post record
            update_data = {
                "status": "published",
                "posted_at": datetime.now().isoformat(),
                "post_id": result.get("post_id"),
                "post_url": result.get("post_url")
            }
            
            if draft_id:
                db.social_posts.update_one(
                    {"_id": draft_id},
                    {"$set": update_data}
                )
            else:
                db.social_posts.insert_one({
                    "user_id": user_id,
                    "post_content": post_content,
                    **update_data
                })
            
            # Record achievement
            db.achievements.insert_one({
                "user_id": user_id,
                "achievement_type": "linkedin_post",
                "description": "Shared progress on LinkedIn",
                "earned_at": datetime.now().isoformat()
            })
            
            return jsonify({
                "success": True,
                "message": "Successfully posted to LinkedIn!",
                "post_url": result.get("post_url")
            })
        else:
            return jsonify({
                "error": result.get("error", "Failed to post to LinkedIn")
            }), 500
    
    except Exception as e:
        print(f"❌ Error posting to LinkedIn: {str(e)}")
        return jsonify({"error": str(e)}), 500

@social_sharing_bp.route("/connect_linkedin", methods=["POST"])
def connect_linkedin():
    """Connect LinkedIn account via Unipile"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session["user_id"]
    
    try:
        from app.utils.unipile_integration import connect_linkedin_via_unipile
        
        # This would typically involve OAuth flow
        # For now, we'll create a placeholder
        result = connect_linkedin_via_unipile(user_id)
        
        if not result.get("error"):
            # Store account info
            db.linkedin_profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "account_id": result.get("id"),
                        "connected_at": datetime.now().isoformat(),
                        "status": "connected"
                    }
                },
                upsert=True
            )
            
            return jsonify({
                "success": True,
                "message": "LinkedIn account connected successfully!"
            })
        else:
            return jsonify({
                "error": result.get("error")
            }), 500
    
    except Exception as e:
        print(f"❌ Error connecting LinkedIn: {str(e)}")
        return jsonify({"error": str(e)}), 500

@social_sharing_bp.route("/preview_post", methods=["POST"])
def preview_post():
    """Preview generated post before posting"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        # Simply return the post content for preview
        return jsonify({
            "success": True,
            "preview": data.get("post_content", "")
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@social_sharing_bp.route("/get_achievements")
def get_achievements():
    """Get user's achievements for sharing"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session["user_id"]
    
    try:
        # Get recent achievements
        achievements = list(db.achievements.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("earned_at", -1).limit(20))
        
        return jsonify({
            "success": True,
            "achievements": achievements
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@social_sharing_bp.route("/delete_post/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    """Delete a draft post"""
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session["user_id"]
    
    try:
        from bson import ObjectId
        
        result = db.social_posts.delete_one({
            "_id": ObjectId(post_id),
            "user_id": user_id,
            "status": "draft"
        })
        
        if result.deleted_count > 0:
            return jsonify({"success": True, "message": "Post deleted"})
        else:
            return jsonify({"error": "Post not found or already published"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
