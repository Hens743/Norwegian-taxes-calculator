import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Define the tax brackets and rates
BRACKETS = [
    (208050, 0.0),   # No tax for income up to 208050
    (292850, 0.017), # 1.7% for income between 208051 and 292850
    (670000, 0.04),  # 4.0% for income between 292851 and 670000
    (937900, 0.136), # 13.6% for income between 670001 and 937900
    (1350000, 0.166),# 16.6% for income between 937901 and 1350000
    (float('inf'), 0.176) # 17.6% for income above 1350001
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

    # Create DataFrame for CSV Export
    data = {'Tax Components': [label for label, _ in details] + ['Net Income'],
            'Amount (NOK)': [value for _, value in details] + [net_income]}
    df = pd.DataFrame(data)

    return df, net_income, tax_percentage

def main():
    st.title("Norwegian Income Tax Calculator 2024")
    salary = st.number_input("Enter your salary (NOK):")

    if st.button("Calculate"):
        if salary <= 0:
            st.error("Invalid input. Please enter a positive value for salary.")
        else:
            df, net_income, tax_percentage = calculate_taxes(salary)

            st.subheader("Tax Breakdown")
            for detail, value in zip(df['Tax Components'], df['Amount (NOK)']):
                st.write(f"- {detail}: NOK {value:.2f}" if detail != 'Net Income' else f"- {detail}: NOK {value:.2f}")

            # Visualization
            st.subheader("Tax breakdown visualization")
            fig = go.Figure()
            labels = df['Tax Components'].tolist()
            values = df['Amount (NOK)'].tolist()
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
                title="Tax breakdown and net income",
                xaxis_title="Tax components",
                yaxis_title="Amount (NOK)",
                xaxis={'categoryorder':'total descending'},
                height=600,  # Increased height for the plot
            )
            
            st.plotly_chart(fig)

            # CSV Download
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name='tax_results.csv',
                mime='text/csv'
            )

            st.markdown(""" Note:  The taxes are calculated based on the tables of Norway, income tax. For simplification purposes some variables (such as marital status, place of living and others) have been assumed. This app does not represent legal authority and shall be used for approximation purposes only.
 """) 

if __name__ == "__main__":
    main()
