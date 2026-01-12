# app/utils/unipile_integration.py
"""Unipile API integration for LinkedIn connectivity"""

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class UnipileClient:
    """Unipile API client for LinkedIn integration"""
    
    def __init__(self):
        """Initialize Unipile client"""
        self.api_key = os.getenv("UNIPILE_API_KEY")
        self.base_url = os.getenv("UNIPILE_BASE_URL", "https://api.unipile.com/v1")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.available = bool(self.api_key)
        
        if self.available:
            print("✅ Unipile client initialized successfully")
        else:
            print("⚠️ Unipile API key not found. LinkedIn features will be limited.")
    
    def connect_linkedin_account(self, user_id, linkedin_credentials=None):
        """
        Connect a LinkedIn account via Unipile
        
        Args:
            user_id: Application user ID
            linkedin_credentials: Optional LinkedIn credentials
            
        Returns:
            Connection response with account info
        """
        if not self.available:
            return {"error": "Unipile API not configured"}
        
        endpoint = f"{self.base_url}/accounts"
        
        payload = {
            "provider": "linkedin",
            "user_id": user_id,
        }
        
        if linkedin_credentials:
            payload["credentials"] = linkedin_credentials
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting LinkedIn account: {str(e)}")
            return {"error": str(e)}
    
    def get_linkedin_profile(self, account_id):
        """
        Fetch LinkedIn profile data via Unipile
        
        Args:
            account_id: Unipile account ID
            
        Returns:
            LinkedIn profile data
        """
        if not self.available:
            return {"error": "Unipile API not configured"}
        
        endpoint = f"{self.base_url}/accounts/{account_id}/profile"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            profile_data = response.json()
            
            # Parse and structure the profile data
            return self._parse_linkedin_profile(profile_data)
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching LinkedIn profile: {str(e)}")
            return {"error": str(e)}
    
    def _parse_linkedin_profile(self, raw_profile):
        """Parse raw LinkedIn profile data into structured format"""
        return {
            "name": raw_profile.get("name", ""),
            "headline": raw_profile.get("headline", ""),
            "location": raw_profile.get("location", ""),
            "summary": raw_profile.get("summary", ""),
            "experience": raw_profile.get("experience", []),
            "education": raw_profile.get("education", []),
            "skills": raw_profile.get("skills", []),
            "certifications": raw_profile.get("certifications", []),
            "profile_url": raw_profile.get("profile_url", ""),
            "profile_picture": raw_profile.get("profile_picture", ""),
            "connections_count": raw_profile.get("connections_count", 0),
            "fetched_at": datetime.now().isoformat()
        }
    
    def post_to_linkedin(self, account_id, post_content, media=None):
        """
        Post content to LinkedIn via Unipile
        
        Args:
            account_id: Unipile account ID
            post_content: Text content to post
            media: Optional media attachments
            
        Returns:
            Post response with post ID
        """
        if not self.available:
            return {"error": "Unipile API not configured"}
        
        endpoint = f"{self.base_url}/accounts/{account_id}/posts"
        
        payload = {
            "text": post_content
        }
        
        if media:
            payload["media"] = media
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            return {
                "success": True,
                "post_id": result.get("id"),
                "post_url": result.get("url"),
                "posted_at": datetime.now().isoformat()
            }
        except requests.exceptions.RequestException as e:
            print(f"❌ Error posting to LinkedIn: {str(e)}")
            return {"error": str(e), "success": False}
    
    def get_account_info(self, account_id):
        """
        Get Unipile account information
        
        Args:
            account_id: Unipile account ID
            
        Returns:
            Account info including connection status
        """
        if not self.available:
            return {"error": "Unipile API not configured"}
        
        endpoint = f"{self.base_url}/accounts/{account_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching account info: {str(e)}")
            return {"error": str(e)}
    
    def disconnect_account(self, account_id):
        """
        Disconnect a LinkedIn account
        
        Args:
            account_id: Unipile account ID
            
        Returns:
            Disconnection confirmation
        """
        if not self.available:
            return {"error": "Unipile API not configured"}
        
        endpoint = f"{self.base_url}/accounts/{account_id}"
        
        try:
            response = requests.delete(endpoint, headers=self.headers)
            response.raise_for_status()
            return {"success": True, "message": "Account disconnected"}
        except requests.exceptions.RequestException as e:
            print(f"❌ Error disconnecting account: {str(e)}")
            return {"error": str(e), "success": False}


# Global instance
unipile_client = UnipileClient()


def get_unipile_client():
    """Get the global Unipile client instance"""
    return unipile_client


def fetch_linkedin_profile_via_unipile(account_id):
    """Convenience function to fetch LinkedIn profile"""
    return unipile_client.get_linkedin_profile(account_id)


def post_to_linkedin_via_unipile(account_id, content, media=None):
    """Convenience function to post to LinkedIn"""
    return unipile_client.post_to_linkedin(account_id, content, media)


def connect_linkedin_via_unipile(user_id, credentials=None):
    """Convenience function to connect LinkedIn account"""
    return unipile_client.connect_linkedin_account(user_id, credentials)
