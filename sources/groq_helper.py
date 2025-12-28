"""
Groq AI Helper
Uses Groq API to enhance search results and find relevant datasets
"""

from groq import Groq
from typing import List, Dict
import json

# Groq API configuration
GROQ_API_KEY = "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"

def _get_client():
    """Get or create Groq client"""
    return Groq(api_key=GROQ_API_KEY)

def get_ai_recommendations(topic: str, source: str, data_type: str) -> List[Dict]:
    """
    Use Groq AI to get specific dataset recommendations
    
    Args:
        topic: The search topic
        source: The data source (YouTube, Reddit, etc.)
        data_type: The type of data needed
    
    Returns:
        List of AI-generated recommendations
    """
    try:
        client = _get_client()
        
        prompt = f"""You are a dataset discovery expert. For the topic "{topic}" and data type "{data_type}", 
suggest 3-5 SPECIFIC, REAL resources from {source} that would be excellent for building AI training datasets.

For each resource, provide:
1. Exact title/name
2. Brief description (50-100 words)
3. Why it's valuable for this specific topic

Format your response as a JSON array with this structure:
[
  {{
    "title": "specific resource title",
    "description": "detailed description",
    "keywords": ["keyword1", "keyword2"],
    "relevance": "why this is valuable"
  }}
]

Be specific and realistic. Only suggest resources that likely exist."""

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful dataset discovery assistant that provides accurate, specific recommendations for AI training data sources."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse the AI response
        ai_text = response.choices[0].message.content
        
        # Try to extract JSON from the response
        start_idx = ai_text.find('[')
        end_idx = ai_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = ai_text[start_idx:end_idx]
            recommendations = json.loads(json_str)
            return recommendations
        
        return []
        
    except Exception as e:
        print(f"Groq API error: {str(e)}")
        return []

def generate_smart_query(topic: str, data_type: str) -> str:
    """
    Use Groq AI to generate an optimized search query
    
    Args:
        topic: The search topic
        data_type: The type of data needed
    
    Returns:
        Optimized search query string
    """
    try:
        client = _get_client()
        
        prompt = f"""Generate the most effective search query to find datasets about "{topic}" 
for {data_type} data. Return ONLY the search query, no explanation."""

        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=100
        )
        
        query = response.choices[0].message.content.strip().strip('"').strip("'")
        return query
        
    except Exception as e:
        return topic
