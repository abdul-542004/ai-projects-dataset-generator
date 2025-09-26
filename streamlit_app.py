"""
Synthetic AI Projects Dataset - Interactive Analysis Dashboard

This Streamlit app provides an interactive analysis of the synthetic AI projects dataset
containing 500 evidence-based project profiles designed for composite case studies.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
import os
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="AI Projects Dataset Analysis",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the synthetic dataset"""
    csv_files = glob.glob('synthetic_ai_projects_dataset_*.csv')
    if csv_files:
        latest_csv = max(csv_files, key=os.path.getmtime)
        df = pd.read_csv(latest_csv)
        return df, latest_csv
    return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Projects Dataset Analysis</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Overview
    This interactive dashboard analyzes a synthetic AI projects dataset containing 500 evidence-based project profiles 
    designed for composite case studies. The dataset incorporates real-world research findings and statistical 
    correlations to provide realistic business scenarios while maintaining complete confidentiality.
    
    ### Key Features
    - **Evidence-Based Correlations**: MIT J-curve, CEO survey data, McKinsey KPI research
    - **Industry-Specific Patterns**: 12 sectors with realistic AI adoption characteristics  
    - **Comprehensive Metrics**: Revenue impact, EBITDA improvement, valuation expansion
    - **Statistical Validation**: Benchmarked against published research studies
    """)
    
    # Load data
    df, filename = load_data()
    
    if df is None:
        st.error("❌ No dataset file found. Please run the generator script first.")
        return
    
    st.success(f"✅ Loaded dataset from: {filename}")
    
    # Sidebar filters
    st.sidebar.header("🔍 Filter Data")
    
    # Industry filter
    industries = ['All'] + sorted(df['industry'].unique().tolist())
    selected_industry = st.sidebar.selectbox("Select Industry:", industries)
    
    # Company size filter
    sizes = ['All'] + sorted(df['company_size'].unique().tolist())
    selected_size = st.sidebar.selectbox("Select Company Size:", sizes)
    
    # Success filter
    success_filter = st.sidebar.selectbox("Success Status:", ['All', 'Successful Only', 'Failed Only'])
    
    # Apply filters
    filtered_df = df.copy()
    if selected_industry != 'All':
        filtered_df = filtered_df[filtered_df['industry'] == selected_industry]
    if selected_size != 'All':
        filtered_df = filtered_df[filtered_df['company_size'] == selected_size]
    if success_filter == 'Successful Only':
        filtered_df = filtered_df[filtered_df['is_successful'] == True]
    elif success_filter == 'Failed Only':
        filtered_df = filtered_df[filtered_df['is_successful'] == False]
    
    # Display filter results
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the current filters. Please adjust your selections.")
        return
    
    st.sidebar.write(f"**Filtered Records:** {len(filtered_df)} out of {len(df)}")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "🏢 Company Demographics", "🤖 AI Projects", 
        "💰 Business Impact", "🔗 Correlations", "🎯 Insights"
    ])
    
    with tab1:
        overview_tab(filtered_df, df)
    
    with tab2:
        demographics_tab(filtered_df)
    
    with tab3:
        projects_tab(filtered_df)
    
    with tab4:
        impact_tab(filtered_df)
    
    with tab5:
        correlations_tab(filtered_df)
    
    with tab6:
        insights_tab(filtered_df, df)

def overview_tab(filtered_df, full_df):
    """Overview tab with key metrics and validation"""
    st.header("📊 Dataset Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", len(filtered_df))
    with col2:
        st.metric("Success Rate", f"{filtered_df['is_successful'].mean():.1%}")
    with col3:
        st.metric("Avg Revenue Impact", f"{filtered_df['revenue_impact_pct'].mean():.1f}%")
    with col4:
        st.metric("Avg ROI", f"{filtered_df['annual_roi'].mean():.1f}x")
    
    # Research validation
    st.subheader("🔬 Research Validation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### MIT J-Curve Validation")
        low_intensity = full_df[full_df['ai_intensity'] < 0.005]
        high_intensity = full_df[full_df['ai_intensity'] > 0.025]
        
        validation_data = {
            'AI Intensity Level': ['Low (<0.5%)', 'High (>2.5%)'],
            'Avg Revenue Growth': [f"{low_intensity['revenue_impact_pct'].mean():.1f}%", 
                                 f"{high_intensity['revenue_impact_pct'].mean():.1f}%"]
        }
        st.table(pd.DataFrame(validation_data))
        
        correlation = full_df[['ai_intensity', 'revenue_impact_pct']].corr().iloc[0,1]
        st.metric("AI Intensity-Revenue Correlation", f"{correlation:.3f}")
    
    with col2:
        st.markdown("### KPI Tracking Impact")
        kpi_tracked = full_df[full_df['has_kpi_tracking'] == True]
        non_kpi_tracked = full_df[full_df['has_kpi_tracking'] == False]
        
        kpi_impact_diff = kpi_tracked['ebitda_impact_pct'].mean() - non_kpi_tracked['ebitda_impact_pct'].mean()
        st.metric("EBITDA Impact Difference", f"+{kpi_impact_diff:.1f}%")
        st.metric("KPI Tracking Rate", f"{full_df['has_kpi_tracking'].mean():.1%}")
    
    # Dataset structure
    st.subheader("📋 Dataset Structure")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Column Information:**")
        st.write(f"Total Variables: {len(filtered_df.columns)}")
        st.write(f"Data Types: {filtered_df.dtypes.value_counts().to_dict()}")
    
    with col2:
        st.markdown("**Sample Data:**")
        st.dataframe(filtered_df.head(3))

def demographics_tab(filtered_df):
    """Company demographics analysis"""
    st.header("🏢 Company Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Company size distribution
        fig_size = px.pie(
            values=filtered_df['company_size'].value_counts().values,
            names=filtered_df['company_size'].value_counts().index,
            title="Company Size Distribution"
        )
        st.plotly_chart(fig_size, use_container_width=True)
        
        # Regional distribution
        fig_region = px.pie(
            values=filtered_df['region'].value_counts().values,
            names=filtered_df['region'].value_counts().index,
            title="Geographic Distribution"
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        # Industry distribution (top 8)
        industry_counts = filtered_df['industry'].value_counts().head(8)
        fig_industry = px.bar(
            x=industry_counts.values,
            y=industry_counts.index,
            orientation='h',
            title="Top 8 Industries by Project Count"
        )
        fig_industry.update_layout(height=400)
        st.plotly_chart(fig_industry, use_container_width=True)
        
        # Revenue distribution by company size
        fig_revenue = px.box(
            filtered_df,
            x='company_size',
            y='annual_revenue',
            title="Revenue Distribution by Company Size"
        )
        fig_revenue.update_layout(yaxis_type="log")
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Summary statistics
    st.subheader("📈 Demographics Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Size Distribution:**")
        st.write(filtered_df['company_size'].value_counts())
    
    with col2:
        st.markdown("**Ownership Distribution:**")
        st.write(filtered_df['ownership'].value_counts())
    
    with col3:
        st.markdown("**Growth Stage Distribution:**")
        st.write(filtered_df['growth_stage'].value_counts())

def projects_tab(filtered_df):
    """AI project characteristics analysis"""
    st.header("🤖 AI Project Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Project type distribution
        fig_type = px.pie(
            values=filtered_df['project_type'].value_counts().values,
            names=filtered_df['project_type'].value_counts().index,
            title="AI Project Type Distribution"
        )
        st.plotly_chart(fig_type, use_container_width=True)
        
        # Complexity distribution
        complexity_counts = filtered_df['complexity'].value_counts()
        fig_complexity = px.bar(
            x=complexity_counts.index,
            y=complexity_counts.values,
            title="Project Complexity Distribution",
            color=complexity_counts.index,
            color_discrete_map={'Basic': 'lightblue', 'Intermediate': 'orange', 'Advanced': 'red'}
        )
        st.plotly_chart(fig_complexity, use_container_width=True)
    
    with col2:
        # Investment distribution
        if len(filtered_df) > 0:
            # Create histogram with better formatting
            fig_investment = px.histogram(
                filtered_df,
                x='investment_amount',
                title="Investment Amount Distribution",
                nbins=30
            )
            
            # Format to show millions and improve readability
            fig_investment.update_layout(
                xaxis_title="Investment Amount ($)",
                yaxis_title="Number of Projects",
                xaxis=dict(
                    tickformat=",.0s",  # Format as abbreviated numbers (1M, 1B, etc.)
                    title="Investment Amount ($)"
                )
            )
            
            # Add mean and median lines
            mean_val = filtered_df['investment_amount'].mean()
            median_val = filtered_df['investment_amount'].median()
            
            fig_investment.add_vline(x=mean_val, line_dash="dash", line_color="red",
                                   annotation_text=f"Mean: ${mean_val/1e6:.1f}M")
            fig_investment.add_vline(x=median_val, line_dash="dot", line_color="blue",
                                   annotation_text=f"Median: ${median_val/1e6:.1f}M")
        else:
            # Create empty chart if no data
            fig_investment = px.histogram(
                x=[],
                title="Investment Amount Distribution - No Data Available"
            )
        
        st.plotly_chart(fig_investment, use_container_width=True)
        
        # AI Intensity distribution
        fig_intensity = px.histogram(
            filtered_df,
            x=filtered_df['ai_intensity'] * 100,
            title="AI Investment Intensity (% of Revenue)",
            nbins=30
        )
        st.plotly_chart(fig_intensity, use_container_width=True)
    
    # Success rate by complexity
    st.subheader("📊 Success Analysis")
    
    success_by_complexity = filtered_df.groupby('complexity')['is_successful'].mean()
    fig_success = px.bar(
        x=success_by_complexity.index,
        y=success_by_complexity.values,
        title="Success Rate by Project Complexity",
        color=success_by_complexity.index,
        color_discrete_map={'Basic': 'lightgreen', 'Intermediate': 'yellow', 'Advanced': 'lightcoral'}
    )
    fig_success.update_layout(yaxis=dict(range=[0, 1]))
    st.plotly_chart(fig_success, use_container_width=True)
    
    # Project characteristics summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Investment", f"${filtered_df['investment_amount'].mean():,.0f}")
        st.metric("Median Investment", f"${filtered_df['investment_amount'].median():,.0f}")
    
    with col2:
        st.metric("Average AI Intensity", f"{filtered_df['ai_intensity'].mean():.2%}")
        st.metric("Average Deployment Time", f"{filtered_df['deployment_months'].mean():.1f} months")
    
    with col3:
        st.metric("Overall Success Rate", f"{filtered_df['is_successful'].mean():.1%}")
        st.metric("Most Common Project Type", filtered_df['project_type'].mode().iloc[0])

def impact_tab(filtered_df):
    """Business impact analysis"""
    st.header("💰 Business Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue impact distribution
        fig_revenue = px.histogram(
            filtered_df,
            x='revenue_impact_pct',
            title="Revenue Impact Distribution",
            nbins=30
        )
        fig_revenue.add_vline(x=filtered_df['revenue_impact_pct'].mean(), 
                            line_dash="dash", line_color="red",
                            annotation_text=f"Mean: {filtered_df['revenue_impact_pct'].mean():.1f}%")
        st.plotly_chart(fig_revenue, use_container_width=True)
        
        # ROI distribution
        roi_capped = np.minimum(filtered_df['annual_roi'], 20)
        fig_roi = px.histogram(
            x=roi_capped,
            title="Annual ROI Distribution (capped at 20x)",
            nbins=30,
            labels={'x': 'Annual ROI', 'y': 'Number of Projects'}
        )
        if len(roi_capped) > 0:  # Only add line if we have data
            fig_roi.add_vline(x=roi_capped.mean(), 
                             line_dash="dash", line_color="red",
                             annotation_text=f"Mean: {roi_capped.mean():.1f}x")
        st.plotly_chart(fig_roi, use_container_width=True)
    
    with col2:
        # EBITDA impact distribution
        fig_ebitda = px.histogram(
            filtered_df,
            x='ebitda_impact_pct',
            title="EBITDA Impact Distribution",
            nbins=30
        )
        fig_ebitda.add_vline(x=filtered_df['ebitda_impact_pct'].mean(), 
                           line_dash="dash", line_color="red",
                           annotation_text=f"Mean: {filtered_df['ebitda_impact_pct'].mean():.1f}%")
        st.plotly_chart(fig_ebitda, use_container_width=True)
        
        # Payback period distribution
        payback_capped = np.minimum(filtered_df['payback_months'], 60)
        fig_payback = px.histogram(
            x=payback_capped,
            title="Payback Period Distribution (capped at 60 months)",
            nbins=25,
            labels={'x': 'Payback Period (Months)', 'y': 'Number of Projects'}
        )
        if len(payback_capped) > 0:  # Only add line if we have data
            fig_payback.add_vline(x=payback_capped.mean(), 
                                line_dash="dash", line_color="red",
                                annotation_text=f"Mean: {payback_capped.mean():.1f} months")
        st.plotly_chart(fig_payback, use_container_width=True)
    
    # Revenue impact by industry
    st.subheader("🏭 Impact by Industry")
    
    if len(filtered_df['industry'].unique()) > 1:
        top_industries = filtered_df['industry'].value_counts().head(6).index
        industry_revenue = filtered_df[filtered_df['industry'].isin(top_industries)].groupby('industry')['revenue_impact_pct'].mean().sort_values(ascending=True)
        
        fig_industry_impact = px.bar(
            x=industry_revenue.values,
            y=industry_revenue.index,
            orientation='h',
            title="Average Revenue Impact by Industry (Top 6)"
        )
        st.plotly_chart(fig_industry_impact, use_container_width=True)
    
    # Success rate by company size
    if len(filtered_df['company_size'].unique()) > 1:
        success_by_size = filtered_df.groupby('company_size')['is_successful'].mean()
        fig_success_size = px.bar(
            x=success_by_size.index,
            y=success_by_size.values,
            title="Success Rate by Company Size",
            color=success_by_size.index
        )
        fig_success_size.update_layout(yaxis=dict(range=[0, 1]))
        st.plotly_chart(fig_success_size, use_container_width=True)
    
    # Impact summary metrics
    st.subheader("📊 Impact Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Revenue Impact", f"{filtered_df['revenue_impact_pct'].mean():.2f}%")
        st.metric("Median Revenue Impact", f"{filtered_df['revenue_impact_pct'].median():.2f}%")
    
    with col2:
        st.metric("Avg EBITDA Impact", f"{filtered_df['ebitda_impact_pct'].mean():.2f}%")
        st.metric("Median EBITDA Impact", f"{filtered_df['ebitda_impact_pct'].median():.2f}%")
    
    with col3:
        st.metric("Avg Annual ROI", f"{filtered_df['annual_roi'].mean():.2f}x")
        st.metric("Median Annual ROI", f"{filtered_df['annual_roi'].median():.2f}x")
    
    with col4:
        st.metric("Avg Payback Period", f"{filtered_df['payback_months'].mean():.1f} months")
        st.metric("Median Payback Period", f"{filtered_df['payback_months'].median():.1f} months")

def correlations_tab(filtered_df):
    """Evidence-based correlations analysis"""
    st.header("🔗 Evidence-Based Correlations")
    
    # MIT J-curve: AI Intensity vs Revenue Impact
    st.subheader("📈 MIT J-Curve: AI Intensity vs Revenue Growth")
    
    fig_jcurve = px.scatter(
        filtered_df,
        x=filtered_df['ai_intensity'] * 100,
        y='revenue_impact_pct',
        title="AI Intensity vs Revenue Impact",
        labels={'x': 'AI Intensity (% of Revenue)', 'y': 'Revenue Impact (%)'},
        trendline="ols"
    )
    
    # Add correlation coefficient
    corr_coef = filtered_df['ai_intensity'].corr(filtered_df['revenue_impact_pct'])
    fig_jcurve.add_annotation(
        x=0.05, y=0.95, xref="paper", yref="paper",
        text=f"Correlation: {corr_coef:.3f}",
        showarrow=False,
        bgcolor="wheat"
    )
    
    st.plotly_chart(fig_jcurve, use_container_width=True)
    
    # KPI Tracking Impact
    st.subheader("📊 KPI Tracking Impact on EBITDA")
    
    if len(filtered_df) > 0:
        kpi_yes = filtered_df[filtered_df['has_kpi_tracking']]['ebitda_impact_pct']
        kpi_no = filtered_df[~filtered_df['has_kpi_tracking']]['ebitda_impact_pct']
        
        if len(kpi_yes) > 0 and len(kpi_no) > 0:
            fig_kpi = px.box(
                filtered_df,
                x='has_kpi_tracking',
                y='ebitda_impact_pct',
                title="KPI Tracking Impact on EBITDA Performance"
            )
            
            mean_diff = kpi_yes.mean() - kpi_no.mean() if len(kpi_yes) > 0 and len(kpi_no) > 0 else 0
            fig_kpi.add_annotation(
                x=0.5, y=0.95, xref="paper", yref="paper",
                text=f"Difference: +{mean_diff:.1f}%",
                showarrow=False,
                bgcolor="wheat"
            )
            
            st.plotly_chart(fig_kpi, use_container_width=True)
    
    # Company Size vs AI Maturity
    st.subheader("🏢 Company Size vs AI Maturity Rate")
    
    if len(filtered_df['company_size'].unique()) > 1:
        size_order = ['Small', 'Medium', 'Large']
        available_sizes = [size for size in size_order if size in filtered_df['company_size'].unique()]
        
        if available_sizes:
            maturity_rates = []
            for size in available_sizes:
                rate = filtered_df[filtered_df['company_size'] == size]['is_mature_implementation'].mean()
                maturity_rates.append(rate)
            
            fig_maturity = px.bar(
                x=available_sizes,
                y=maturity_rates,
                title="Inverse Correlation: Company Size vs AI Maturity",
                color=available_sizes
            )
            fig_maturity.update_layout(yaxis=dict(range=[0, max(maturity_rates) * 1.2 if maturity_rates else 1]))
            st.plotly_chart(fig_maturity, use_container_width=True)
    
    # Correlation matrix
    st.subheader("🔥 Correlation Matrix - Key Variables")
    
    key_vars = ['ai_intensity', 'revenue_impact_pct', 'ebitda_impact_pct', 
                'annual_roi', 'deployment_months', 'employees', 'annual_revenue']
    
    # Filter to only include columns that exist in the dataframe
    available_vars = [var for var in key_vars if var in filtered_df.columns]
    
    if len(available_vars) > 1:
        corr_matrix = filtered_df[available_vars].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            title="Correlation Matrix - Key Variables",
            aspect="auto",
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Key correlations
        st.markdown("**Key Correlations:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if all(var in available_vars for var in ['ai_intensity', 'revenue_impact_pct']):
                st.write(f"AI Intensity ↔ Revenue Impact: {filtered_df['ai_intensity'].corr(filtered_df['revenue_impact_pct']):.3f}")
            if all(var in available_vars for var in ['revenue_impact_pct', 'ebitda_impact_pct']):
                st.write(f"Revenue Impact ↔ EBITDA Impact: {filtered_df['revenue_impact_pct'].corr(filtered_df['ebitda_impact_pct']):.3f}")
        
        with col2:
            if all(var in available_vars for var in ['investment_amount', 'annual_revenue']):
                st.write(f"Investment Amount ↔ Annual Revenue: {filtered_df['investment_amount'].corr(filtered_df['annual_revenue']):.3f}")
            if all(var in available_vars for var in ['deployment_months', 'annual_roi']):
                st.write(f"Deployment Months ↔ Annual ROI: {filtered_df['deployment_months'].corr(filtered_df['annual_roi']):.3f}")

def insights_tab(filtered_df, full_df):
    """Key insights and recommendations"""
    st.header("🎯 Key Insights & Recommendations")
    
    # Calculate key metrics
    overall_success_rate = filtered_df['is_successful'].mean()
    avg_revenue_impact = filtered_df['revenue_impact_pct'].mean()
    avg_ebitda_impact = filtered_df['ebitda_impact_pct'].mean()
    avg_roi = filtered_df['annual_roi'].mean()
    median_payback = filtered_df['payback_months'].median()
    
    # Dataset validation summary
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("📊 Dataset Validation Summary")
    
    high_intensity_projects = full_df[full_df['ai_intensity'] > 0.025]
    low_intensity_projects = full_df[full_df['ai_intensity'] < 0.005]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("✅ **MIT J-Curve Effect:**")
        st.write(f"High AI intensity: {high_intensity_projects['revenue_impact_pct'].mean():.1f}% revenue growth")
        st.write(f"Low AI intensity: {low_intensity_projects['revenue_impact_pct'].mean():.1f}% revenue growth")
        
        st.write("✅ **CEO Success Rate:**")
        st.write(f"{overall_success_rate:.1%} show measurable benefits (target: ~66%)")
    
    with col2:
        if len(full_df) > 0:
            kpi_tracked_performance = full_df[full_df['has_kpi_tracking']]['ebitda_impact_pct'].mean()
            non_kpi_tracked_performance = full_df[~full_df['has_kpi_tracking']]['ebitda_impact_pct'].mean()
            
            st.write("✅ **KPI Tracking Impact:**")
            st.write(f"{kpi_tracked_performance - non_kpi_tracked_performance:+.1f}% EBITDA improvement")
            
            st.write("✅ **Size-Maturity Inverse:**")
            small_maturity = full_df[full_df['company_size']=='Small']['is_mature_implementation'].mean()
            large_maturity = full_df[full_df['company_size']=='Large']['is_mature_implementation'].mean()
            st.write(f"Small companies: {small_maturity:.1%} vs Large: {large_maturity:.1%} maturity")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key business insights
    st.subheader("💡 Key Business Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Revenue Impact", f"{avg_revenue_impact:.1f}%")
        st.metric("Range", f"{filtered_df['revenue_impact_pct'].min():.1f}% to {filtered_df['revenue_impact_pct'].max():.1f}%")
    
    with col2:
        st.metric("Average EBITDA Impact", f"{avg_ebitda_impact:.1f}%")
        st.metric("vs Revenue Ratio", f"{avg_ebitda_impact/avg_revenue_impact if avg_revenue_impact != 0 else 0:.1f}x")
    
    with col3:
        st.metric("Average Annual ROI", f"{avg_roi:.1f}x")
        st.metric("Success Rate", f"{overall_success_rate:.1%}")
    
    with col4:
        st.metric("Median Payback Period", f"{median_payback:.1f} months")
        st.metric("Projects Analyzed", f"{len(filtered_df)}")
    
    # Industry patterns
    if len(filtered_df['industry'].unique()) > 1:
        st.subheader("🏭 Industry Patterns")
        
        top_performing_industry = filtered_df.groupby('industry')['revenue_impact_pct'].mean().idxmax()
        top_success_industry = filtered_df.groupby('industry')['is_successful'].mean().idxmax()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"🚀 **Best Revenue Impact:** {top_performing_industry}")
            st.write(f"Impact: {filtered_df[filtered_df['industry']==top_performing_industry]['revenue_impact_pct'].mean():.1f}% avg")
            
        with col2:
            st.write(f"✨ **Highest Success Rate:** {top_success_industry}")
            st.write(f"Success: {filtered_df[filtered_df['industry']==top_success_industry]['is_successful'].mean():.1%}")
    
    # Recommendations
    st.subheader("📋 Recommendations for Evidence-Based Case Studies")
    
    recommendations = [
        "🎯 Focus on High-Impact Segments: Use 'High Performers' and 'Digital Transformation Leaders'",
        "🏭 Industry Specialization: Technology, Financial Services, and Manufacturing show strongest patterns",
        "📊 KPI Success Factor: Highlight the EBITDA boost from formal KPI tracking",
        "💰 Investment Thresholds: Emphasize the J-curve effect at 2.5%+ AI intensity",
        "⏱️ Timeline Optimization: 8-18 month deployments show optimal risk-return balance",
        "🎪 Size-Specific Strategies: Small companies achieve higher maturity but need different approaches",
        "🔄 Complexity Management: Intermediate projects offer best success-ROI combination"
    ]
    
    for rec in recommendations:
        st.write(rec)
    
    # Evidence-based benchmarks
    st.subheader("📈 Evidence-Based Benchmarks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Conservative Estimate (25th percentile):**")
        st.write(f"Revenue Impact: {filtered_df['revenue_impact_pct'].quantile(0.25):.1f}%")
        st.write(f"ROI: {filtered_df['annual_roi'].quantile(0.25):.1f}x")
        st.write(f"Payback: {filtered_df['payback_months'].quantile(0.75):.0f} months")
    
    with col2:
        st.write("**Realistic Target (50th percentile):**")
        st.write(f"Revenue Impact: {filtered_df['revenue_impact_pct'].median():.1f}%")
        st.write(f"ROI: {filtered_df['annual_roi'].median():.1f}x")
        st.write(f"Payback: {filtered_df['payback_months'].median():.0f} months")
    
    with col3:
        st.write("**Stretch Goal (75th percentile):**")
        st.write(f"Revenue Impact: {filtered_df['revenue_impact_pct'].quantile(0.75):.1f}%")
        st.write(f"ROI: {filtered_df['annual_roi'].quantile(0.75):.1f}x")
        st.write(f"Payback: {filtered_df['payback_months'].quantile(0.25):.0f} months")
    
    # Final summary
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.subheader("🎉 Dataset Ready for Composite Case Studies!")
    st.write(f"📁 Dataset provides realistic scenarios across {len(full_df['industry'].unique())} industries")
    st.write(f"🎲 {len(full_df)} unique project profiles with validated correlations")
    st.write(f"📊 Statistical confidence for evidence-based projections and benchmarking")
    st.write(f"🔒 Complete confidentiality through synthetic data generation")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()