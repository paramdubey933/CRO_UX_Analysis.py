# app.py (refined, dark theme + no KPIs)
import streamlit as st
from PIL import Image
import os
from pathlib import Path

st.set_page_config(
    page_title="CRO / UX Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

#this lets your cloned repo give the needed output smoothly
BASE_DIR = Path(__file__).resolve().parent

SESSION_DIR = BASE_DIR / "analytics" / "session_analysis"
EDA_DIR = BASE_DIR / "analytics" / "eda"
ITEM_DIR = BASE_DIR / "analytics" / "item_funnel"

ACCENT = "#00BFA6"
BG = "#0E1117"
CARD = "#1A1C21"
TEXT = "#F1F3F6"
MUTED = "#9AA3AD"

st.markdown(
    f"""
    <style>
    /* General page background */
    .reportview-container, .main, .block-container {{
        background-color: {BG};
        color: {TEXT};
    }}
    /* Sidebar */
    section[data-testid="stSidebar"], .stSidebar, .css-1d391kg {{
        background-color: {CARD} !important;
        color: {TEXT} !important;
    }}
    /* Text and headings */
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {TEXT} !important;
    }}
    /* Buttons */
    .stButton>button {{
        background-color: {CARD} !important;
        color: {TEXT} !important;
        border: 1px solid #2b2f33 !important;
        border-radius: 8px !important;
        padding: .5rem 1rem !important;
    }}
    .stButton>button:hover {{
        background-color: #23262a !important;
        border-color: {ACCENT} !important;
    }}
    /* Image cards */
    .image-card {{
        box-shadow: 0 6px 18px rgba(0,0,0,0.6);
        border-radius: 8px;
        padding: 8px;
        background-color: #15171B;
    }}
    /* Info boxes */
    .stAlert {{
        border-radius: 8px !important;
    }}
    /* Footer */
    .footer {{
        color: {MUTED};
        font-size: 0.9rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

def safe_open_image(path: Path):
    try:
        return Image.open(path)
    except Exception:
        return None

def display_plot_with_insight(image_path: Path, insight: str, caption: str):
    if image_path.exists():
        img = safe_open_image(image_path)
        if img:
            st.markdown("<div class='image-card'>", unsafe_allow_html=True)
            st.image(img, use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error(f"Could not load image: {image_path.name}")
    else:
        st.warning(f"Plot not found: {image_path.name}")

    st.info(insight)
    st.markdown(f"<p style='color:{MUTED}; font-style: italic; margin-top:6px;'>\"{caption}\"</p>", unsafe_allow_html=True)

st.sidebar.title("CRO / UX Analytics Dashboard")
page = st.sidebar.radio("Navigate", ["Home", "Session Analysis", "Exploratory Data (EDA)", "Item Funnel", "About"])
st.sidebar.markdown("---")
st.sidebar.caption("Use this panel to switch sections")

if page == "Home":
    st.title("CRO / UX Analytics Dashboard")
    st.markdown("<h4 style='color:#cfd8dc;'>RetailRocket Dataset Analysis</h4>", unsafe_allow_html=True)

    st.markdown("---")
    st.write(
        """
        Welcome to the **CRO/UX Behavior Analytics Dashboard** —  
        A data-driven exploration of user sessions, funnels, and behavioral insights  
        derived from the **Retail Rocket** dataset.
        
        Navigate using the sidebar to explore:
        - **Session Analysis**: engagement clusters, funnel drop-offs, and time-based conversion trends.  
        - **Exploratory Data (EDA)**: activity patterns and event flows.  
        - **Item Funnel**: product-level funnel metrics and best/worst performers.  
        """
    )

    st.markdown("---")
    st.markdown("<div style='color:#9aa3ad;'>Built with ❤️ using Python & Streamlit</div>", unsafe_allow_html=True)

elif page == "Session Analysis":
    st.title("Session-Level Analytics")
    st.markdown("### Visual Insights")

    session_plots = [
        {
            "title": "Engagement Clusters",
            "filename": "engagement_clusters.png",
            "dir": SESSION_DIR,
            "insight": (
                'The vast majority of sessions fall under the "Bounce" category, indicating users who leave after minimal interaction. '
                'A much smaller fraction explore products ("Browser"), and an even tinier group proceed to meaningful engagement or conversion. '
                'This distribution reveals a drop-off challenge early in the journey, suggesting that the landing experience or product discovery flow may be failing to hold attention. '
                'Optimizing first impressions could greatly improve engagement.'
            ),
            "caption": "Most sessions end in a bounce — improving the landing experience and early interaction can significantly increase engagement."
        },
        {
            "title": "Session Funnel (Views → Cart → Transaction)",
            "filename": "session_funnel.png",
            "dir": SESSION_DIR,
            "insight": (
                "Only a small portion of sessions progress from viewing to adding to cart, and even fewer reach a transaction. "
                "This drop-off highlights friction during cart or checkout — unclear CTAs, missing trust signals, or unexpected costs may be to blame."
            ),
            "caption": "Users view products but rarely proceed to checkout — optimizing cart and checkout can lift conversion."
        },
        {
            "title": "Conversion Rate by Hour of Day",
            "filename": "conversion_by_hour.png",
            "dir": SESSION_DIR,
            "insight": (
                "Conversion rates dip in the morning but spike around 3–4 PM, remaining strong into the evening. "
                "This reveals ideal times for campaigns or push notifications."
            ),
            "caption": "Conversions peak around late afternoon — schedule marketing for high-impact hours."
        },
        {
            "title": "Conversion Rate by Events per Session (Binned)",
            "filename": "conversion_by_events_binned.png",
            "dir": SESSION_DIR,
            "insight": (
                "Conversion rate rises with session depth — the more events a user triggers, the likelier they are to convert."
            ),
            "caption": "More engaged sessions yield higher conversions — encourage deeper exploration."
        },
        {
            "title": "Events per Session (Histogram)",
            "filename": "events_per_session.png",
            "dir": SESSION_DIR,
            "insight": (
                "Most sessions have very few events, suggesting many users leave early without exploring much."
            ),
            "caption": "Low event depth per session — optimize browsing experience to retain users longer."
        }
    ]

    chosen = st.selectbox("Choose a session plot", [p["title"] for p in session_plots])
    sel = next(p for p in session_plots if p["title"] == chosen)
    st.markdown(f"### {sel['title']}")
    display_plot_with_insight(sel["dir"] / sel["filename"], sel["insight"], sel["caption"])

elif page == "Exploratory Data (EDA)":
    st.title("Exploratory Data Analysis")
    st.subheader("Events Over Time (7-Day Moving Average)")

    eda_file = EDA_DIR / "events_over_time_7dma.png"
    eda_insight = (
        "Event activity fluctuates over time, peaking mid-year and declining later. "
        "This may correspond to seasonal interest or campaign effects."
    )
    eda_caption = "Engagement peaks mid-year but drops later — reactivation campaigns can revive interest."
    display_plot_with_insight(eda_file, eda_insight, eda_caption)

elif page == "Item Funnel":
    st.title("Item Funnel & Product Performance")
    st.markdown("### Product-Level Funnel Insights")

    item_plots = [
        {
            "title": "Top 20 Items: Conversion Rate",
            "filename": "top20_items_conversion.png",
            "dir": ITEM_DIR,
            "insight": (
                "A few standout items convert far better than the rest, suggesting strong appeal or presentation quality. "
                "Analyzing them can reveal winning patterns."
            ),
            "caption": "Top products dominate conversions — replicate their appeal across the catalog."
        },
        {
            "title": "Top 20 Items: Add-to-Cart vs Purchases",
            "filename": "top20_items_funnel.png",
            "dir": ITEM_DIR,
            "insight": (
                "Many items are added to carts but not purchased, indicating friction during checkout or hesitation post-cart."
            ),
            "caption": "High add-to-cart but low purchase — refine checkout and build trust."
        },
        {
            "title": "Worst 20 Items: High Views, Low Conversion",
            "filename": "worst20_items_funnel.png",
            "dir": ITEM_DIR,
            "insight": (
                "These items get visibility but fail to convert — possible price mismatch or unclear descriptions."
            ),
            "caption": "High attention but low action — improve product pages and alignment."
        }
    ]

    chosen_item = st.selectbox("Choose an item plot", [p["title"] for p in item_plots])
    sel_item = next(p for p in item_plots if p["title"] == chosen_item)
    st.markdown(f"### {sel_item['title']}")
    display_plot_with_insight(sel_item["dir"] / sel_item["filename"], sel_item["insight"], sel_item["caption"])

elif page == "About":
    st.title("About This Project")
    st.write(
        """
        This project was created as part of a **CRO / UX Analytics** study on the Retail Rocket e-commerce dataset.  
        It highlights how behavioral data analysis can uncover conversion patterns and optimize user experiences.
        """
    )

    st.markdown("### Author")
    st.markdown("**Param Dubey** — Data Analytics & Conversion Optimization")

    st.markdown("---")
    st.markdown("### Links")
    st.markdown(
        """
        - [LinkedIn](https://www.linkedin.com/in/param-dubey-408bb9343/)
        - [GitHub](https://github.com/paramdubey933)
        - [Kaggle Profile](https://www.kaggle.com/pardub)
        - [Dataset: RetailRocket (Kaggle)](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)
        """
    )

    st.markdown("---")
    st.markdown("### Tools & Technologies")
    st.markdown("- Python 3.x\n- Streamlit\n- Pandas\n- Matplotlib\n- Pillow\n- Seaborn")

st.markdown("---")
st.markdown("<div class='footer'>© 2025 Param Dubey | CRO/UX Analytics Dashboard</div>", unsafe_allow_html=True)
