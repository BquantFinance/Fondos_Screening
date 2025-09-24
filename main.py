import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import plotly.figure_factory as ff

# Page config with dark theme
st.set_page_config(
    page_title="Analizador Avanzado de Fondos BQuant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar and custom CSS
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
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #fafafa;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 13px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(90deg, #1a1f2e 0%, #252b3b 100%);
        padding: 10px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        color: #fafafa;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #252b3b 0%, #2d3748 100%);
        border-color: #4a5568;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Select boxes and inputs */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background-color: #1a1f2e;
        border-color: #2d3748;
        border-radius: 10px;
    }
    
    /* Newsletter banner */
    .newsletter-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 16px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        animation: glow 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .newsletter-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
        }
    }
    
    @keyframes glow {
        0%, 100% {
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
        }
        50% {
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.6);
        }
    }
    
    .newsletter-banner h3 {
        color: white !important;
        margin: 0 0 10px 0;
        font-size: 1.5em;
        font-weight: 700;
    }
    
    .newsletter-banner p {
        color: rgba(255, 255, 255, 0.95);
        margin: 0 0 20px 0;
        font-size: 1.1em;
    }
    
    .newsletter-button {
        background: white;
        color: #667eea;
        padding: 12px 35px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        transition: all 0.3s;
        margin: 0 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .newsletter-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-decoration: none;
        background: linear-gradient(135deg, #f0f0f0 0%, white 100%);
    }
    
    /* Survivorship bias banner */
    .survivorship-banner {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        padding: 25px;
        border-radius: 16px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .survivorship-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        );
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    .survivorship-button {
        background: white;
        color: #ef4444;
        padding: 12px 35px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .survivorship-button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-decoration: none;
        background: linear-gradient(135deg, #f0f0f0 0%, white 100%);
    }
    
    /* Guide section */
    .guide-section {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        padding: 25px;
        border-radius: 16px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #252b3b 0%, #2d3748 100%);
        padding: 18px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 4px solid;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .metric-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .metric-card:nth-child(3n+1) {
        border-left-color: #667eea;
    }
    
    .metric-card:nth-child(3n+2) {
        border-left-color: #764ba2;
    }
    
    .metric-card:nth-child(3n) {
        border-left-color: #f59e0b;
    }
    
    .metric-title {
        font-weight: 700;
        margin-bottom: 8px;
        font-size: 1.1em;
    }
    
    /* Expandable sections */
    .stExpander {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        border-radius: 12px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
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

def create_beautiful_histogram(data, title, x_label, color='#667eea'):
    """Create beautiful histogram with KDE overlay"""
    # Remove NaN values
    clean_data = data.dropna()
    
    if len(clean_data) == 0:
        return go.Figure()
    
    # Create histogram
    fig = go.Figure()
    
    # Add histogram
    fig.add_trace(go.Histogram(
        x=clean_data,
        nbinsx=50,
        name='Distribución',
        marker=dict(
            color=color,
            line=dict(color='#2d3748', width=0.5)
        ),
        opacity=0.7,
        histnorm='probability density'
    ))
    
    # Calculate KDE
    kde_x = np.linspace(clean_data.min(), clean_data.max(), 200)
    from scipy import stats
    kde = stats.gaussian_kde(clean_data)
    kde_y = kde(kde_x)
    
    # Add KDE line
    fig.add_trace(go.Scatter(
        x=kde_x,
        y=kde_y,
        mode='lines',
        name='Densidad',
        line=dict(color='#fbbf24', width=3),
        fill='tozeroy',
        fillcolor='rgba(251, 191, 36, 0.1)'
    ))
    
    # Calculate statistics
    mean_val = clean_data.mean()
    median_val = clean_data.median()
    
    # Add vertical lines for mean and median
    fig.add_vline(x=mean_val, line_width=2, line_dash="dash", 
                  line_color="#ef4444", annotation_text=f"Media: {mean_val:.2f}")
    fig.add_vline(x=median_val, line_width=2, line_dash="dash", 
                  line_color="#10b981", annotation_text=f"Mediana: {median_val:.2f}")
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title="Densidad",
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1f2e',
        font=dict(color='#fafafa'),
        height=400,
        showlegend=True,
        legend=dict(
            bgcolor='rgba(26, 31, 46, 0.8)',
            bordercolor='#2d3748',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='#2d3748',
            zerolinecolor='#2d3748'
        ),
        yaxis=dict(
            gridcolor='#2d3748',
            zerolinecolor='#2d3748'
        )
    )
    
    return fig

def create_performance_heatmap(df, fund_names):
    """Create a heatmap of returns across different time periods"""
    periods = ['totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m', 
               'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 'totalReturn_10y']
    period_labels = ['1M', '3M', '6M', '1A', '3A', '5A', '10A']
    
    # Create matrix for heatmap
    matrix = []
    fund_labels = []
    
    for fund_name in fund_names[:10]:  # Limit to 10 funds for visibility
        fund_data = df[df['name'] == fund_name].iloc[0]
        returns = [fund_data.get(p, np.nan) for p in periods]
        matrix.append(returns)
        fund_labels.append(fund_name[:30] + '...' if len(fund_name) > 30 else fund_name)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=period_labels,
        y=fund_labels,
        colorscale=[
            [0.0, '#ef4444'],
            [0.25, '#f59e0b'],
            [0.5, '#fbbf24'],
            [0.75, '#84cc16'],
            [1.0, '#10b981']
        ],
        text=[[f"{val:.1f}%" if not pd.isna(val) else "N/D" for val in row] for row in matrix],
        texttemplate="%{text}",
        textfont={"size": 10},
        colorbar=dict(
            title="Retorno (%)",
            titleside="right",
            tickmode="linear",
            tick0=-50,
            dtick=25,
            thickness=15,
            len=0.7
        )
    ))
    
    fig.update_layout(
        title="Mapa de Calor - Retornos por Período",
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1f2e',
        font=dict(color='#fafafa'),
        height=400,
        xaxis=dict(title="Período", side="bottom"),
        yaxis=dict(title="Fondo", autorange="reversed")
    )
    
    return fig

def create_risk_metrics_radar(fund_data, fund_name):
    """Create a comprehensive risk metrics radar chart"""
    metrics = {
        'Volatilidad 1A': fund_data.get('standardDeviation_1yMonthly', 0),
        'Volatilidad 3A': fund_data.get('standardDeviation_3yMonthly', 0),
        'Volatilidad 5A': fund_data.get('standardDeviation_5yMonthly', 0),
        'Beta 1A': abs(fund_data.get('beta_1yMonthly', 0)) * 10,  # Scale for visibility
        'Beta 3A': abs(fund_data.get('beta_3yMonthly', 0)) * 10,
        'Gastos': fund_data.get('ongoingCharge', 0) * 5,  # Scale for visibility
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        name=fund_name[:30] + '...' if len(fund_name) > 30 else fund_name,
        line_color='#667eea'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor='#2d3748',
                range=[0, max(metrics.values()) * 1.2]
            ),
            bgcolor='#1a1f2e'
        ),
        showlegend=True,
        paper_bgcolor='#0e1117',
        font=dict(color='#fafafa'),
        title=f"Perfil de Riesgo - {fund_name[:40]}",
        height=400
    )
    
    return fig

