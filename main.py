import pandas as pd
import plotly.express as px
import streamlit as st

# Load your dataset
# Replace with the actual path or code to load your dataset
df = pd.read_csv('pirate_attacks.csv')


# Handle missing values
df['location_description'].fillna('Unknown', inplace=True)
df['nearest_country'].fillna('Unknown', inplace=True)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Extract the year from the 'date' column
df['year'] = df['date'].dt.year

# Filter the dataset for attacks off the coast of Somalia
somalia_df = df[(df['latitude'] >= -7) & (df['latitude'] <= 12) &
                (df['longitude'] >= 35) & (df['longitude'] <= 70)]

# Streamlit app
st.title("Interactive Visualization of Pirate Attacks")

st.sidebar.header("Filter Options")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(somalia_df['year'].min()),
    int(somalia_df['year'].max()),
    (int(somalia_df['year'].min()), int(somalia_df['year'].max()))
)

# Filter data based on selected year range
filtered_data = somalia_df[
    (somalia_df['year'] >= year_range[0]) &
    (somalia_df['year'] <= year_range[1])
]

# Create the time plot
fig_time_plot = px.histogram(
    filtered_data,
    x='year',
    title='Pirate Attacks Over Time around Somalia',
    labels={'year': 'Year', 'count': 'Number of Attacks'},
    template='plotly_dark',
    nbins=len(filtered_data['year'].unique()),  # Use one bin per unique year
    marginal='rug',  # Add rug plot for each data point
    histfunc='count',
)

# Add a red line plot
line_data = filtered_data.groupby('year').size().reset_index(name='count')
fig_time_plot.add_trace(
    px.line(
        line_data,
        x='year',
        y='count',
    ).update_traces(line=dict(color='red')).data[0]
)

# Display the plot
st.plotly_chart(fig_time_plot)
