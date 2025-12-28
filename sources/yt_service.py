"""
YouTube Search Service
Searches for YouTube videos with transcripts that can be used as data
"""

from typing import List, Dict, Optional
import urllib.parse
import requests
from .groq_helper import get_ai_recommendations, generate_smart_query

def search(topic: str, data_type_filter: str, format_filter: List[str], cost_filter: str) -> List[Dict]:
    """
    Generate YouTube search URLs for videos related to the topic
    Note: This service generates search URLs rather than direct API calls
    to avoid requiring YouTube API credentials
    
    Args:
        topic: The search topic/domain
        data_type_filter: Type of data (Conversational, Factual, etc.)
        format_filter: List of desired formats
        cost_filter: Cost preference (Free, Paid, All)
    
    Returns:
        List of data cards with standardized format
    """
    results = []
    
    # YouTube transcripts are only suitable for certain data types
    suitable_types = [
        "All Types",
        "Conversational (Dialog)",
        "Factual (Knowledge-Base)",
        "Instructional (Fine-tuning)",
        "Multimedia (Audio/Video)"
    ]
    
    # Skip if data type filter doesn't match
    if data_type_filter not in suitable_types:
        return results
    
    # YouTube is always free (public videos)
    if cost_filter == "Paid/Commercial API":
        return results
    
    # YouTube transcripts are typically Raw Text or Audio Metadata
    yt_formats = ["Raw Text", "Audio (Metadata)"]
    if format_filter and not any(fmt in format_filter for fmt in yt_formats):
        return results
    
    try:
        # Use Groq AI to get specific video recommendations
        ai_recommendations = get_ai_recommendations(topic, "YouTube", data_type_filter)
        
        # For each AI recommendation, create a search link to find the actual video
        for idx, rec in enumerate(ai_recommendations[:5]):  # Limit to 5
            # Create a targeted search query
            search_query = f"{rec['title']} {' '.join(rec.get('keywords', []))}"
            encoded_query = urllib.parse.quote_plus(search_query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            # Determine data type
            if "tutorial" in rec['title'].lower() or "course" in rec['title'].lower():
                data_type = "Instructional (Fine-tuning)"
            elif "lecture" in rec['title'].lower() or "explained" in rec['title'].lower():
                data_type = "Factual (Knowledge-Base)"
            else:
                data_type = "Multimedia (Audio/Video)"
            
            data_card = {
                "source": "YouTube",
                "title": rec['title'],
                "description": f"{rec['description']}\n\n💡 AI Recommendation: {rec.get('relevance', 'Highly relevant to your topic')}",
                "url": search_url,
                "type": data_type,
                "format": "Raw Text",
                "cost": "Free",
                "preview_url": search_url
            }
            
            results.append(data_card)
        
        # Add generic searches if AI didn't return enough results
        if len(results) < 3:
            optimized_query = generate_smart_query(topic, data_type_filter)
            encoded_query = urllib.parse.quote_plus(optimized_query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            data_card = {
                "source": "YouTube",
                "title": f"YouTube: {optimized_query}",
                "description": f"AI-optimized search for '{optimized_query}'. Videos may contain transcripts that can be extracted for training data using youtube-transcript-api.",
                "url": search_url,
                "type": "Multimedia (Audio/Video)",
                "format": "Raw Text",
                "cost": "Free",
                "preview_url": search_url
            }
            
            results.append(data_card)
        
        # Add a generic note about transcript extraction
        data_card = {
            "source": "YouTube",
            "title": "💡 YouTube Transcript Extraction Guide",
            "description": "Use the youtube-transcript-api library to extract transcripts from any YouTube video. Simply provide the video ID to get subtitle text in various languages. Great for conversational and educational datasets.",
            "url": "https://pypi.org/project/youtube-transcript-api/",
            "type": "Multimedia (Audio/Video)",
            "format": "Raw Text",
            "cost": "Free",
            "preview_url": "https://github.com/jdepoix/youtube-transcript-api"
        }
        
        results.append(data_card)
        
    except Exception as e:
        # Return error as a result card
        results.append({
            "source": "YouTube",
            "title": "Search Error",
            "description": f"Unable to generate YouTube searches: {str(e)}",
            "url": "https://youtube.com",
            "type": "Error",
            "format": "N/A",
            "cost": "N/A",
            "preview_url": None
        })
    
    return results