"""
Hugging Face Hub Search Service
Searches for datasets on Hugging Face Hub based on user filters
"""

from huggingface_hub.hf_api import HfApi, list_datasets
from typing import List, Dict, Optional

def search(topic: str, data_type_filter: str, format_filter: List[str], cost_filter: str) -> List[Dict]:
    """
    Search Hugging Face Hub for datasets matching the topic and filters
    
    Args:
        topic: The search topic/domain
        data_type_filter: Type of data (Conversational, Factual, etc.)
        format_filter: List of desired formats
        cost_filter: Cost preference (Free, Paid, All)
    
    Returns:
        List of data cards with standardized format
    """
    results = []
    
    try:
        # Initialize Hugging Face API
        api = HfApi()
        
        # Build search query based on data type
        search_query = topic.lower()
        
        # Map data type to potential tags/keywords
        type_keywords = {
            "Conversational (Dialog)": ["conversational", "dialogue", "chat"],
            "Factual (Knowledge-Base)": ["knowledge", "facts", "qa", "question-answering"],
            "Instructional (Fine-tuning)": ["instruction", "finetune", "training"],
            "Q&A": ["qa", "question-answering", "questions"],
            "Code Snippets": ["code", "programming", "github"],
            "Multimedia (Audio/Video)": ["audio", "video", "speech", "multimodal"]
        }
        
        # Search datasets with topic
        datasets = list(list_datasets(search=search_query, limit=10))
        
        # Process each dataset
        for dataset in datasets:
            # Determine format (default to common HF formats)
            dataset_format = "Parquet"
            if "csv" in str(dataset.tags).lower():
                dataset_format = "CSV"
            elif "json" in str(dataset.tags).lower():
                dataset_format = "JSONL"
            
            # Check if format matches filter (if filter is specified)
            if format_filter and dataset_format not in format_filter:
                continue
            
            # Determine data type based on tags
            dataset_type = "General"
            if data_type_filter != "All Types":
                type_key = data_type_filter
                if type_key in type_keywords:
                    keywords = type_keywords[type_key]
                    tags_str = " ".join(dataset.tags).lower()
                    if not any(kw in tags_str for kw in keywords):
                        continue
                    dataset_type = data_type_filter
            
            # All HF datasets are free and open-source
            cost = "Free"
            if cost_filter == "Paid/Commercial API":
                continue
            
            # Build data card
            # Get description safely - cardData may not always have description
            description = "No description available"
            if hasattr(dataset, 'cardData') and dataset.cardData:
                description = str(dataset.cardData)[:200] + "..."
            elif hasattr(dataset, 'id'):
                description = f"Hugging Face dataset: {dataset.id}"
            
            data_card = {
                "source": "Hugging Face",
                "title": dataset.id,
                "description": description,
                "url": f"https://huggingface.co/datasets/{dataset.id}",
                "type": dataset_type,
                "format": dataset_format,
                "cost": cost,
                "preview_url": f"https://huggingface.co/datasets/{dataset.id}/viewer"
            }
            
            results.append(data_card)
        
    except Exception as e:
        # Return error as a result card
        results.append({
            "source": "Hugging Face",
            "title": "Search Error",
            "description": f"Unable to search Hugging Face: {str(e)}",
            "url": "https://huggingface.co/datasets",
            "type": "Error",
            "format": "N/A",
            "cost": "N/A",
            "preview_url": None
        })
    
    return results