import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Book Analytics Dashboard",
    page_icon="📚",
    layout="wide"
)

# Set style
sns.set_style("whitegrid")

# File path
file_path = r"C:\Users\rahul\Desktop\python\Internship_Projects\Project_1\books_dataset.csv"

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    
    # Clean Price column
    df["Price"] = df["Price"].str.replace(r'[^\d.]', '', regex=True).astype(float)
    
    # Clean Rating column
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["Rating"] = df["Rating"].map(rating_map)
    
    return df

# Load data
try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
except FileNotFoundError:
    st.error(f"❌ File not found at: {file_path}")
    st.info("Please make sure the file exists in the correct location.")
    st.stop()

# Sidebar
st.sidebar.title("📚 Navigation")
st.sidebar.markdown("---")

# Sidebar filters
st.sidebar.subheader("🔍 Filter Data")
min_price = st.sidebar.slider(
    "Minimum Price (£)",
    min_value=float(df["Price"].min()),
    max_value=float(df["Price"].max()),
    value=float(df["Price"].min())
)

max_price = st.sidebar.slider(
    "Maximum Price (£)",
    min_value=float(df["Price"].min()),
    max_value=float(df["Price"].max()),
    value=float(df["Price"].max())
)

selected_ratings = st.sidebar.multiselect(
    "Select Ratings",
    options=sorted(df["Rating"].unique()),
    default=sorted(df["Rating"].unique())
)

# Apply filters
filtered_df = df[
    (df["Price"] >= min_price) & 
    (df["Price"] <= max_price) &
    (df["Rating"].isin(selected_ratings))
]

# Main title
st.title("📚 Book Analytics Dashboard")
st.markdown("---")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Books",
        f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df)} filtered"
    )

with col2:
    st.metric(
        "Average Price",
        f"£{filtered_df['Price'].mean():.2f}",
        delta=f"£{filtered_df['Price'].mean() - df['Price'].mean():.2f}"
    )

with col3:
    st.metric(
        "Average Rating",
        f"{filtered_df['Rating'].mean():.2f} ⭐",
        delta=f"{filtered_df['Rating'].mean() - df['Rating'].mean():.2f}"
    )

with col4:
    st.metric(
        "Most Common Rating",
        f"{filtered_df['Rating'].mode()[0]} ⭐",
        delta=f"{filtered_df['Rating'].value_counts().max()} books"
    )

st.markdown("---")

# Tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "📈 Price Analysis", "⭐ Rating Analysis", "📉 Business Insights"])

# Tab 1: Data Overview
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Raw Data")
        st.dataframe(filtered_df, use_container_width=True)
    
    with col2:
        st.subheader("📊 Data Summary")
        st.write(f"**Rows:** {filtered_df.shape[0]}")
        st.write(f"**Columns:** {filtered_df.shape[1]}")
        st.write("**Column Names:**")
        for col in filtered_df.columns:
            st.write(f"- {col}")
        
        st.subheader("📝 Null Values")
        null_counts = filtered_df.isnull().sum()
        if null_counts.sum() == 0:
            st.success("✅ No null values found!")
        else:
            st.write(null_counts)

