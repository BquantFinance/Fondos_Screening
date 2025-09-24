import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page config with dark theme
st.set_page_config(
    page_title="Analizador de Fondos Españoles",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
st.markdown("""
<style>
    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Dark theme overrides */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Metric cards styling */
    div[data-testid="metric-container"] {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #fafafa;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 14px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1f2e;
        border-radius: 8px;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2d3748;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        color: #fafafa;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #2d3748;
        border-color: #4a5568;
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background-color: #1a1f2e;
        border-color: #2d3748;
    }
    
    /* Alert boxes */
    .stAlert {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
    }
    
    /* Newsletter banner */
    .newsletter-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        50% {
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.6);
        }
        100% {
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
    }
    
    .newsletter-banner h3 {
        color: white !important;
        margin: 0 0 10px 0;
        font-size: 1.4em;
    }
    
    .newsletter-banner p {
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 15px 0;
        font-size: 1.1em;
    }
    
    .newsletter-button {
        background-color: white;
        color: #667eea;
        padding: 10px 30px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        transition: transform 0.3s;
        margin: 0 10px;
    }
    
    .newsletter-button:hover {
        transform: scale(1.05);
        text-decoration: none;
        color: #764ba2;
    }
    
    /* Survivorship bias banner */
    .survivorship-banner {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }
    
    .survivorship-button {
        background-color: white;
        color: #ef4444;
        padding: 10px 30px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        transition: transform 0.3s;
    }
    
    .survivorship-button:hover {
        transform: scale(1.05);
        text-decoration: none;
        color: #dc2626;
    }
    
    /* Guide section */
    .guide-section {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    .metric-card {
        background-color: #252b3b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #667eea;
    }
    
    .metric-title {
        color: #667eea;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    /* Creator credit */
    .creator-credit {
        text-align: center;
        color: #8b949e;
        padding: 10px;
        border-top: 1px solid #2d3748;
        margin-top: 20px;
    }
    
    .creator-credit a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
    }
    
    /* Expandable sections */
    .stExpander {
        background-color: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv('Fondos_España.csv')
    
    # Clean column names (remove brackets)
    df.columns = df.columns.str.replace(r'\[', '_', regex=True).str.replace(r'\]', '', regex=True)
    
    # Convert boolean strings to actual booleans
    bool_cols = ['hasPerformanceFee', 'isIndexFund']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({'True': True, 'False': False, True: True, False: False})
    
    # Convert date column
    if 'inceptionDate' in df.columns:
        df['inceptionDate'] = pd.to_datetime(df['inceptionDate'], errors='coerce')
    
    # Translate fund types to Spanish
    type_translations = {
        'Equity': 'Renta Variable',
        'Fixed Income': 'Renta Fija',
        'Alternative': 'Alternativo',
        'Other/Mixed': 'Mixto/Otro'
    }
    if 'fund_type' in df.columns:
        df['fund_type'] = df['fund_type'].map(type_translations).fillna(df['fund_type'])
    
    return df

# Helper functions
def format_number(value, decimals=2, suffix=''):
    if pd.isna(value):
        return "N/D"
    if abs(value) >= 1e9:
        return f"{value/1e9:.{decimals}f}B{suffix}"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.{decimals}f}M{suffix}"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.{decimals}f}K{suffix}"
    else:
        return f"{value:.{decimals}f}{suffix}"

def create_performance_chart(df, fund_names):
    """Create performance comparison chart"""
    periods = ['totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m', 
               'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y']
    period_labels = ['1M', '3M', '6M', '1A', '3A', '5A']
    
    fig = go.Figure()
    
    for fund_name in fund_names:
        fund_data = df[df['name'] == fund_name].iloc[0]
        returns = [fund_data.get(p, np.nan) for p in periods]
        
        fig.add_trace(go.Bar(
            name=fund_name[:30] + '...' if len(fund_name) > 30 else fund_name,
            x=period_labels,
            y=returns,
            text=[f"{r:.2f}%" if not pd.isna(r) else "N/D" for r in returns],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Retorno: %{y:.2f}%<extra></extra>'
        ))
    
    fig.update_layout(
        title="Comparación de Rendimiento",
        xaxis_title="Período",
        yaxis_title="Retorno (%)",
        barmode='group',
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1f2e',
        font=dict(color='#fafafa'),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_risk_return_scatter(filtered_df):
    """Create risk-return scatter plot"""
    fig = px.scatter(
        filtered_df.dropna(subset=['standardDeviation_3yMonthly', 'totalReturn_3y']),
        x='standardDeviation_3yMonthly',
        y='totalReturn_3y',
        color='fund_type',
        size='fundSize',
        hover_data=['name', 'firmName', 'morningstarCategory'],
        labels={
            'standardDeviation_3yMonthly': 'Riesgo (Desv. Est. 3A)',
            'totalReturn_3y': 'Retorno 3A (%)',
            'fund_type': 'Tipo de Fondo'
        },
        title="Perfil Riesgo-Retorno (3 Años)",
        color_discrete_map={
            'Renta Variable': '#3b82f6',
            'Renta Fija': '#10b981',
            'Alternativo': '#f59e0b',
            'Mixto/Otro': '#8b5cf6'
        }
    )
    
    fig.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1f2e',
        font=dict(color='#fafafa'),
        height=500,
        xaxis=dict(gridcolor='#2d3748', zeroline=False),
        yaxis=dict(gridcolor='#2d3748', zeroline=False)
    )
    
    return fig

# Main app
def main():
    # Title with custom styling
    st.markdown("""
        <h1 style='text-align: center; color: #fafafa; padding: 20px 0; margin-bottom: 0;'>
            📊 Analizador de Fondos Españoles
        </h1>
    """, unsafe_allow_html=True)
    
    # Dual banner section
    col1, col2 = st.columns(2)
    
    with col1:
        # Newsletter banner
        st.markdown("""
            <div class="newsletter-banner">
                <h3>📈 ¡Únete a Nuestra Comunidad!</h3>
                <p>Análisis exclusivos y estrategias cuantitativas</p>
                <a href="https://bquantfundlab.substack.com/" target="_blank" class="newsletter-button">
                    Suscríbete Gratis →
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Survivorship bias banner
        st.markdown("""
            <div class="survivorship-banner">
                <h3>⚠️ Sesgo de Supervivencia</h3>
                <p>Descubre cómo afecta a los fondos españoles</p>
                <a href="https://fondossupervivientes.streamlit.app/" target="_blank" class="survivorship-button">
                    Explorar Análisis →
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Guide section
    with st.expander("📖 **GUÍA DE USO Y MÉTRICAS** - Click para expandir", expanded=False):
        st.markdown("""
        ### 🎯 **Cómo Usar Esta Herramienta**
        
        Esta aplicación analiza más de **44,000 fondos de inversión españoles** con 96 métricas diferentes. 
        Puedes filtrar, analizar y comparar fondos para tomar mejores decisiones de inversión.
        
        ---
        
        ### 📊 **Métricas Principales Explicadas**
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">📈 Retorno (1A, 3A, 5A)</div>
                <div>Rendimiento total del fondo en diferentes períodos. Un retorno del 10% anual significa que 100€ se convierten en 110€.</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📊 Ratio Sharpe</div>
                <div>Mide el retorno ajustado al riesgo. Mayor es mejor. Un Sharpe > 1 es bueno, > 2 es excelente.</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🎯 Alpha</div>
                <div>Retorno extra vs el mercado. Alpha positivo indica que el gestor añade valor.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">📉 Volatilidad (Desv. Est.)</div>
                <div>Mide el riesgo. Mayor volatilidad = mayores fluctuaciones. RV suele tener 15-20%, RF 3-5%.</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">💰 Gastos Corrientes</div>
                <div>Coste anual del fondo. Incluye comisión de gestión. Menor es mejor (típico: 0.5-2%).</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">📊 Beta</div>
                <div>Sensibilidad al mercado. Beta = 1 se mueve igual que el mercado, > 1 más volátil.</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-title">⭐ Rating Estrellas</div>
                <div>Calificación Morningstar (1-5). Basada en rendimiento ajustado al riesgo vs categoría.</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">🌱 Rating ESG</div>
                <div>Sostenibilidad del fondo (1-5). Evalúa criterios ambientales, sociales y de gobernanza.</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">💼 AUM</div>
                <div>Patrimonio bajo gestión. Fondos grandes (>100M€) suelen ser más líquidos y estables.</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        ---
        
        ### 🔍 **Consejos de Uso**
        
        1. **Para principiantes**: Busca fondos con rating ⭐⭐⭐⭐ o más, gastos < 1.5%, y Sharpe > 0.5
        2. **Para comparar**: Usa la pestaña "Comparador" y selecciona hasta 5 fondos similares
        3. **Para screening**: Filtra por tu perfil de riesgo y ordena por la métrica que más te interese
        4. **Importante**: Rendimientos pasados no garantizan resultados futuros
        
        <div style='background-color: #2d3748; padding: 15px; border-radius: 8px; margin-top: 20px;'>
            <strong>⚠️ Nota sobre el Sesgo de Supervivencia:</strong> Esta base de datos solo incluye fondos activos. 
            Los fondos cerrados o fusionados no aparecen, lo que puede hacer que los retornos promedio parezcan mejores. 
            <a href='https://fondossupervivientes.streamlit.app/' target='_blank' style='color: #f59e0b;'>
                Aprende más sobre este sesgo aquí →
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filters Section
    st.markdown("### 🎯 Filtros de Búsqueda")
    
    # Create filter columns
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        # Fund Type Filter
        fund_types = df['fund_type'].dropna().unique()
        selected_fund_types = st.multiselect(
            "Tipo de Fondo",
            options=fund_types,
            default=fund_types
        )
        
        # Data Quality Filter
        min_quality = st.slider(
            "Calidad de Datos Mínima",
            min_value=0,
            max_value=5,
            value=3,
            help="Mayor calidad = datos más completos"
        )
    
    with filter_col2:
        # Category Filter
        categories = df['morningstarCategory'].dropna().unique()
        selected_categories = st.multiselect(
            "Categoría Morningstar",
            options=sorted(categories),
            default=None,
            placeholder="Todas las categorías"
        )
        
        # Star Rating Filter
        min_stars = st.selectbox(
            "Rating Mínimo ⭐",
            options=[1, 2, 3, 4, 5],
            index=0
        )
    
    with filter_col3:
        # Size Filter
        min_size = st.number_input(
            "Tamaño Mín (M€)",
            min_value=0.0,
            value=0.0,
            step=10.0
        )
        
        max_size = st.number_input(
            "Tamaño Máx (M€)",
            min_value=0.0,
            value=10000.0,
            step=100.0
        )
    
    with filter_col4:
        # Performance Filters
        return_1y_min = st.number_input(
            "Retorno 1A Mín (%)",
            value=-50.0,
            step=1.0
        )
        
        return_1y_max = st.number_input(
            "Retorno 1A Máx (%)",
            value=100.0,
            step=1.0
        )
    
    # Additional filters in expandable section
    with st.expander("⚙️ Filtros Avanzados"):
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        
        with adv_col1:
            min_sharpe = st.number_input(
                "Ratio Sharpe Mínimo (3A)",
                value=-5.0,
                step=0.1
            )
        
        with adv_col2:
            min_esg = st.slider(
                "Rating ESG Mínimo 🌱",
                min_value=1,
                max_value=5,
                value=1
            )
        
        with adv_col3:
            max_expense = st.number_input(
                "Gastos Máximos (%)",
                value=5.0,
                min_value=0.0,
                step=0.1
            )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_fund_types:
        filtered_df = filtered_df[filtered_df['fund_type'].isin(selected_fund_types)]
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['morningstarCategory'].isin(selected_categories)]
    
    filtered_df = filtered_df[filtered_df['data_quality'] >= min_quality]
    
    # Size filter (convert to millions)
    if 'fundSize' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['fundSize'] >= min_size * 1e6) & 
            (filtered_df['fundSize'] <= max_size * 1e6)
        ]
    
    # Performance filters
    filtered_df = filtered_df[
        (filtered_df['totalReturn_1y'] >= return_1y_min) & 
        (filtered_df['totalReturn_1y'] <= return_1y_max)
    ]
    
    if 'sharpeRatio_3yMonthly' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['sharpeRatio_3yMonthly'] >= min_sharpe) | 
            (filtered_df['sharpeRatio_3yMonthly'].isna())
        ]
    
    if 'sustainabilityRating' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['sustainabilityRating'] >= min_esg) | 
            (filtered_df['sustainabilityRating'].isna())
        ]
    
    if 'fundStarRating_overall' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['fundStarRating_overall'] >= min_stars) | 
            (filtered_df['fundStarRating_overall'].isna())
        ]
    
    if 'ongoingCharge' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['ongoingCharge'] <= max_expense) | 
            (filtered_df['ongoingCharge'].isna())
        ]
    
    st.markdown("---")
    
    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Fondos", f"{len(filtered_df):,}")
    
    with col2:
        avg_return = filtered_df['totalReturn_1y'].mean()
        st.metric("Retorno Promedio 1A", f"{avg_return:.2f}%")
    
    with col3:
        median_expense = filtered_df['ongoingCharge'].median()
        st.metric("Gastos Mediana", f"{median_expense:.2f}%")
    
    with col4:
        total_aum = filtered_df['fundSize'].sum() / 1e9
        st.metric("AUM Total", f"€{total_aum:.1f}B")
    
    with col5:
        avg_sharpe = filtered_df['sharpeRatio_3yMonthly'].mean()
        st.metric("Sharpe Promedio 3A", f"{avg_sharpe:.2f}")
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 **ANÁLISIS**", "🔍 **SCREENING**", "⚖️ **COMPARADOR**"])
    
    with tab1:
        # Analysis tab
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk-Return Scatter
            if not filtered_df.empty:
                fig = create_risk_return_scatter(filtered_df)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category Distribution
            category_counts = filtered_df['morningstarCategory'].value_counts().head(10)
            fig = px.bar(
                x=category_counts.values,
                y=category_counts.index,
                orientation='h',
                labels={'x': 'Cantidad', 'y': 'Categoría'},
                title='Top 10 Categorías'
            )
            fig.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1f2e',
                font=dict(color='#fafafa'),
                height=400,
                xaxis=dict(gridcolor='#2d3748'),
                yaxis=dict(gridcolor='#2d3748')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance distribution
        st.markdown("### 📈 Distribución de Métricas Clave")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig = px.histogram(
                filtered_df.dropna(subset=['totalReturn_1y']),
                x='totalReturn_1y',
                nbins=30,
                title='Distribución Retorno 1A',
                labels={'totalReturn_1y': 'Retorno 1A (%)'}
            )
            fig.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1f2e',
                font=dict(color='#fafafa'),
                height=300,
                showlegend=False,
                xaxis=dict(gridcolor='#2d3748'),
                yaxis=dict(gridcolor='#2d3748', title='Cantidad')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                filtered_df.dropna(subset=['sharpeRatio_3yMonthly']),
                x='sharpeRatio_3yMonthly',
                nbins=30,
                title='Distribución Ratio Sharpe (3A)',
                labels={'sharpeRatio_3yMonthly': 'Ratio Sharpe'}
            )
            fig.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1f2e',
                font=dict(color='#fafafa'),
                height=300,
                showlegend=False,
                xaxis=dict(gridcolor='#2d3748'),
                yaxis=dict(gridcolor='#2d3748', title='Cantidad')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            fig = px.histogram(
                filtered_df.dropna(subset=['ongoingCharge']),
                x='ongoingCharge',
                nbins=30,
                title='Distribución Gastos Corrientes',
                labels={'ongoingCharge': 'Gastos Corrientes (%)'}
            )
            fig.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1f2e',
                font=dict(color='#fafafa'),
                height=300,
                showlegend=False,
                xaxis=dict(gridcolor='#2d3748'),
                yaxis=dict(gridcolor='#2d3748', title='Cantidad')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top performers by category
        st.markdown("### 🏆 Mejores Fondos por Categoría")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Best returns by type
            best_by_type = filtered_df.groupby('fund_type').apply(
                lambda x: x.nlargest(1, 'totalReturn_1y')[['name', 'totalReturn_1y']]
            ).reset_index(drop=True)
            
            st.markdown("**📈 Mejor Retorno 1A por Tipo**")
            for _, row in best_by_type.iterrows():
                if not pd.isna(row['totalReturn_1y']):
                    st.markdown(f"• {row['name'][:40]}... : **{row['totalReturn_1y']:.2f}%**")
        
        with col2:
            # Best Sharpe by type
            best_sharpe = filtered_df.groupby('fund_type').apply(
                lambda x: x.nlargest(1, 'sharpeRatio_3yMonthly')[['name', 'sharpeRatio_3yMonthly']]
            ).reset_index(drop=True)
            
            st.markdown("**📊 Mejor Sharpe 3A por Tipo**")
            for _, row in best_sharpe.iterrows():
                if not pd.isna(row['sharpeRatio_3yMonthly']):
                    st.markdown(f"• {row['name'][:40]}... : **{row['sharpeRatio_3yMonthly']:.2f}**")
    
    with tab2:
        # Screening tab
        st.markdown("### 🔍 Resultados del Screening")
        
        # Sorting options
        col1, col2, col3 = st.columns(3)
        with col1:
            sort_by = st.selectbox(
                "Ordenar por",
                options=['totalReturn_1y', 'totalReturn_3y', 'sharpeRatio_3yMonthly', 
                        'fundSize', 'ongoingCharge', 'fundStarRating_overall'],
                format_func=lambda x: {
                    'totalReturn_1y': 'Retorno 1A',
                    'totalReturn_3y': 'Retorno 3A',
                    'sharpeRatio_3yMonthly': 'Ratio Sharpe 3A',
                    'fundSize': 'Tamaño del Fondo',
                    'ongoingCharge': 'Gastos Corrientes',
                    'fundStarRating_overall': 'Calificación Estrellas'
                }.get(x, x)
            )
        with col2:
            sort_order = st.radio(
                "Orden",
                options=['Descendente', 'Ascendente'],
                horizontal=True
            )
        with col3:
            num_results = st.number_input(
                "Mostrar top",
                min_value=10,
                max_value=100,
                value=25,
                step=5
            )
        
        # Sort and display
        ascending = sort_order == 'Ascendente'
        sorted_df = filtered_df.sort_values(by=sort_by, ascending=ascending, na_position='last').head(num_results)
        
        # Display columns
        display_cols = ['name', 'firmName', 'morningstarCategory', 'fund_type',
                       'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y',
                       'sharpeRatio_3yMonthly', 'standardDeviation_3yMonthly',
                       'fundSize', 'ongoingCharge', 'fundStarRating_overall',
                       'sustainabilityRating']
        
        # Filter to existing columns
        display_cols = [col for col in display_cols if col in sorted_df.columns]
        
        # Format display dataframe
        display_df = sorted_df[display_cols].copy()
        
        # Format numeric columns
        if 'fundSize' in display_df.columns:
            display_df['fundSize'] = display_df['fundSize'].apply(lambda x: format_number(x, 1, '€'))
        
        for col in ['totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 'ongoingCharge']:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
        
        for col in ['sharpeRatio_3yMonthly', 'standardDeviation_3yMonthly']:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/D")
        
        # Rename columns to Spanish
        column_names = {
            'name': 'Nombre del Fondo',
            'firmName': 'Gestora',
            'morningstarCategory': 'Categoría',
            'fund_type': 'Tipo',
            'totalReturn_1y': 'Retorno 1A',
            'totalReturn_3y': 'Retorno 3A',
            'totalReturn_5y': 'Retorno 5A',
            'sharpeRatio_3yMonthly': 'Sharpe 3A',
            'standardDeviation_3yMonthly': 'Volatilidad 3A',
            'fundSize': 'AUM',
            'ongoingCharge': 'Gastos',
            'fundStarRating_overall': 'Estrellas',
            'sustainabilityRating': 'ESG'
        }
        display_df = display_df.rename(columns=column_names)
        
        # Display table
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Estrellas": st.column_config.NumberColumn("Estrellas", format="⭐ %.0f"),
                "ESG": st.column_config.NumberColumn("ESG", format="🌱 %.0f")
            }
        )
        
        # Export functionality
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📥 Exportar Resultados a CSV", type="primary", use_container_width=True):
                csv = sorted_df.to_csv(index=False)
                st.download_button(
                    label="💾 Descargar CSV",
                    data=csv,
                    file_name=f"fondos_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with tab3:
        # Comparison tab
        st.markdown("### ⚖️ Comparador de Fondos")
        
        # Fund selection
        fund_names = sorted(filtered_df['name'].unique())
        selected_funds = st.multiselect(
            "Selecciona fondos para comparar (máximo 5)",
            options=fund_names,
            max_selections=5,
            help="Elige hasta 5 fondos para una comparación detallada"
        )
        
        if selected_funds:
            comparison_df = filtered_df[filtered_df['name'].isin(selected_funds)]
            
            # Performance comparison chart
            if len(selected_funds) > 0:
                fig = create_performance_chart(filtered_df, selected_funds)
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison table
            st.markdown("### 📊 Tabla Comparativa Detallada")
            
            # Key metrics for comparison
            comparison_metrics = ['name', 'morningstarCategory', 'fundSize', 'ongoingCharge',
                                 'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y',
                                 'sharpeRatio_3yMonthly', 'standardDeviation_3yMonthly',
                                 'alpha_3yMonthly', 'beta_3yMonthly',
                                 'fundStarRating_overall', 'sustainabilityRating',
                                 'maximumEntryCost', 'maximumExitCost']
            
            comparison_metrics = [m for m in comparison_metrics if m in comparison_df.columns]
            
            # Create comparison display
            comp_display = comparison_df[comparison_metrics].set_index('name').T
            
            # Translate index names
            index_translations = {
                'morningstarCategory': 'Categoría',
                'fundSize': 'Tamaño (€)',
                'ongoingCharge': 'Gastos Corrientes (%)',
                'totalReturn_1y': 'Retorno 1 Año (%)',
                'totalReturn_3y': 'Retorno 3 Años (%)',
                'totalReturn_5y': 'Retorno 5 Años (%)',
                'sharpeRatio_3yMonthly': 'Ratio Sharpe 3A',
                'standardDeviation_3yMonthly': 'Volatilidad 3A (%)',
                'alpha_3yMonthly': 'Alpha 3A',
                'beta_3yMonthly': 'Beta 3A',
                'fundStarRating_overall': 'Calificación Estrellas',
                'sustainabilityRating': 'Calificación ESG',
                'maximumEntryCost': 'Comisión Entrada Máx (%)',
                'maximumExitCost': 'Comisión Salida Máx (%)'
            }
            
            comp_display.index = comp_display.index.map(lambda x: index_translations.get(x, x))
            
            # Format values
            for col in comp_display.columns:
                if 'Tamaño' in comp_display.index:
                    comp_display.loc['Tamaño (€)', col] = format_number(comp_display.loc['Tamaño (€)', col], 1, '€')
            
            st.dataframe(comp_display, use_container_width=True)
            
            # Visual comparisons
            st.markdown("### 📈 Análisis Visual Comparativo")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk comparison
                risk_metrics = ['standardDeviation_1yMonthly', 'standardDeviation_3yMonthly', 
                              'standardDeviation_5yMonthly']
                risk_metrics = [m for m in risk_metrics if m in comparison_df.columns]
                
                if risk_metrics:
                    fig = go.Figure()
                    
                    for fund in selected_funds:
                        fund_data = comparison_df[comparison_df['name'] == fund].iloc[0]
                        values = [fund_data[m] if not pd.isna(fund_data[m]) else 0 for m in risk_metrics]
                        
                        fig.add_trace(go.Scatterpolar(
                            r=values,
                            theta=['1 Año', '3 Años', '5 Años'],
                            fill='toself',
                            name=fund[:25] + '...' if len(fund) > 25 else fund
                        ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                gridcolor='#2d3748'
                            ),
                            bgcolor='#1a1f2e'
                        ),
                        showlegend=True,
                        paper_bgcolor='#0e1117',
                        font=dict(color='#fafafa'),
                        title="Perfil de Riesgo (Volatilidad)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Expense and rating comparison
                fig = go.Figure()
                
                # Add expense ratio bars
                expenses = []
                ratings = []
                for fund in selected_funds:
                    fund_data = comparison_df[comparison_df['name'] == fund].iloc[0]
                    expenses.append(fund_data['ongoingCharge'] if not pd.isna(fund_data['ongoingCharge']) else 0)
                    ratings.append(fund_data['fundStarRating_overall'] if not pd.isna(fund_data['fundStarRating_overall']) else 0)
                
                fig.add_trace(go.Bar(
                    name='Gastos (%)',
                    x=[f[:20] + '...' if len(f) > 20 else f for f in selected_funds],
                    y=expenses,
                    yaxis='y',
                    marker_color='#ef4444'
                ))
                
                fig.add_trace(go.Bar(
                    name='Rating ⭐',
                    x=[f[:20] + '...' if len(f) > 20 else f for f in selected_funds],
                    y=ratings,
                    yaxis='y2',
                    marker_color='#fbbf24'
                ))
                
                fig.update_layout(
                    title="Gastos vs Rating",
                    paper_bgcolor='#0e1117',
                    plot_bgcolor='#1a1f2e',
                    font=dict(color='#fafafa'),
                    height=400,
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(
                        title='Gastos (%)',
                        gridcolor='#2d3748',
                        side='left'
                    ),
                    yaxis2=dict(
                        title='Rating Estrellas',
                        overlaying='y',
                        side='right',
                        range=[0, 5.5]
                    ),
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Selecciona fondos de la lista para comenzar la comparación")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 12px; margin-top: 30px;'>
            <h4 style='color: #fafafa; margin-bottom: 15px;'>📚 Recursos Adicionales</h4>
            <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;'>
                <a href='https://bquantfundlab.substack.com/' target='_blank' class='newsletter-button'>
                    📧 Newsletter Gratis
                </a>
                <a href='https://fondossupervivientes.streamlit.app/' target='_blank' class='survivorship-button' style='background-color: #ef4444;'>
                    ⚠️ Sesgo de Supervivencia
                </a>
            </div>
            <p style='color: #8b949e; margin-top: 20px;'>
                Creado con ❤️ por <a href='https://twitter.com/Gnschez' target='_blank' style='color: #667eea; text-decoration: none;'>@Gnschez</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
