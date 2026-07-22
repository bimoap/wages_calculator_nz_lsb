import streamlit as st

# Set page config
st.set_page_config(page_title="Weekly Wage Calculator", page_icon="📝", layout="centered")

st.title("📝 Weekly Wage Calculator")
st.caption("Modeled after standard hourly payslip calculations")

# Sidebar - Developer Credit
st.sidebar.markdown("### App Information")
st.sidebar.text("App developed & maintained by: Bimo")

# 1. Inputs Section
st.subheader("1. Enter Hourly Rate & Total Hours")

col1, col2 = st.columns(2)

with col1:
    base_rate = st.number_input(
        "Base Hourly Rate ($)", 
        min_value=0.0, 
        value=33.29, 
        step=0.25, 
        format="%.4f"
    )

with col2:
    total_hours = st.number_input(
        "Total Hours Worked", 
        min_value=0.0, 
        value=56.75, 
        step=0.25
    )

# Optional Allowances (toggle to include)
with st.expander("Additional Allowances (Optional)"):
    col_al1, col_al2 = st.columns(2)
    with col_al1:
        taxable_allowance = st.number_input(
            "Taxable Allowance ($)", 
            min_value=0.0, 
            value=63.46, 
            step=1.0, 
            format="%.2f"
        )
    with col_al2:
        non_taxable_allowance = st.number_input(
            "Non-Taxable Allowance ($)", 
            min_value=0.0, 
            value=12.36, 
            step=1.0, 
            format="%.2f"
        )

# 2. Calculation Logic
# Hours breakdown based on tiers: 0-40 (1.0x), 40-49 (1.5x), >49 (2.0x)
ord_hours = min(total_hours, 40.0)
ot15_hours = max(0.0, min(total_hours - 40.0, 9.0))
ot20_hours = max(0.0, total_hours - 49.0)

# Pay Rates
ord_rate = base_rate * 1.0000
ot15_rate = base_rate * 1.5000
ot20_rate = base_rate * 2.0000

# Values
ord_val = ord_hours * ord_rate
ot15_val = ot15_hours * ot15_rate
ot20_val = ot20_hours * ot20_rate

total_hourly_earnings = ord_val + ot15_val + ot20_val
total_taxable = total_hourly_earnings + taxable_allowance
gross_pay = total_taxable + non_taxable_allowance

# 3. Output / Display
st.divider()

# High-level metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Hours", f"{total_hours:.2f} hrs")
m2.metric("Total Taxable", f"${total_taxable:,.2f}")
m3.metric("Gross Pay", f"${gross_pay:,.2f}")

st.subheader("Earnings Breakdown")

# Table structured like the payslip
earnings_data = [
    {
        "Earnings Type": "Ordinary Time",
        "Hours": f"{ord_hours:.2f}",
        "Rate Multiplier": f"{base_rate:.4f} x 1.0000",
        "Pay Rate ($)": f"{ord_rate:.4f}",
        "Value ($)": f"{ord_val:,.2f}"
    },
    {
        "Earnings Type": "Time & One Half",
        "Hours": f"{ot15_hours:.2f}",
        "Rate Multiplier": f"{base_rate:.4f} x 1.5000",
        "Pay Rate ($)": f"{ot15_rate:.4f}",
        "Value ($)": f"{ot15_val:,.2f}"
    },
    {
        "Earnings Type": "Double Time",
        "Hours": f"{ot20_hours:.2f}",
        "Rate Multiplier": f"{base_rate:.4f} x 2.0000",
        "Pay Rate ($)": f"{ot20_rate:.4f}",
        "Value ($)": f"{ot20_val:,.2f}"
    }
]

st.table(earnings_data)

# Summary list for final gross calculation
st.markdown(
    f"""
    * **Total Hourly Earnings:** `${total_hourly_earnings:,.2f}`
    * **Taxable Allowances:** `${taxable_allowance:,.2f}`
    * **Total Taxable:** `${total_taxable:,.2f}`
    * **Non-Taxable Payments:** `${non_taxable_allowance:,.2f}`
    * **Gross Pay:** **`${gross_pay:,.2f}`**
    """
)
