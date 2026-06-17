import os
import matplotlib.pyplot as plt

# 1. Map user-facing countries to their currency tags and static exchange rates
# Rates are configured as: How many units of local currency equal $1.00 USD
COUNTRY_MAP = {
    "United States": {"currency": "USD", "rate_per_usd": 1.0, "base": True},
    "Germany": {"currency": "EUR", "rate_per_usd": 0.92, "base": False},
    "United Kingdom": {"currency": "GBP", "rate_per_usd": 0.79, "base": False},
    "Japan": {"currency": "JPY", "rate_per_usd": 155.0, "base": False},
    "Australia": {"currency": "AUD", "rate_per_usd": 1.51, "base": False},
    "Spain": {"currency": "EUR", "rate_per_usd": 0.92, "base": False},
    "Italy": {"currency": "EUR", "rate_per_usd": 0.92, "base": False},
    "Poland": {"currency": "PLN", "rate_per_usd": 4.02, "base": False},
    "Mexico": {"currency": "MXN", "rate_per_usd": 17.25, "base": False},
    "Canada": {"currency": "CAD", "rate_per_usd": 1.37, "base": False},
    "Egypt": {"currency": "EGP", "rate_per_usd": 47.50, "base": False},
    "United Arab Emirates": {"currency": "AED", "rate_per_usd": 3.67, "base": False},
    "Argentina": {"currency": "ARS", "rate_per_usd": 1430.0, "base": False}
}

def generate_and_save_chart(us_price, foreign_price_usd, target_country, foreign_currency, valuation):
    """
    Generates a 2-bar chart comparing the base US price to the foreign price in USD,
    with symmetrical outer margins, a side text box, and stacked bottom legend markers.
    """
    currency_names = {
        "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
        "AUD": "Australian Dollar", "PLN": "Polish Zloty", "MXN": "Mexican Peso",
        "CAD": "Canadian Dollar", "EGP": "Egyptian Pound", "AED": "UAE Dirham",
        "ARS": "Argentine Peso"
    }
    target_currency_name = currency_names.get(foreign_currency, f"{foreign_currency} Currency")

    categories = ['U.S. Dollar', target_currency_name]
    prices = [us_price, foreign_price_usd]
    
    fig, ax = plt.subplots(figsize=(8.5, 5.3))  # Slightly wider figure size to accommodate text comfortably
    colors = ['#4f46e5', '#f59e0b'] if valuation > 0 else ['#4f46e5', '#10b981']
    
    bars = ax.bar(categories, prices, color=colors, width=0.4, edgecolor='black', linewidth=0.7)
    ax.set_ylabel('Price in US Dollars ($)', fontsize=11, fontweight='bold')
    ax.set_ylim(0, max(prices) * 1.2)
    ax.set_xlim(-0.6, 2.5)
    
    # 🆕 Force fixed, symmetrical margins around the main plot grid
    # left=0.15 and right=0.85 means the chart takes up the middle 70%, leaving an exact 15% white margin on both sides!
    fig.subplots_adjust(left=0.15, right=0.85, bottom=0.15, top=0.88)
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Data-Driven Multiplier Engine
    if valuation < 0:
        ratio = us_price / foreign_price_usd
        ratio_str = f"{ratio:.1f}".rstrip('0').rstrip('.') if ratio % 1 != 0 else f"{int(ratio)}"
        
        message = (
            f"🍔 Currency Power Tip!\n\n"
            f"The U.S. Dollar stretches\n"
            f"much further here.\n\n"
            f"One U.S. Big Mac gets you\n"
            f"about {ratio_str} Big Macs in {target_country}!\n\n"
            f"Pack your bags! ✈️"
        )
        box_color = '#e6f4ea'
        edge_color = '#10b981'
    else:
        ratio = foreign_price_usd / us_price
        ratio_str = f"{ratio:.1f}".rstrip('0').rstrip('.') if ratio % 1 != 0 else f"{int(ratio)}"
        
        message = (
            f"💸 Pricey Travels!\n\n"
            f"Your U.S. Dollars will shrink\n"
            f"a bit in {target_country}.\n\n"
            f"You pay about {ratio_str}x the\n"
            f"price for the same burger!\n\n"
            f"Ouch! 🤕"
        )
        box_color = '#fffbeb'
        edge_color = '#f59e0b'

    # Place text box on the right side panel
    props = dict(boxstyle='round,pad=1', facecolor=box_color, edgecolor=edge_color, alpha=0.9, linewidth=1.5)
    ax.text(1.35, max(prices) * 0.5, message, fontsize=9.5, color='#1f2937',
            fontweight='medium', va='center', bbox=props, linespacing=1.4)
    
    status = "OVERVALUED" if valuation > 0 else "UNDERVALUED"
    ax.set_title(f'Big Mac Index: {target_country} is {status} by {abs(valuation)}%\nRelative to the U.S. Dollar', 
                 fontsize=12, fontweight='bold', pad=15)
    
    ax.yaxis.grid(True, linestyle='--', alpha=0.6)
    ax.set_axisbelow(True)
    
    # Custom Legend Boxes stacked vertically at the outer bottom-right margin
    orange_box = dict(boxstyle='square,pad=0.2', facecolor='#fffbeb', edgecolor='#f59e0b', linewidth=0.8)
    green_box = dict(boxstyle='square,pad=0.2', facecolor='#e6f4ea', edgecolor='#10b981', linewidth=0.8)
    
    # Adjusted X position to 0.65 to fit cleanly in our newly expanded margin space
    fig.text(0.65, 0.05, "  Stronger currency (Undervalued)  ", color='#15803d', fontsize=8, bbox=green_box)
    fig.text(0.65, 0.02, "  Weaker currency (Overvalued)  ", color='#b45309', fontsize=8, bbox=orange_box)
    
    clean_country_name = target_country.lower().replace(' ', '_')
    output_filename = f"bigmac_{clean_country_name}.png"
    
    # 🆕 Dropped bbox_inches='tight' because subplots_adjust is now explicitly handling the uniform margins
    plt.savefig(output_filename, dpi=150)
    plt.close()
    print(f"📈 Chart successfully saved to: '{os.path.abspath(output_filename)}'")

