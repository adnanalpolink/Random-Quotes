import streamlit as st
import requests
import json
import random
from datetime import datetime
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Random Quote Generator",
    page_icon="💬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .quote-container {
        background-color: #f8f9fa;
        border-left: 5px solid #6c757d;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .quote-text {
        font-size: 24px;
        font-style: italic;
        color: #343a40;
    }
    .quote-author {
        margin-top: 10px;
        text-align: right;
        font-weight: bold;
        color: #495057;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border-radius: 4px;
        padding: 10px 24px;
        font-weight: bold;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .favorites-section {
        margin-top: 40px;
        border-top: 1px solid #dee2e6;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Function to fetch quotes
@st.cache_data(ttl=3600)
def fetch_quotes():
    try:
        response = requests.get("https://type.fit/api/quotes")
        quotes = response.json()
        return quotes
    except:
        # Fallback quotes if API fails
        return [
            {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
            {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
            {"text": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
            {"text": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
            {"text": "Success is not final, failure is not fatal: It is the courage to continue that counts.", "author": "Winston Churchill"}
        ]

# Initialize session state for favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Main app
st.title("✨ Random Quote Generator")

# Get quotes
quotes = fetch_quotes()

# Extract unique categories/tags (using authors as proxy for categories in this API)
authors = list(set([quote.get("author", "Unknown").replace(", type.fit", "") for quote in quotes]))
authors = [author for author in authors if author and author != "Unknown" and author != "null"]

# Sidebar for filtering
st.sidebar.title("Quote Filters")
selected_author = st.sidebar.selectbox("Filter by Author", ["All Authors"] + sorted(authors))

# Apply filters
if selected_author != "All Authors":
    filtered_quotes = [q for q in quotes if q.get("author", "Unknown").replace(", type.fit", "") == selected_author]
else:
    filtered_quotes = quotes

# Main quote display
if st.button("Generate Random Quote", key="main_button"):
    if filtered_quotes:
        random_quote = random.choice(filtered_quotes)
        quote_text = random_quote.get("text", "")
        quote_author = random_quote.get("author", "Unknown").replace(", type.fit", "")
        if quote_author == "null":
            quote_author = "Unknown"
            
        # Store current quote for potential saving
        st.session_state.current_quote = {
            "text": quote_text,
            "author": quote_author,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Display quote
        st.markdown(f"""
        <div class="quote-container">
            <div class="quote-text">"{quote_text}"</div>
            <div class="quote-author">— {quote_author}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add to favorites button
        if st.button("Add to Favorites"):
            if 'current_quote' in st.session_state:
                if st.session_state.current_quote not in st.session_state.favorites:
                    st.session_state.favorites.append(st.session_state.current_quote)
                    st.success("Quote added to favorites!")
                else:
                    st.info("This quote is already in your favorites!")
    else:
        st.error("No quotes found with the selected filters.")

# Quick category buttons
st.subheader("Popular Categories")
col1, col2, col3 = st.columns(3)

categories = ["Motivation", "Success", "Life", "Wisdom", "Leadership", "Happiness"]
author_mapping = {
    "Motivation": "Tony Robbins",
    "Success": "Zig Ziglar",
    "Life": "John Lennon",
    "Wisdom": "Albert Einstein",
    "Leadership": "Simon Sinek",
    "Happiness": "Dalai Lama"
}

with col1:
    if st.button("Motivation", key="cat1"):
        filtered_quotes = [q for q in quotes if "Tony Robbins" in q.get("author", "")]
        if filtered_quotes:
            random_quote = random.choice(filtered_quotes)
            st.session_state.current_quote = {
                "text": random_quote.get("text", ""),
                "author": random_quote.get("author", "Unknown").replace(", type.fit", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    if st.button("Success", key="cat2"):
        filtered_quotes = [q for q in quotes if "Zig Ziglar" in q.get("author", "")]
        if filtered_quotes:
            random_quote = random.choice(filtered_quotes)
            st.session_state.current_quote = {
                "text": random_quote.get("text", ""),
                "author": random_quote.get("author", "Unknown").replace(", type.fit", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

with col2:
    if st.button("Life", key="cat3"):
        filtered_quotes = [q for q in quotes if "John Lennon" in q.get("author", "")]
        if filtered_quotes:
            random_quote = random.choice(filtered_quotes)
            st.session_state.current_quote = {
                "text": random_quote.get("text", ""),
                "author": random_quote.get("author", "Unknown").replace(", type.fit", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    if st.button("Wisdom", key="cat4"):
        filtered_quotes = [q for q in quotes if "Einstein" in q.get("author", "")]
        if filtered_quotes:
            random_quote = random.choice(filtered_quotes)
            st.session_state.current_quote = {
                "text": random_quote.get("text", ""),
                "author": random_quote.get("author", "Unknown").replace(", type.fit", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

with col3:
    if st.button("Leadership", key="cat5"):
        filtered_quotes = [q for q in quotes if "Simon Sinek" in q.get("author", "")]
        if filtered_quotes:
            random_quote = random.choice(filtered_quotes)
            st.session_state.current_quote = {
                "text": random_quote.get("text", ""),
                "author": random_quote.get("author", "Unknown").replace(", type.fit", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    if st.button("Happiness", key="cat6"):
        filtered_quotes = [q for q in quotes if "Dalai Lama" in q.get("author", "")]
        if filtered_quotes:
            random_quote = random.choice(filtered_quotes)
            st.session_state.current_quote = {
                "text": random_quote.get("text", ""),
                "author": random_quote.get("author", "Unknown").replace(", type.fit", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

# Display current quote if selected from category
if 'current_quote' in st.session_state:
    st.markdown(f"""
    <div class="quote-container">
        <div class="quote-text">"{st.session_state.current_quote['text']}"</div>
        <div class="quote-author">— {st.session_state.current_quote['author']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add to favorites button for category-selected quotes
    if st.button("Add to Favorites", key="fav_cat"):
        if st.session_state.current_quote not in st.session_state.favorites:
            st.session_state.favorites.append(st.session_state.current_quote)
            st.success("Quote added to favorites!")
        else:
            st.info("This quote is already in your favorites!")

# Favorites section
st.markdown('<div class="favorites-section"></div>', unsafe_allow_html=True)
st.subheader("Your Favorite Quotes")

if st.session_state.favorites:
    # Convert to DataFrame for better display
    df = pd.DataFrame(st.session_state.favorites)
    
    # Display each favorite quote
    for i, row in df.iterrows():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"""
            <div class="quote-container" style="margin: 5px 0;">
                <div class="quote-text" style="font-size: 18px;">"{row['text']}"</div>
                <div class="quote-author">— {row['author']}</div>
                <div style="font-size: 12px; color: #6c757d;">Saved on {row['timestamp']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.favorites.pop(i)
                st.experimental_rerun()
    
    # Export favorites as CSV
    if st.button("Export Favorites"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="favorite_quotes.csv",
            mime="text/csv",
        )
    
    # Clear all favorites
    if st.button("Clear All Favorites"):
        st.session_state.favorites = []
        st.success("All favorites cleared!")
        st.experimental_rerun()
else:
    st.info("You haven't added any favorites yet. Click 'Add to Favorites' on quotes you like!")

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit | Data source: type.fit API", 
    unsafe_allow_html=True
)
