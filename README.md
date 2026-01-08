
# CRO / UX Analytics Dashboard
A data-driven CRO &amp; UX analytics tool to uncover drop-offs, optimize funnels, and boost conversions.
Conversion Rate Optimization (CRO) and User Experience (UX) analytics dashboard built using Python and Streamlit.  
This project analyzes real-world e-commerce user behavior from the Retail Rocket dataset and transforms it into actionable, story-driven insights.

---

## Project Overview

This dashboard explores how users interact with an e-commerce platform by analyzing:
- session-level engagement
- conversion funnels
- time-based conversion trends
- item-level performance

The goal is to demonstrate how data analytics can be used to identify UX friction points and improve conversion outcomes.

---

## Key Features

- Session-level engagement clustering (bounce, browser, engaged, converting)
- Conversion funnel analysis (view → add-to-cart → transaction)
- Time-based conversion trends
- Item-level funnel and product performance analysis
- Static, high-performance Streamlit dashboard
- Storytelling-style insights below each visualization

---

## Tech Stack

- Python 3.x
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Pillow

---

## Project Structure

CRO_UX_Analytics/
├── app.py # Streamlit dashboard
├── analytics/ # Data processing & analysis scripts
│ ├── data_cleaning.py
│ ├── simulate_users.py
│ ├── eda/
│ ├── session_analysis/
│ └── item_funnel/
├── docs/ # SRS and documentation
├── screenshots/ # App previews
└── requirements.txt

---

## How to Run the Project

1. Clone the repository:
git clone https://github.com/your-username/CRO_UX_Analytics.git
cd CRO_UX_Analytics

2. Install dependencies:
pip install -r requirements.txt

3. Run the dashboard:
streamlit run app.py

---

## Dataset

This project uses the **Retail Rocket E-commerce Dataset** from Kaggle.

Due to size constraints, the dataset is not included in the repository.

Dataset link:
https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset

---

## Documentation

- Software Requirements Specification (SRS) is available in the `docs/` folder.

---

## Author

**Param Dubey**  
B.Tech Computer Science & Engineering  
KIIT University, Bhubaneswar  

LinkedIn: https://www.linkedin.com/in/param-dubey-408bb9343/  
GitHub: https://github.com/paramdubey933
