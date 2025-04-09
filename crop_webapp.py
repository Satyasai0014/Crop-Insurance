import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset (replace with actual file path)
df = pd.read_excel("Soyabean Shiny Input (1).xlsx")

# Streamlit App Title
# st.title("Crop Revenue Protection Dashboard")
col1, col2 = st.columns([1, 4])  # Adjust ratio as needed
    
    with col1:
        st.image("logo.png", width=120)  # Replace "logo.png" with your logo path

    with col2:
        
        # st.title("MFI Credit Risk Management Tool - Default Classifier")
        st.markdown(
        """
        <div style="text-align: left; font-size: 32px; font-weight: bold;">
            Crop Revenue Protection Dashboard
        </div>
        """,
        unsafe_allow_html=True
        )

# Creating dropdowns in a single row
col1, col2, col3, col4 = st.columns(4)

crop_options = df["Crop"].unique().tolist()
sowing_season_options = df["Sowing_season"].unique().tolist()
liability_projection_options = df["Liability Projection"].unique().tolist()
type_of_strategy_options = df["Type_of_Strategy"].unique().tolist()

selected_crop = col1.multiselect("Select the Crop", crop_options, default=crop_options[:1])
selected_sowing_season = col2.multiselect("Select the Sowing Season", sowing_season_options, default=sowing_season_options[:1])
selected_liability_projection = col3.multiselect("Select the Liability Projection", liability_projection_options, default=liability_projection_options[:1])
selected_type_of_strategy = col4.multiselect("Select the Type of Strategy", type_of_strategy_options, default=type_of_strategy_options[:1])

# Filter data based on selections
filtered_data = df[
    (df["Crop"].isin(selected_crop)) &
    (df["Sowing_season"].isin(selected_sowing_season)) &
    (df["Liability Projection"].isin(selected_liability_projection)) &
    (df["Type_of_Strategy"].isin(selected_type_of_strategy))
]

# Creating two columns for data and graphs
data_col, graph_col = st.columns(2)

# Display dataset in tabs
cost_values = df["Cost"].unique().tolist()
data_tabs = data_col.tabs(cost_values)
graph_tabs = graph_col.tabs(cost_values)

# graph_col.write("### Visualization")

for i, cost in enumerate(cost_values):
    with data_tabs[i]:
        filtered_tab_data = filtered_data[filtered_data["Cost"] == cost]
        if not filtered_tab_data.empty:
            st.write(f"### Data for Cost: {cost}")
            st.dataframe(filtered_tab_data)
        else:
            st.write("No data available for this selection.")

    with graph_tabs[i]:
        filtered_graph_data = filtered_data[filtered_data["Cost"] == cost]
        if not filtered_graph_data.empty:
            if cost == "Asset":  # Custom stacked bar chart for 'Assets' tab
                fig = px.bar(filtered_graph_data, x="Liability Projection", y="Premium (In Crores)",
                             color="Cost Components", title=f"Premium Breakdown for Cost: {cost}",
                             category_orders={"Cost Components": ["Initial Margin", "Basis Risk", "Shortfall Costs"]},
                             barmode='stack')
            else:
                fig = px.bar(filtered_graph_data, x="Liability Projection", y="Premium (In Crores)",
                             color="Sowing_season", title=f"Premium vs Liability Projection for Cost: {cost}")
            st.plotly_chart(fig)
        else:
            st.write("No data available for this selection.")
