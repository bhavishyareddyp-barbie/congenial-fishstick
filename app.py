import streamlit as st
import requests

# --------------------------------
# CONFIG
# --------------------------------
API_KEY = "pub_a3798fb1fa1c4a85a7c7cf07a6de8b18"
BASE_URL = "https://newsdata.io/api/1/news"

st.set_page_config(
    page_title="NewsData News App",
    layout="wide"
)

st.title("📰 Advanced News Headlines App")
st.write("Get latest news using NewsData.io")

# --------------------------------
# SIDEBAR FILTERS
# --------------------------------
st.sidebar.header("Filters")

country_options = {
    "India": "in",
    "USA": "us",
    "UK": "gb",
    "Canada": "ca",
    "Australia": "au",
    "UAE": "ae"
}

selected_country = st.sidebar.selectbox(
    "Select Country",
    list(country_options.keys())
)

category = st.sidebar.selectbox(
    "Select Category",
    [
        "top",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology",
        "politics",
        "world"
    ]
)

keyword = st.text_input(
    "🔍 Search Keyword",
    placeholder="e.g. AI, cricket, Tesla"
)

article_count = st.slider(
    "Number of Articles",
    min_value=5,
    max_value=20,
    value=10
)

# --------------------------------
# FETCH NEWS FUNCTION
# --------------------------------
def fetch_news(country, category, keyword):
    params = {
        "apikey": API_KEY,
        "country": country,
        "category": category,
        "language": "en"
    }

    if keyword:
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        st.error("Failed to fetch news")
        st.json(response.json())
        return []

# --------------------------------
# BUTTON
# --------------------------------
if st.button("Get News"):
    with st.spinner("Fetching latest headlines..."):

        articles = fetch_news(
            country_options[selected_country],
            category,
            keyword
        )

        articles = articles[:article_count]

    if articles:
        st.success(f"Found {len(articles)} articles")

        for article in articles:
            st.markdown("---")

            title = article.get("title", "No Title")
            description = article.get("description", "No description")
            image = article.get("image_url")
            source = article.get("source_id", "Unknown")
            date = article.get("pubDate", "")
            link = article.get("link")

            col1, col2 = st.columns([1, 2])

            with col1:
                if image:
                    st.image(image, use_container_width=True)

            with col2:
                st.subheader(title)
                st.write(f"**Source:** {source}")
                st.write(f"**Published:** {date}")

                if description:
                    st.write(description)

                st.markdown(
                    f"[📖 Read Full Article]({link})"
                )

    else:
        st.warning("No news articles found.")