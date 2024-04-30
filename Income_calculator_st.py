import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Define the tax brackets and rates
BRACKETS = [
    (208050, 0.0),  # No tax for income up to 208050
    (292850, 0.017),  # 1.7% for income between 208051 and 292850
    (670000, 0.04),  # 4.0% for income between 292851 and 670000
    (937900, 0.136),  # 13.6% for income between 670001 and 937900
    (1350000, 0.166),  # 16.6% for income between 937901 and 1350000
    (float('inf'), 0.176)  # 17.6% for income above 1350001
]

NATIONAL_INSURANCE_RATE = 0.078
GENERAL_TAX_RATE = 0.22

def calculate_taxes(salary):
    details = []
    bracket_tax = 0
    last_bracket_max = 0
    
    for bracket in BRACKETS:
        if salary > last_bracket_max:
            upper_bound = min(salary, bracket[0])
            taxable_income = upper_bound - last_bracket_max
            tax = taxable_income * bracket[1]
            details.append((f"Bracket Tax @ {bracket[1]*100:.1f}%", tax))
            bracket_tax += tax
            last_bracket_max = bracket[0]
    
    national_insurance = salary * NATIONAL_INSURANCE_RATE
    details.append(("National Insurance", national_insurance))
    
    general_tax = salary * GENERAL_TAX_RATE
    details.append(("General Tax", general_tax))
    
    total_tax = bracket_tax + national_insurance + general_tax
    net_income = salary - total_tax
    
    tax_percentage = (total_tax / salary) * 100
    
    return details, net_income, tax_percentage

def main():
    st.title("Norwegian Income Tax Calculator 2024")
    
    # Input for salary
    salary = st.number_input("Enter your salary (NOK):")
    
    if st.button("Calculate"):
        if salary <= 0:
            st.error("Invalid input. Please enter a positive value for salary.")
        else:
            tax_details, net_income, tax_percentage = calculate_taxes(salary)
            
            # Display tax breakdown
            st.subheader("Tax Breakdown")
            for detail, value in tax_details:
                st.write(f"- {detail}: NOK {value:.2f}")
            
            # Display net income
            st.subheader("Net Income")
            st.write(f"Net income after tax: NOK {net_income:.2f}")
            
            # Display tax as a percentage of salary
            st.subheader("Tax as Percentage of Salary")
            st.write(f"Tax as a percentage of salary: {tax_percentage:.2f}%")
            
            # Visualization
            st.subheader("Tax Breakdown Visualization")
            fig = go.Figure()
            labels = [label for label, _ in tax_details] + ['Net Income']
            values = [value for _, value in tax_details] + [net_income]
            colors = ['orange', 'red', 'yellow', 'green', 'purple', 'pink']  # Custom colors for each tax type
            
            for i, (label, value) in enumerate(zip(labels, values)):
                fig.add_trace(go.Bar(
                    x=[label],
                    y=[value],
                    name=label,
                    marker_color=colors[i % len(colors)]
                ))

            fig.update_layout(
                barmode='stack',
                title="Tax Breakdown and Net Income",
                xaxis_title="Tax Components",
                yaxis_title="Amount (NOK)",
                xaxis={'categoryorder':'total descending'},
                height=600,  # Increased height for the plot
            )
            
            st.plotly_chart(fig)
            
            # Create DataFrame for Excel file
            data = {'Component': [label for label, _ in tax_details] + ['Net Income'],
                    'Amount (NOK)': [value for _, value in tax_details] + [net_income]}
            df = pd.DataFrame(data)
            
            # Download option for Excel file
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    
    st.markdown("""
    ### Note:
    The taxes are calculated based on the tables of Norway, income tax. For simplification purposes some variables (such as marital status, place of living and others) have been assumed. This document does not represent legal authority and shall be used for approximation purposes only.
    """)

def get_table_download_link(df):
    """Generates a link allowing the data in a given pandas DataFrame to be downloaded as an Excel file."""
    excel_file = df.to_excel(index=False)
    b64 = base64.b64encode(excel_file.encode()).decode()  # Convert DataFrame to bytes
    href = f'<a href="data:file/excel;base64,{b64}" download="tax_breakdown.xlsx">Download Excel file</a>'
    return href

if __name__ == "__main__":
    main()