# Main app
def main():
    # Title
    st.markdown("""
        <h1 style='text-align: center; color: #fafafa; padding: 25px 0; margin-bottom: 0; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   border-radius: 16px; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);'>
            📊 Analizador Avanzado de Fondos Españoles
        </h1>
    """, unsafe_allow_html=True)
    
    # Dual banner section
    col1, col2 = st.columns(2)
    
    with col1:
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
    with st.expander("📖 **GUÍA COMPLETA Y MÉTRICAS AVANZADAS** - Click para expandir", expanded=False):
        st.markdown("""
        ### 🎯 **Cómo Usar Esta Herramienta**
        
        Esta aplicación analiza más de **44,000 fondos de inversión españoles** con 96 métricas diferentes. 
        """)
        
        tab1_guide, tab2_guide, tab3_guide = st.tabs(["📊 Métricas Básicas", "📈 Métricas Avanzadas", "🎓 Consejos Pro"])
        
        with tab1_guide:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">📈 Retornos</div>
                    <div>• <b>1A, 3A, 5A, 10A:</b> Rendimiento anualizado<br>
                    • <b>YTD:</b> Retorno año actual<br>
                    • <b>QTD:</b> Retorno trimestre actual</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-title">💰 Costes</div>
                    <div>• <b>Gastos Corrientes:</b> Coste anual total<br>
                    • <b>Comisión Entrada:</b> Al comprar<br>
                    • <b>Comisión Salida:</b> Al vender</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">📊 Riesgo</div>
                    <div>• <b>Volatilidad:</b> Desviación estándar<br>
                    • <b>Beta:</b> Sensibilidad al mercado<br>
                    • <b>R²:</b> Correlación con benchmark</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-title">⭐ Calificaciones</div>
                    <div>• <b>Estrellas:</b> Rating Morningstar (1-5)<br>
                    • <b>ESG:</b> Sostenibilidad (1-5)<br>
                    • <b>Medalist:</b> Rating analistas</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">🎯 Rendimiento Ajustado</div>
                    <div>• <b>Sharpe:</b> Retorno/Riesgo<br>
                    • <b>Alpha:</b> Valor añadido gestor<br>
                    • <b>Info Ratio:</b> Consistencia</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-title">🏢 Características</div>
                    <div>• <b>AUM:</b> Patrimonio gestionado<br>
                    • <b>Antigüedad:</b> Años del fondo<br>
                    • <b>Gestor:</b> Tenure del equipo</div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2_guide:
            st.markdown("""
            ### 🔬 **Métricas Avanzadas Explicadas**
            
            | Métrica | Qué Mide | Interpretación |
            |---------|----------|----------------|
            | **Alpha** | Exceso de retorno vs benchmark | > 0 = Supera al mercado |
            | **Beta** | Sensibilidad al mercado | 1 = Se mueve igual, >1 = Más volátil |
            | **R-Squared** | % explicado por el mercado | >75 = Alta correlación |
            | **Information Ratio** | Consistencia del alpha | > 0.5 = Bueno, > 1 = Excelente |
            | **Sharpe Ratio** | Retorno por unidad de riesgo | > 1 = Bueno, > 2 = Muy bueno |
            | **Percentil Categoría** | Posición vs competidores | < 25 = Top quartil |
            | **Style Box** | Estilo de inversión | Define estrategia del fondo |
            
            ### 📊 **Periodos de Análisis Disponibles**
            - **Corto Plazo:** 1D, 1S, 1M, 2M, 3M, 6M, 9M
            - **Medio Plazo:** 1A, 2A, 3A, 4A, 5A
            - **Largo Plazo:** 6A, 7A, 8A, 9A, 10A, 15A, 20A
            """)
        
        with tab3_guide:
            st.markdown("""
            ### 💡 **Consejos Profesionales**
            
            #### Para Principiantes:
            1. **Empieza con fondos 4-5 estrellas** con más de 5 años de historia
            2. **Gastos < 1.5%** para RV, **< 0.5%** para RF
            3. **AUM > 50M€** para mejor liquidez
            4. **Sharpe > 0.5** indica buen ratio riesgo/retorno
            
            #### Para Inversores Avanzados:
            1. **Analiza el Alpha a 3-5 años** para ver consistencia del gestor
            2. **R² < 70** puede indicar gestión activa genuina
            3. **Information Ratio > 0.5** sugiere habilidad del gestor
            4. **Compara percentiles** dentro de la categoría, no entre categorías
            
            #### Red Flags 🚩:
            - Volatilidad extrema sin retorno acorde
            - Gastos > 2.5% sin justificación clara
            - Alta rotación del equipo gestor
            - AUM en declive constante
            - Alpha negativo persistente
            
            <div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                        padding: 15px; border-radius: 12px; margin-top: 20px;'>
                <strong>⚠️ Sesgo de Supervivencia:</strong> Los fondos cerrados no aparecen aquí. 
                <a href='https://fondossupervivientes.streamlit.app/' target='_blank' 
                   style='color: #fbbf24; font-weight: bold;'>
                    Conoce más sobre este importante sesgo →
                </a>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Advanced Filters Section
    st.markdown("### 🎯 **Filtros Avanzados de Búsqueda**")
    
    # Create filter tabs
    filter_tabs = st.tabs(["🏷️ Básicos", "📊 Rendimiento", "⚡ Riesgo", "💎 Calidad", "🌱 ESG"])
    
    with filter_tabs[0]:  # Basic filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fund_types = df['fund_type'].dropna().unique()
            selected_fund_types = st.multiselect(
                "Tipo de Fondo",
                options=fund_types,
                default=fund_types
            )
        
        with col2:
            categories = df['morningstarCategory'].dropna().unique()
            selected_categories = st.multiselect(
                "Categoría Morningstar",
                options=sorted(categories),
                placeholder="Todas"
            )
        
        with col3:
            domiciles = df['domicile'].dropna().unique()
            selected_domiciles = st.multiselect(
                "Domicilio",
                options=sorted(domiciles),
                placeholder="Todos"
            )
        
        with col4:
            # Index fund filter
            index_filter = st.selectbox(
                "Tipo de Gestión",
                options=["Todos", "Solo Indexados", "Solo Activos"]
            )
    
    with filter_tabs[1]:  # Performance filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            return_period = st.selectbox(
                "Período de Retorno",
                options=['1y', '3y', '5y', '10y'],
                format_func=lambda x: {'1y': '1 Año', '3y': '3 Años', 
                                      '5y': '5 Años', '10y': '10 Años'}[x]
            )
            
            return_col = f'totalReturn_{return_period}'
            if return_col in df.columns:
                min_val = float(df[return_col].min()) if not df[return_col].isna().all() else -50
                max_val = float(df[return_col].max()) if not df[return_col].isna().all() else 100
                
                return_range = st.slider(
                    f"Rango Retorno {return_period.upper()} (%)",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    step=0.5
                )
        
        with col2:
            # YTD filter
            if 'totalReturn_ytd' in df.columns:
                ytd_min = st.number_input(
                    "YTD Mínimo (%)",
                    value=-100.0,
                    step=1.0
                )
        
        with col3:
            # Alpha filter
            alpha_period = st.selectbox(
                "Alpha Período",
                options=['3y', '5y', '10y'],
                format_func=lambda x: f"Alpha {x.upper()}"
            )
            
            alpha_col = f'alpha_{alpha_period}Monthly'
            if alpha_col in df.columns:
                min_alpha = st.number_input(
                    f"Alpha Mínimo ({alpha_period.upper()})",
                    value=-10.0,
                    step=0.5
                )
        
        with col4:
            # Percentile filter
            percentile_col = f'returnRankCategory_{return_period.replace("y", "y")}'
            if percentile_col in df.columns:
                max_percentile = st.slider(
                    "Percentil Máximo (Top %)",
                    min_value=1,
                    max_value=100,
                    value=100,
                    help="1 = Top 1%, 100 = Todos"
                )
    
    with filter_tabs[2]:  # Risk filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Volatility filter
            vol_period = st.selectbox(
                "Volatilidad Período",
                options=['1y', '3y', '5y'],
                format_func=lambda x: f"Volatilidad {x.upper()}"
            )
            
            vol_col = f'standardDeviation_{vol_period}Monthly'
            if vol_col in df.columns:
                max_vol = st.number_input(
                    f"Volatilidad Máx ({vol_period.upper()}) %",
                    value=50.0,
                    min_value=0.0,
                    step=1.0
                )
        
        with col2:
            # Sharpe filter
            sharpe_period = st.selectbox(
                "Sharpe Período",
                options=['1y', '3y', '5y'],
                format_func=lambda x: f"Sharpe {x.upper()}"
            )
            
            sharpe_col = f'sharpeRatio_{sharpe_period}Monthly'
            if sharpe_col in df.columns:
                min_sharpe = st.number_input(
                    f"Sharpe Mínimo ({sharpe_period.upper()})",
                    value=-5.0,
                    step=0.1
                )
        
        with col3:
            # Beta filter
            beta_col = f'beta_{vol_period}Monthly'
            if beta_col in df.columns:
                beta_range = st.slider(
                    f"Rango Beta ({vol_period.upper()})",
                    min_value=-2.0,
                    max_value=3.0,
                    value=(-2.0, 3.0),
                    step=0.1
                )
        
        with col4:
            # Risk rating
            risk_ratings = ['Low', 'Below Average', 'Average', 'Above Average', 'High']
            selected_risk = st.multiselect(
                "Rating Riesgo",
                options=risk_ratings,
                placeholder="Todos"
            )
    
    with filter_tabs[3]:  # Quality filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Fund size
            size_range = st.slider(
                "Tamaño Fondo (M€)",
                min_value=0,
                max_value=10000,
                value=(0, 10000),
                step=50
            )
        
        with col2:
            # Star rating
            min_stars = st.slider(
                "Rating Mínimo ⭐",
                min_value=1,
                max_value=5,
                value=1
            )
        
        with col3:
            # Expense ratio
            max_expense = st.number_input(
                "Gastos Máximos (%)",
                value=5.0,
                min_value=0.0,
                step=0.1
            )
        
        with col4:
            # Data quality
            min_quality = st.slider(
                "Calidad Datos Mín",
                min_value=0,
                max_value=5,
                value=3
            )
    
    with filter_tabs[4]:  # ESG filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Overall ESG
            min_esg = st.slider(
                "Rating ESG Mínimo 🌱",
                min_value=1,
                max_value=5,
                value=1
            )
        
        with col2:
            # Environmental score
            if 'corporateSustainabilityScore_environmental' in df.columns:
                min_env = st.number_input(
                    "Score Ambiental Mín",
                    value=0.0,
                    step=1.0
                )
        
        with col3:
            # Social score
            if 'corporateSustainabilityScore_social' in df.columns:
                min_social = st.number_input(
                    "Score Social Mín",
                    value=0.0,
                    step=1.0
                )
        
        with col4:
            # Governance score
            if 'corporateSustainabilityScore_governance' in df.columns:
                min_gov = st.number_input(
                    "Score Gobernanza Mín",
                    value=0.0,
                    step=1.0
                )
    
    # Apply all filters
    filtered_df = df.copy()
    
    # Basic filters
    if selected_fund_types:
        filtered_df = filtered_df[filtered_df['fund_type'].isin(selected_fund_types)]
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['morningstarCategory'].isin(selected_categories)]
    
    if selected_domiciles:
        filtered_df = filtered_df[filtered_df['domicile'].isin(selected_domiciles)]
    
    if index_filter == "Solo Indexados":
        filtered_df = filtered_df[filtered_df['isIndexFund'] == True]
    elif index_filter == "Solo Activos":
        filtered_df = filtered_df[filtered_df['isIndexFund'] == False]
    
    # Performance filters
    if return_col in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df[return_col] >= return_range[0]) & 
            (filtered_df[return_col] <= return_range[1])
        ]
    
    if 'totalReturn_ytd' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['totalReturn_ytd'] >= ytd_min) | 
            filtered_df['totalReturn_ytd'].isna()
        ]
    
    if alpha_col in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df[alpha_col] >= min_alpha) | 
            filtered_df[alpha_col].isna()
        ]
    
    if percentile_col in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df[percentile_col] <= max_percentile) | 
            filtered_df[percentile_col].isna()
        ]
    
    # Risk filters
    if vol_col in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df[vol_col] <= max_vol) | 
            filtered_df[vol_col].isna()
        ]
    
    if sharpe_col in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df[sharpe_col] >= min_sharpe) | 
            filtered_df[sharpe_col].isna()
        ]
    
    if beta_col in filtered_df.columns:
        filtered_df = filtered_df[
            ((filtered_df[beta_col] >= beta_range[0]) & 
             (filtered_df[beta_col] <= beta_range[1])) | 
            filtered_df[beta_col].isna()
        ]
    
    # Quality filters
    filtered_df = filtered_df[filtered_df['data_quality'] >= min_quality]
    
    if 'fundSize' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['fundSize'] >= size_range[0] * 1e6) & 
            (filtered_df['fundSize'] <= size_range[1] * 1e6)
        ]
    
    if 'fundStarRating_overall' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['fundStarRating_overall'] >= min_stars) | 
            filtered_df['fundStarRating_overall'].isna()
        ]
    
    if 'ongoingCharge' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['ongoingCharge'] <= max_expense) | 
            filtered_df['ongoingCharge'].isna()
        ]
    
    # ESG filters
    if 'sustainabilityRating' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['sustainabilityRating'] >= min_esg) | 
            filtered_df['sustainabilityRating'].isna()
        ]
    
    st.markdown("---")
    
    # Enhanced metrics dashboard
    st.markdown("### 📊 **Dashboard de Métricas**")
    
    metric_cols = st.columns(6)
    
    with metric_cols[0]:
        st.metric(
            "Total Fondos", 
            f"{len(filtered_df):,}",
            delta=f"{len(filtered_df)/len(df)*100:.1f}% del total"
        )
    
    with metric_cols[1]:
        avg_return = filtered_df[return_col].mean() if return_col in filtered_df.columns else 0
        st.metric(
            f"Retorno Medio {return_period.upper()}", 
            f"{avg_return:.2f}%"
        )
    
    with metric_cols[2]:
        avg_sharpe = filtered_df[sharpe_col].mean() if sharpe_col in filtered_df.columns else 0
        st.metric(
            f"Sharpe Medio {sharpe_period.upper()}", 
            f"{avg_sharpe:.2f}"
        )
    
    with metric_cols[3]:
        median_expense = filtered_df['ongoingCharge'].median() if 'ongoingCharge' in filtered_df.columns else 0
        st.metric(
            "Gastos Mediana", 
            f"{median_expense:.2f}%"
        )
    
    with metric_cols[4]:
        total_aum = filtered_df['fundSize'].sum() / 1e9 if 'fundSize' in filtered_df.columns else 0
        st.metric(
            "AUM Total", 
            f"€{total_aum:.1f}B"
        )
    
    with metric_cols[5]:
        avg_stars = filtered_df['fundStarRating_overall'].mean() if 'fundStarRating_overall' in filtered_df.columns else 0
        st.metric(
            "Rating Medio", 
            f"⭐ {avg_stars:.1f}"
        )
    
    st.markdown("---")
    
    # Main tabs
    main_tabs = st.tabs(["📊 **ANÁLISIS**", "🔍 **SCREENING**", "⚖️ **COMPARADOR**", "📈 **VISUALIZACIONES**"])
    
    with main_tabs[0]:  # Analysis
        # Beautiful histograms with KDE
        st.markdown("### 📊 **Distribuciones con Análisis de Densidad**")
        
        hist_col1, hist_col2 = st.columns(2)
        
        with hist_col1:
            if return_col in filtered_df.columns:
                fig = create_beautiful_histogram(
                    filtered_df[return_col],
                    f"Distribución Retorno {return_period.upper()}",
                    f"Retorno {return_period.upper()} (%)",
                    '#667eea'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with hist_col2:
            if sharpe_col in filtered_df.columns:
                fig = create_beautiful_histogram(
                    filtered_df[sharpe_col],
                    f"Distribución Sharpe {sharpe_period.upper()}",
                    f"Ratio Sharpe {sharpe_period.upper()}",
                    '#764ba2'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Risk-Return Scatter
        st.markdown("### 🎯 **Análisis Riesgo-Retorno Interactivo**")
        
        if vol_col in filtered_df.columns and return_col in filtered_df.columns:
            fig = px.scatter(
                filtered_df.dropna(subset=[vol_col, return_col]),
                x=vol_col,
                y=return_col,
                color='fund_type',
                size='fundSize',
                hover_data=['name', 'firmName', 'morningstarCategory', 
                           'fundStarRating_overall', 'ongoingCharge'],
                labels={
                    vol_col: f'Riesgo (Volatilidad {vol_period.upper()}) %',
                    return_col: f'Retorno {return_period.upper()} (%)',
                    'fund_type': 'Tipo de Fondo'
                },
                title=f"Perfil Riesgo-Retorno ({return_period.upper()})",
                color_discrete_map={
                    'Renta Variable': '#3b82f6',
                    'Renta Fija': '#10b981',
                    'Alternativo': '#f59e0b',
                    'Mixto/Otro': '#8b5cf6'
                }
            )
            
            # Add quadrant lines
            x_median = filtered_df[vol_col].median()
            y_median = filtered_df[return_col].median()
            
            fig.add_hline(y=y_median, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=x_median, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add annotations for quadrants
            fig.add_annotation(x=x_median*0.5, y=y_median*2, text="⭐ Ideal", showarrow=False,
                             font=dict(size=14, color="#10b981"))
            fig.add_annotation(x=x_median*1.5, y=y_median*2, text="📈 Alto Riesgo/Retorno", 
                             showarrow=False, font=dict(size=14, color="#f59e0b"))
            fig.add_annotation(x=x_median*0.5, y=y_median*0.5, text="💤 Conservador", 
                             showarrow=False, font=dict(size=14, color="#3b82f6"))
            fig.add_annotation(x=x_median*1.5, y=y_median*0.5, text="❌ Evitar", 
                             showarrow=False, font=dict(size=14, color="#ef4444"))
            
            fig.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1f2e',
                font=dict(color='#fafafa'),
                height=600,
                xaxis=dict(gridcolor='#2d3748', zeroline=False),
                yaxis=dict(gridcolor='#2d3748', zeroline=False)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Category analysis
        st.markdown("### 🏆 **Top Performers por Categoría**")
        
        perf_col1, perf_col2, perf_col3 = st.columns(3)
        
        with perf_col1:
            st.markdown("**📈 Mejor Retorno**")
            if return_col in filtered_df.columns:
                top_returns = filtered_df.nlargest(5, return_col)[['name', return_col, 'fund_type']]
                for _, row in top_returns.iterrows():
                    st.markdown(f"""
                    <div style='background: linear-gradient(90deg, #10b981, #059669); 
                                padding: 8px; border-radius: 8px; margin: 5px 0;'>
                        <b>{row['name'][:35]}...</b><br>
                        {row[return_col]:.2f}% | {row['fund_type']}
                    </div>
                    """, unsafe_allow_html=True)
        
        with perf_col2:
            st.markdown("**📊 Mejor Sharpe**")
            if sharpe_col in filtered_df.columns:
                top_sharpe = filtered_df.nlargest(5, sharpe_col)[['name', sharpe_col, 'fund_type']]
                for _, row in top_sharpe.iterrows():
                    if not pd.isna(row[sharpe_col]):
                        st.markdown(f"""
                        <div style='background: linear-gradient(90deg, #667eea, #764ba2); 
                                    padding: 8px; border-radius: 8px; margin: 5px 0;'>
                            <b>{row['name'][:35]}...</b><br>
                            Sharpe: {row[sharpe_col]:.2f} | {row['fund_type']}
                        </div>
                        """, unsafe_allow_html=True)
        
        with perf_col3:
            st.markdown("**💰 Menores Gastos**")
            if 'ongoingCharge' in filtered_df.columns:
                low_expense = filtered_df.nsmallest(5, 'ongoingCharge')[['name', 'ongoingCharge', 'fund_type']]
                for _, row in low_expense.iterrows():
                    st.markdown(f"""
                    <div style='background: linear-gradient(90deg, #fbbf24, #f59e0b); 
                                padding: 8px; border-radius: 8px; margin: 5px 0;'>
                        <b>{row['name'][:35]}...</b><br>
                        {row['ongoingCharge']:.2f}% | {row['fund_type']}
                    </div>
                    """, unsafe_allow_html=True)
    
    with main_tabs[1]:  # Screening
        st.markdown("### 🔍 **Screening Avanzado**")
        
        # Sorting configuration
        sort_col1, sort_col2, sort_col3, sort_col4 = st.columns(4)
        
        with sort_col1:
            # Dynamic sort options based on selected period
            sort_options = [
                f'totalReturn_{return_period}',
                f'sharpeRatio_{sharpe_period}Monthly',
                f'alpha_{alpha_period}Monthly',
                f'standardDeviation_{vol_period}Monthly',
                'fundSize',
                'ongoingCharge',
                'fundStarRating_overall',
                'totalReturn_ytd'
            ]
            
            # Filter to existing columns
            sort_options = [opt for opt in sort_options if opt in filtered_df.columns]
            
            sort_by = st.selectbox(
                "Ordenar por",
                options=sort_options,
                format_func=lambda x: x.replace('_', ' ').replace('Monthly', '').title()
            )
        
        with sort_col2:
            sort_order = st.radio(
                "Orden",
                options=['Descendente', 'Ascendente'],
                horizontal=True
            )
        
        with sort_col3:
            num_results = st.slider(
                "Número de resultados",
                min_value=10,
                max_value=200,
                value=50,
                step=10
            )
        
        with sort_col4:
            # Export format
            export_format = st.selectbox(
                "Formato exportación",
                options=['CSV', 'Excel']
            )
        
        # Apply sorting
        ascending = sort_order == 'Ascendente'
        sorted_df = filtered_df.sort_values(by=sort_by, ascending=ascending, na_position='last').head(num_results)
        
        # Prepare display columns dynamically
        base_cols = ['name', 'firmName', 'morningstarCategory', 'fund_type']
        
        # Add dynamic columns based on selected periods
        dynamic_cols = [
            f'totalReturn_{return_period}',
            'totalReturn_ytd',
            f'sharpeRatio_{sharpe_period}Monthly',
            f'alpha_{alpha_period}Monthly',
            f'standardDeviation_{vol_period}Monthly',
            f'beta_{vol_period}Monthly',
            'fundSize',
            'ongoingCharge',
            'fundStarRating_overall',
            'sustainabilityRating',
            f'returnRankCategory_{return_period}'
        ]
        
        display_cols = base_cols + [col for col in dynamic_cols if col in sorted_df.columns]
        
        # Create display dataframe
        display_df = sorted_df[display_cols].copy()
        
        # Format columns
        if 'fundSize' in display_df.columns:
            display_df['fundSize'] = display_df['fundSize'].apply(lambda x: format_number(x, 1, '€'))
        
        # Format return columns
        return_cols = [col for col in display_df.columns if 'totalReturn' in col]
        for col in return_cols:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
        
        # Format ratio columns
        ratio_cols = [col for col in display_df.columns if any(x in col for x in ['sharpe', 'alpha', 'beta', 'standard'])]
        for col in ratio_cols:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/D")
        
        # Format other numeric columns
        if 'ongoingCharge' in display_df.columns:
            display_df['ongoingCharge'] = display_df['ongoingCharge'].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
        
        # Display table with custom formatting
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "fundStarRating_overall": st.column_config.NumberColumn("⭐", format="%.0f"),
                "sustainabilityRating": st.column_config.NumberColumn("🌱", format="%.0f"),
                f"returnRankCategory_{return_period}": st.column_config.NumberColumn("Percentil", format="%.0f")
            },
            height=600
        )
        
        # Export functionality
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("📥 **Exportar Datos**", type="primary", use_container_width=True):
                if export_format == "CSV":
                    csv = sorted_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Descargar CSV",
                        data=csv,
                        file_name=f"screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    # Excel export would require xlsxwriter or openpyxl
                    st.info("Excel export requiere librerías adicionales")
    
    with main_tabs[2]:  # Comparator
        st.markdown("### ⚖️ **Comparador Avanzado de Fondos**")
        
        # Fund selection with search
        fund_names = sorted(filtered_df['name'].unique())
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_funds = st.multiselect(
                "Selecciona hasta 10 fondos para comparar",
                options=fund_names,
                max_selections=10,
                help="Puedes seleccionar hasta 10 fondos para una comparación detallada"
            )
        
        with col2:
            comparison_view = st.radio(
                "Vista",
                ["Gráficos", "Tabla", "Ambos"],
                index=2
            )
        
        if selected_funds:
            comparison_df = filtered_df[filtered_df['name'].isin(selected_funds)]
            
            if comparison_view in ["Gráficos", "Ambos"]:
                # Performance heatmap
                st.markdown("#### 🔥 **Mapa de Calor - Retornos**")
                fig = create_performance_heatmap(filtered_df, selected_funds)
                st.plotly_chart(fig, use_container_width=True)
                
                # Risk profiles
                st.markdown("#### 🎯 **Perfiles de Riesgo**")
                
                risk_cols = st.columns(min(3, len(selected_funds)))
                for i, fund_name in enumerate(selected_funds[:3]):
                    with risk_cols[i]:
                        fund_data = comparison_df[comparison_df['name'] == fund_name].iloc[0]
                        fig = create_risk_metrics_radar(fund_data, fund_name)
                        st.plotly_chart(fig, use_container_width=True)
            
            if comparison_view in ["Tabla", "Ambos"]:
                # Comprehensive comparison table
                st.markdown("#### 📊 **Comparación Detallada**")
                
                # Select metrics to compare
                metric_categories = {
                    'Identificación': ['name', 'isin', 'morningstarCategory', 'domicile'],
                    'Retornos': ['totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m',
                                'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 
                                'totalReturn_10y', 'totalReturn_ytd'],
                    'Riesgo': ['standardDeviation_1yMonthly', 'standardDeviation_3yMonthly',
                              'standardDeviation_5yMonthly', 'beta_1yMonthly', 'beta_3yMonthly'],
                    'Ajustado al Riesgo': ['sharpeRatio_1yMonthly', 'sharpeRatio_3yMonthly',
                                          'sharpeRatio_5yMonthly', 'alpha_3yMonthly', 'alpha_5yMonthly'],
                    'Costes': ['ongoingCharge', 'maximumEntryCost', 'maximumExitCost'],
                    'Ratings': ['fundStarRating_overall', 'fundStarRating_3y', 'fundStarRating_5y',
                               'sustainabilityRating', 'morningstarRiskRating_overall'],
                    'ESG': ['corporateSustainabilityScore_total', 'corporateSustainabilityScore_environmental',
                           'corporateSustainabilityScore_social', 'corporateSustainabilityScore_governance'],
                    'Características': ['fundSize', 'fund_age_years', 'averageManagerTenure_fund']
                }
                
                selected_categories = st.multiselect(
                    "Categorías de métricas a comparar",
                    options=list(metric_categories.keys()),
                    default=['Retornos', 'Riesgo', 'Ajustado al Riesgo', 'Costes', 'Ratings']
                )
                
                # Build comparison metrics list
                comparison_metrics = []
                for cat in selected_categories:
                    comparison_metrics.extend(metric_categories[cat])
                
                # Filter to existing columns
                comparison_metrics = [m for m in comparison_metrics if m in comparison_df.columns]
                
                # Create comparison table
                comp_display = comparison_df[comparison_metrics].set_index('name').T
                
                # Format the display
                st.dataframe(
                    comp_display,
                    use_container_width=True,
                    height=600
                )
        else:
            st.info("👆 Selecciona fondos para comenzar la comparación")
    
    with main_tabs[3]:  # Visualizations
        st.markdown("### 📈 **Visualizaciones Avanzadas**")
        
        viz_tabs = st.tabs(["📊 Distribuciones", "🗺️ Mapa de Mercado", "⏰ Series Temporales", "🎨 Correlaciones"])
        
        with viz_tabs[0]:
            # Multiple distributions
            st.markdown("#### Análisis de Distribuciones Múltiples")
            
            dist_col1, dist_col2 = st.columns(2)
            
            with dist_col1:
                if 'ongoingCharge' in filtered_df.columns:
                    fig = create_beautiful_histogram(
                        filtered_df['ongoingCharge'],
                        "Distribución de Gastos Corrientes",
                        "Gastos (%)",
                        '#ef4444'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with dist_col2:
                if vol_col in filtered_df.columns:
                    fig = create_beautiful_histogram(
                        filtered_df[vol_col],
                        f"Distribución de Volatilidad {vol_period.upper()}",
                        "Volatilidad (%)",
                        '#f59e0b'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Alpha distribution if available
            if alpha_col in filtered_df.columns:
                fig = create_beautiful_histogram(
                    filtered_df[alpha_col],
                    f"Distribución de Alpha {alpha_period.upper()}",
                    "Alpha",
                    '#10b981'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with viz_tabs[1]:
            # Market map (treemap)
            st.markdown("#### Mapa del Mercado por Categorías")
            
            if len(filtered_df) > 0:
                # Prepare data for treemap
                treemap_data = filtered_df.groupby(['fund_type', 'morningstarCategory']).agg({
                    'fundSize': 'sum',
                    return_col: 'mean',
                    'name': 'count'
                }).reset_index()
                
                treemap_data = treemap_data[treemap_data['fundSize'] > 0]
                treemap_data['label'] = treemap_data['morningstarCategory'].str[:30]
                
                fig = px.treemap(
                    treemap_data,
                    path=['fund_type', 'label'],
                    values='fundSize',
                    color=return_col,
                    color_continuous_scale='RdYlGn',
                    title=f'Mapa del Mercado - Tamaño por AUM, Color por Retorno {return_period.upper()}',
                    hover_data={'name': True, return_col: ':.2f'}
                )
                
                fig.update_layout(
                    paper_bgcolor='#0e1117',
                    font=dict(color='#fafafa'),
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with viz_tabs[2]:
            # Time series analysis
            st.markdown("#### Análisis de Series Temporales")
            
            # Select funds for time series
            ts_funds = st.multiselect(
                "Selecciona fondos para análisis temporal",
                options=fund_names[:100],  # Limit options for performance
                max_selections=5
            )
            
            if ts_funds:
                # Create time series data
                periods_map = {
                    '1M': 'totalReturn_1m',
                    '3M': 'totalReturn_3m',
                    '6M': 'totalReturn_6m',
                    '1Y': 'totalReturn_1y',
                    '2Y': 'totalReturn_2y',
                    '3Y': 'totalReturn_3y',
                    '5Y': 'totalReturn_5y',
                    '10Y': 'totalReturn_10y'
                }
                
                fig = go.Figure()
                
                for fund_name in ts_funds:
                    fund_data = filtered_df[filtered_df['name'] == fund_name].iloc[0]
                    
                    periods = []
                    returns = []
                    for period, col in periods_map.items():
                        if col in filtered_df.columns and not pd.isna(fund_data.get(col)):
                            periods.append(period)
                            returns.append(fund_data[col])
                    
                    fig.add_trace(go.Scatter(
                        x=periods,
                        y=returns,
                        mode='lines+markers',
                        name=fund_name[:30] + '...' if len(fund_name) > 30 else fund_name,
                        line=dict(width=3),
                        marker=dict(size=10)
                    ))
                
                fig.update_layout(
                    title="Evolución de Retornos por Período",
                    xaxis_title="Período",
                    yaxis_title="Retorno Acumulado (%)",
                    paper_bgcolor='#0e1117',
                    plot_bgcolor='#1a1f2e',
                    font=dict(color='#fafafa'),
                    height=500,
                    hovermode='x unified',
                    xaxis=dict(gridcolor='#2d3748'),
                    yaxis=dict(gridcolor='#2d3748')
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with viz_tabs[3]:
            # Correlation matrix
            st.markdown("#### Matriz de Correlaciones")
            
            # Select metrics for correlation
            corr_metrics = [
                col for col in [return_col, sharpe_col, vol_col, alpha_col, beta_col, 
                               'ongoingCharge', 'fundSize', 'fundStarRating_overall',
                               'sustainabilityRating', 'fund_age_years']
                if col in filtered_df.columns
            ]
            
            if len(corr_metrics) > 2:
                corr_data = filtered_df[corr_metrics].dropna()
                
                if len(corr_data) > 10:
                    corr_matrix = corr_data.corr()
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale='RdBu',
                        zmid=0,
                        text=corr_matrix.round(2).values,
                        texttemplate='%{text}',
                        textfont={"size": 10},
                        colorbar=dict(title="Correlación")
                    ))
                    
                    fig.update_layout(
                        title="Matriz de Correlación entre Métricas",
                        paper_bgcolor='#0e1117',
                        plot_bgcolor='#1a1f2e',
                        font=dict(color='#fafafa'),
                        height=600,
                        xaxis=dict(tickangle=-45)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 30px; 
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    border-radius: 16px; margin-top: 30px;'>
            <h3 style='color: #fafafa; margin-bottom: 20px;'>📚 Recursos y Herramientas Adicionales</h3>
            <div style='display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;'>
                <a href='https://bquantfundlab.substack.com/' target='_blank' class='newsletter-button'>
                    📧 Newsletter Análisis Cuantitativo
                </a>
                <a href='https://fondossupervivientes.streamlit.app/' target='_blank' 
                   class='survivorship-button' style='background-color: #ef4444;'>
                    ⚠️ Análisis Sesgo de Supervivencia
                </a>
            </div>
            <p style='color: #8b949e; margin-top: 25px; font-size: 1.1em;'>
                Creado con ❤️ por <a href='https://twitter.com/Gnschez' target='_blank' 
                                     style='color: #667eea; text-decoration: none; font-weight: 700;'>
                    @Gnschez
                </a>
            </p>
            <p style='color: #6b7280; margin-top: 10px; font-size: 0.9em;'>
                Datos actualizados | 44,341 fondos | 96 métricas | Análisis profesional
            </p>
        </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
    
    main()
