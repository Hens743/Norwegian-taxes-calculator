import streamlit as st
import matplotlib.pyplot as plt

def calculate_tax(salary):
    if salary <= 208050:
        tax = 0
    elif salary <= 292850:
        tax = (salary - 208050) * 0.017
    elif salary <= 670000:
        tax = (292850 - 208051) * 0.017 + (salary - 292850) * 0.04
    elif salary <= 937900:
        tax = (292850 - 208051) * 0.017 + (670000 - 292851) * 0.04 + (salary - 670000) * 0.136
    elif salary <= 1350000:
        tax = (292850 - 208051) * 0.017 + (670000 - 292851) * 0.04 + (937900 - 670001) * 0.136 + (salary - 937900) * 0.166
    else:
        tax = (292850 - 208051) * 0.017 + (670000 - 292851) * 0.04 + (937900 - 670001) * 0.136 + (1350000 - 937901) * 0.166 + (salary - 1350000) * 0.176
    net_income = salary - tax
    return net_income, tax

def main():
    st.title("Norway Tax Calculator")
    salary = st.number_input("Enter your salary:", value=0.0)
    if salary < 0:
        st.warning("Salary must be a positive number.")
        return

    net_income, tax = calculate_tax(salary)
    st.write(f"Net income after tax: NOK {net_income:.2f}")
    st.write(f"Tax paid: NOK {tax:.2f}")

    # Visualization
    labels = ['Income', 'Tax']
    sizes = [salary, tax]
    explode = (0, 0.1)  # only "explode" the 2nd slice
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

if __name__ == "__main__":
    main()

