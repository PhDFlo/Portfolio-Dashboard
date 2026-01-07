import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        /* RESET & BASE */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* --- THEME VARIABLES --- */
        :root {
            /* Light Mode Defaults (Soft UI) */
            --bg-color: #F3F4F6; /* Gray-100 */
            --card-bg: #FFFFFF;
            --text-color: #1F2937; /* Gray-800 */
            --sidebar-bg: #111827; /* Gray-900 (Dark Navy/Black) */
            --sidebar-text: #F9FAFB;
            --accent-gradient: linear-gradient(135deg, #EC4899 0%, #8B5CF6 100%); /* Pink to Purple */
            --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --border-radius-card: 16px;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                /* Dark Mode Adaptation */
                --bg-color: #1F2937; /* Gray-800 */
                --card-bg: #374151; /* Gray-700 */
                --text-color: #F9FAFB; /* Gray-50 */
                --sidebar-bg: #111827; /* Keep dark */
                --sidebar-text: #F9FAFB;
                --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
            }
        }

        /* --- MAIN LAYOUT --- */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
        }

        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg);
        }
        [data-testid="stSidebar"] .css-17lntkn, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: var(--sidebar-text); /* Ensure text is white */
        }
        
        /* Custom sidebar nav items (approximate targeting) */
        section[data-testid="stSidebar"] .stButton button, section[data-testid="stSidebar"] div[role="radiogroup"] {
             color: var(--sidebar-text) !important;
        }

        /* --- "CARDS" (Styling specific block containers) --- */
        [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: var(--card-bg);
            border-radius: var(--border-radius-card);
            padding: 1.5rem !important; /* Increase padding */
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(255,255,255,0.05); /* Subtle border for dark mode */
        }

        /* --- DATAFRAME STYLING --- */
        [data-testid="stDataFrame"] {
            background-color: var(--card-bg);
            border-radius: var(--border-radius-card);
            padding: 1rem;
            box-shadow: var(--shadow-card);
        }

        /* --- BUTTONS --- */
        .stButton button {
            border-radius: 12px;
            font-weight: 600;
            border: none;
            transition: all 0.2s;
        }
        
        /* Primary Button Style (Gradient) - heuristic targeting based on context if possible, 
           or just style all primary-positioned buttons. Streamlit 'primary' buttons have specific classes.
        */
        button[kind="primary"] {
            background: var(--accent-gradient) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
        }
        button[kind="primary"]:hover {
            box-shadow: 0 6px 16px rgba(236, 72, 153, 0.5);
            transform: translateY(-1px);
        }

        /* Secondary Button Style */
        button[kind="secondary"] {
            background-color: var(--card-bg);
            color: var(--text-color);
            border: 1px solid rgba(0,0,0,0.1);
        }
        
        /* --- HEADERS --- */
        h1, h2, h3 {
            font-weight: 700 !important;
            color: var(--text-color) !important;
        }
        
        /* Custom Gradient Text Class (Usage: st.markdown('<span class="gradient-text">Text</span>', unsafe_allow_html=True)) */
        .gradient-text {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        /* --- METRICS --- */
        [data-testid="stMetric"] {
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: var(--shadow-card);
        }
        [data-testid="stMetricLabel"] {
            color: #6B7280; /* Gray-500 */
        }
        [data-testid="stMetricValue"] {
            color: var(--text-color);
            font-weight: 700;
        }

        /* Remove default top padding */
        .block-container {
            padding-top: 2rem;
        }

        </style>
    """, unsafe_allow_html=True)