def run_big_mac_analysis(target_country):
    country_info = COUNTRY_MAP.get(target_country)
    if not country_info or country_info["base"]:
        print("❌ Please choose a valid foreign country from the list.")
        return

    print("🤖 Processing baseline metrics via standard exchange matrix...")
    
    # Static US baseline price configuration
    us_price = 5.89
    currency = country_info["currency"]
    actual_exchange_rate = country_info["rate_per_usd"]
    
    # For this simplified model, we use simulated regional local costs derived from currency metrics
    # Poland: 4.02 rate * $5.89 base = ~23.67 PLN. If actual local price behaves at a discount, valuation updates cleanly.
    # To demonstrate variation, we introduce a slight local cost index variance factor (.85 to 1.1) to mimic global PPP gaps
    variance_factors = {
        "Germany": 0.95, "United Kingdom": 0.90, "Japan": 0.55, "Australia": 0.98,
        "Spain": 0.88, "Italy": 0.85, "Poland": 0.62, "Mexico": 0.82,
        "Canada": 1.05, "Egypt": 0.40, "United Arab Emirates": 1.12, "Argentina": 0.35
    }
    variance = variance_factors.get(target_country, 1.0)
    
    # Deriving simulated local currency price using your standard dollar multiplier layer
    local_price = round((us_price * actual_exchange_rate) * variance, 2)
    
    # Calculate index outputs using baseline architecture
    foreign_price_in_usd = local_price / actual_exchange_rate
    implied_ppp = local_price / us_price
    valuation_pct = round(((implied_ppp - actual_exchange_rate) / actual_exchange_rate) * 100, 2)
    
    print(f"\n--- Analysis Complete for {target_country} ---")
    print(f"Base US Value: ${us_price:.2f}")
    print(f"Local Matrix Price: {local_price} {currency} (Equal to ${foreign_price_in_usd:.2f} USD)")
    print(f"Matrix Valuation Scale: 1 USD = {actual_exchange_rate} {currency}")
    
    generate_and_save_chart(us_price, foreign_price_in_usd, target_country, currency, valuation_pct)


# --- Execute App Logic ---
if __name__ == "__main__":
    while True:
        print("\n=========================================")
        print("🍔 WELCOME TO THE NOVICE BIG MAC INDEX 🍔")
        print("=========================================")
        print("Available countries:")
        print("• Germany, United Kingdom, Japan, Australia, Spain, Italy")
        print("• Poland, Mexico, Canada, Egypt, United Arab Emirates, Argentina")
        print("👉 Type 'exit' to quit the application.\n")
        
        user_choice = input("Enter a country name to analyze: ").strip()
        
        if user_choice.lower() in ['exit', 'quit']:
            print("\n👋 Thank you for using the Big Mac Index Simulator! Happy trading!")
            break
            
        user_choice = user_choice.title()
        
        if user_choice == "United Kingdom":
            user_choice = "United Kingdom"
        elif user_choice in ["United Arab Emirates", "Uae"]:
            user_choice = "United Arab Emirates"
            
        print("") 
        run_big_mac_analysis(user_choice)
        print("\n" + "-"*40)
