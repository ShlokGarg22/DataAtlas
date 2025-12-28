"""
Reddit Search Service
Generates Reddit search URLs for finding datasets and discussions
Note: Uses direct URL generation to avoid requiring Reddit API credentials
"""

from typing import List, Dict, Optional
import urllib.parse
from .groq_helper import get_ai_recommendations, generate_smart_query

def search(topic: str, data_type_filter: str, format_filter: List[str], cost_filter: str) -> List[Dict]:
    """
    Generate Reddit search URLs for finding datasets and relevant discussions
    
    Args:
        topic: The search topic/domain
        data_type_filter: Type of data (Conversational, Factual, etc.)
        format_filter: List of desired formats
        cost_filter: Cost preference (Free, Paid, All)
    
    Returns:
        List of data cards with standardized format
    """
    results = []
    
    # Reddit is suitable for most data types, especially conversational
    suitable_types = [
        "All Types",
        "Conversational (Dialog)",
        "Q&A",
        "Instructional (Fine-tuning)"
    ]
    
    # Skip if data type filter doesn't match
    if data_type_filter not in suitable_types:
        return results
    
    # Reddit content is always free
    if cost_filter == "Paid/Commercial API":
        return results
    
    # Reddit content is typically Raw Text or JSONL (via API)
    reddit_formats = ["Raw Text", "JSONL", "CSV"]
    if format_filter and not any(fmt in format_filter for fmt in reddit_formats):
        return results
    
    try:
        # Use Groq AI to get specific subreddit and discussion recommendations
        ai_recommendations = get_ai_recommendations(topic, "Reddit", data_type_filter)
        
        # For each AI recommendation, create targeted Reddit links
        for idx, rec in enumerate(ai_recommendations[:4]):  # Limit to 4
            # Extract potential subreddit from keywords or create search
            keywords = rec.get('keywords', [])
            search_term = rec['title']
            
            # Create a more targeted search
            encoded_query = urllib.parse.quote_plus(f"{search_term} dataset")
            search_url = f"https://www.reddit.com/search/?q={encoded_query}"
            
            data_card = {
                "source": "Reddit",
                "title": rec['title'],
                "description": f"{rec['description']}\n\n💡 AI Insight: {rec.get('relevance', 'Relevant for your dataset needs')}",
                "url": search_url,
                "type": "Conversational (Dialog)",
                "format": "Raw Text",
                "cost": "Free",
                "preview_url": search_url
            }
            
            results.append(data_card)
        
        # Add searches in relevant subreddits with AI-optimized query
        optimized_query = generate_smart_query(topic, data_type_filter)
        
        # Relevant subreddits for dataset discovery
        dataset_subreddits = [
            ("datasets", "Dataset Discovery Hub"),
            ("MachineLearning", "ML Community Datasets"),
            ("datascience", "Data Science Resources")
        ]
        
        # Generate search URLs for each relevant subreddit
        for subreddit, description in dataset_subreddits[:2]:  # Limit to 2 subreddits
            encoded_query = urllib.parse.quote_plus(optimized_query)
            search_url = f"https://www.reddit.com/r/{subreddit}/search/?q={encoded_query}&restrict_sr=1&sort=relevance"
            
            # Create data card
            data_card = {
                "source": "Reddit",
                "title": f"r/{subreddit}: {optimized_query}",
                "description": f"{description} - AI-optimized search for '{optimized_query}' in r/{subreddit}. Find community-recommended datasets and discussions.",
                "url": search_url,
                "type": "Q&A",
                "format": "Raw Text",
                "cost": "Free",
                "preview_url": search_url
            }
            
            results.append(data_card)
        
        # Add a note about Reddit API usage
        data_card = {
            "source": "Reddit",
            "title": "💡 Reddit API Data Collection",
            "description": "Use PRAW (Python Reddit API Wrapper) to programmatically collect Reddit posts and comments. Great for building conversational datasets, Q&A pairs, and community knowledge bases. Requires Reddit API credentials.",
            "url": "https://praw.readthedocs.io/",
            "type": "Conversational (Dialog)",
            "format": "JSONL",
            "cost": "Free",
            "preview_url": "https://www.reddit.com/wiki/api"
        }
        
        results.append(data_card)
        
    except Exception as e:
        # Return error as a result card
        results.append({
            "source": "Reddit",
            "title": "Search Error",
            "description": f"Unable to generate Reddit searches: {str(e)}",
            "url": "https://reddit.com",
            "type": "Error",
            "format": "N/A",
            "cost": "N/A",
            "preview_url": None
        })
    
    return results