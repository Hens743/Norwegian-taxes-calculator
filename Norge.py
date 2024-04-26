import plotly.graph_objects as go

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
    
    return details, net_income, total_tax, (total_tax / salary) * 100  # Calculate tax as a percentage of salary

def main():
    try:
        salary = float(input("Enter your salary (NOK): "))
    except ValueError:
        print("Invalid input. Please enter a numeric value for salary.")
        return
    
    tax_details, net_income, total_tax, tax_percentage = calculate_taxes(salary)
    print(f"Total tax: NOK {total_tax:.2f} which is {tax_percentage:.2f}% of your salary")
    print(f"Net income after tax: NOK {net_income:.2f}")
    
    # Data for visualization
    tax_labels = [label for label, _ in tax_details] + ['Net Income']
    tax_values = [value for _, value in tax_details] + [net_income]
    colors = ['orange', 'red', 'yellow', 'green', 'purple', 'pink']  # Custom colors for each tax type
    
    # Create the vertical stacked bar chart with Plotly
    fig = go.Figure()
    for i, (label, value) in enumerate(zip(tax_labels, tax_values)):
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
        xaxis={'categoryorder':'total descending'}
    )
    
    fig.show()

if __name__ == "__main__":
    main()


