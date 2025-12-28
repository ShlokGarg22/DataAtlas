"""
DataScout Pro - Advanced Dataset Hub
Main dashboard for discovering AI datasets across multiple sources
"""

import streamlit as st
from sources import hf_service, wiki_service, yt_service, reddit_service, stack_overflow_service, kaggle_service

# Page configuration
st.set_page_config(
    page_title="DataScout Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title and description
st.title("🔍 DataScout Pro")
st.markdown("### Discover AI Datasets Across Multiple Sources")
st.markdown("---")

# Primary topic input
topic = st.text_input(
    "What specific topic or domain is your AI project about?",
    placeholder="e.g., medical imaging, sentiment analysis, code generation...",
    help="Enter the main focus area for your AI project"
)

# Sidebar for advanced filters
st.sidebar.header("🎯 Advanced Filters")

# Data Type Focus filter
data_type_filter = st.sidebar.selectbox(
    "Data Type Focus",
    options=[
        "All Types",
        "Conversational (Dialog)",
        "Factual (Knowledge-Base)",
        "Instructional (Fine-tuning)",
        "Q&A",
        "Code Snippets",
        "Multimedia (Audio/Video)"
    ],
    help="Select the primary type of data you need"
)

# Desired Format filter
format_filter = st.sidebar.multiselect(
    "Desired Format",
    options=["JSONL", "CSV", "Markdown", "Raw Text", "Audio (Metadata)", "Parquet"],
    default=["JSONL", "CSV"],
    help="Select one or more preferred data formats"
)

# Access & Cost filter
cost_filter = st.sidebar.radio(
    "Access & Cost",
    options=["All Sources", "Free & Open-Source", "Paid/Commercial API"],
    help="Filter by data access cost"
)

# Include Sources filter
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Data Sources")
sources_dict = {
    "Hugging Face": True,
    "Wikipedia": True,
    "YouTube": True,
    "Reddit": True,
    "Stack Overflow": True,
    "Kaggle": True
}

# Create checkboxes for each source
selected_sources = {}
for source_name, default_value in sources_dict.items():
    selected_sources[source_name] = st.sidebar.checkbox(
        source_name,
        value=default_value,
        help=f"Search {source_name} for relevant datasets"
    )

# Search button
st.markdown("---")
search_button = st.button("🚀 Discover Data", type="primary", use_container_width=True)

# Initialize session state for results
if 'results' not in st.session_state:
    st.session_state.results = []

# Search execution
if search_button:
    if not topic.strip():
        st.error("⚠️ Please enter a topic to search for datasets.")
    else:
        st.session_state.results = []
        
        # Show progress
        with st.spinner("🔎 Searching across multiple sources..."):
            progress_bar = st.progress(0)
            
            # Map of sources to their service modules
            source_map = {
                "Hugging Face": hf_service,
                "Wikipedia": wiki_service,
                "YouTube": yt_service,
                "Reddit": reddit_service,
                "Stack Overflow": stack_overflow_service,
                "Kaggle": kaggle_service
            }
            
            # Search each selected source
            total_sources = sum(selected_sources.values())
            current_source = 0
            
            for source_name, is_selected in selected_sources.items():
                if is_selected:
                    try:
                        service = source_map[source_name]
                        results = service.search(topic, data_type_filter, format_filter, cost_filter)
                        st.session_state.results.extend(results)
                    except Exception as e:
                        st.warning(f"⚠️ Error searching {source_name}: {str(e)}")
                    
                    current_source += 1
                    progress_bar.progress(current_source / total_sources)
            
            progress_bar.empty()
        
        # Display success message
        if st.session_state.results:
            st.success(f"✅ Found {len(st.session_state.results)} results across {sum(selected_sources.values())} sources!")
        else:
            st.info("ℹ️ No results found. Try adjusting your filters or topic.")

# Display results
if st.session_state.results:
    st.markdown("---")
    st.header("📊 Search Results")
    
    # Group results by source
    results_by_source = {}
    for result in st.session_state.results:
        source = result['source']
        if source not in results_by_source:
            results_by_source[source] = []
        results_by_source[source].append(result)
    
    # Display results grouped by source
    for source, results in results_by_source.items():
        st.subheader(f"🔹 {source} Results ({len(results)})")
        
        # Create columns for better layout
        for idx, result in enumerate(results):
            with st.expander(f"📄 {result['title']}", expanded=(idx == 0)):
                # Create two columns for metadata
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {result['description']}")
                    st.markdown(f"**URL:** [{result['url']}]({result['url']})")
                
                with col2:
                    # Display badges
                    st.markdown(f"**Type:** `{result['type']}`")
                    st.markdown(f"**Format:** `{result['format']}`")
                    
                    # Cost badge with color
                    if result['cost'] == "Free":
                        st.markdown(f"**Cost:** :green[{result['cost']}]")
                    elif result['cost'] == "Paid":
                        st.markdown(f"**Cost:** :orange[{result['cost']}]")
                    else:
                        st.markdown(f"**Cost:** {result['cost']}")
                
                # Preview URL if available
                if result.get('preview_url'):
                    st.markdown(f"**Preview:** [{result['preview_url']}]({result['preview_url']})")
                
                # Action buttons
                button_col1, button_col2 = st.columns(2)
                with button_col1:
                    if st.button(f"📥 View Raw Data", key=f"raw_{idx}_{source}"):
                        st.info("🚧 Raw data viewer coming soon!")
                with button_col2:
                    if st.button(f"📤 Export Mock", key=f"export_{idx}_{source}"):
                        st.info("🚧 Export functionality coming soon!")
        
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>DataScout Pro v1.0 | Built with Streamlit | 
        <a href='https://github.com' target='_blank'>GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)