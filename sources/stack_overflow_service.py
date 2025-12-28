"""
Stack Overflow Search Service
Generates Stack Overflow search URLs for finding Q&A and code snippets
"""

from typing import List, Dict, Optional
import urllib.parse
from .groq_helper import get_ai_recommendations, generate_smart_query

def search(topic: str, data_type_filter: str, format_filter: List[str], cost_filter: str) -> List[Dict]:
    """
    Generate Stack Overflow search URLs for finding Q&A and code snippets
    
    Args:
        topic: The search topic/domain
        data_type_filter: Type of data (Conversational, Factual, etc.)
        format_filter: List of desired formats
        cost_filter: Cost preference (Free, Paid, All)
    
    Returns:
        List of data cards with standardized format
    """
    results = []
    
    # Stack Overflow is primarily suitable for Q&A and code snippets
    suitable_types = [
        "All Types",
        "Q&A",
        "Code Snippets",
        "Instructional (Fine-tuning)"
    ]
    
    # Skip if data type filter doesn't match
    if data_type_filter not in suitable_types:
        return results
    
    # Stack Overflow content is always free
    if cost_filter == "Paid/Commercial API":
        return results
    
    # Stack Overflow content is typically Raw Text, Markdown, or code
    so_formats = ["Raw Text", "Markdown", "JSONL"]
    if format_filter and not any(fmt in format_filter for fmt in so_formats):
        return results
    
    try:
        # Use Groq AI to get specific Stack Overflow topic recommendations
        ai_recommendations = get_ai_recommendations(topic, "Stack Overflow", data_type_filter)
        
        # For each AI recommendation, create targeted Stack Overflow searches
        for idx, rec in enumerate(ai_recommendations[:3]):  # Limit to 3
            search_term = rec['title']
            encoded_query = urllib.parse.quote_plus(search_term)
            search_url = f"https://stackoverflow.com/search?q={encoded_query}"
            
            # Determine data type based on content
            title_lower = rec['title'].lower()
            if "code" in title_lower or "example" in title_lower:
                data_type = "Code Snippets"
            elif "how to" in title_lower or "tutorial" in title_lower:
                data_type = "Instructional (Fine-tuning)"
            else:
                data_type = "Q&A"
            
            data_card = {
                "source": "Stack Overflow",
                "title": rec['title'],
                "description": f"{rec['description']}\n\n💡 AI Insight: {rec.get('relevance', 'Valuable for code-related datasets')}",
                "url": search_url,
                "type": data_type,
                "format": "Markdown",
                "cost": "Free",
                "preview_url": search_url
            }
            
            results.append(data_card)
        
        # Add AI-optimized searches with specific intent
        optimized_query = generate_smart_query(topic, data_type_filter)
        
        search_variations = [
            ("General Q&A", optimized_query, "Q&A"),
            ("Code Examples", f"{optimized_query} code example", "Code Snippets")
        ]
        
        # Create data cards for each search variation
        for search_type, query, data_type in search_variations:
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://stackoverflow.com/search?q={encoded_query}&sort=votes"
            
            data_card = {
                "source": "Stack Overflow",
                "title": f"{search_type}: {optimized_query}",
                "description": f"AI-optimized search for {search_type.lower()} about '{optimized_query}'. Results sorted by votes for highest quality content. Stack Overflow Q&A pairs are excellent for training coding assistants.",
                "url": search_url,
                "type": data_type,
                "format": "Markdown",
                "cost": "Free",
                "preview_url": search_url
            }
            
            results.append(data_card)
        
        # Add a tagged search (more specific)
        tag_query = topic.replace(" ", "-").lower()
        tagged_url = f"https://stackoverflow.com/questions/tagged/{tag_query}"
        
        data_card = {
            "source": "Stack Overflow",
            "title": f"Tag: {tag_query}",
            "description": f"Browse all highly-rated questions tagged '{tag_query}'. Tagged questions are curated by the community and contain the most relevant content.",
            "url": tagged_url,
            "type": "Q&A",
            "format": "Markdown",
            "cost": "Free",
            "preview_url": tagged_url
        }
        
        results.append(data_card)
        
        # Add a note about Stack Exchange API
        data_card = {
            "source": "Stack Overflow",
            "title": "💡 Stack Exchange API",
            "description": "Use the Stack Exchange API to programmatically collect questions, answers, and code snippets. The API provides structured access to millions of Q&A pairs across programming topics. No authentication required for read access (rate limits apply).",
            "url": "https://api.stackexchange.com/docs",
            "type": "Q&A",
            "format": "JSONL",
            "cost": "Free",
            "preview_url": "https://stackapps.com/questions/tagged/api"
        }
        
        results.append(data_card)
        
    except Exception as e:
        # Return error as a result card
        results.append({
            "source": "Stack Overflow",
            "title": "Search Error",
            "description": f"Unable to generate Stack Overflow searches: {str(e)}",
            "url": "https://stackoverflow.com",
            "type": "Error",
            "format": "N/A",
            "cost": "N/A",
            "preview_url": None
        })
    
    return results