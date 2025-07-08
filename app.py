import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the emissions dataset
df = pd.read_csv("full_scope_emission_factors_mep.csv")

st.title("🌍 Scope 1, 2, 3 Emission Visualizer – MEP Sector")
st.caption("Interactive tool to explore GHG emission factors by scope, category, and item.")

# Show full dataset
if st.checkbox("Show Emission Dataset"):
    st.dataframe(df)

# Dropdowns for filtering
selected_scope = st.selectbox("Select Scope", df["Scope"].unique())
filtered_scope = df[df["Scope"] == selected_scope]

selected_category = st.selectbox("Select Category", filtered_scope["Category"].unique())
filtered_category = filtered_scope[filtered_scope["Category"] == selected_category]

selected_item = st.selectbox("Select Item", filtered_category["Item"].unique())
selected_row = filtered_category[filtered_category["Item"] == selected_item].iloc[0]

# Input quantity
quantity = st.number_input(f"Enter quantity ({selected_row['Unit']}):", min_value=0.0, value=1.0)

# Calculate emissions
emissions = quantity * selected_row["Emission Factor (kg CO₂e/unit)"]
st.metric(label=f"Estimated Emissions from {selected_item}", value=f"{emissions:.2f} kg CO₂e")

# Bar chart for top items in selected category
st.subheader(f"🔍 Emission Factors – {selected_category} in {selected_scope}")
top_items = filtered_scope[filtered_scope["Category"] == selected_category]

fig, ax = plt.subplots()
ax.bar(top_items["Item"], top_items["Emission Factor (kg CO₂e/unit)"], color='teal')
plt.xticks(rotation=45, ha='right')
plt.ylabel("kg CO₂e per unit")
plt.tight_layout()
st.pyplot(fig)
