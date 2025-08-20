import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="AI Overviews Impact Study",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2b0573 0%, #4c1d95 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .methodology-box {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #6325f4;
    }
    
    .timeline-phase {
        background: #fff7ed;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #fb923c;
        margin: 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Create sample data structure matching the Excel format"""
    
    # Sample data for demonstration - replace with actual data processing
    dates = pd.date_range(start='2024-04-01', end='2025-08-31', freq='M')
    
    # Non-brand informational CTR data
    nb_info_data = []
    for date in dates:
        # Desktop informational
        nb_info_data.append({
            'Year Month': date,
            'informational': True,
            'desktop ctr': np.random.uniform(0.006, 0.024),
            'mobile ctr': np.random.uniform(0.014, 0.025)
        })
        # Desktop non-informational
        nb_info_data.append({
            'Year Month': date,
            'informational': False,
            'desktop ctr': np.random.uniform(0.011, 0.028),
            'mobile ctr': np.random.uniform(0.022, 0.033)
        })
    
    # Word length data
    word_length_data = []
    for date in dates:
        for word_count in range(1, 11):
            word_length_data.append({
                'Year Month': date,
                'n_bucket': word_count,
                'calculated ctr': np.random.uniform(0.01, 0.05)
            })
    
    # Brand vs non-brand data
    brand_data = []
    for date in dates:
        brand_data.append({
            'date (Date)': date,
            'is_brand': True,
            'calculated ctr': np.random.uniform(0.26, 0.32)
        })
        brand_data.append({
            'date (Date)': date,
            'is_brand': False,
            'calculated ctr': np.random.uniform(0.018, 0.031)
        })
    
    return (
        pd.DataFrame(nb_info_data),
        pd.DataFrame(word_length_data),
        pd.DataFrame(brand_data)
    )

def process_uploaded_data(uploaded_file):
    """Process uploaded Excel file and extract data from all sheets"""
    try:
        # Read all sheets from the Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        
        # Extract specific sheets based on expected names
        nb_info_ctr = excel_data.get('NB Informatiponal CTR', pd.DataFrame())
        word_length = excel_data.get('Word Length Non Brand', pd.DataFrame())
        brand_vs_nonbrand = excel_data.get('CTR - Brand vs Non Brand - All', pd.DataFrame())
        
        # Process date columns
        if not nb_info_ctr.empty:
            nb_info_ctr['Year Month'] = pd.to_datetime(nb_info_ctr['Year Month'])
        if not word_length.empty:
            word_length['Year Month'] = pd.to_datetime(word_length['Year Month'])
        if not brand_vs_nonbrand.empty:
            brand_vs_nonbrand['date (Date)'] = pd.to_datetime(brand_vs_nonbrand['date (Date)'])
        
        return nb_info_ctr, word_length, brand_vs_nonbrand
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None, None, None

def create_timeline_annotations():
    """Create timeline annotations for AI Overviews rollout phases"""
    return [
        dict(x='2024-05-14', xref='x', y=0.95, yref='paper',
             text="AIO Launch", showarrow=True, arrowhead=2,
             bgcolor="#f59e0b", bordercolor="#f59e0b"),
        dict(x='2024-10-13', xref='x', y=0.95, yref='paper',
             text="US Expansion", showarrow=True, arrowhead=2,
             bgcolor="#dc2626", bordercolor="#dc2626"),
        dict(x='2025-03-01', xref='x', y=0.95, yref='paper',
             text="EU Rollout", showarrow=True, arrowhead=2,
             bgcolor="#6325f4", bordercolor="#6325f4")
    ]

def plot_intent_analysis(nb_info_ctr):
    """Create intent analysis charts"""
    if nb_info_ctr.empty:
        return None, None
    
    # Separate informational and non-informational data
    info_desktop = nb_info_ctr[nb_info_ctr['informational'] == True]['desktop ctr'] * 100
    info_mobile = nb_info_ctr[nb_info_ctr['informational'] == True]['mobile ctr'] * 100
    non_info_desktop = nb_info_ctr[nb_info_ctr['informational'] == False]['desktop ctr'] * 100
    non_info_mobile = nb_info_ctr[nb_info_ctr['informational'] == False]['mobile ctr'] * 100
    
    dates = nb_info_ctr[nb_info_ctr['informational'] == True]['Year Month']
    
    # Desktop chart
    fig_desktop = go.Figure()
    fig_desktop.add_trace(go.Scatter(
        x=dates, y=info_desktop,
        mode='lines+markers',
        name='Informational Queries',
        line=dict(color='#6325f4', width=3),
        fill='tonexty'
    ))
    fig_desktop.add_trace(go.Scatter(
        x=dates, y=non_info_desktop,
        mode='lines+markers',
        name='Non-Informational Queries',
        line=dict(color='#10b981', width=3),
        fill='tozeroy'
    ))
    
    fig_desktop.update_layout(
        title="Desktop CTR by Query Intent",
        xaxis_title="Date",
        yaxis_title="CTR (%)",
        height=400,
        annotations=create_timeline_annotations()
    )
    
    # Mobile chart
    fig_mobile = go.Figure()
    fig_mobile.add_trace(go.Scatter(
        x=dates, y=info_mobile,
        mode='lines+markers',
        name='Informational Queries',
        line=dict(color='#6325f4', width=3),
        fill='tonexty'
    ))
    fig_mobile.add_trace(go.Scatter(
        x=dates, y=non_info_mobile,
        mode='lines+markers',
        name='Non-Informational Queries',
        line=dict(color='#10b981', width=3),
        fill='tozeroy'
    ))
    
    fig_mobile.update_layout(
        title="Mobile CTR by Query Intent",
        xaxis_title="Date",
        yaxis_title="CTR (%)",
        height=400,
        annotations=create_timeline_annotations()
    )
    
    return fig_desktop, fig_mobile

def plot_word_length_analysis(word_length_data):
    """Create word length analysis charts"""
    if word_length_data.empty:
        return None, None
    
    # Calculate decline percentages
    word_length_pivot = word_length_data.pivot(index='Year Month', columns='n_bucket', values='calculated ctr')
    
    # Calculate percentage change from first to last month
    first_month = word_length_pivot.iloc[0] * 100
    last_month = word_length_pivot.iloc[-1] * 100
    decline_pct = ((last_month - first_month) / first_month * 100)
    
    # Word length decline chart
    fig_decline = go.Figure(data=[
        go.Bar(
            x=[f"{i} word{'s' if i > 1 else ''}" for i in range(1, 11)],
            y=decline_pct.values[:10],
            marker_color='#64748b'
        )
    ])
    
    fig_decline.update_layout(
        title="CTR Decline by Query Length",
        xaxis_title="Query Length",
        yaxis_title="Decline (%)",
        height=400
    )
    
    # Word length trends chart
    fig_trends = go.Figure()
    
    # Show trends for selected word counts
    selected_lengths = [1, 3, 5, 7]
    colors = ['#2b0573', '#10b981', '#6325f4', '#ef4444']
    
    for i, length in enumerate(selected_lengths):
        if length in word_length_pivot.columns:
            fig_trends.add_trace(go.Scatter(
                x=word_length_pivot.index,
                y=word_length_pivot[length] * 100,
                mode='lines+markers',
                name=f'{length} Word Queries',
                line=dict(color=colors[i], width=3)
            ))
    
    fig_trends.update_layout(
        title="Query Length CTR Trends",
        xaxis_title="Date",
        yaxis_title="CTR (%)",
        height=400,
        annotations=create_timeline_annotations()
    )
    
    return fig_decline, fig_trends

def plot_brand_analysis(brand_data):
    """Create brand vs non-brand analysis charts"""
    if brand_data.empty:
        return None, None, None
    
    # Separate brand and non-brand data
    brand_ctr = brand_data[brand_data['is_brand'] == True]
    non_brand_ctr = brand_data[brand_data['is_brand'] == False]
    
    # Brand vs Non-Brand trends
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=brand_ctr['date (Date)'],
        y=brand_ctr['calculated ctr'] * 100,
        mode='lines+markers',
        name='Brand CTR',
        line=dict(color='#2b0573', width=3),
        fill='tonexty'
    ))
    fig_trends.add_trace(go.Scatter(
        x=non_brand_ctr['date (Date)'],
        y=non_brand_ctr['calculated ctr'] * 100,
        mode='lines+markers',
        name='Non-Brand CTR',
        line=dict(color='#ef4444', width=3),
        fill='tozeroy'
    ))
    
    fig_trends.update_layout(
        title="Brand vs Non-Brand CTR Trends",
        xaxis_title="Date",
        yaxis_title="CTR (%)",
        height=400,
        annotations=create_timeline_annotations()
    )
    
    # CTR Gap Evolution
    gap_ratio = (brand_ctr['calculated ctr'] / non_brand_ctr['calculated ctr']).values
    fig_gap = go.Figure(data=[
        go.Scatter(
            x=brand_ctr['date (Date)'],
            y=gap_ratio,
            mode='lines+markers',
            name='Brand/Non-Brand Ratio',
            line=dict(color='#64748b', width=3),
            fill='tozeroy'
        )
    ])
    
    fig_gap.update_layout(
        title="CTR Gap Evolution",
        xaxis_title="Date",
        yaxis_title="Ratio (x times)",
        height=400
    )
    
    # Performance divergence
    brand_change = ((brand_ctr['calculated ctr'].iloc[-1] - brand_ctr['calculated ctr'].iloc[0]) / brand_ctr['calculated ctr'].iloc[0] * 100)
    non_brand_change = ((non_brand_ctr['calculated ctr'].iloc[-1] - non_brand_ctr['calculated ctr'].iloc[0]) / non_brand_ctr['calculated ctr'].iloc[0] * 100)
    
    fig_divergence = go.Figure(data=[
        go.Bar(
            x=['Brand Performance', 'Non-Brand Performance'],
            y=[brand_change, non_brand_change],
            marker_color=['#2b0573', '#ef4444']
        )
    ])
    
    fig_divergence.update_layout(
        title="Performance Divergence",
        yaxis_title="Change (%)",
        height=400
    )
    
    return fig_trends, fig_gap, fig_divergence

def calculate_metrics(nb_info_ctr, word_length_data, brand_data):
    """Calculate key metrics for the scorecard"""
    metrics = {}
    
    if not nb_info_ctr.empty:
        # Intent analysis metrics
        info_desktop_start = nb_info_ctr[nb_info_ctr['informational'] == True]['desktop ctr'].iloc[0] * 100
        info_desktop_end = nb_info_ctr[nb_info_ctr['informational'] == True]['desktop ctr'].iloc[-1] * 100
        metrics['info_desktop_change'] = ((info_desktop_end - info_desktop_start) / info_desktop_start * 100)
        
        info_mobile_start = nb_info_ctr[nb_info_ctr['informational'] == True]['mobile ctr'].iloc[0] * 100
        info_mobile_end = nb_info_ctr[nb_info_ctr['informational'] == True]['mobile ctr'].iloc[-1] * 100
        metrics['info_mobile_change'] = ((info_mobile_end - info_mobile_start) / info_mobile_start * 100)
        
        non_info_desktop_start = nb_info_ctr[nb_info_ctr['informational'] == False]['desktop ctr'].iloc[0] * 100
        non_info_desktop_end = nb_info_ctr[nb_info_ctr['informational'] == False]['desktop ctr'].iloc[-1] * 100
        metrics['non_info_desktop_change'] = ((non_info_desktop_end - non_info_desktop_start) / non_info_desktop_start * 100)
        
        non_info_mobile_start = nb_info_ctr[nb_info_ctr['informational'] == False]['mobile ctr'].iloc[0] * 100
        non_info_mobile_end = nb_info_ctr[nb_info_ctr['informational'] == False]['mobile ctr'].iloc[-1] * 100
        metrics['non_info_mobile_change'] = ((non_info_mobile_end - non_info_mobile_start) / non_info_mobile_start * 100)
    
    if not brand_data.empty:
        # Brand vs non-brand metrics
        brand_start = brand_data[brand_data['is_brand'] == True]['calculated ctr'].iloc[0] * 100
        brand_end = brand_data[brand_data['is_brand'] == True]['calculated ctr'].iloc[-1] * 100
        metrics['brand_change'] = ((brand_end - brand_start) / brand_start * 100)
        
        non_brand_start = brand_data[brand_data['is_brand'] == False]['calculated ctr'].iloc[0] * 100
        non_brand_end = brand_data[brand_data['is_brand'] == False]['calculated ctr'].iloc[-1] * 100
        metrics['non_brand_change'] = ((non_brand_end - non_brand_start) / non_brand_start * 100)
        
        metrics['current_gap'] = brand_end / non_brand_end
        metrics['gap_expansion'] = metrics['brand_change'] - metrics['non_brand_change']
    
    return metrics

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 1.1rem; font-weight: 600; opacity: 0.9; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 5px;">
            Journey Further
        </div>
        <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 10px;">
            Search Console CTR Analysis
        </h1>
        <p style="font-size: 1.1rem; opacity: 0.9; max-width: 800px; margin: 0 auto;">
            Comprehensive analysis of click-through rate trends across query types, word lengths, and brand classifications during the AI Overviews rollout period
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for file upload and controls
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload Excel file",
            type=['xlsx', 'xls'],
            help="Upload an Excel file with the same format as the original dataset"
        )
        
        st.markdown("---")
        
        # Methodology
        st.markdown("""
        <div class="methodology-box">
            <strong>Expected Data Format:</strong><br>
            • <em>NB Informatiponal CTR</em> sheet: Date, informational flag, desktop/mobile CTR<br>
            • <em>Word Length Non Brand</em> sheet: Date, word count bucket, CTR<br>
            • <em>CTR - Brand vs Non Brand - All</em> sheet: Date, brand flag, CTR
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Use Sample Data"):
            st.session_state.use_sample = True
    
    # Process data
    if uploaded_file is not None:
        nb_info_ctr, word_length_data, brand_data = process_uploaded_data(uploaded_file)
        st.success("✅ Data uploaded successfully!")
    elif st.session_state.get('use_sample', False):
        nb_info_ctr, word_length_data, brand_data = load_sample_data()
        st.info("📊 Using sample data for demonstration")
    else:
        st.warning("⬆️ Please upload a data file or use sample data to view the analysis")
        return
    
    # Calculate metrics
    metrics = calculate_metrics(nb_info_ctr, word_length_data, brand_data)
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Query Intent Analysis", "📏 Query Length Analysis", "🏷️ Brand vs Non-Brand Analysis"])
    
    with tab1:
        st.markdown("### Non-Brand Query Intent Classification Analysis")
        
        # Methodology
        st.markdown("""
        <div class="methodology-box">
            <strong>Analysis Framework:</strong> This analysis focuses exclusively on non-brand queries to examine AI Overviews impact on generic search intent. 
            Queries are classified as "informational" using regex patterns for question words and tutorial/guide indicators.
            <br><br>
            <strong>Key Hypothesis:</strong> If AI Overviews primarily serve informational queries, we should observe significantly greater CTR decline in informational queries compared to non-informational queries.
        </div>
        """, unsafe_allow_html=True)
        
        # Timeline phases
        with st.expander("📅 AI Overviews Rollout Timeline & Impact Correlation"):
            st.markdown("""
            <div class="timeline-phase">
                <strong>Phase 1 (May 14, 2024):</strong> Initial AI Overviews launch in US for signed-in users
                <div style="color: #ea580c; font-size: 0.9rem; margin-top: 5px;">Impact: Moderate decline begins across both query types, desktop shows early sensitivity</div>
            </div>
            <div class="timeline-phase">
                <strong>Phase 2 (October 13, 2024):</strong> Major US expansion to all users + mobile optimization
                <div style="color: #ea580c; font-size: 0.9rem; margin-top: 5px;">Impact: Accelerated decline particularly in desktop informational queries</div>
            </div>
            <div class="timeline-phase">
                <strong>Phase 3 (March 1, 2025):</strong> European rollout begins across EU markets
                <div style="color: #ea580c; font-size: 0.9rem; margin-top: 5px;">Impact: Sharp decline acceleration, mobile queries show delayed but significant impact</div>
            </div>
            <div class="timeline-phase">
                <strong>Phase 4 (June 2025+):</strong> Full global expansion and enhanced features
                <div style="color: #ea580c; font-size: 0.9rem; margin-top: 5px;">Impact: Continued decline stabilization at new lower baseline levels</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Metrics scorecard
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Informational Desktop",
                    f"{metrics.get('info_desktop_change', 0):.1f}%",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Informational Mobile",
                    f"{metrics.get('info_mobile_change', 0):.1f}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "Non-Informational Desktop",
                    f"{metrics.get('non_info_desktop_change', 0):.1f}%",
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Non-Informational Mobile",
                    f"{metrics.get('non_info_mobile_change', 0):.1f}%",
                    delta=None
                )
        
        # Charts
        fig_desktop, fig_mobile = plot_intent_analysis(nb_info_ctr)
        
        if fig_desktop and fig_mobile:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_desktop, use_container_width=True)
            with col2:
                st.plotly_chart(fig_mobile, use_container_width=True)
        
        # Key findings
        st.markdown("""
        ### 🔍 Key Findings
        
        **Cross-Intent Impact:** Both informational and commercial queries show substantial CTR decline, contradicting the hypothesis that AI Overviews primarily affect informational searches.
        
        **Device Differential:** Desktop shows consistently higher impact across both query types, with informational queries experiencing the most severe decline.
        
        **Timeline Correlation:** CTR decline patterns show clear correlation with AI Overviews rollout phases.
        """)
    
    with tab2:
        st.markdown("### Non-Brand Query Length Distribution Analysis")
        
        # Methodology
        st.markdown("""
        <div class="methodology-box">
            <strong>Analysis Framework:</strong> This analysis examines non-brand queries segmented by word count (1-10+ words) to understand how query length correlates with CTR impact.
            <br><br>
            <strong>Key Hypothesis:</strong> If AI Overviews primarily target long-tail informational queries, shorter non-brand queries should show minimal impact while longer queries should show substantial decline.
        </div>
        """, unsafe_allow_html=True)
        
        # Charts
        fig_decline, fig_trends = plot_word_length_analysis(word_length_data)
        
        if fig_decline and fig_trends:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_decline, use_container_width=True)
            with col2:
                st.plotly_chart(fig_trends, use_container_width=True)
        
        # Key findings
        st.markdown("""
        ### 🔍 Key Findings
        
        **Universal Impact:** All non-brand query lengths show CTR decline, indicating impact extends beyond long-tail informational queries.
        
        **Short Query Impact:** Even 1-word non-brand queries show decline, while 2-3 word queries show significant impact.
        
        **Peak Impact Zone:** 6-7 word queries show maximum decline, suggesting this length range is most affected by AI Overviews.
        """)
    
    with tab3:
        st.markdown("### Brand vs Non-Brand Traffic Analysis")
        
        # Methodology
        st.markdown("""
        <div class="methodology-box">
            <strong>Analysis Framework:</strong> Queries are classified as "brand" or "non-brand" using automated detection algorithms. Brand queries include company/product names, while non-brand queries represent generic search intent.
            <br><br>
            <strong>Key Hypothesis:</strong> If AI Overviews improve search quality uniformly, both brand and non-brand queries should show similar patterns.
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics scorecard
        if metrics:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Brand CTR Change",
                    f"{metrics.get('brand_change', 0):.1f}%",
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Non-Brand CTR Change",
                    f"{metrics.get('non_brand_change', 0):.1f}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "Current CTR Gap",
                    f"{metrics.get('current_gap', 0):.1f}x",
                    delta=None
                )
            
            with col4:
                st.metric(
                    "Gap Expansion",
                    f"{metrics.get('gap_expansion', 0):.1f}pp",
                    delta=None
                )
        
        # Charts
        fig_trends, fig_gap, fig_divergence = plot_brand_analysis(brand_data)
        
        if fig_trends and fig_gap and fig_divergence:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_trends, use_container_width=True)
                st.plotly_chart(fig_divergence, use_container_width=True)
            with col2:
                st.plotly_chart(fig_gap, use_container_width=True)
        
        # Key findings
        st.markdown("""
        ### 🔍 Key Findings
        
        **Divergent Trajectories:** Brand CTR increased while non-brand CTR declined significantly, representing substantial performance divergence.
        
        **Expanding Performance Gap:** The brand/non-brand CTR ratio increased dramatically, indicating an accelerating performance differential.
        
        **Phased Divergence Pattern:** Each rollout phase correlates with accelerated non-brand decline while brand CTR maintains stability.
        """)

if __name__ == "__main__":
    main()
