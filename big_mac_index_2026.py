import os
import streamlit as st
import matplotlib.pyplot as plt

# Set up Streamlit Page Configuration
st.set_page_config(page_title="Big Mac Index Simulator 2026", page_icon="🍔", layout="centered")

# 1. Map user-facing countries to their currency tags and static exchange rates
COUNTRY_MAP = {
    "Germany": {"currency": "EUR", "rate_per_usd": 0.92},
    "United Kingdom": {"currency": "GBP", "rate_per_usd": 0.79},
    "Japan": {"currency": "JPY", "rate_per_usd": 156.0},
    "Australia": {"currency": "AUD", "rate_per_usd": 1.51},
    "Spain": {"currency": "EUR", "rate_per_usd": 0.92},
    "Italy": {"currency": "EUR", "rate_per_usd": 0.92},
    "Poland": {"currency": "PLN", "rate_per_usd": 4.02},
    "Mexico": {"currency": "MXN", "rate_per_usd": 17.25},
    "Canada": {"currency": "CAD", "rate_per_usd": 1.37},
    "Egypt": {"currency": "EGP", "rate_per_usd": 47.50},
    "United Arab Emirates": {"currency": "AED", "rate_per_usd": 3.67},
    "Argentina": {"currency": "ARS", "rate_per_usd": 1430.0}
}

def generate_chart(us_price, foreign_price_usd, target_country, foreign_currency, valuation):
    """ Generates and returns a 2-bar chart comparing the prices """
    currency_names = {
        "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen", 
        "AUD": "Australian Dollar", "PLN": "Polish Zloty", "MXN": "Mexican Peso", 
        "CAD": "Canadian Dollar", "EGP": "Egyptian Pound", "AED": "UAE Dirham", "ARS": "Argentine Peso"
    }
    
    target_currency_name = currency_names.get(foreign_currency, f"{foreign_currency} Currency")
    categories = ['U.S. Dollar', target_currency_name]
    prices = [us_price, foreign_price_usd]
    
    fig, ax = plt.subplots(figsize=(8.5, 5.3))
    colors = ['#4f46e5', '#f59e0b'] if valuation > 0 else ['#4f46e5', '#10b981']
    bars = ax.bar(categories, prices, color=colors, width=0.4, edgecolor='black', linewidth=0.7)
    
    ax.set_ylabel('Price in US Dollars ($)', fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(prices) * 1.2)
    ax.set_xlim(-0.6, 2.5)
    
    fig.subplots_adjust(left=0.15, right=0.85, bottom=0.15, top=0.88)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10, fontweight='bold')

    if valuation < 0:
        ratio = us_price / foreign_price_usd
        ratio_str = f"{ratio:.1f}".rstrip('0').rstrip('.') if ratio % 1 != 0 else f"{int(ratio)}"
        message = (f"🍔 Currency Power Tip!\n\nThe U.S. Dollar stretches\nmuch further here.\n\n"
                   f"One U.S. Big Mac gets you\nabout {ratio_str} Big Macs in {target_country}!\n\nPack your bags! ✈️")
        box_color, edge_color = '#e6f4ea', '#10b981'
    else:
        ratio = foreign_price_usd / us_price
        ratio_str = f"{ratio:.1f}".rstrip('0').rstrip('.') if ratio % 1 != 0 else f"{int(ratio)}"
        message = (f"💸 Pricey Travels!\n\nYour U.S. Dollars will shrink\na bit in {target_country}.\n\n"
                   f"You pay about {ratio_str}x the\nprice for the same burger!\n\nOuch! 🤕")
        box_color, edge_color = '#fffbeb', '#f59e0b'

    props = dict(boxstyle='round,pad=1', facecolor=box_color, edgecolor=edge_color, alpha=0.9, linewidth=1.5)
    ax.text(1.35, max(prices) * 0.5, message, fontsize=9.5, color='#1f2937', fontweight='medium', va='center', bbox=props, linespacing=1.4)
    
    status = "OVERVALUED" if valuation > 0 else "UNDERVALUED"
    ax.set_title(f'Big Mac Index: {target_country} is {status} by {abs(valuation)}%\nRelative to the U.S. Dollar', fontsize=12, fontweight='bold', pad=15)
    ax.yaxis.grid(True, linestyle='--', alpha=0.6)
    ax.set_axisbelow(True)
    
    orange_box = dict(boxstyle='square,pad=0.2', facecolor='#fffbeb', edgecolor='#f59e0b', linewidth=0.8)
    green_box = dict(boxstyle='square,pad=0.2', facecolor='#e6f4ea', edgecolor='#10b981', linewidth=0.8)
    
    fig.text(0.65, 0.05, " Stronger currency (Undervalued) ", color='#15803d', fontsize=8, bbox=green_box)
    fig.text(0.65, 0.02, " Weaker currency (Overvalued) ", color='#b45309', fontsize=8, bbox=orange_box)
    
    return fig

