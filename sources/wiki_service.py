"""
Wikipedia Search Service
Searches for Wikipedia articles that can serve as knowledge base data
"""

import wikipedia
from typing import List, Dict, Optional

def search(topic: str, data_type_filter: str, format_filter: List[str], cost_filter: str) -> List[Dict]:
    """
    Search Wikipedia for articles related to the topic
    
    Args:
        topic: The search topic/domain
        data_type_filter: Type of data (Conversational, Factual, etc.)
        format_filter: List of desired formats
        cost_filter: Cost preference (Free, Paid, All)
    
    Returns:
        List of data cards with standardized format
    """
    results = []
    
    # Wikipedia is only suitable for certain data types
    suitable_types = [
        "All Types",
        "Factual (Knowledge-Base)",
        "Q&A"
    ]
    
    # Skip if data type filter doesn't match
    if data_type_filter not in suitable_types:
        return results
    
    # Wikipedia is always free
    if cost_filter == "Paid/Commercial API":
        return results
    
    # Wikipedia content is typically Markdown or Raw Text
    wiki_formats = ["Markdown", "Raw Text"]
    if format_filter and not any(fmt in format_filter for fmt in wiki_formats):
        return results
    
    try:
        # Set language to English
        wikipedia.set_lang("en")
        
        # Search for articles
        search_results = wikipedia.search(topic, results=5)
        
        # Process each search result
        for title in search_results:
            try:
                # Get page summary
                page = wikipedia.page(title, auto_suggest=False)
                summary = page.summary[:250] + "..." if len(page.summary) > 250 else page.summary
                
                # Build data card
                data_card = {
                    "source": "Wikipedia",
                    "title": page.title,
                    "description": summary,
                    "url": page.url,
                    "type": "Factual (Knowledge-Base)",
                    "format": "Markdown",
                    "cost": "Free",
                    "preview_url": page.url
                }
                
                results.append(data_card)
                
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation pages by picking first option
                if e.options:
                    try:
                        page = wikipedia.page(e.options[0], auto_suggest=False)
                        summary = page.summary[:250] + "..." if len(page.summary) > 250 else page.summary
                        
                        data_card = {
                            "source": "Wikipedia",
                            "title": page.title,
                            "description": summary,
                            "url": page.url,
                            "type": "Factual (Knowledge-Base)",
                            "format": "Markdown",
                            "cost": "Free",
                            "preview_url": page.url
                        }
                        
                        results.append(data_card)
                    except:
                        continue
                        
            except wikipedia.exceptions.PageError:
                # Page not found, skip
                continue
            except Exception:
                # Other errors, skip this result
                continue
                
    except Exception as e:
        # Return error as a result card
        results.append({
            "source": "Wikipedia",
            "title": "Search Error",
            "description": f"Unable to search Wikipedia: {str(e)}",
            "url": "https://wikipedia.org",
            "type": "Error",
            "format": "N/A",
            "cost": "N/A",
            "preview_url": None
        })
    
    return results