# 📚 Book Analytics Dashboard using Streamlit

## Overview

This project is an interactive **Book Analytics Dashboard** developed using **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn**. The dashboard provides an intuitive interface for exploring a books dataset through interactive filters, statistical summaries, business insights, and visualizations.

The project demonstrates how raw data can be transformed into meaningful visualizations that support data-driven decision making.

This project was developed as part of a **Data Analytics Internship**.

---

# Objectives

The primary objectives of this project are:

- Transform raw data into meaningful visualizations.
- Build an interactive dashboard.
- Explore business insights using visual analytics.
- Perform descriptive statistical analysis.
- Detect outliers and trends.
- Allow users to interact with the dataset using filters.
- Support decision making through data storytelling.

---

# Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn

---

# Dataset

The dataset was created by scraping the **Books to Scrape** website.

Dataset Features

| Column | Description |
|---------|-------------|
| Title | Book Name |
| Price | Price of Book (£) |
| Rating | Book Rating (1–5 Stars) |

---

# Dashboard Features

## Interactive Filters

Users can filter the dashboard using

- Minimum Price
- Maximum Price
- Rating Selection

---

## Dashboard KPIs

The dashboard displays

- Total Books
- Average Book Price
- Average Rating
- Most Common Rating

---

## Dashboard Sections

### 📊 Data Overview

Displays

- Dataset Preview
- Number of Rows
- Number of Columns
- Dataset Information
- Missing Values

---

### 💰 Price Analysis

Includes

- Price Statistics
- Mean
- Median
- Maximum Price
- Minimum Price
- Standard Deviation
- Quartile Analysis
- Price Histogram
- Box Plot
- Outlier Detection

---

### ⭐ Rating Analysis

Displays

- Rating Statistics
- Rating Distribution
- Percentage of Ratings
- High Rated Books
- Dominant Rating Category
- Rating Bar Chart

---

### 💼 Business Insights

Provides

- Price vs Rating Correlation
- Scatter Plot
- Trend Line
- Average Price by Rating
- Business Insights
- Variance Analysis

---

### 💾 Data Export

Users can export the filtered and cleaned dataset into a CSV file directly from the dashboard.

---

# Dashboard Workflow

```

Books Dataset

↓

Load Dataset

↓

Data Cleaning

↓

Interactive Filters

↓

Statistical Analysis

↓

Visualizations

↓

Business Insights

↓

Export Dataset

```

---

# Visualizations Included

- Price Distribution Histogram
- Rating Distribution Bar Chart
- Price vs Rating Scatter Plot
- Price Box Plot
- Trend Line
- KPI Cards

---

# Statistical Analysis

The dashboard performs

- Descriptive Statistics
- Correlation Analysis
- Quartile Analysis
- Variance Analysis
- Outlier Detection
- Distribution Analysis

---

# Key Insights

The dashboard helps answer questions such as

- What is the average book price?
- Which rating is most common?
- Are expensive books rated higher?
- What percentage of books have ratings above 4?
- Are there any price outliers?
- What is the overall price distribution?
- How does rating affect price?

---

# Project Structure

```

Book-Analytics-Dashboard/

│

├── app.py

├── books_dataset.csv

├── requirements.txt

├── README.md

└── screenshots/

```

---

# Installation

Clone the repository

```bash
git clone https://github.com/kantisharma07/Book-Analytics-Dashboard.git
```

Move into the project folder

```bash
cd Book-Analytics-Dashboard
```

Install the required libraries

```bash
pip install -r requirements.txt
```

---

# Run the Application

```bash
streamlit run app.py
```

The dashboard will automatically open in your default web browser.

---

# Requirements

```
streamlit
pandas
numpy
matplotlib
seaborn
```

---

# Skills Demonstrated

- Interactive Dashboard Development
- Data Visualization
- Exploratory Data Analysis
- Business Intelligence
- Data Cleaning
- Statistical Analysis
- Correlation Analysis
- Outlier Detection
- Python Programming
- Streamlit Development

---

# Future Improvements

- Add Category Analysis
- Add Availability Analysis
- Integrate SQL Database
- Deploy Dashboard on Streamlit Cloud
- Add Advanced Filters
- Add Time Series Analysis
- Add Download Options (Excel/PDF)

---

# Author

**Kanti Sharma**

GitHub:
https://github.com/kantisharma07