# --- Streamlit UI App Layout ---
st.title("🍔 Big Mac Index Simulator 2026")
st.caption("Originally created by Pam Woodall for The Economist magazine in 1986. Updated and expanded by Jeff Diamond, 2026")
st.write("Compare purchasing power globally using simulation matrices based on local cost variants.")

# Sidebar Selection
st.sidebar.header("Configuration")
target_country = st.sidebar.selectbox(
    "Select a country to analyze:", 
    list(COUNTRY_MAP.keys()),
    help="Purchasing Power Parity (PPP) states that exchange rates between currencies are in equilibrium when their purchasing power is the same in each of the two countries. This means a basket of goods (or a Big Mac!) should cost the same everywhere when converted to a common currency."
)

if target_country:
    country_info = COUNTRY_MAP[target_country]
    # Sidebar Configuration
 # Use whole integers for cents to prevent floating-point rounding skips
us_price = st.sidebar.slider(
        "Set local U.S. Big Mac Price ($):",
        min_value=4.99,
        max_value=8.99,
        value=5.89,
        step=0.10,
        format="$%.2f",
        help="Adjust to match the price of a Big Mac in your area. FYI: The national average is between 5.29 to 6.72"
    )
   
currency = country_info["currency"]
actual_exchange_rate = country_info["rate_per_usd"]
    
variance_factors = {
        "Germany": 0.95, "United Kingdom": 0.90, "Japan": 0.55, "Australia": 0.98,
        "Spain": 0.88, "Italy": 0.85, "Poland": 0.62, "Mexico": 0.82,
        "Canada": 1.05, "Egypt": 0.40, "United Arab Emirates": 1.12, "Argentina": 0.35
    }
    
variance = variance_factors.get(target_country, 1.0)
local_price = round((us_price * actual_exchange_rate) * variance, 2)
foreign_price_in_usd = local_price / actual_exchange_rate
implied_ppp = local_price / us_price
valuation_pct = round(((implied_ppp - actual_exchange_rate) / actual_exchange_rate) * 100, 2)
    
# Visual Metrics Cards
col1, col2, col3 = st.columns(3)
col1.metric("Base US Price", f"${us_price:.2f}")
col2.metric(f"Local Price ({currency})", f"{local_price} {currency}")
col3.metric("USD Equivalent", f"${foreign_price_in_usd:.2f}")
    
st.info(f"**Approximate exchange rate:** 1 USD = {actual_exchange_rate} {currency}")
    
    # Generate and render chart directly on the web page
with st.spinner("Generating analysis chart..."):
        fig = generate_chart(us_price, foreign_price_in_usd, target_country, currency, valuation_pct)
        st.pyplot(fig)
# --- Add this right at the very bottom of your script ---
st.write("---") # Visual divider line

with st.expander("🎓 Understanding the Economic Theory: Law of One Price vs. PPP"):
    st.markdown("""
    ### The Law of One Price
    This foundational economic rule states that in an efficient market, identical goods must sell for the exact same price when expressed in a common currency. If a Big Mac costs more in one country than another, it signals that the currency may be mispriced (overvalued or undervalued).
    
    ### Why do prices vary in reality?
    While the **Law of One Price** works perfectly in theory, real-world variations occur due to:
    * **Non-tradable inputs:** Local wages, restaurant rent, and utility costs cannot be imported or exported.
    * **Trade barriers:** Tariffs, shipping costs, and import regulations change regional pricing.
    * **Local market positioning:** Profit margins and local competition influence corporate pricing strategy.
    """)
