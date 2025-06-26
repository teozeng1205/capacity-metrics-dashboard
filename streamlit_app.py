import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configure Streamlit page
st.set_page_config(
    page_title="Site Capacity Metrics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1f77b4 0%, #ff7f0e 100%);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚀 Site Capacity Metrics Dashboard</h1>', unsafe_allow_html=True)

# Dashboard explanation
st.markdown("""
<div style='background-color: #f0f8ff; padding: 1rem; border-radius: 10px; margin-bottom: 2rem; border-left: 5px solid #1f77b4;'>
    <h3 style='margin-top: 0; color: #1f77b4;'>📊 About This Dashboard</h3>
    <p style='margin-bottom: 0;'>
        This dashboard visualizes <strong>derived site capacity metrics</strong> aggregated by <strong>Provider → Site → Hour</strong>.
        Each data point represents the performance characteristics of a specific site during a particular hour of the day.
        The metrics include transaction throughput (TPH), response delays, and transaction counts to help analyze capacity patterns and performance trends.
    </p>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/site_metrics_final_20250610_to_20250623.csv')
    df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M')
    return df

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.header("🔧 Filters & Controls")

# Data granularity explanation in sidebar
st.sidebar.markdown("""
<div style='background-color: #f0f8ff; padding: 0.5rem; border-radius: 5px; font-size: 0.9rem; margin-bottom: 1rem;'>
<strong>📊 Data Granularity:</strong><br>
Each record = Provider + Site + Hour<br>
<em>Example: AI-F9-14 = Provider AI, Site F9, Hour 14</em>
</div>
""", unsafe_allow_html=True)

# Smart filtering: Site-centric or Provider-centric
st.sidebar.subheader("🎯 Smart Filtering")
filter_mode = st.sidebar.radio(
    "Filter Mode:",
    ["Provider Focus", "Site Focus", "Custom"],
    help="Choose filtering strategy: Provider Focus shows all sites for selected providers, Site Focus shows all providers for selected sites, Custom allows manual selection"
)

if filter_mode == "Provider Focus":
    # Provider filter
    providers = df['providercode'].unique()
    selected_providers = st.sidebar.multiselect(
        "Select Provider(s)", 
        providers, 
        default=[providers[0]] if len(providers) > 0 else [],
        help="Shows ALL sites for the selected provider(s)"
    )
    
    # Auto-select all sites for the selected providers
    if selected_providers:
        selected_sites = df[df['providercode'].isin(selected_providers)]['sitecode'].unique().tolist()
        st.sidebar.info(f"📍 Showing all {len(selected_sites)} sites for selected provider(s)")
    else:
        selected_sites = []

elif filter_mode == "Site Focus":
    # Site filter first
    sites = df['sitecode'].unique()
    selected_sites = st.sidebar.multiselect(
        "Select Site(s)", 
        sites, 
        default=[sites[0]] if len(sites) > 0 else [],
        help="Shows ALL providers for the selected site(s)"
    )
    
    # Auto-select all providers for the selected sites
    if selected_sites:
        selected_providers = df[df['sitecode'].isin(selected_sites)]['providercode'].unique().tolist()
        st.sidebar.info(f"🏢 Showing all {len(selected_providers)} providers for selected site(s)")
    else:
        selected_providers = []

else:  # Custom mode
    # Traditional filtering
    providers = df['providercode'].unique()
    selected_providers = st.sidebar.multiselect(
        "Select Provider(s)", 
        providers, 
        default=providers,
        help="Filter data by provider codes"
    )
    
    sites = df[df['providercode'].isin(selected_providers)]['sitecode'].unique()
    selected_sites = st.sidebar.multiselect(
        "Select Site(s)", 
        sites, 
        default=sites[:10] if len(sites) > 10 else sites,
        help="Filter data by site codes"
    )

# Hour range filter
hour_range = st.sidebar.slider(
    "Select Hour Range",
    min_value=0,
    max_value=23,
    value=(0, 23),
    help="Filter data by hour of day"
)

# Metric selection
metric_options = {
    'TPH Median': 'tph_median',
    'Count Sum': 'ct_sum',
    'Avg Response Delay': 'avg_first_resp_delay_minute'
}
selected_metric = st.sidebar.selectbox(
    "Primary Metric for Analysis",
    list(metric_options.keys()),
    help="Choose the main metric to focus on"
)

# Filter data
filtered_df = df[
    (df['providercode'].isin(selected_providers)) &
    (df['sitecode'].isin(selected_sites)) &
    (df['hour'] >= hour_range[0]) &
    (df['hour'] <= hour_range[1])
]

# Main dashboard
if len(filtered_df) == 0:
    st.error("No data available for the selected filters. Please adjust your selection.")
else:
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📈 Total Sites",
            value=len(filtered_df['sitecode'].unique()),
            delta=f"{len(selected_providers)} providers"
        )
    
    with col2:
        avg_tph = filtered_df['tph_median'].mean()
        st.metric(
            label="⚡ Avg TPH",
            value=f"{avg_tph:,.0f}",
            delta=f"Max: {filtered_df['tph_median'].max():,.0f}"
        )
    
    with col3:
        avg_delay = filtered_df['avg_first_resp_delay_minute'].mean()
        st.metric(
            label="⏱️ Avg Response Delay",
            value=f"{avg_delay:.1f} min",
            delta=f"Min: {filtered_df['avg_first_resp_delay_minute'].min():.1f} min"
        )
    
    with col4:
        total_ct = filtered_df['ct_sum'].sum()
        st.metric(
            label="📊 Total Count",
            value=f"{total_ct:,.0f}",
            delta=f"Avg: {filtered_df['ct_sum'].mean():,.0f}"
        )
    
    with col5:
        data_points = len(filtered_df)
        st.metric(
            label="🔢 Data Points",
            value=f"{data_points:,}",
            delta=f"{len(filtered_df['hour'].unique())} hours"
        )

    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Time Series", "🗺️ Heatmaps", "📊 Comparisons", "🔍 Site Analysis", "🔗 Provider-Site Combinations", "📋 Data Table"])
    
    with tab1:
        st.subheader("Time Series Analysis")
        
        # Explanation for Time Series tab
        st.markdown(f"""
        **📈 Time Series Analysis ({filter_mode})**: These charts show how site capacity metrics change throughout the day.
        
        **Current Mode: {filter_mode}**
        - **Provider Focus**: Left chart shows all sites for selected provider(s), Right chart breaks down individual site performance
        - **Site Focus**: Left chart shows all providers at selected site(s), Right chart shows provider response delay comparison
        - **Custom**: Traditional view with provider aggregation (left) and top sites analysis (right)
        
        **Usage**: Look for peak performance hours, identify patterns, and spot anomalies in capacity utilization based on your selected focus area.
        """)
        st.markdown("---")
        
        # Hourly trend for selected metric
        col1, col2 = st.columns(2)
        
        with col1:
            if filter_mode == "Site Focus":
                # When focusing on sites, show all providers for those sites
                hourly_data = filtered_df.groupby(['hour', 'providercode']).agg({
                    'tph_median': 'mean',
                    'ct_sum': 'sum',
                    'avg_first_resp_delay_minute': 'mean'
                }).reset_index()
                
                fig = px.line(
                    hourly_data, 
                    x='hour', 
                    y=metric_options[selected_metric],
                    color='providercode',
                    title=f"All Providers at Selected Site(s) - {selected_metric}",
                    markers=True
                )
                interpretation = f"""
                **💡 Site Focus Interpretation**: Shows how different providers perform at the selected site(s) throughout the day.
                Each line represents a different provider's performance at your selected site(s). 
                This helps compare provider efficiency and identify which providers perform better at specific sites during different hours.
                """
            elif filter_mode == "Provider Focus":
                # When focusing on providers, show all their sites
                hourly_data = filtered_df.groupby(['hour', 'sitecode']).agg({
                    'tph_median': 'mean',
                    'ct_sum': 'sum',
                    'avg_first_resp_delay_minute': 'mean'
                }).reset_index()
                
                fig = px.line(
                    hourly_data, 
                    x='hour', 
                    y=metric_options[selected_metric],
                    color='sitecode',
                    title=f"All Sites for Selected Provider(s) - {selected_metric}",
                    markers=True
                )
                interpretation = f"""
                **💡 Provider Focus Interpretation**: Shows how all sites perform for the selected provider(s) throughout the day.
                Each line represents a different site operated by your selected provider(s). 
                This helps identify which sites are performing best/worst and understand site-specific capacity patterns.
                """
            else:
                # Custom mode - traditional view
                hourly_data = filtered_df.groupby(['hour', 'providercode']).agg({
                    'tph_median': 'mean',
                    'ct_sum': 'sum',
                    'avg_first_resp_delay_minute': 'mean'
                }).reset_index()
                
                fig = px.line(
                    hourly_data, 
                    x='hour', 
                    y=metric_options[selected_metric],
                    color='providercode',
                    title=f"Hourly {selected_metric} by Provider",
                    markers=True
                )
                interpretation = """
                **💡 Custom Mode Interpretation**: This line chart aggregates all site data by provider and hour. 
                Each point represents the average performance across all sites for that provider during that specific hour.
                Look for patterns like business hours peaks, off-hours performance, and provider comparisons.
                """
            
            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title=selected_metric,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(interpretation)
        
        with col2:
            if filter_mode == "Provider Focus":
                # When focusing on providers, show site breakdown
                site_hourly = filtered_df.groupby(['hour', 'sitecode']).agg({
                    'tph_median': 'mean'
                }).reset_index()
                
                # Show all sites for selected providers, or top 10 if too many
                if len(selected_sites) <= 10:
                    display_sites = selected_sites
                    title = f"All {len(selected_sites)} Sites - TPH Performance"
                else:
                    top_sites = filtered_df.groupby('sitecode')['tph_median'].mean().nlargest(10).index
                    display_sites = top_sites
                    title = "Top 10 Sites - TPH Performance"
                
                display_data = site_hourly[site_hourly['sitecode'].isin(display_sites)]
                
                fig = px.line(
                    display_data,
                    x='hour',
                    y='tph_median',
                    color='sitecode',
                    title=title,
                    markers=True
                )
                interpretation = """
                **💡 Provider Focus**: Shows individual site performance for your selected provider(s).
                Each line represents one site. Compare sites to identify high/low performers and optimal capacity hours.
                """
            elif filter_mode == "Site Focus":
                # When focusing on sites, show provider breakdown with additional metrics
                provider_hourly = filtered_df.groupby(['hour', 'providercode']).agg({
                    'avg_first_resp_delay_minute': 'mean',
                    'ct_sum': 'sum'
                }).reset_index()
                
                fig = px.line(
                    provider_hourly,
                    x='hour',
                    y='avg_first_resp_delay_minute',
                    color='providercode',
                    title="Provider Response Delay at Selected Site(s)",
                    markers=True
                )
                interpretation = """
                **💡 Site Focus**: Shows response delay patterns for different providers at your selected site(s).
                Each line represents one provider. Lower delays indicate better performance. Compare providers to identify efficiency differences.
                """
            else:
                # Custom mode - show top sites
                site_hourly = filtered_df.groupby(['hour', 'sitecode']).agg({
                    'tph_median': 'mean'
                }).reset_index()
                
                top_sites = filtered_df.groupby('sitecode')['tph_median'].mean().nlargest(5).index
                top_site_data = site_hourly[site_hourly['sitecode'].isin(top_sites)]
                
                fig = px.line(
                    top_site_data,
                    x='hour',
                    y='tph_median',
                    color='sitecode',
                    title="Top 5 Sites - TPH Performance Throughout the Day",
                    markers=True
                )
                interpretation = """
                **💡 Custom Mode**: Shows the 5 highest-performing sites based on average TPH.
                Each line represents an individual site's hourly performance pattern.
                This helps identify top sites and understand their capacity utilization throughout the day.
                """
            
            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="TPH Median" if filter_mode != "Site Focus" else "Avg Response Delay (min)",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(interpretation)
    
    with tab2:
        st.subheader("Heatmap Visualizations")
        
        # Explanation for Heatmaps tab
        st.markdown("""
        **🗺️ Heatmap Analysis**: Visual matrices showing performance patterns across providers/sites and time.
        - **Left Chart**: Provider performance by hour - darker colors indicate higher values
        - **Right Chart**: Response delay patterns for top sites - red intensity shows delay levels
        - **Usage**: Quickly identify performance hotspots, peak hours, and problematic time periods across different dimensions
        """)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Provider vs Hour heatmap
            pivot_data = filtered_df.pivot_table(
                values='tph_median',
                index='providercode',
                columns='hour',
                aggfunc='mean'
            )
            
            fig = px.imshow(
                pivot_data,
                title="TPH Median - Provider vs Hour Heatmap",
                color_continuous_scale="RdYlBu_r",
                aspect="auto"
            )
            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Provider Code"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Each cell shows average TPH for a provider during a specific hour.
            Darker blue colors indicate higher transaction throughput. This reveals daily patterns and peak performance times for each provider.
            """)
        
        with col2:
            # Site vs Hour heatmap (top sites only)
            top_sites = filtered_df.groupby('sitecode')['tph_median'].mean().nlargest(10).index
            site_data = filtered_df[filtered_df['sitecode'].isin(top_sites)]
            
            pivot_site = site_data.pivot_table(
                values='avg_first_resp_delay_minute',
                index='sitecode',
                columns='hour',
                aggfunc='mean'
            )
            
            fig = px.imshow(
                pivot_site,
                title="Response Delay - Top 10 Sites vs Hour",
                color_continuous_scale="Reds",
                aspect="auto"
            )
            fig.update_layout(
                xaxis_title="Hour of Day",
                yaxis_title="Site Code"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Response delay heatmap for top 10 sites by TPH performance.
            Red intensity indicates higher delays. This helps identify sites with response time issues during specific hours.
            """)
    
    with tab3:
        st.subheader("Comparative Analysis")
        
        # Explanation for Comparisons tab
        st.markdown("""
        **📊 Comparative Analysis**: Side-by-side comparisons and correlation analysis between different metrics.
        - **Top Row**: Provider performance comparison and scatter plot showing TPH vs Response Delay correlation
        - **Bottom Row**: Distribution analysis showing performance spread and outliers
        - **Usage**: Compare provider performance, identify correlations between metrics, and understand performance distributions
        """)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Provider comparison
            provider_stats = filtered_df.groupby('providercode').agg({
                'tph_median': 'mean',
                'ct_sum': 'sum',
                'avg_first_resp_delay_minute': 'mean'
            }).reset_index()
            
            fig = px.bar(
                provider_stats,
                x='providercode',
                y='tph_median',
                title="Average TPH by Provider",
                color='tph_median',
                color_continuous_scale="viridis"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Compares average TPH performance across providers.
            Higher bars indicate better transaction throughput capacity. Color intensity correlates with performance level.
            """)
        
        with col2:
            # TPH vs Response Delay scatter
            fig = px.scatter(
                filtered_df,
                x='tph_median',
                y='avg_first_resp_delay_minute',
                color='providercode',
                size='ct_sum',
                hover_data=['sitecode', 'hour'],
                title="TPH vs Response Delay (Bubble Size = Count Sum)",
                opacity=0.7
            )
            fig.update_layout(
                xaxis_title="TPH Median",
                yaxis_title="Avg Response Delay (minutes)"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Scatter plot showing correlation between TPH and response delay.
            Each bubble is a site-hour data point. Bubble size represents transaction count. Look for trade-offs between throughput and response time.
            """)
        
        # Performance distribution
        st.subheader("Performance Distribution Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.box(
                filtered_df,
                x='providercode',
                y='tph_median',
                title="TPH Distribution by Provider"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Box plot showing TPH distribution for each provider.
            Box shows quartiles, whiskers show range, dots are outliers. Compare median performance and variability between providers.
            """)
        
        with col2:
            fig = px.violin(
                filtered_df,
                x='providercode',
                y='avg_first_resp_delay_minute',
                title="Response Delay Distribution by Provider"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Violin plot showing response delay distribution density.
            Width indicates frequency of values at that delay level. Wider sections = more common delay times for that provider.
            """)
    
    with tab4:
        st.subheader("Individual Site Analysis")
        
        # Explanation for Site Analysis tab
        st.markdown("""
        **🔍 Individual Site Deep Dive**: Detailed analysis of a single site's performance across all hours.
        - **Site Metrics**: Key performance indicators for the selected site
        - **Left Chart**: TPH performance with average line - shows hourly capacity patterns
        - **Right Chart**: Dual-axis showing response delay and count sum relationship
        - **Usage**: Investigate specific site issues, understand capacity patterns, and identify optimal operating hours
        """)
        st.markdown("---")
        
        # Site selector
        analysis_site = st.selectbox(
            "Select Site for Detailed Analysis",
            selected_sites,
            help="Choose a site to see detailed performance metrics"
        )
        
        site_data = filtered_df[filtered_df['sitecode'] == analysis_site]
        
        if len(site_data) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🎯 Site Code",
                    analysis_site,
                    delta=f"Provider: {site_data['providercode'].iloc[0]}"
                )
            
            with col2:
                st.metric(
                    "📊 Avg TPH",
                    f"{site_data['tph_median'].mean():,.0f}",
                    delta=f"Range: {site_data['tph_median'].min():,.0f}-{site_data['tph_median'].max():,.0f}"
                )
            
            with col3:
                st.metric(
                    "⏱️ Avg Delay",
                    f"{site_data['avg_first_resp_delay_minute'].mean():.1f} min",
                    delta=f"Std: {site_data['avg_first_resp_delay_minute'].std():.1f}"
                )
            
            # Site performance charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(
                    site_data,
                    x='hour',
                    y='tph_median',
                    title=f"TPH Performance - Site {analysis_site}",
                    markers=True
                )
                fig.add_hline(
                    y=site_data['tph_median'].mean(),
                    line_dash="dash",
                    annotation_text="Average"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                **💡 Interpretation**: Hourly TPH performance for this specific site.
                Dashed line shows the site's average. Look for peak hours, consistency, and deviation patterns.
                """)
            
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=site_data['hour'],
                    y=site_data['avg_first_resp_delay_minute'],
                    mode='lines+markers',
                    name='Response Delay',
                    line=dict(color='red')
                ))
                fig.add_trace(go.Scatter(
                    x=site_data['hour'],
                    y=site_data['ct_sum'],
                    mode='lines+markers',
                    name='Count Sum',
                    yaxis='y2',
                    line=dict(color='blue')
                ))
                
                fig.update_layout(
                    title=f"Response Delay & Count Sum - Site {analysis_site}",
                    xaxis_title="Hour",
                    yaxis_title="Response Delay (min)",
                    yaxis2=dict(
                        title="Count Sum",
                        overlaying='y',
                        side='right'
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                **💡 Interpretation**: Dual-axis chart showing response delay (red, left axis) and transaction count (blue, right axis).
                Look for correlations: do high transaction volumes increase response delays? Identify optimal load levels.
                """)
        else:
            st.warning("No data available for the selected site.")
    
    with tab5:
        st.subheader("Provider-Site Combination Analysis")
        
        # Explanation for Provider-Site Combinations tab
        st.markdown("""
        **🔗 Provider-Site Combination TPH Analysis**: Comprehensive view of all unique provider-site combinations and their TPH performance.
        - **Summary Table**: All unique provider-site combinations with aggregated TPH metrics
        - **TPH Distribution**: Visual distribution of TPH values across all combinations
        - **Performance Matrix**: Heatmap showing TPH performance across providers and sites
        - **Top Performers**: Ranking of highest and lowest performing combinations
        - **Usage**: Identify best performing provider-site pairs, compare combinations, and understand capacity distribution patterns
        """)
        st.markdown("---")
        
        # Create provider-site combination data
        combo_data = filtered_df.groupby(['providercode', 'sitecode']).agg({
            'tph_median': ['mean', 'min', 'max', 'std'],
            'ct_sum': ['mean', 'sum'],
            'avg_first_resp_delay_minute': ['mean', 'min', 'max']
        }).round(2)
        
        # Flatten column names
        combo_data.columns = ['_'.join(col).strip() for col in combo_data.columns]
        combo_data = combo_data.reset_index()
        
        # Rename columns for better readability
        combo_data.rename(columns={
            'tph_median_mean': 'TPH_Avg',
            'tph_median_min': 'TPH_Min',
            'tph_median_max': 'TPH_Max',
            'tph_median_std': 'TPH_StdDev',
            'ct_sum_mean': 'Count_Avg',
            'ct_sum_sum': 'Count_Total',
            'avg_first_resp_delay_minute_mean': 'Delay_Avg',
            'avg_first_resp_delay_minute_min': 'Delay_Min',
            'avg_first_resp_delay_minute_max': 'Delay_Max'
        }, inplace=True)
        
        # Add combination identifier
        combo_data['Provider_Site'] = combo_data['providercode'] + '-' + combo_data['sitecode']
        
        # Key metrics for combinations
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🔗 Total Combinations",
                value=len(combo_data),
                delta=f"{len(combo_data['providercode'].unique())} providers"
            )
        
        with col2:
            best_combo = combo_data.loc[combo_data['TPH_Avg'].idxmax()]
            st.metric(
                label="🏆 Best TPH Avg",
                value=f"{best_combo['TPH_Avg']:,.0f}",
                delta=best_combo['Provider_Site']
            )
        
        with col3:
            worst_combo = combo_data.loc[combo_data['TPH_Avg'].idxmin()]
            st.metric(
                label="⚠️ Lowest TPH Avg",
                value=f"{worst_combo['TPH_Avg']:,.0f}",
                delta=worst_combo['Provider_Site']
            )
        
        with col4:
            avg_tph_all = combo_data['TPH_Avg'].mean()
            st.metric(
                label="📊 Overall Avg TPH",
                value=f"{avg_tph_all:,.0f}",
                delta=f"Range: {combo_data['TPH_Avg'].std():.0f}"
            )
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # TPH Distribution histogram
            fig = px.histogram(
                combo_data,
                x='TPH_Avg',
                nbins=20,
                title="TPH Distribution Across Provider-Site Combinations",
                labels={'TPH_Avg': 'Average TPH', 'count': 'Number of Combinations'}
            )
            fig.update_layout(
                xaxis_title="Average TPH",
                yaxis_title="Number of Combinations"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Distribution of average TPH values across all provider-site combinations.
            Shows how many combinations fall into different TPH ranges. Look for clusters and outliers.
            """)
        
        with col2:
            # Top 10 and Bottom 10 combinations
            top_10 = combo_data.nlargest(10, 'TPH_Avg')[['Provider_Site', 'TPH_Avg']]
            bottom_10 = combo_data.nsmallest(10, 'TPH_Avg')[['Provider_Site', 'TPH_Avg']]
            
            fig = go.Figure()
            
            # Top 10
            fig.add_trace(go.Bar(
                x=top_10['TPH_Avg'],
                y=top_10['Provider_Site'],
                orientation='h',
                name='Top 10',
                marker_color='green',
                text=top_10['TPH_Avg'].round(0),
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Top 10 Provider-Site Combinations by Average TPH",
                xaxis_title="Average TPH",
                yaxis_title="Provider-Site Combination",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretation**: Horizontal bar chart showing the top 10 performing provider-site combinations.
            Identify which specific combinations deliver the highest throughput.
            """)
        
        # Performance Matrix Heatmap
        st.subheader("Performance Matrix")
        
        # Create pivot table for heatmap
        pivot_data = combo_data.pivot(index='providercode', columns='sitecode', values='TPH_Avg')
        
        fig = px.imshow(
            pivot_data,
            title="TPH Performance Matrix: Providers vs Sites",
            labels=dict(x="Site Code", y="Provider Code", color="Average TPH"),
            aspect="auto",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **💡 Interpretation**: Heatmap showing TPH performance across all provider-site combinations.
        Darker/brighter colors indicate higher TPH values. Quickly identify high-performing combinations and patterns.
        """)
        
        # Detailed table
        st.subheader("Detailed Provider-Site Combination Table")
        
        # Add sorting options
        sort_options = ['TPH_Avg', 'TPH_Max', 'Count_Total', 'Delay_Avg']
        sort_by = st.selectbox("Sort combinations by:", sort_options)
        sort_ascending = st.checkbox("Sort ascending", value=False)
        
        sorted_combo_data = combo_data.sort_values(sort_by, ascending=sort_ascending)
        
        st.dataframe(
            sorted_combo_data[[
                'Provider_Site', 'providercode', 'sitecode', 
                'TPH_Avg', 'TPH_Min', 'TPH_Max', 'TPH_StdDev',
                'Count_Total', 'Delay_Avg'
            ]],
            use_container_width=True
        )
        
        # Download button for combination data
        combo_csv = sorted_combo_data.to_csv(index=False)
        st.download_button(
            label="📥 Download Provider-Site Combination Data as CSV",
            data=combo_csv,
            file_name=f"provider_site_combinations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with tab6:
        st.subheader("Data Explorer")
        
        # Explanation for Data Table tab
        st.markdown("""
        **📋 Data Explorer**: Raw data access and statistical summaries for the filtered dataset.
        - **Summary Statistics**: Descriptive statistics for all numeric columns
        - **Filtered Data**: Sortable table showing individual provider-site-hour records
        - **Download**: Export filtered data for external analysis
        - **Usage**: Verify specific data points, export for further analysis, and get detailed statistical insights
        """)
        st.markdown("---")
        
        # Summary statistics
        st.write("### Summary Statistics")
        st.dataframe(filtered_df.describe())
        
        # Raw data with search and sort
        st.write("### Filtered Data")
        st.write(f"Showing {len(filtered_df)} records")
        
        # Add sorting options
        sort_col = st.selectbox("Sort by:", filtered_df.columns)
        sort_asc = st.checkbox("Ascending", value=True)
        
        sorted_df = filtered_df.sort_values(sort_col, ascending=sort_asc)
        st.dataframe(sorted_df, use_container_width=True)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"filtered_site_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
last_update_str = df['last_updated'].max()
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🚀 Site Capacity Metrics Dashboard | Built with Streamlit & Plotly</p>
        <p>Data Period: June 10-23, 2025 | Last Updated: {last_update_str}</p>
    </div>
    """,
    unsafe_allow_html=True
) 