# Tab 2: Price Analysis
with tab2:
    st.subheader("💰 Price Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Price Statistics**")
        price_stats = pd.DataFrame({
            "Statistic": ["Mean", "Median", "Maximum", "Minimum", "Std Dev"],
            "Value": [
                f"£{filtered_df['Price'].mean():.2f}",
                f"£{filtered_df['Price'].median():.2f}",
                f"£{filtered_df['Price'].max():.2f}",
                f"£{filtered_df['Price'].min():.2f}",
                f"£{filtered_df['Price'].std():.2f}"
            ]
        })
        st.dataframe(price_stats, hide_index=True, use_container_width=True)
        
        # Price quartiles
        quartiles = filtered_df['Price'].quantile([0.25, 0.5, 0.75])
        st.write("**Price Distribution**")
        st.write(f"- 25th Percentile: £{quartiles[0.25]:.2f}")
        st.write(f"- 50th Percentile (Median): £{quartiles[0.5]:.2f}")
        st.write(f"- 75th Percentile: £{quartiles[0.75]:.2f}")
    
    with col2:
        # Price histogram
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        ax1.hist(filtered_df['Price'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
        ax1.axvline(filtered_df['Price'].mean(), color='red', linestyle='--', 
                   label=f'Mean: £{filtered_df["Price"].mean():.2f}')
        ax1.axvline(filtered_df['Price'].median(), color='green', linestyle='--', 
                   label=f'Median: £{filtered_df["Price"].median():.2f}')
        ax1.set_xlabel('Price (£)')
        ax1.set_ylabel('Number of Books')
        ax1.set_title('Price Distribution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
        plt.close()
    
    # Outlier detection
    st.subheader("📊 Outlier Analysis")
    Q1 = filtered_df['Price'].quantile(0.25)
    Q3 = filtered_df['Price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = filtered_df[(filtered_df['Price'] < lower_bound) | (filtered_df['Price'] > upper_bound)]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Number of Outliers", len(outliers))
        st.metric("Outlier Percentage", f"{len(outliers)/len(filtered_df)*100:.1f}%")
    
    with col2:
        if len(outliers) > 0:
            st.write("**Outlier Price Range:**")
            st.write(f"Min: £{outliers['Price'].min():.2f}")
            st.write(f"Max: £{outliers['Price'].max():.2f}")
            
            # Box plot
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.boxplot(filtered_df['Price'], patch_artist=True, 
                       boxprops=dict(facecolor='lightblue'))
            ax2.set_ylabel('Price (£)')
            ax2.set_title('Price Box Plot with Outliers')
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)
            plt.close()

# Tab 3: Rating Analysis
with tab3:
    st.subheader("⭐ Rating Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Rating Statistics**")
        rating_stats = pd.DataFrame({
            "Statistic": ["Mean", "Median", "Mode", "Most Common"],
            "Value": [
                f"{filtered_df['Rating'].mean():.2f} ⭐",
                f"{filtered_df['Rating'].median():.0f} ⭐",
                f"{filtered_df['Rating'].mode()[0]} ⭐",
                f"{filtered_df['Rating'].value_counts().max()} books"
            ]
        })
        st.dataframe(rating_stats, hide_index=True, use_container_width=True)
        
        # Rating distribution table
        st.write("**Rating Distribution**")
        rating_dist = filtered_df['Rating'].value_counts().sort_index()
        rating_df = pd.DataFrame({
            'Rating': rating_dist.index,
            'Count': rating_dist.values,
            'Percentage': (rating_dist.values / len(filtered_df) * 100).round(1)
        })
        rating_df['Percentage'] = rating_df['Percentage'].astype(str) + '%'
        st.dataframe(rating_df, hide_index=True, use_container_width=True)
    
    with col2:
        # Rating bar chart
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        colors = ['#ff9999', '#ffcc99', '#99cc99', '#66b3ff', '#c2c2f0']
        rating_counts = filtered_df['Rating'].value_counts().sort_index()
        bars = ax3.bar(rating_counts.index, rating_counts.values, color=colors, edgecolor='black')
        for bar, count in zip(bars, rating_counts.values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{count}', ha='center', va='bottom')
        ax3.set_xlabel('Rating (Stars)')
        ax3.set_ylabel('Number of Books')
        ax3.set_title('Rating Distribution')
        ax3.grid(True, alpha=0.3)
        st.pyplot(fig3)
        plt.close()
    
    # High rating analysis
    st.subheader("🏆 High Rating Analysis")
    high_rating_pct = (filtered_df[filtered_df['Rating'] > 4].shape[0] / len(filtered_df)) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Books with Rating > 4", 
                 f"{filtered_df[filtered_df['Rating'] > 4].shape[0]}",
                 f"{high_rating_pct:.1f}%")
    with col2:
        st.metric("Books with Rating = 5", 
                 f"{filtered_df[filtered_df['Rating'] == 5].shape[0]}",
                 f"{filtered_df[filtered_df['Rating'] == 5].shape[0]/len(filtered_df)*100:.1f}%")
    with col3:
        st.metric("Dominant Rating", 
                 f"{filtered_df['Rating'].mode()[0]} ⭐",
                 f"{filtered_df['Rating'].value_counts().max()} books")

# Tab 4: Business Insights
with tab4:
    st.subheader("💼 Business Insights")
    
    # Price vs Rating Correlation
    correlation = filtered_df['Price'].corr(filtered_df['Rating'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Price vs Rating Correlation**")
        st.metric("Correlation Coefficient", f"{correlation:.3f}")
        
        if correlation > 0.3:
            st.success("✅ Positive correlation: Expensive books tend to have higher ratings")
        elif correlation < -0.3:
            st.warning("⚠️ Negative correlation: Cheaper books tend to have higher ratings")
        else:
            st.info("ℹ️ Weak correlation: Price and rating are not strongly related")
        
        # Price by rating group
        st.write("**Average Price by Rating**")
        price_by_rating = filtered_df.groupby('Rating')['Price'].mean().round(2)
        price_df = pd.DataFrame({
            'Rating': price_by_rating.index,
            'Average Price': price_by_rating.values
        })
        price_df['Average Price'] = '£' + price_df['Average Price'].astype(str)
        st.dataframe(price_df, hide_index=True, use_container_width=True)
    
    with col2:
        # Scatter plot
        fig4, ax4 = plt.subplots(figsize=(8, 6))
        scatter = ax4.scatter(filtered_df['Rating'], filtered_df['Price'], 
                            alpha=0.6, c=filtered_df['Price'], 
                            cmap='viridis', s=50)
        ax4.set_xlabel('Rating (Stars)')
        ax4.set_ylabel('Price (£)')
        ax4.set_title('Price vs Rating Correlation')
        ax4.grid(True, alpha=0.3)
        
        # Add trend line
        if len(filtered_df) > 1:
            z = np.polyfit(filtered_df['Rating'], filtered_df['Price'], 1)
            p = np.poly1d(z)
            ax4.plot(sorted(filtered_df['Rating'].unique()), 
                    p(sorted(filtered_df['Rating'].unique())), 
                    "r--", linewidth=2, label=f'Trend (r={correlation:.3f})')
            ax4.legend()
        
        plt.colorbar(scatter, ax=ax4, label='Price (£)')
        st.pyplot(fig4)
        plt.close()
    
    # Additional Insights
    st.subheader("📊 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Price Analysis**")
        st.write(f"- Price range: £{filtered_df['Price'].min():.2f} - £{filtered_df['Price'].max():.2f}")
        st.write(f"- Price spread: £{filtered_df['Price'].max() - filtered_df['Price'].min():.2f}")
        st.write(f"- Price variance: {filtered_df['Price'].var():.2f}")
    
    with col2:
        st.write("**Rating Analysis**")
        st.write(f"- Rating range: {filtered_df['Rating'].min()} - {filtered_df['Rating'].max()} ⭐")
        st.write(f"- Most common rating: {filtered_df['Rating'].mode()[0]} ⭐")
        st.write(f"- Rating variance: {filtered_df['Rating'].var():.2f}")
    
    # Export data option
    st.subheader("💾 Export Data")
    if st.button("Download Cleaned Data (CSV)"):
        save_path = r"C:\Users\rahul\Desktop\python\Internship_Projects\Project_1\cleaned_books_data.csv"
        filtered_df.to_csv(save_path, index=False)
        st.success(f"✅ Data saved to: {save_path}")

# Footer
st.markdown("---")
st.markdown("📊 **Book Analytics Dashboard** | Created with Streamlit")
