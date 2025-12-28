"""
Kaggle Search Service
Generates Kaggle search URLs for finding datasets and competitions
"""

from typing import List, Dict, Optional
import urllib.parse
from .groq_helper import get_ai_recommendations, generate_smart_query

def search(topic: str, data_type_filter: str, format_filter: List[str], cost_filter: str) -> List[Dict]:
    """
    Generate Kaggle search URLs for finding datasets and competitions
    
    Args:
        topic: The search topic/domain
        data_type_filter: Type of data (Conversational, Factual, etc.)
        format_filter: List of desired formats
        cost_filter: Cost preference (Free, Paid, All)
    
    Returns:
        List of data cards with standardized format
    """
    results = []
    
    # Kaggle is suitable for most structured data types
    suitable_types = [
        "All Types",
        "Factual (Knowledge-Base)",
        "Instructional (Fine-tuning)",
        "Code Snippets",
        "Multimedia (Audio/Video)"
    ]
    
    # Skip if data type filter doesn't match
    if data_type_filter not in suitable_types:
        return results
    
    # Kaggle datasets are always free
    if cost_filter == "Paid/Commercial API":
        return results
    
    # Kaggle supports various formats
    kaggle_formats = ["CSV", "JSONL", "Parquet", "Raw Text"]
    if format_filter and not any(fmt in format_filter for fmt in kaggle_formats):
        return results
    
    try:
        # Use Groq AI to get specific Kaggle dataset recommendations
        ai_recommendations = get_ai_recommendations(topic, "Kaggle", data_type_filter)
        
        # For each AI recommendation, create targeted Kaggle dataset links
        for idx, rec in enumerate(ai_recommendations[:4]):  # Limit to 4
            search_term = rec['title']
            keywords = rec.get('keywords', [])
            
            # Create a more specific search query
            search_query = f"{search_term} {' '.join(keywords[:2])}"
            encoded_query = urllib.parse.quote_plus(search_query)
            dataset_search_url = f"https://www.kaggle.com/datasets?search={encoded_query}"
            
            data_card = {
                "source": "Kaggle",
                "title": rec['title'],
                "description": f"{rec['description']}\n\n💡 AI Recommendation: {rec.get('relevance', 'Highly relevant dataset for your needs')}",
                "url": dataset_search_url,
                "type": "Factual (Knowledge-Base)",
                "format": "CSV",
                "cost": "Free",
                "preview_url": dataset_search_url
            }
            
            results.append(data_card)
        
        # Add AI-optimized general searches
        optimized_query = generate_smart_query(topic, data_type_filter)
        
        # Generate dataset search URL
        encoded_query = urllib.parse.quote_plus(optimized_query)
        dataset_search_url = f"https://www.kaggle.com/datasets?search={encoded_query}&sort=hotness"
        
        data_card = {
            "source": "Kaggle",
            "title": f"Kaggle Datasets: {optimized_query}",
            "description": f"AI-optimized search for '{optimized_query}' datasets. Results sorted by popularity. Kaggle hosts thousands of high-quality, community-curated datasets with CSV and structured formats.",
            "url": dataset_search_url,
            "type": "Factual (Knowledge-Base)",
            "format": "CSV",
            "cost": "Free",
            "preview_url": dataset_search_url
        }
        
        results.append(data_card)
        
        # Generate competition search URL
        competition_search_url = f"https://www.kaggle.com/competitions?search={encoded_query}"
        
        data_card = {
            "source": "Kaggle",
            "title": f"Kaggle Competitions: {optimized_query}",
            "description": f"Browse competitions related to '{optimized_query}'. Competition datasets are often large-scale, well-labeled, and designed for real-world ML challenges.",
            "url": competition_search_url,
            "type": "Instructional (Fine-tuning)",
            "format": "CSV",
            "cost": "Free",
            "preview_url": competition_search_url
        }
        
        results.append(data_card)
        
        # Generate code/notebooks search URL with optimized query
        code_search_url = f"https://www.kaggle.com/code?search={encoded_query}"
        
        data_card = {
            "source": "Kaggle",
            "title": f"Kaggle Notebooks: {optimized_query}",
            "description": f"AI-optimized search for notebooks about '{optimized_query}'. Notebooks contain code examples, data analysis workflows, and model implementations.",
            "url": code_search_url,
            "type": "Code Snippets",
            "format": "Markdown",
            "cost": "Free",
            "preview_url": code_search_url
        }
        
        results.append(data_card)
        
        # Add a note about Kaggle API
        data_card = {
            "source": "Kaggle",
            "title": "💡 Kaggle API Access",
            "description": "Use the Kaggle API to programmatically download datasets, competition data, and notebooks. The API provides command-line tools and Python bindings for automated data collection. Requires free Kaggle account and API token.",
            "url": "https://www.kaggle.com/docs/api",
            "type": "Factual (Knowledge-Base)",
            "format": "CSV",
            "cost": "Free",
            "preview_url": "https://github.com/Kaggle/kaggle-api"
        }
        
        results.append(data_card)
        
        # Add popular dataset categories relevant to the topic
        categories = {
            "machine learning": "Classification",
            "nlp": "NLP",
            "computer vision": "Computer Vision",
            "image": "Image Data",
            "text": "Text Data",
            "time series": "Time Series",
            "deep learning": "Deep Learning"
        }
        
        # Check if topic matches any category
        topic_lower = topic.lower()
        for key, category in categories.items():
            if key in topic_lower:
                category_url = f"https://www.kaggle.com/datasets?tags={urllib.parse.quote_plus(category)}"
                
                data_card = {
                    "source": "Kaggle",
                    "title": f"Kaggle {category} Datasets",
                    "description": f"Browse curated {category} datasets on Kaggle. These datasets are tagged and categorized for easy discovery of domain-specific data.",
                    "url": category_url,
                    "type": "Factual (Knowledge-Base)",
                    "format": "CSV",
                    "cost": "Free",
                    "preview_url": category_url
                }
                
                results.append(data_card)
                break  # Only add one category match
        
    except Exception as e:
        # Return error as a result card
        results.append({
            "source": "Kaggle",
            "title": "Search Error",
            "description": f"Unable to generate Kaggle searches: {str(e)}",
            "url": "https://kaggle.com",
            "type": "Error",
            "format": "N/A",
            "cost": "N/A",
            "preview_url": None
        })
    
    return results