import streamlit as st

# Set page config
st.set_page_config(page_title="Weekly Wage Calculator", page_icon="📝", layout="centered")

st.title("📝 Weekly Wage Calculator")
st.caption("Modeled after standard hourly payslip calculations")

# Sidebar - Developer Credit
st.sidebar.markdown("### App Information")
st.sidebar.markdown("App developed & maintained by: **Bimo**")

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

# 2. Allowances & Deductions Section
st.subheader("2. Allowances & Deductions")
col_al1, col_al2, col_al3 = st.columns(3)

with col_al1:
    st.markdown("**Taxable Allowances**")
    unimed_contribution = st.number_input(
        "Company Contribution Unimed ($)", 
        value=63.46,
        step=1.0,
        format="%.2f"
    )
    total_taxable_allowances = unimed_contribution

with col_al2:
    st.markdown("**Non-Taxable Payments**")
    weekend_days = st.number_input(
        "Weekend Allowance (Days)", 
        min_value=0.0, 
        value=1.0, 
        step=1.0
    )
    weekend_rate = 12.36
    total_non_taxable = weekend_days * weekend_rate

with col_al3:
    st.markdown("**Employee Deductions**")
    kiwisaver_percent = st.number_input(
        "KiwiSaver (%)", 
        min_value=0.0, 
        max_value=10.0, 
        value=3.5, 
        step=0.5
    )
    unimed_deduction = st.number_input(
        "Unimed Deduction ($)", 
        value=52.88, 
        step=1.0, 
        format="%.2f"
    )

# 3. Calculation Logic

# Earnings
ord_hours = min(total_hours, 40.0)
ot15_hours = max(0.0, min(total_hours - 40.0, 9.0))
ot20_hours = max(0.0, total_hours - 49.0)

ord_rate = base_rate * 1.0000
ot15_rate = base_rate * 1.5000
ot20_rate = base_rate * 2.0000

ord_val = ord_hours * ord_rate
ot15_val = ot15_hours * ot15_rate
ot20_val = ot20_hours * ot20_rate

total_hourly_earnings = ord_val + ot15_val + ot20_val
total_taxable = total_hourly_earnings + total_taxable_allowances
gross_pay = total_taxable + total_non_taxable

# PAYE & ACC Calculation (Tax Code: M)
# Annualize taxable income to find the bracket
annual_taxable = total_taxable * 52

annual_tax = 0.0
if annual_taxable <= 15600:
    annual_tax = annual_taxable * 0.105
elif annual_taxable <= 53500:
    annual_tax = (15600 * 0.105) + ((annual_taxable - 15600) * 0.175)
elif annual_taxable <= 78100:
    annual_tax = (15600 * 0.105) + (37900 * 0.175) + ((annual_taxable - 53500) * 0.30)
elif annual_taxable <= 180000:
    annual_tax = (15600 * 0.105) + (37900 * 0.175) + (24600 * 0.30) + ((annual_taxable - 78100) * 0.33)
else:
    annual_tax = (15600 * 0.105) + (37900 * 0.175) + (24600 * 0.30) + (101900 * 0.33) + ((annual_taxable - 180000) * 0.39)

weekly_income_tax = annual_tax / 52

# ACC Levy (1.75% up to a maximum salary of $156,641)
annual_acc = min(annual_taxable, 156641) * 0.0175
weekly_acc = annual_acc / 52

total_paye = weekly_income_tax + weekly_acc

# KiwiSaver Calculation (calculated on total taxable pay)
kiwisaver_deduction = total_taxable * (kiwisaver_percent / 100)

# Total Deductions & Net Pay
total_deductions = total_paye + kiwisaver_deduction + unimed_deduction
net_pay = gross_pay - total_deductions

# 4. Output / Display
st.divider()

# High-level metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Hours", f"{total_hours:.2f} hrs")
m2.metric("Gross Pay", f"${gross_pay:,.2f}")
m3.metric("Total Deductions", f"${total_deductions:,.2f}")
m4.metric("Net Pay", f"${net_pay:,.2f}")

st.subheader("Earnings Breakdown")
earnings_data = [
    {
        "Type": "Ordinary Time",
        "Hours": f"{ord_hours:.2f}",
        "Rate": f"{base_rate:.4f} x 1.0000",
        "Value ($)": f"{ord_val:,.2f}"
    },
    {
        "Type": "Time & One Half",
        "Hours": f"{ot15_hours:.2f}",
        "Rate": f"{base_rate:.4f} x 1.5000",
        "Value ($)": f"{ot15_val:,.2f}"
    },
    {
        "Type": "Double Time",
        "Hours": f"{ot20_hours:.2f}",
        "Rate": f"{base_rate:.4f} x 2.0000",
        "Value ($)": f"{ot20_val:,.2f}"
    },
    {
        "Type": "Comp Contr Unimed (Taxable)",
        "Hours": "-",
        "Rate": "-",
        "Value ($)": f"{unimed_contribution:,.2f}"
    },
    {
        "Type": "Weekend Meal (Non-Taxable)",
        "Hours": "-",
        "Rate": "-",
        "Value ($)": f"{total_non_taxable:,.2f}"
    }
]
st.table(earnings_data)

st.subheader("Deductions Breakdown")
deductions_data = [
    {"Deduction": "P.A.Y.E. (Inc. ACC)", "Amount ($)": f"{total_paye:,.2f}"},
    {"Deduction": f"KiwiSaver ({kiwisaver_percent}%)", "Amount ($)": f"{kiwisaver_deduction:,.2f}"},
    {"Deduction": "Unimed", "Amount ($)": f"{unimed_deduction:,.2f}"}
]
st.table(deductions_data)
