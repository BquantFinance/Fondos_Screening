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
    page_title="Screener Pro - Fondos Españoles",
    page_icon="🔍",
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
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px) scale(1.02);
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
        padding: 20px;
        border-radius: 16px;
        margin: 15px 0;
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
    
    .newsletter-button {
        background: white;
        color: #667eea;
        padding: 10px 25px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        transition: all 0.3s;
        margin: 0 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .newsletter-button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-decoration: none;
    }
    
    /* Survivorship banner */
    .survivorship-banner {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        padding: 20px;
        border-radius: 16px;
        margin: 15px 0;
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
        padding: 10px 25px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 700;
        display: inline-block;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .survivorship-button:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        text-decoration: none;
    }
    
    /* Config panel */
    .config-panel {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Column selector */
    .column-selector {
        background-color: #252b3b;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #2d3748;
    }
    
    /* Quick filter buttons */
    .quick-filter {
        background: linear-gradient(135deg, #2d3748 0%, #1a1f2e 100%);
        padding: 8px 16px;
        border-radius: 8px;
        margin: 4px;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s;
        border: 1px solid #4a5568;
    }
    
    .quick-filter:hover {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        transform: translateY(-1px);
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
    
    /* Saved filters */
    .saved-filter-card {
        background: linear-gradient(135deg, #252b3b 0%, #2d3748 100%);
        padding: 12px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
        transition: all 0.3s;
    }
    
    .saved-filter-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
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

# Column definitions with categories and Spanish translations
COLUMN_DEFINITIONS = {
    'Identificación': {
        'name': 'Nombre',
        'isin': 'ISIN',
        'fundID': 'ID Fondo',
        'firmName': 'Gestora',
        'domicile': 'Domicilio',
        'baseCurrency': 'Divisa Base'
    },
    'Clasificación': {
        'fund_type': 'Tipo',
        'morningstarCategory': 'Categoría',
        'investmentType': 'Tipo Inversión',
        'isIndexFund': 'Es Indexado',
        'fundEquityStyleBox': 'Style Box RV',
        'fundFixedIncomeStyleBox': 'Style Box RF',
        'fundAlternativeStyleBox': 'Style Box Alt'
    },
    'Retornos Corto Plazo': {
        'totalReturn_1d': '1 Día %',
        'totalReturn_1w': '1 Semana %',
        'totalReturn_1m': '1 Mes %',
        'totalReturn_3m': '3 Meses %',
        'totalReturn_6m': '6 Meses %',
        'totalReturn_ytd': 'YTD %',
        'totalReturn_qtd': 'QTD %'
    },
    'Retornos Largo Plazo': {
        'totalReturn_1y': '1 Año %',
        'totalReturn_2y': '2 Años %',
        'totalReturn_3y': '3 Años %',
        'totalReturn_5y': '5 Años %',
        'totalReturn_10y': '10 Años %',
        'totalReturn_15y': '15 Años %',
        'totalReturn_20y': '20 Años %'
    },
    'Riesgo': {
        'standardDeviation_1yMonthly': 'Vol 1A %',
        'standardDeviation_3yMonthly': 'Vol 3A %',
        'standardDeviation_5yMonthly': 'Vol 5A %',
        'standardDeviation_10yMonthly': 'Vol 10A %',
        'beta_1yMonthly': 'Beta 1A',
        'beta_3yMonthly': 'Beta 3A',
        'beta_5yMonthly': 'Beta 5A'
    },
    'Riesgo Ajustado': {
        'sharpeRatio_1yMonthly': 'Sharpe 1A',
        'sharpeRatio_3yMonthly': 'Sharpe 3A',
        'sharpeRatio_5yMonthly': 'Sharpe 5A',
        'sharpeRatio_10yMonthly': 'Sharpe 10A',
        'alpha_1yMonthly': 'Alpha 1A',
        'alpha_3yMonthly': 'Alpha 3A',
        'alpha_5yMonthly': 'Alpha 5A',
        'informationRatio_3y': 'Info Ratio 3A',
        'informationRatio_5y': 'Info Ratio 5A'
    },
    'Costes': {
        'ongoingCharge': 'Gastos %',
        'maximumEntryCost': 'Com. Entrada %',
        'maximumExitCost': 'Com. Salida %',
        'maximumManagementFee': 'Com. Gestión %',
        'hasPerformanceFee': 'Com. Éxito'
    },
    'Ratings': {
        'fundStarRating_overall': '⭐ General',
        'fundStarRating_3y': '⭐ 3A',
        'fundStarRating_5y': '⭐ 5A',
        'fundStarRating_10y': '⭐ 10A',
        'morningstarRiskRating_overall': 'Riesgo MS',
        'medalistRating_overall': 'Medalist',
        'data_quality': 'Calidad Datos'
    },
    'ESG': {
        'sustainabilityRating': '🌱 ESG',
        'corporateSustainabilityScore_total': 'ESG Total',
        'corporateSustainabilityScore_environmental': 'ESG Ambiental',
        'corporateSustainabilityScore_social': 'ESG Social',
        'corporateSustainabilityScore_governance': 'ESG Gobernanza'
    },
    'Características': {
        'fundSize': 'AUM €',
        'fund_age_years': 'Antigüedad',
        'averageManagerTenure_fund': 'Tenure Gestor',
        'minimumInitialInvestment': 'Inversión Mín',
        'distributionYield': 'Yield %'
    },
    'Ranking': {
        'returnRankCategory_1y': 'Percentil 1A',
        'returnRankCategory_3y': 'Percentil 3A',
        'returnRankCategory_5y': 'Percentil 5A',
        'returnRankCategory_10y': 'Percentil 10A'
    }
}

# Preset configurations
PRESET_CONFIGS = {
    'Básico': ['name', 'fund_type', 'morningstarCategory', 'totalReturn_1y', 
               'sharpeRatio_3yMonthly', 'ongoingCharge', 'fundStarRating_overall'],
    
    'Performance': ['name', 'totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m',
                   'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 
                   'totalReturn_ytd', 'returnRankCategory_1y'],
    
    'Riesgo': ['name', 'standardDeviation_1yMonthly', 'standardDeviation_3yMonthly',
              'beta_3yMonthly', 'sharpeRatio_3yMonthly', 'alpha_3yMonthly',
              'morningstarRiskRating_overall'],
    
    'ESG': ['name', 'sustainabilityRating', 'corporateSustainabilityScore_total',
           'corporateSustainabilityScore_environmental', 'corporateSustainabilityScore_social',
           'corporateSustainabilityScore_governance'],
    
    'Completo': ['name', 'fund_type', 'morningstarCategory', 'totalReturn_1y', 
                'totalReturn_3y', 'totalReturn_5y', 'sharpeRatio_3yMonthly',
                'standardDeviation_3yMonthly', 'alpha_3yMonthly', 'beta_3yMonthly',
                'ongoingCharge', 'fundSize', 'fundStarRating_overall', 
                'sustainabilityRating', 'returnRankCategory_1y']
}

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
    clean_data = data.dropna()
    
    if len(clean_data) == 0:
        return go.Figure()
    
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
    
    matrix = []
    fund_labels = []
    
    for fund_name in fund_names[:10]:
        fund_data = df[df['name'] == fund_name].iloc[0]
        returns = [fund_data.get(p, np.nan) for p in periods]
        matrix.append(returns)
        fund_labels.append(fund_name[:30] + '...' if len(fund_name) > 30 else fund_name)
    
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

# Main app
def main():
    # Title
    st.markdown("""
        <h1 style='text-align: center; color: #fafafa; padding: 20px 0; margin-bottom: 0; 
                   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   border-radius: 16px; box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);'>
            🔍 Screener Profesional - Fondos Españoles
        </h1>
    """, unsafe_allow_html=True)
    
    # Dual banner section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="newsletter-banner">
                <h3 style='color: white; margin: 0 0 8px 0; font-size: 1.2em;'>📈 Newsletter Gratuita</h3>
                <p style='color: rgba(255,255,255,0.95); margin: 0 0 12px 0; font-size: 0.95em;'>
                    Análisis cuantitativo profesional
                </p>
                <a href="https://bquantfundlab.substack.com/" target="_blank" class="newsletter-button">
                    Suscríbete →
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="survivorship-banner">
                <h3 style='color: white; margin: 0 0 8px 0; font-size: 1.2em;'>⚠️ Sesgo de Supervivencia</h3>
                <p style='color: rgba(255,255,255,0.95); margin: 0 0 12px 0; font-size: 0.95em;'>
                    Análisis de fondos cerrados
                </p>
                <a href="https://fondossupervivientes.streamlit.app/" target="_blank" class="survivorship-button">
                    Explorar →
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Main tabs
    main_tabs = st.tabs(["🔍 **SCREENER**", "📊 **ANÁLISIS**", "⚖️ **COMPARADOR**", "📖 **GUÍA**"])
    
    with main_tabs[0]:  # SCREENER TAB (Main)
        # Configuration section
        with st.expander("⚙️ **CONFIGURACIÓN DEL SCREENER**", expanded=True):
            config_col1, config_col2, config_col3 = st.columns([2, 2, 1])
            
            with config_col1:
                # Preset configurations
                selected_preset = st.selectbox(
                    "📋 Configuración Preestablecida",
                    options=['Personalizado'] + list(PRESET_CONFIGS.keys()),
                    help="Selecciona una configuración predefinida o personaliza tu propia vista"
                )
                
                if selected_preset != 'Personalizado':
                    selected_columns = PRESET_CONFIGS[selected_preset]
                else:
                    # Custom column selector
                    st.markdown("**Selecciona columnas por categoría:**")
                    selected_columns = ['name']  # Always include name
                    
                    col_tabs = st.tabs(list(COLUMN_DEFINITIONS.keys()))
                    for i, (category, columns) in enumerate(COLUMN_DEFINITIONS.items()):
                        with col_tabs[i]:
                            cols = st.multiselect(
                                f"Columnas de {category}",
                                options=list(columns.keys()),
                                format_func=lambda x: columns[x],
                                key=f"cols_{category}"
                            )
                            selected_columns.extend(cols)
            
            with config_col2:
                # View options
                st.markdown("**Opciones de Vista:**")
                
                view_col1, view_col2 = st.columns(2)
                with view_col1:
                    num_results = st.slider(
                        "📊 Número de resultados",
                        min_value=10,
                        max_value=500,
                        value=50,
                        step=10
                    )
                    
                    highlight_top = st.checkbox(
                        "✨ Resaltar top performers",
                        value=True
                    )
                
                with view_col2:
                    compact_view = st.checkbox(
                        "📐 Vista compacta",
                        value=False
                    )
                    
                    show_percentiles = st.checkbox(
                        "📈 Mostrar percentiles",
                        value=True
                    )
            
            with config_col3:
                # Save configuration
                st.markdown("**Guardar Config:**")
                
                config_name = st.text_input(
                    "Nombre",
                    placeholder="Mi config"
                )
                
                if st.button("💾 Guardar", type="primary"):
                    st.success("✅ Configuración guardada")
        
        st.markdown("---")
        
        # Quick filters
        st.markdown("### 🎯 **Filtros Rápidos**")
        
        quick_filters = st.columns(6)
        
        with quick_filters[0]:
            quick_fund_type = st.selectbox(
                "Tipo",
                options=['Todos'] + list(df['fund_type'].dropna().unique()),
                key="quick_type"
            )
        
        with quick_filters[1]:
            quick_stars = st.selectbox(
                "⭐ Mínimo",
                options=[0, 3, 4, 5],
                key="quick_stars"
            )
        
        with quick_filters[2]:
            quick_return = st.selectbox(
                "Retorno 1A",
                options=['Todos', '> 0%', '> 10%', '> 20%'],
                key="quick_return"
            )
        
        with quick_filters[3]:
            quick_expense = st.selectbox(
                "Gastos Máx",
                options=['Todos', '< 2%', '< 1.5%', '< 1%', '< 0.5%'],
                key="quick_expense"
            )
        
        with quick_filters[4]:
            quick_size = st.selectbox(
                "AUM Mín",
                options=['Todos', '> 10M€', '> 50M€', '> 100M€', '> 500M€'],
                key="quick_size"
            )
        
        with quick_filters[5]:
            quick_esg = st.selectbox(
                "🌱 ESG Mín",
                options=[0, 3, 4, 5],
                key="quick_esg"
            )
        
        # Advanced filters
        with st.expander("🔬 **Filtros Avanzados**"):
            adv_tabs = st.tabs(["📊 Performance", "⚡ Riesgo", "💰 Costes", "🏆 Ratings", "📈 Percentiles"])
            
            with adv_tabs[0]:
                perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
                
                with perf_col1:
                    adv_return_1y = st.slider(
                        "Retorno 1A (%)",
                        min_value=-50.0,
                        max_value=100.0,
                        value=(-50.0, 100.0),
                        key="adv_ret_1y"
                    )
                
                with perf_col2:
                    adv_return_3y = st.slider(
                        "Retorno 3A (%)",
                        min_value=-30.0,
                        max_value=50.0,
                        value=(-30.0, 50.0),
                        key="adv_ret_3y"
                    )
                
                with perf_col3:
                    adv_ytd = st.number_input(
                        "YTD Mínimo (%)",
                        value=-100.0,
                        key="adv_ytd"
                    )
                
                with perf_col4:
                    adv_alpha = st.number_input(
                        "Alpha 3A Mínimo",
                        value=-10.0,
                        key="adv_alpha"
                    )
            
            with adv_tabs[1]:
                risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)
                
                with risk_col1:
                    adv_vol = st.slider(
                        "Volatilidad 3A Máx (%)",
                        min_value=0.0,
                        max_value=50.0,
                        value=50.0,
                        key="adv_vol"
                    )
                
                with risk_col2:
                    adv_sharpe = st.number_input(
                        "Sharpe 3A Mínimo",
                        value=-5.0,
                        key="adv_sharpe"
                    )
                
                with risk_col3:
                    adv_beta = st.slider(
                        "Beta 3A",
                        min_value=-2.0,
                        max_value=3.0,
                        value=(-2.0, 3.0),
                        key="adv_beta"
                    )
                
                with risk_col4:
                    adv_risk_rating = st.multiselect(
                        "Rating Riesgo",
                        options=['Low', 'Below Average', 'Average', 'Above Average', 'High'],
                        key="adv_risk"
                    )
        
        # Apply all filters
        filtered_df = df.copy()
        
        # Quick filters
        if quick_fund_type != 'Todos':
            filtered_df = filtered_df[filtered_df['fund_type'] == quick_fund_type]
        
        if quick_stars > 0:
            filtered_df = filtered_df[
                (filtered_df['fundStarRating_overall'] >= quick_stars) |
                filtered_df['fundStarRating_overall'].isna()
            ]
        
        if quick_return == '> 0%':
            filtered_df = filtered_df[(filtered_df['totalReturn_1y'] > 0) | filtered_df['totalReturn_1y'].isna()]
        elif quick_return == '> 10%':
            filtered_df = filtered_df[(filtered_df['totalReturn_1y'] > 10) | filtered_df['totalReturn_1y'].isna()]
        elif quick_return == '> 20%':
            filtered_df = filtered_df[(filtered_df['totalReturn_1y'] > 20) | filtered_df['totalReturn_1y'].isna()]
        
        if quick_expense == '< 2%':
            filtered_df = filtered_df[(filtered_df['ongoingCharge'] < 2) | filtered_df['ongoingCharge'].isna()]
        elif quick_expense == '< 1.5%':
            filtered_df = filtered_df[(filtered_df['ongoingCharge'] < 1.5) | filtered_df['ongoingCharge'].isna()]
        elif quick_expense == '< 1%':
            filtered_df = filtered_df[(filtered_df['ongoingCharge'] < 1) | filtered_df['ongoingCharge'].isna()]
        elif quick_expense == '< 0.5%':
            filtered_df = filtered_df[(filtered_df['ongoingCharge'] < 0.5) | filtered_df['ongoingCharge'].isna()]
        
        if quick_size == '> 10M€':
            filtered_df = filtered_df[(filtered_df['fundSize'] > 10e6) | filtered_df['fundSize'].isna()]
        elif quick_size == '> 50M€':
            filtered_df = filtered_df[(filtered_df['fundSize'] > 50e6) | filtered_df['fundSize'].isna()]
        elif quick_size == '> 100M€':
            filtered_df = filtered_df[(filtered_df['fundSize'] > 100e6) | filtered_df['fundSize'].isna()]
        elif quick_size == '> 500M€':
            filtered_df = filtered_df[(filtered_df['fundSize'] > 500e6) | filtered_df['fundSize'].isna()]
        
        if quick_esg > 0:
            filtered_df = filtered_df[
                (filtered_df['sustainabilityRating'] >= quick_esg) |
                filtered_df['sustainabilityRating'].isna()
            ]
        
        st.markdown("---")
        
        # Sort configuration
        st.markdown("### 📊 **Resultados del Screening**")
        
        sort_col1, sort_col2, sort_col3, sort_col4, sort_col5 = st.columns([2, 2, 1, 1, 1])
        
        with sort_col1:
            # Dynamic sort options based on selected columns
            available_sort_cols = [col for col in selected_columns if col in filtered_df.columns]
            
            sort_by = st.selectbox(
                "🔽 Ordenar por",
                options=available_sort_cols,
                index=available_sort_cols.index('totalReturn_1y') if 'totalReturn_1y' in available_sort_cols else 0
            )
        
        with sort_col2:
            secondary_sort = st.selectbox(
                "🔽 Orden secundario",
                options=['Ninguno'] + available_sort_cols,
                key="secondary_sort"
            )
        
        with sort_col3:
            sort_order = st.radio(
                "Orden",
                options=['↓ Desc', '↑ Asc'],
                key="sort_order"
            )
        
        with sort_col4:
            st.metric(
                "Fondos filtrados",
                f"{len(filtered_df):,}",
                delta=f"{len(filtered_df)/len(df)*100:.1f}%"
            )
        
        with sort_col5:
            export_format = st.selectbox(
                "📥 Exportar",
                options=['CSV', 'Excel'],
                key="export_format"
            )
        
        # Apply sorting
        ascending = sort_order == '↑ Asc'
        if secondary_sort != 'Ninguno' and secondary_sort in filtered_df.columns:
            sorted_df = filtered_df.sort_values(
                by=[sort_by, secondary_sort],
                ascending=[ascending, ascending],
                na_position='last'
            ).head(num_results)
        else:
            sorted_df = filtered_df.sort_values(
                by=sort_by,
                ascending=ascending,
                na_position='last'
            ).head(num_results)
        
        # Prepare display dataframe
        display_cols = [col for col in selected_columns if col in sorted_df.columns]
        display_df = sorted_df[display_cols].copy()
        
        # Format columns based on type
        for col in display_df.columns:
            if 'fundSize' in col:
                display_df[col] = display_df[col].apply(lambda x: format_number(x, 1, '€'))
            elif 'Return' in col or 'return' in col or 'ongoing' in col.lower() or 'maximum' in col.lower():
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
            elif 'sharpe' in col.lower() or 'alpha' in col.lower() or 'beta' in col.lower() or 'standard' in col.lower():
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/D")
            elif col == 'isIndexFund' or col == 'hasPerformanceFee':
                display_df[col] = display_df[col].apply(lambda x: '✓' if x else '✗' if not pd.isna(x) else "N/D")
        
        # Apply column name translations
        column_translations = {}
        for category, cols in COLUMN_DEFINITIONS.items():
            column_translations.update(cols)
        
        display_df = display_df.rename(columns=column_translations)
        
        # Display with conditional formatting
        if highlight_top and not display_df.empty:
            # Highlight top 10% of numerical columns
            def highlight_top_values(val, props=''):
                return np.where(val > val.quantile(0.9), props, '')
            
            # Apply to relevant columns
            numeric_cols = display_df.select_dtypes(include=[np.number]).columns
            styled_df = display_df.style.apply(
                lambda x: highlight_top_values(x, 'background-color: rgba(102, 126, 234, 0.2)'),
                subset=numeric_cols,
                axis=0
            )
        else:
            styled_df = display_df
        
        # Display the screener results
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=600 if not compact_view else 400,
            column_config={
                "⭐ General": st.column_config.NumberColumn(format="%.0f ⭐"),
                "⭐ 3A": st.column_config.NumberColumn(format="%.0f ⭐"),
                "⭐ 5A": st.column_config.NumberColumn(format="%.0f ⭐"),
                "🌱 ESG": st.column_config.NumberColumn(format="%.0f 🌱"),
                "Es Indexado": st.column_config.TextColumn(),
                "Com. Éxito": st.column_config.TextColumn()
            }
        )
        
        # Export button
        if st.button(f"📥 Exportar {len(sorted_df)} resultados como {export_format}", type="primary"):
            if export_format == "CSV":
                csv = sorted_df.to_csv(index=False)
                st.download_button(
                    label=f"💾 Descargar CSV ({len(sorted_df)} fondos)",
                    data=csv,
                    file_name=f"screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Summary statistics
        if show_percentiles and len(sorted_df) > 0:
            st.markdown("---")
            st.markdown("### 📈 **Estadísticas del Screening**")
            
            stats_cols = st.columns(4)
            
            with stats_cols[0]:
                if 'totalReturn_1y' in sorted_df.columns:
                    clean_returns = sorted_df['totalReturn_1y'].dropna()
                    if len(clean_returns) > 0:
                        p25 = clean_returns.quantile(0.25)
                        p50 = clean_returns.quantile(0.50)
                        p75 = clean_returns.quantile(0.75)
                        
                        st.markdown(f"""
                        **Retorno 1A (Percentiles)**
                        - P25: {p25:.2f}%
                        - P50: {p50:.2f}%
                        - P75: {p75:.2f}%
                        """)
            
            with stats_cols[1]:
                if 'sharpeRatio_3yMonthly' in sorted_df.columns:
                    clean_sharpe = sorted_df['sharpeRatio_3yMonthly'].dropna()
                    if len(clean_sharpe) > 0:
                        p25 = clean_sharpe.quantile(0.25)
                        p50 = clean_sharpe.quantile(0.50)
                        p75 = clean_sharpe.quantile(0.75)
                        
                        st.markdown(f"""
                        **Sharpe 3A (Percentiles)**
                        - P25: {p25:.2f}
                        - P50: {p50:.2f}
                        - P75: {p75:.2f}
                        """)
            
            with stats_cols[2]:
                if 'ongoingCharge' in sorted_df.columns:
                    clean_charges = sorted_df['ongoingCharge'].dropna()
                    if len(clean_charges) > 0:
                        p25 = clean_charges.quantile(0.25)
                        p50 = clean_charges.quantile(0.50)
                        p75 = clean_charges.quantile(0.75)
                        
                        st.markdown(f"""
                        **Gastos (Percentiles)**
                        - P25: {p25:.2f}%
                        - P50: {p50:.2f}%
                        - P75: {p75:.2f}%
                        """)
            
            with stats_cols[3]:
                if 'fundSize' in sorted_df.columns:
                    clean_sizes = sorted_df['fundSize'].dropna()
                    if len(clean_sizes) > 0:
                        total_aum = clean_sizes.sum() / 1e9
                        avg_aum = clean_sizes.mean() / 1e6
                        
                        st.markdown(f"""
                        **AUM Agregado**
                        - Total: €{total_aum:.1f}B
                        - Promedio: €{avg_aum:.1f}M
                        """)
    
    with main_tabs[1]:  # ANALYSIS TAB
        st.markdown("### 📊 **Análisis de Distribuciones**")
        
        # Risk-return scatter
        if 'standardDeviation_3yMonthly' in filtered_df.columns and 'totalReturn_3y' in filtered_df.columns:
            # Prepare data for scatter plot
            scatter_data = filtered_df.dropna(subset=['standardDeviation_3yMonthly', 'totalReturn_3y']).copy()
            
            # Handle NaN values in fundSize - replace with a default value
            if 'fundSize' in scatter_data.columns:
                scatter_data['fundSize'] = scatter_data['fundSize'].fillna(1e6)  # Default 1M for missing values
                size_col = 'fundSize'
            else:
                size_col = None
            
            fig = px.scatter(
                scatter_data,
                x='standardDeviation_3yMonthly',
                y='totalReturn_3y',
                color='fund_type',
                size=size_col if size_col else None,
                hover_data=['name', 'firmName', 'morningstarCategory'],
                labels={
                    'standardDeviation_3yMonthly': 'Riesgo (Volatilidad 3A) %',
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
            
            # Add quadrant lines
            x_median = scatter_data['standardDeviation_3yMonthly'].median()
            y_median = scatter_data['totalReturn_3y'].median()
            
            fig.add_hline(y=y_median, line_dash="dash", line_color="gray", opacity=0.5)
            fig.add_vline(x=x_median, line_dash="dash", line_color="gray", opacity=0.5)
            
            fig.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#1a1f2e',
                font=dict(color='#fafafa'),
                height=600,
                xaxis=dict(gridcolor='#2d3748', zeroline=False),
                yaxis=dict(gridcolor='#2d3748', zeroline=False)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Distribution plots
        dist_col1, dist_col2 = st.columns(2)
        
        with dist_col1:
            if 'totalReturn_1y' in filtered_df.columns:
                fig = create_beautiful_histogram(
                    filtered_df['totalReturn_1y'],
                    "Distribución Retorno 1 Año",
                    "Retorno 1A (%)",
                    '#667eea'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with dist_col2:
            if 'sharpeRatio_3yMonthly' in filtered_df.columns:
                fig = create_beautiful_histogram(
                    filtered_df['sharpeRatio_3yMonthly'],
                    "Distribución Ratio Sharpe 3A",
                    "Sharpe 3A",
                    '#764ba2'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with main_tabs[2]:  # COMPARATOR TAB
        st.markdown("### ⚖️ **Comparador de Fondos**")
        
        fund_names = sorted(filtered_df['name'].unique())
        selected_funds = st.multiselect(
            "Selecciona hasta 10 fondos para comparar",
            options=fund_names,
            max_selections=10
        )
        
        if selected_funds:
            comparison_df = filtered_df[filtered_df['name'].isin(selected_funds)]
            
            # Heatmap
            fig = create_performance_heatmap(filtered_df, selected_funds)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison
            st.markdown("### 📊 **Métricas Comparadas**")
            
            # Select metric categories to compare
            selected_categories = st.multiselect(
                "Selecciona categorías de métricas",
                options=list(COLUMN_DEFINITIONS.keys()),
                default=['Retornos Largo Plazo', 'Riesgo', 'Riesgo Ajustado', 'Costes', 'Ratings']
            )
            
            # Build comparison metrics
            comparison_metrics = ['name']
            for cat in selected_categories:
                comparison_metrics.extend([col for col in COLUMN_DEFINITIONS[cat].keys() 
                                         if col in comparison_df.columns])
            
            # Display comparison
            comp_display = comparison_df[comparison_metrics].set_index('name').T
            
            # Apply translations
            index_translations = {}
            for category, cols in COLUMN_DEFINITIONS.items():
                index_translations.update(cols)
            
            comp_display.index = comp_display.index.map(lambda x: index_translations.get(x, x))
            
            st.dataframe(comp_display, use_container_width=True, height=600)
    
    with main_tabs[3]:  # GUIDE TAB
        st.markdown("### 📖 **Guía del Screener**")
        
        guide_tabs = st.tabs(["🎯 Uso Básico", "📊 Métricas", "💡 Tips Pro"])
        
        with guide_tabs[0]:
            st.markdown("""
            ### **Cómo usar el Screener**
            
            1. **Configuración del Screener**: Elige un preset o personaliza las columnas
            2. **Filtros Rápidos**: Usa los filtros superiores para búsquedas comunes
            3. **Filtros Avanzados**: Para criterios más específicos
            4. **Ordenamiento**: Ordena por cualquier columna (primaria y secundaria)
            5. **Exportar**: Descarga los resultados en CSV o Excel
            
            ### **Presets Disponibles**
            
            - **Básico**: Vista general con métricas esenciales
            - **Performance**: Enfocado en retornos y rankings
            - **Riesgo**: Volatilidad, beta, y métricas ajustadas
            - **ESG**: Sostenibilidad y criterios ESG
            - **Completo**: Todas las métricas principales
            """)
        
        with guide_tabs[1]:
            st.markdown("""
            ### **Explicación de Métricas**
            
            | Categoría | Métrica | Descripción |
            |-----------|---------|-------------|
            | **Retornos** | 1Y, 3Y, 5Y | Rendimiento anualizado |
            | **Riesgo** | Volatilidad | Desviación estándar de retornos |
            | **Riesgo** | Beta | Sensibilidad al mercado |
            | **Ajustado** | Sharpe | Retorno por unidad de riesgo |
            | **Ajustado** | Alpha | Exceso de retorno vs benchmark |
            | **Costes** | Ongoing | Gastos corrientes anuales |
            | **Ratings** | Stars | Calificación Morningstar (1-5) |
            | **ESG** | Sustainability | Rating sostenibilidad (1-5) |
            | **Ranking** | Percentil | Posición en categoría (1-100) |
            """)
        
        with guide_tabs[2]:
            st.markdown("""
            ### **Tips Profesionales**
            
            #### **🎯 Para encontrar los mejores fondos:**
            1. Filtra por 4-5 estrellas
            2. Sharpe > 1 (idealmente > 1.5)
            3. Gastos < mediana de categoría
            4. Percentil < 25 (top cuartil)
            
            #### **⚠️ Red Flags a evitar:**
            - Alpha negativo persistente
            - Volatilidad extrema sin compensación
            - Gastos > 2.5% sin justificación
            - Rating de riesgo "High" con bajo retorno
            
            #### **💡 Combinaciones efectivas:**
            - **Value**: P/B bajo + calidad + momentum positivo
            - **Growth**: Alto ROE + crecimiento + baja deuda
            - **Income**: Alto yield + estabilidad + bajo riesgo
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px; 
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    border-radius: 16px; margin-top: 20px;'>
            <p style='color: #8b949e; font-size: 0.9em;'>
                44,341 fondos | 96 métricas | Actualización diaria
            </p>
            <p style='color: #8b949e; margin-top: 10px;'>
                Creado con ❤️ por <a href='https://twitter.com/Gnschez' target='_blank' 
                                     style='color: #667eea; text-decoration: none; font-weight: 700;'>
                    @Gnschez
                </a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
