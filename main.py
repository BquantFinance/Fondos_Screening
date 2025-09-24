# Initialize filter variables with default values
        selected_return_1y = 'Todos'
        selected_return_3y = 'Todos'
        selected_return_5y = 'Todos'
        selected_ytd = 'Todos'
        selected_percentile = 'Todos'
        selected_volatility = 'Todos'
        selected_sharpe = 'Todos'
        selected_alpha = 'Todos'
        selected_beta = 'Todos'
        selected_risk_rating = 'Todos'
        selected_age = 'Todos'
        selected_index = 'Todos'
        selected_entry_fee = 'Todos'import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

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
    
    /* Filter section */
    .filter-section {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid #2d3748;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
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

# Column definitions with categories and Spanish translations
COLUMN_DEFINITIONS = {
    'Identificación': {
        'name': 'Nombre',
        'isin': 'ISIN',
        'fundID': 'ID Fondo',
        'firmName': 'Gestora',
        'domicile': 'Domicilio',
        'baseCurrency': 'Divisa'
    },
    'Clasificación': {
        'fund_type': 'Tipo',
        'morningstarCategory': 'Categoría',
        'isIndexFund': 'Indexado',
    },
    'Retornos': {
        'totalReturn_1m': '1 Mes %',
        'totalReturn_3m': '3 Meses %',
        'totalReturn_6m': '6 Meses %',
        'totalReturn_1y': '1 Año %',
        'totalReturn_3y': '3 Años %',
        'totalReturn_5y': '5 Años %',
        'totalReturn_10y': '10 Años %',
        'totalReturn_ytd': 'YTD %',
    },
    'Riesgo': {
        'standardDeviation_1yMonthly': 'Vol 1A %',
        'standardDeviation_3yMonthly': 'Vol 3A %',
        'standardDeviation_5yMonthly': 'Vol 5A %',
        'beta_1yMonthly': 'Beta 1A',
        'beta_3yMonthly': 'Beta 3A',
        'beta_5yMonthly': 'Beta 5A'
    },
    'Riesgo Ajustado': {
        'sharpeRatio_1yMonthly': 'Sharpe 1A',
        'sharpeRatio_3yMonthly': 'Sharpe 3A',
        'sharpeRatio_5yMonthly': 'Sharpe 5A',
        'alpha_1yMonthly': 'Alpha 1A',
        'alpha_3yMonthly': 'Alpha 3A',
        'alpha_5yMonthly': 'Alpha 5A',
    },
    'Costes': {
        'ongoingCharge': 'Gastos %',
        'maximumEntryCost': 'Com. Entrada %',
        'maximumExitCost': 'Com. Salida %',
    },
    'Ratings': {
        'fundStarRating_overall': '⭐ Rating',
        'fundStarRating_3y': '⭐ 3A',
        'fundStarRating_5y': '⭐ 5A',
        'sustainabilityRating': '🌱 ESG',
        'morningstarRiskRating_overall': 'Rating Riesgo',
    },
    'Características': {
        'fundSize': 'AUM €',
        'fund_age_years': 'Antigüedad',
        'minimumInitialInvestment': 'Inv. Mínima',
        'returnRankCategory_1y': 'Percentil 1A',
        'returnRankCategory_3y': 'Percentil 3A',
    }
}

# Create a flat dictionary for all column translations
ALL_COLUMN_TRANSLATIONS = {}
for category, columns in COLUMN_DEFINITIONS.items():
    ALL_COLUMN_TRANSLATIONS.update(columns)

# Add additional translations for columns not in the main definitions
ADDITIONAL_TRANSLATIONS = {
    # Retornos adicionales
    'totalReturn_1d': 'Retorno 1 Día %',
    'totalReturn_1w': 'Retorno 1 Semana %',
    'totalReturn_2m': 'Retorno 2 Meses %',
    'totalReturn_2y': 'Retorno 2 Años %',
    'totalReturn_4y': 'Retorno 4 Años %',
    'totalReturn_6y': 'Retorno 6 Años %',
    'totalReturn_7y': 'Retorno 7 Años %',
    'totalReturn_8y': 'Retorno 8 Años %',
    'totalReturn_9y': 'Retorno 9 Años %',
    'totalReturn_15y': 'Retorno 15 Años %',
    'totalReturn_20y': 'Retorno 20 Años %',
    'totalReturn_qtd': 'Retorno Trimestre %',
    
    # Volatilidad adicional
    'standardDeviation_10yMonthly': 'Volatilidad 10 Años %',
    'standardDeviation_15yMonthly': 'Volatilidad 15 Años %',
    'standardDeviation_20yMonthly': 'Volatilidad 20 Años %',
    
    # Sharpe adicional
    'sharpeRatio_10yMonthly': 'Sharpe Ratio 10 Años',
    'sharpeRatio_15yMonthly': 'Sharpe Ratio 15 Años',
    'sharpeRatio_20yMonthly': 'Sharpe Ratio 20 Años',
    
    # Beta adicional
    'beta_10yMonthly': 'Beta 10 Años',
    'beta_15yMonthly': 'Beta 15 Años',
    'beta_20yMonthly': 'Beta 20 Años',
    
    # Alpha adicional
    'alpha_10yMonthly': 'Alpha 10 Años',
    'alpha_15yMonthly': 'Alpha 15 Años',
    'alpha_20yMonthly': 'Alpha 20 Años',
    
    # Información adicional
    'informationRatio_3y': 'Info Ratio 3 Años',
    'informationRatio_5y': 'Info Ratio 5 Años',
    'rSquared_3yMonthly': 'R-Cuadrado 3 Años',
    'rSquared_5yMonthly': 'R-Cuadrado 5 Años',
    
    # Gestión
    'averageManagerTenure_fund': 'Años del Gestor',
    'averageManagerTenure_firm': 'Años en la Firma',
    'distributionYield': 'Rentabilidad por Dividendo %',
    
    # Comisiones
    'maximumManagementFee': 'Comisión Gestión Máx %',
    'hasPerformanceFee': 'Tiene Com. Éxito',
    
    # Ratings adicionales
    'fundStarRating_10y': '⭐ Rating 10 Años',
    'morningstarRiskRating_3y': 'Riesgo 3 Años',
    'morningstarRiskRating_5y': 'Riesgo 5 Años',
    'morningstarRiskRating_10y': 'Riesgo 10 Años',
    'medalistRating_overall': 'Rating Medallista',
    
    # Percentiles adicionales
    'returnRankCategory_5y': 'Percentil 5 Años',
    'returnRankCategory_10y': 'Percentil 10 Años',
    
    # ESG detallado
    'corporateSustainabilityScore_total': 'ESG Score Total',
    'corporateSustainabilityScore_environmental': 'ESG Ambiental',
    'corporateSustainabilityScore_social': 'ESG Social',
    'corporateSustainabilityScore_governance': 'ESG Gobernanza',
    
    # Características adicionales
    'totalNetAssetsForShareClass': 'Activos Netos Clase',
    'investmentType': 'Tipo de Inversión',
    'primaryBenchmark': 'Benchmark Principal',
    'inceptionDate': 'Fecha de Inicio',
    'data_quality': 'Calidad de Datos',
    'data_completeness': 'Completitud de Datos %',
    
    # Style boxes
    'fundEquityStyleBox': 'Style Box Renta Variable',
    'fundFixedIncomeStyleBox': 'Style Box Renta Fija',
    'fundAlternativeStyleBox': 'Style Box Alternativo'
}

ALL_COLUMN_TRANSLATIONS.update(ADDITIONAL_TRANSLATIONS)

# Preset configurations
PRESET_CONFIGS = {
    'Básico': ['name', 'fund_type', 'morningstarCategory', 'totalReturn_1y', 
               'sharpeRatio_3yMonthly', 'ongoingCharge', 'fundStarRating_overall', 'fundSize'],
    
    'Performance': ['name', 'fund_type', 'totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m',
                   'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 
                   'totalReturn_ytd', 'sharpeRatio_3yMonthly', 'alpha_3yMonthly'],
    
    'Riesgo': ['name', 'fund_type', 'standardDeviation_1yMonthly', 'standardDeviation_3yMonthly',
              'beta_3yMonthly', 'sharpeRatio_3yMonthly', 'alpha_3yMonthly',
              'morningstarRiskRating_overall', 'fundSize'],
    
    'ESG': ['name', 'fund_type', 'sustainabilityRating', 'corporateSustainabilityScore_environmental',
           'corporateSustainabilityScore_social', 'corporateSustainabilityScore_governance',
           'fundStarRating_overall', 'totalReturn_1y', 'ongoingCharge'],
    
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
    main_tabs = st.tabs(["🔍 **SCREENER**", "⚖️ **COMPARADOR**", "📖 **GUÍA**"])
    
    with main_tabs[0]:  # SCREENER TAB
        # Configuration section
        st.markdown("### ⚙️ **Configuración del Screener**")
        
        config_col1, config_col2, config_col3 = st.columns([2, 1, 1])
        
        with config_col1:
            selected_preset = st.selectbox(
                "📋 Vista Preestablecida",
                options=list(PRESET_CONFIGS.keys()),
                index=0,  # Default to 'Básico'
                help="Selecciona qué columnas quieres ver en los resultados"
            )
            selected_columns = PRESET_CONFIGS[selected_preset]
        
        with config_col2:
            num_results = st.number_input(
                "📊 Número de resultados",
                min_value=10,
                max_value=500,
                value=50,
                step=10,
                help="Cuántos fondos mostrar"
            )
        
        with config_col3:
            show_stats = st.checkbox(
                "📈 Mostrar estadísticas",
                value=True,
                help="Ver resumen estadístico"
            )
        
        st.markdown("---")
        
        # FILTROS SECTION
        st.markdown("### 🎯 **Filtros** - *Usa estos controles para filtrar los fondos*")
        
        # Basic filters
        st.markdown("#### 📌 **Filtros Básicos**")
        basic_cols = st.columns(6)
        
        with basic_cols[0]:
            fund_types_available = ['Todos'] + df['fund_type'].dropna().unique().tolist()
            selected_fund_type = st.selectbox(
                "🏷️ Tipo de Fondo",
                options=fund_types_available,
                help="Filtra por tipo de fondo"
            )
        
        with basic_cols[1]:
            if 'morningstarCategory' in df.columns:
                categories = ['Todas'] + sorted(df['morningstarCategory'].dropna().unique().tolist())
                selected_category = st.selectbox(
                    "📁 Categoría",
                    options=categories,
                    help="Categoría Morningstar"
                )
            else:
                selected_category = 'Todas'
        
        with basic_cols[2]:
            selected_stars = st.selectbox(
                "⭐ Rating Mínimo",
                options=[0, 3, 4, 5],
                format_func=lambda x: "Todos" if x == 0 else f"≥ {x} estrellas",
                help="Fondos con este rating o superior"
            )
        
        with basic_cols[3]:
            selected_esg = st.selectbox(
                "🌱 ESG Mínimo",
                options=[0, 3, 4, 5],
                format_func=lambda x: "Todos" if x == 0 else f"≥ {x} hojas",
                help="Rating ESG mínimo"
            )
        
        with basic_cols[4]:
            if 'domicile' in df.columns:
                domiciles = ['Todos'] + sorted(df['domicile'].dropna().unique().tolist())
                selected_domicile = st.selectbox(
                    "🌍 Domicilio",
                    options=domiciles,
                    help="País de domicilio"
                )
            else:
                selected_domicile = 'Todos'
        
        with basic_cols[5]:
            if 'baseCurrency' in df.columns:
                currencies = ['Todas'] + sorted(df['baseCurrency'].dropna().unique().tolist())
                selected_currency = st.selectbox(
                    "💱 Divisa",
                    options=currencies,
                    help="Divisa base del fondo"
                )
            else:
                selected_currency = 'Todas'
        
        # Performance filters
        with st.expander("📈 **Filtros de Rendimiento**", expanded=False):
            perf_cols = st.columns(5)
            
            with perf_cols[0]:
                selected_return_1y = st.selectbox(
                    "Retorno 1 Año",
                    options=['Todos', '> 20%', '> 10%', '> 0%', '0% a 10%', '< 0%', '< -10%'],
                    help="Filtra por retorno anual"
                )
            
            with perf_cols[1]:
                selected_return_3y = st.selectbox(
                    "Retorno 3 Años",
                    options=['Todos', '> 10%', '> 5%', '> 0%', '< 0%'],
                    help="Filtra por retorno a 3 años"
                )
            
            with perf_cols[2]:
                selected_return_5y = st.selectbox(
                    "Retorno 5 Años",
                    options=['Todos', '> 10%', '> 5%', '> 0%', '< 0%'],
                    help="Filtra por retorno a 5 años"
                )
            
            with perf_cols[3]:
                selected_ytd = st.selectbox(
                    "YTD",
                    options=['Todos', '> 10%', '> 5%', '> 0%', '< 0%'],
                    help="Retorno año actual"
                )
            
            with perf_cols[4]:
                if 'returnRankCategory_1y' in df.columns:
                    selected_percentile = st.selectbox(
                        "Percentil 1A",
                        options=['Todos', 'Top 10%', 'Top 25%', 'Top 50%'],
                        help="Posición en su categoría"
                    )
                else:
                    selected_percentile = 'Todos'
        
        # Risk filters
        with st.expander("⚡ **Filtros de Riesgo**", expanded=False):
            risk_cols = st.columns(5)
            
            with risk_cols[0]:
                selected_volatility = st.selectbox(
                    "Volatilidad 3A",
                    options=['Todos', '< 5%', '< 10%', '< 15%', '< 20%', '> 20%'],
                    help="Volatilidad a 3 años"
                )
            
            with risk_cols[1]:
                selected_sharpe = st.selectbox(
                    "Sharpe Ratio 3A",
                    options=['Todos', '> 2', '> 1.5', '> 1', '> 0.5', '> 0', '< 0'],
                    help="Ratio Sharpe a 3 años"
                )
            
            with risk_cols[2]:
                selected_alpha = st.selectbox(
                    "Alpha 3A",
                    options=['Todos', '> 5', '> 2', '> 0', '< 0'],
                    help="Alpha a 3 años"
                )
            
            with risk_cols[3]:
                selected_beta = st.selectbox(
                    "Beta 3A",
                    options=['Todos', '< 0.5', '0.5-1', '0.8-1.2', '> 1.2'],
                    help="Beta a 3 años"
                )
            
            with risk_cols[4]:
                if 'morningstarRiskRating_overall' in df.columns:
                    risk_ratings = ['Todos'] + df['morningstarRiskRating_overall'].dropna().unique().tolist()
                    selected_risk_rating = st.selectbox(
                        "Rating Riesgo",
                        options=risk_ratings,
                        help="Calificación de riesgo Morningstar"
                    )
                else:
                    selected_risk_rating = 'Todos'
        
        # Cost and size filters
        with st.expander("💰 **Filtros de Costes y Tamaño**", expanded=False):
            cost_cols = st.columns(5)
            
            with cost_cols[0]:
                selected_expense = st.selectbox(
                    "Gastos Totales",
                    options=['Todos', '< 0.25%', '< 0.5%', '< 1%', '< 1.5%', '< 2%', '> 2%'],
                    help="Gastos corrientes máximos"
                )
            
            with cost_cols[1]:
                selected_size = st.selectbox(
                    "AUM",
                    options=['Todos', '> 1000M€', '> 500M€', '> 100M€', '> 50M€', '> 10M€', '< 10M€'],
                    help="Tamaño del fondo"
                )
            
            with cost_cols[2]:
                if 'fund_age_years' in df.columns:
                    selected_age = st.selectbox(
                        "Antigüedad",
                        options=['Todos', '> 10 años', '> 5 años', '> 3 años', '> 1 año', '< 1 año'],
                        help="Años desde inicio"
                    )
                else:
                    selected_age = 'Todos'
            
            with cost_cols[3]:
                if 'isIndexFund' in df.columns:
                    selected_index = st.selectbox(
                        "Tipo Gestión",
                        options=['Todos', 'Solo Indexados', 'Solo Activos'],
                        help="Gestión pasiva o activa"
                    )
                else:
                    selected_index = 'Todos'
            
            with cost_cols[4]:
                if 'maximumEntryCost' in df.columns:
                    selected_entry_fee = st.selectbox(
                        "Com. Entrada",
                        options=['Todos', 'Sin comisión', '< 1%', '< 3%', '< 5%'],
                        help="Comisión de entrada máxima"
                    )
                else:
                    selected_entry_fee = 'Todos'
        
        # Apply all filters
        filtered_df = df.copy()
        
        # Basic filters
        if selected_fund_type != 'Todos':
            filtered_df = filtered_df[filtered_df['fund_type'] == selected_fund_type]
        
        if selected_category != 'Todas':
            filtered_df = filtered_df[filtered_df['morningstarCategory'] == selected_category]
        
        if selected_stars > 0 and 'fundStarRating_overall' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['fundStarRating_overall'] >= selected_stars) |
                filtered_df['fundStarRating_overall'].isna()
            ]
        
        if selected_esg > 0 and 'sustainabilityRating' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['sustainabilityRating'] >= selected_esg) |
                filtered_df['sustainabilityRating'].isna()
            ]
        
        if selected_domicile != 'Todos':
            filtered_df = filtered_df[filtered_df['domicile'] == selected_domicile]
        
        if selected_currency != 'Todas':
            filtered_df = filtered_df[filtered_df['baseCurrency'] == selected_currency]
        
        # Performance filters
        if 'totalReturn_1y' in filtered_df.columns and selected_return_1y != 'Todos':
            if selected_return_1y == '> 20%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] > 20]
            elif selected_return_1y == '> 10%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] > 10]
            elif selected_return_1y == '> 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] > 0]
            elif selected_return_1y == '0% a 10%':
                filtered_df = filtered_df[(filtered_df['totalReturn_1y'] >= 0) & (filtered_df['totalReturn_1y'] <= 10)]
            elif selected_return_1y == '< 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] < 0]
            elif selected_return_1y == '< -10%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] < -10]
        
        if 'totalReturn_3y' in filtered_df.columns and selected_return_3y != 'Todos':
            if selected_return_3y == '> 10%':
                filtered_df = filtered_df[filtered_df['totalReturn_3y'] > 10]
            elif selected_return_3y == '> 5%':
                filtered_df = filtered_df[filtered_df['totalReturn_3y'] > 5]
            elif selected_return_3y == '> 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_3y'] > 0]
            elif selected_return_3y == '< 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_3y'] < 0]
        
        if 'totalReturn_5y' in filtered_df.columns and selected_return_5y != 'Todos':
            if selected_return_5y == '> 10%':
                filtered_df = filtered_df[filtered_df['totalReturn_5y'] > 10]
            elif selected_return_5y == '> 5%':
                filtered_df = filtered_df[filtered_df['totalReturn_5y'] > 5]
            elif selected_return_5y == '> 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_5y'] > 0]
            elif selected_return_5y == '< 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_5y'] < 0]
        
        if 'totalReturn_ytd' in filtered_df.columns and selected_ytd != 'Todos':
            if selected_ytd == '> 10%':
                filtered_df = filtered_df[filtered_df['totalReturn_ytd'] > 10]
            elif selected_ytd == '> 5%':
                filtered_df = filtered_df[filtered_df['totalReturn_ytd'] > 5]
            elif selected_ytd == '> 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_ytd'] > 0]
            elif selected_ytd == '< 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_ytd'] < 0]
        
        if 'returnRankCategory_1y' in filtered_df.columns and selected_percentile != 'Todos':
            if selected_percentile == 'Top 10%':
                filtered_df = filtered_df[filtered_df['returnRankCategory_1y'] <= 10]
            elif selected_percentile == 'Top 25%':
                filtered_df = filtered_df[filtered_df['returnRankCategory_1y'] <= 25]
            elif selected_percentile == 'Top 50%':
                filtered_df = filtered_df[filtered_df['returnRankCategory_1y'] <= 50]
        
        # Risk filters
        if 'standardDeviation_3yMonthly' in filtered_df.columns and selected_volatility != 'Todos':
            if selected_volatility == '< 5%':
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] < 5]
            elif selected_volatility == '< 10%':
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] < 10]
            elif selected_volatility == '< 15%':
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] < 15]
            elif selected_volatility == '< 20%':
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] < 20]
            elif selected_volatility == '> 20%':
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] > 20]
        
        if 'sharpeRatio_3yMonthly' in filtered_df.columns and selected_sharpe != 'Todos':
            if selected_sharpe == '> 2':
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] > 2]
            elif selected_sharpe == '> 1.5':
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] > 1.5]
            elif selected_sharpe == '> 1':
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] > 1]
            elif selected_sharpe == '> 0.5':
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] > 0.5]
            elif selected_sharpe == '> 0':
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] > 0]
            elif selected_sharpe == '< 0':
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] < 0]
        
        if 'alpha_3yMonthly' in filtered_df.columns and selected_alpha != 'Todos':
            if selected_alpha == '> 5':
                filtered_df = filtered_df[filtered_df['alpha_3yMonthly'] > 5]
            elif selected_alpha == '> 2':
                filtered_df = filtered_df[filtered_df['alpha_3yMonthly'] > 2]
            elif selected_alpha == '> 0':
                filtered_df = filtered_df[filtered_df['alpha_3yMonthly'] > 0]
            elif selected_alpha == '< 0':
                filtered_df = filtered_df[filtered_df['alpha_3yMonthly'] < 0]
        
        if 'beta_3yMonthly' in filtered_df.columns and selected_beta != 'Todos':
            if selected_beta == '< 0.5':
                filtered_df = filtered_df[filtered_df['beta_3yMonthly'] < 0.5]
            elif selected_beta == '0.5-1':
                filtered_df = filtered_df[(filtered_df['beta_3yMonthly'] >= 0.5) & (filtered_df['beta_3yMonthly'] <= 1)]
            elif selected_beta == '0.8-1.2':
                filtered_df = filtered_df[(filtered_df['beta_3yMonthly'] >= 0.8) & (filtered_df['beta_3yMonthly'] <= 1.2)]
            elif selected_beta == '> 1.2':
                filtered_df = filtered_df[filtered_df['beta_3yMonthly'] > 1.2]
        
        if 'morningstarRiskRating_overall' in filtered_df.columns and selected_risk_rating != 'Todos':
            filtered_df = filtered_df[filtered_df['morningstarRiskRating_overall'] == selected_risk_rating]
        
        # Cost and size filters
        if 'ongoingCharge' in filtered_df.columns and selected_expense != 'Todos':
            if selected_expense == '< 0.25%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 0.25]
            elif selected_expense == '< 0.5%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 0.5]
            elif selected_expense == '< 1%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 1]
            elif selected_expense == '< 1.5%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 1.5]
            elif selected_expense == '< 2%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 2]
            elif selected_expense == '> 2%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] > 2]
        
        if 'fundSize' in filtered_df.columns and selected_size != 'Todos':
            if selected_size == '> 1000M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 1000e6]
            elif selected_size == '> 500M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 500e6]
            elif selected_size == '> 100M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 100e6]
            elif selected_size == '> 50M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 50e6]
            elif selected_size == '> 10M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 10e6]
            elif selected_size == '< 10M€':
                filtered_df = filtered_df[filtered_df['fundSize'] < 10e6]
        
        if 'fund_age_years' in filtered_df.columns and selected_age != 'Todos':
            if selected_age == '> 10 años':
                filtered_df = filtered_df[filtered_df['fund_age_years'] > 10]
            elif selected_age == '> 5 años':
                filtered_df = filtered_df[filtered_df['fund_age_years'] > 5]
            elif selected_age == '> 3 años':
                filtered_df = filtered_df[filtered_df['fund_age_years'] > 3]
            elif selected_age == '> 1 año':
                filtered_df = filtered_df[filtered_df['fund_age_years'] > 1]
            elif selected_age == '< 1 año':
                filtered_df = filtered_df[filtered_df['fund_age_years'] < 1]
        
        if 'isIndexFund' in filtered_df.columns and selected_index != 'Todos':
            if selected_index == 'Solo Indexados':
                filtered_df = filtered_df[filtered_df['isIndexFund'] == True]
            elif selected_index == 'Solo Activos':
                filtered_df = filtered_df[filtered_df['isIndexFund'] == False]
        
        if 'maximumEntryCost' in filtered_df.columns and selected_entry_fee != 'Todos':
            if selected_entry_fee == 'Sin comisión':
                filtered_df = filtered_df[(filtered_df['maximumEntryCost'] == 0) | filtered_df['maximumEntryCost'].isna()]
            elif selected_entry_fee == '< 1%':
                filtered_df = filtered_df[filtered_df['maximumEntryCost'] < 1]
            elif selected_entry_fee == '< 3%':
                filtered_df = filtered_df[filtered_df['maximumEntryCost'] < 3]
            elif selected_entry_fee == '< 5%':
                filtered_df = filtered_df[filtered_df['maximumEntryCost'] < 5]
        
        st.markdown("---")
        
        # SORTING SECTION
        st.markdown("### 📊 **Ordenamiento** - *Elige cómo ordenar los resultados*")
        
        sort_cols = st.columns([3, 2, 2])
        
        with sort_cols[0]:
            # Get available columns for sorting
            available_columns = filtered_df.columns.tolist()
            
            # Create friendly names for sorting columns
            sort_friendly_names = {}
            for col in available_columns:
                if col in ALL_COLUMN_TRANSLATIONS:
                    sort_friendly_names[col] = ALL_COLUMN_TRANSLATIONS[col]
                else:
                    # Create a friendly name for columns not in translations
                    friendly_name = col.replace('_', ' ').replace('[', ' ').replace(']', '')
                    sort_friendly_names[col] = friendly_name.title()
            
            # Prioritize common sorting columns
            priority_cols = ['totalReturn_1y', 'totalReturn_3y', 'sharpeRatio_3yMonthly', 
                           'fundSize', 'ongoingCharge', 'fundStarRating_overall']
            available_priority = [col for col in priority_cols if col in available_columns]
            other_cols = [col for col in available_columns if col not in priority_cols]
            
            sort_options = available_priority + other_cols
            
            sort_by = st.selectbox(
                "🔽 Ordenar por",
                options=sort_options,
                format_func=lambda x: sort_friendly_names.get(x, x),
                index=0 if sort_options else None,
                help="Selecciona la columna para ordenar"
            )
        
        with sort_cols[1]:
            sort_order = st.radio(
                "📈 Dirección",
                options=['Descendente ↓', 'Ascendente ↑'],
                horizontal=True,
                help="Mayor a menor o menor a mayor"
            )
        
        with sort_cols[2]:
            # Display filter stats
            st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: #1a1f2e; border-radius: 10px;'>
                    <b>Fondos encontrados</b><br>
                    <span style='font-size: 24px; color: #667eea;'>{len(filtered_df):,}</span><br>
                    <span style='font-size: 12px; color: #8b949e;'>de {len(df):,} totales</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Apply sorting
        if sort_by:
            ascending = 'Ascendente' in sort_order
            sorted_df = filtered_df.sort_values(
                by=sort_by,
                ascending=ascending,
                na_position='last'
            ).head(num_results)
        else:
            sorted_df = filtered_df.head(num_results)
        
        st.markdown("---")
        
        # RESULTS SECTION
        st.markdown(f"### 📋 **Resultados** - *Mostrando {min(num_results, len(sorted_df))} de {len(filtered_df)} fondos filtrados*")
        
        # Prepare display dataframe
        display_cols = [col for col in selected_columns if col in sorted_df.columns]
        
        if display_cols:
            display_df = sorted_df[display_cols].copy()
            
            # Format columns
            for col in display_df.columns:
                if col == 'fundSize':
                    display_df[col] = display_df[col].apply(lambda x: format_number(x, 1, '€'))
                elif 'totalReturn' in col or 'return' in col.lower():
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                elif 'ongoingCharge' in col or 'maximum' in col.lower():
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                elif any(metric in col.lower() for metric in ['sharpe', 'alpha', 'beta', 'standard']):
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/D")
                elif col in ['isIndexFund', 'hasPerformanceFee']:
                    display_df[col] = display_df[col].apply(lambda x: '✓' if x else '✗' if not pd.isna(x) else "N/D")
            
            # Apply translations using the comprehensive dictionary
            rename_dict = {col: ALL_COLUMN_TRANSLATIONS.get(col, col) for col in display_df.columns}
            display_df = display_df.rename(columns=rename_dict)
            
            # Display results
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Export button
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                csv = sorted_df.to_csv(index=False)
                st.download_button(
                    label=f"📥 Descargar CSV ({len(sorted_df)} fondos)",
                    data=csv,
                    file_name=f"screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    type="primary"
                )
            
            # Statistics section
            if show_stats and len(sorted_df) > 0:
                st.markdown("---")
                st.markdown("### 📊 **Estadísticas de los Resultados**")
                
                stats_cols = st.columns(4)
                
                with stats_cols[0]:
                    if 'totalReturn_1y' in sorted_df.columns:
                        clean_returns = sorted_df['totalReturn_1y'].dropna()
                        if len(clean_returns) > 0:
                            st.markdown(f"""
                            <div style='background: #1a1f2e; padding: 15px; border-radius: 10px;'>
                                <b>📈 Retorno 1A</b><br>
                                Media: {clean_returns.mean():.2f}%<br>
                                Mediana: {clean_returns.median():.2f}%<br>
                                Max: {clean_returns.max():.2f}%
                            </div>
                            """, unsafe_allow_html=True)
                
                with stats_cols[1]:
                    if 'sharpeRatio_3yMonthly' in sorted_df.columns:
                        clean_sharpe = sorted_df['sharpeRatio_3yMonthly'].dropna()
                        if len(clean_sharpe) > 0:
                            st.markdown(f"""
                            <div style='background: #1a1f2e; padding: 15px; border-radius: 10px;'>
                                <b>📊 Sharpe 3A</b><br>
                                Media: {clean_sharpe.mean():.2f}<br>
                                Mediana: {clean_sharpe.median():.2f}<br>
                                Max: {clean_sharpe.max():.2f}
                            </div>
                            """, unsafe_allow_html=True)
                
                with stats_cols[2]:
                    if 'ongoingCharge' in sorted_df.columns:
                        clean_charges = sorted_df['ongoingCharge'].dropna()
                        if len(clean_charges) > 0:
                            st.markdown(f"""
                            <div style='background: #1a1f2e; padding: 15px; border-radius: 10px;'>
                                <b>💰 Gastos</b><br>
                                Media: {clean_charges.mean():.2f}%<br>
                                Mediana: {clean_charges.median():.2f}%<br>
                                Min: {clean_charges.min():.2f}%
                            </div>
                            """, unsafe_allow_html=True)
                
                with stats_cols[3]:
                    if 'fundSize' in sorted_df.columns:
                        clean_sizes = sorted_df['fundSize'].dropna()
                        if len(clean_sizes) > 0:
                            st.markdown(f"""
                            <div style='background: #1a1f2e; padding: 15px; border-radius: 10px;'>
                                <b>📊 AUM Total</b><br>
                                Total: €{clean_sizes.sum()/1e9:.1f}B<br>
                                Media: €{clean_sizes.mean()/1e6:.1f}M<br>
                                Fondos: {len(clean_sizes):,}
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning("No hay columnas seleccionadas para mostrar")
    
    with main_tabs[1]:  # COMPARATOR TAB
        st.markdown("### ⚖️ **Comparador y Análisis**")
        
        # Fund selection
        if len(filtered_df) > 0:
            fund_names = sorted(filtered_df['name'].dropna().unique())
            
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_funds = st.multiselect(
                    "📌 Selecciona fondos para comparar (máximo 10)",
                    options=fund_names,
                    max_selections=10,
                    help="Elige hasta 10 fondos para comparación detallada"
                )
            
            with col2:
                if selected_funds:
                    if st.button("🗑️ Limpiar selección", type="secondary"):
                        selected_funds = []
            
            if selected_funds:
                comparison_df = filtered_df[filtered_df['name'].isin(selected_funds)]
                
                # Quick comparison metrics
                st.markdown("#### 📊 **Resumen Comparativo**")
                
                metric_cols = st.columns(len(selected_funds) if len(selected_funds) <= 5 else 5)
                for i, fund in enumerate(selected_funds[:5]):
                    fund_data = comparison_df[comparison_df['name'] == fund].iloc[0]
                    with metric_cols[i]:
                        st.markdown(f"**{fund[:25]}...**")
                        
                        ret_1y = fund_data.get('totalReturn_1y', np.nan)
                        sharpe = fund_data.get('sharpeRatio_3yMonthly', np.nan)
                        expense = fund_data.get('ongoingCharge', np.nan)
                        stars = fund_data.get('fundStarRating_overall', np.nan)
                        
                        st.metric("Retorno 1A", f"{ret_1y:.1f}%" if not pd.isna(ret_1y) else "N/D")
                        st.metric("Sharpe 3A", f"{sharpe:.2f}" if not pd.isna(sharpe) else "N/D")
                        st.metric("Gastos", f"{expense:.2f}%" if not pd.isna(expense) else "N/D")
                        st.metric("Rating", f"⭐ {int(stars)}" if not pd.isna(stars) else "N/D")
                
                st.markdown("---")
                
                # Tabbed comparison views
                comp_tabs = st.tabs(["📈 Retornos", "⚡ Riesgo", "💰 Costes", "📊 Gráficos", "📋 Tabla Completa"])
                
                with comp_tabs[0]:  # Returns comparison
                    st.markdown("#### 📈 Comparación de Retornos")
                    
                    # Returns heatmap
                    fig = create_performance_heatmap(filtered_df, selected_funds)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Bar chart comparison
                    return_periods = ['totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y']
                    return_data = []
                    for fund in selected_funds:
                        fund_info = comparison_df[comparison_df['name'] == fund].iloc[0]
                        for period in return_periods:
                            if period in comparison_df.columns:
                                return_data.append({
                                    'Fondo': fund[:25] + '...' if len(fund) > 25 else fund,
                                    'Período': ALL_COLUMN_TRANSLATIONS.get(period, period),
                                    'Retorno': fund_info.get(period, 0)
                                })
                    
                    if return_data:
                        df_returns = pd.DataFrame(return_data)
                        fig = px.bar(df_returns, x='Período', y='Retorno', color='Fondo',
                                    title="Comparación de Retornos por Período",
                                    barmode='group')
                        fig.update_layout(
                            paper_bgcolor='#0e1117',
                            plot_bgcolor='#1a1f2e',
                            font=dict(color='#fafafa'),
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with comp_tabs[1]:  # Risk comparison
                    st.markdown("#### ⚡ Comparación de Riesgo")
                    
                    risk_metrics = ['standardDeviation_1yMonthly', 'standardDeviation_3yMonthly',
                                   'beta_1yMonthly', 'beta_3yMonthly', 'morningstarRiskRating_overall']
                    
                    risk_data = []
                    for fund in selected_funds:
                        fund_info = comparison_df[comparison_df['name'] == fund].iloc[0]
                        risk_row = {'Fondo': fund[:30] + '...' if len(fund) > 30 else fund}
                        for metric in risk_metrics:
                            if metric in comparison_df.columns:
                                risk_row[ALL_COLUMN_TRANSLATIONS.get(metric, metric)] = fund_info.get(metric, np.nan)
                        risk_data.append(risk_row)
                    
                    if risk_data:
                        risk_df = pd.DataFrame(risk_data)
                        
                        # Format numeric columns
                        for col in risk_df.columns:
                            if col != 'Fondo':
                                risk_df[col] = risk_df[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) and isinstance(x, (int, float)) else x)
                        
                        st.dataframe(risk_df, use_container_width=True, hide_index=True)
                        
                        # Risk radar chart
                        if 'standardDeviation_3yMonthly' in comparison_df.columns and 'beta_3yMonthly' in comparison_df.columns:
                            fig = go.Figure()
                            
                            for fund in selected_funds:
                                fund_data = comparison_df[comparison_df['name'] == fund].iloc[0]
                                
                                categories = []
                                values = []
                                
                                if not pd.isna(fund_data.get('standardDeviation_1yMonthly')):
                                    categories.append('Vol 1A')
                                    values.append(fund_data['standardDeviation_1yMonthly'])
                                
                                if not pd.isna(fund_data.get('standardDeviation_3yMonthly')):
                                    categories.append('Vol 3A')
                                    values.append(fund_data['standardDeviation_3yMonthly'])
                                
                                if not pd.isna(fund_data.get('beta_3yMonthly')):
                                    categories.append('Beta 3A')
                                    values.append(abs(fund_data['beta_3yMonthly']) * 10)  # Scale for visibility
                                
                                if categories and values:
                                    fig.add_trace(go.Scatterpolar(
                                        r=values,
                                        theta=categories,
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
                                title="Perfil de Riesgo Comparativo",
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                with comp_tabs[2]:  # Costs comparison
                    st.markdown("#### 💰 Comparación de Costes")
                    
                    cost_metrics = ['ongoingCharge', 'maximumEntryCost', 'maximumExitCost', 
                                   'maximumManagementFee', 'hasPerformanceFee']
                    
                    cost_data = []
                    for fund in selected_funds:
                        fund_info = comparison_df[comparison_df['name'] == fund].iloc[0]
                        cost_row = {'Fondo': fund[:30] + '...' if len(fund) > 30 else fund}
                        for metric in cost_metrics:
                            if metric in comparison_df.columns:
                                value = fund_info.get(metric, np.nan)
                                if metric == 'hasPerformanceFee':
                                    cost_row[ALL_COLUMN_TRANSLATIONS.get(metric, metric)] = '✓' if value else '✗'
                                else:
                                    cost_row[ALL_COLUMN_TRANSLATIONS.get(metric, metric)] = f"{value:.2f}%" if not pd.isna(value) else "N/D"
                        cost_data.append(cost_row)
                    
                    if cost_data:
                        cost_df = pd.DataFrame(cost_data)
                        st.dataframe(cost_df, use_container_width=True, hide_index=True)
                        
                        # Cost bar chart
                        if 'ongoingCharge' in comparison_df.columns:
                            costs = []
                            for fund in selected_funds:
                                fund_data = comparison_df[comparison_df['name'] == fund].iloc[0]
                                costs.append({
                                    'Fondo': fund[:25] + '...' if len(fund) > 25 else fund,
                                    'Gastos Corrientes': fund_data.get('ongoingCharge', 0)
                                })
                            
                            df_costs = pd.DataFrame(costs)
                            fig = px.bar(df_costs, x='Fondo', y='Gastos Corrientes',
                                       title="Comparación de Gastos Corrientes (%)",
                                       text='Gastos Corrientes')
                            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
                            fig.update_layout(
                                paper_bgcolor='#0e1117',
                                plot_bgcolor='#1a1f2e',
                                font=dict(color='#fafafa'),
                                height=400
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                with comp_tabs[3]:  # Charts
                    st.markdown("#### 📈 **Gráfico de Dispersión Configurable**")
                    
                    # Get numeric columns for scatter plot
                    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
                    
                    # Create friendly names for the columns
                    friendly_names = {}
                    for col in numeric_cols:
                        if col in ALL_COLUMN_TRANSLATIONS:
                            friendly_names[col] = ALL_COLUMN_TRANSLATIONS[col]
                        else:
                            friendly_name = col.replace('_', ' ').replace('[', ' ').replace(']', '')
                            friendly_names[col] = friendly_name.title()
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        default_x = 'standardDeviation_3yMonthly' if 'standardDeviation_3yMonthly' in numeric_cols else numeric_cols[0] if numeric_cols else None
                        
                        x_axis = st.selectbox(
                            "📊 Eje X",
                            options=numeric_cols,
                            format_func=lambda x: friendly_names.get(x, x),
                            index=numeric_cols.index(default_x) if default_x in numeric_cols else 0,
                            help="Selecciona la métrica para el eje horizontal"
                        )
                    
                    with col2:
                        default_y = 'totalReturn_3y' if 'totalReturn_3y' in numeric_cols else numeric_cols[0] if numeric_cols else None
                        
                        y_axis = st.selectbox(
                            "📈 Eje Y",
                            options=numeric_cols,
                            format_func=lambda x: friendly_names.get(x, x),
                            index=numeric_cols.index(default_y) if default_y in numeric_cols else 0,
                            help="Selecciona la métrica para el eje vertical"
                        )
                    
                    with col3:
                        size_options = ['Ninguno'] + numeric_cols
                        default_size = 'fundSize' if 'fundSize' in numeric_cols else 'Ninguno'
                        
                        size_var = st.selectbox(
                            "⭕ Tamaño de punto",
                            options=size_options,
                            format_func=lambda x: 'Sin tamaño variable' if x == 'Ninguno' else friendly_names.get(x, x),
                            index=size_options.index(default_size),
                            help="Variable para determinar el tamaño de los puntos"
                        )
                    
                    # Create scatter plot
                    if x_axis and y_axis:
                        scatter_data = filtered_df.dropna(subset=[x_axis, y_axis]).copy()
                        
                        if size_var != 'Ninguno':
                            scatter_data[size_var] = scatter_data[size_var].fillna(scatter_data[size_var].median())
                            size_col = size_var
                        else:
                            size_col = None
                        
                        x_label = friendly_names.get(x_axis, x_axis)
                        y_label = friendly_names.get(y_axis, y_axis)
                        
                        fig = px.scatter(
                            scatter_data,
                            x=x_axis,
                            y=y_axis,
                            color='fund_type',
                            size=size_col if size_col else None,
                            hover_data=['name', 'firmName', 'morningstarCategory'],
                            title=f"{y_label} vs {x_label}",
                            labels={
                                x_axis: x_label,
                                y_axis: y_label,
                                'fund_type': 'Tipo de Fondo',
                                size_var: friendly_names.get(size_var, size_var) if size_var != 'Ninguno' else None
                            },
                            color_discrete_map={
                                'Renta Variable': '#3b82f6',
                                'Renta Fija': '#10b981',
                                'Alternativo': '#f59e0b',
                                'Mixto/Otro': '#8b5cf6'
                            }
                        )
                        
                        # Add median lines
                        x_median = scatter_data[x_axis].median()
                        y_median = scatter_data[y_axis].median()
                        
                        fig.add_hline(y=y_median, line_dash="dash", line_color="gray", opacity=0.5,
                                     annotation_text=f"Mediana: {y_median:.2f}")
                        fig.add_vline(x=x_median, line_dash="dash", line_color="gray", opacity=0.5,
                                     annotation_text=f"Mediana: {x_median:.2f}")
                        
                        # Highlight selected funds
                        if selected_funds:
                            selected_data = scatter_data[scatter_data['name'].isin(selected_funds)]
                            if not selected_data.empty:
                                fig.add_trace(go.Scatter(
                                    x=selected_data[x_axis],
                                    y=selected_data[y_axis],
                                    mode='markers',
                                    marker=dict(
                                        size=15,
                                        color='red',
                                        symbol='star',
                                        line=dict(color='white', width=2)
                                    ),
                                    name='Fondos Seleccionados',
                                    showlegend=True,
                                    hovertemplate='<b>%{text}</b><br>' + 
                                                f'{x_label}: ' + '%{x:.2f}<br>' +
                                                f'{y_label}: ' + '%{y:.2f}<extra></extra>',
                                    text=selected_data['name']
                                ))
                        
                        fig.update_layout(
                            paper_bgcolor='#0e1117',
                            plot_bgcolor='#1a1f2e',
                            font=dict(color='#fafafa'),
                            height=600,
                            xaxis=dict(gridcolor='#2d3748', zeroline=False, title=x_label),
                            yaxis=dict(gridcolor='#2d3748', zeroline=False, title=y_label)
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                with comp_tabs[4]:  # Complete table
                    st.markdown("#### 📋 **Tabla Comparativa Completa**")
                    
                    # Select categories to compare
                    categories_to_compare = st.multiselect(
                        "Selecciona categorías de métricas",
                        options=list(COLUMN_DEFINITIONS.keys()),
                        default=['Retornos', 'Riesgo Ajustado', 'Costes', 'Ratings']
                    )
                    
                    # Build comparison metrics
                    comparison_metrics = ['name']
                    for cat in categories_to_compare:
                        comparison_metrics.extend([col for col in COLUMN_DEFINITIONS[cat].keys() 
                                                 if col in comparison_df.columns])
                    
                    if len(comparison_metrics) > 1:
                        comp_display = comparison_df[comparison_metrics].set_index('name').T
                        
                        # Apply translations
                        comp_display.index = comp_display.index.map(lambda x: ALL_COLUMN_TRANSLATIONS.get(x, x))
                        
                        st.dataframe(comp_display, use_container_width=True, height=500)
                        
                        # Export comparison
                        csv = comparison_df[comparison_metrics].to_csv(index=False)
                        st.download_button(
                            label="📥 Descargar comparación CSV",
                            data=csv,
                            file_name=f"comparacion_fondos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
            else:
                st.info("👆 Selecciona fondos arriba para comenzar la comparación")
        else:
            st.warning("Aplica filtros primero para ver fondos disponibles")
    
    with main_tabs[2]:  # GUIDE TAB
        st.markdown("### 📖 **Guía de Uso**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🔍 **Cómo usar el Screener**
            
            1. **Configura la Vista**: Elige qué columnas quieres ver
            2. **Aplica Filtros**: Usa los 6 filtros para refinar
            3. **Ordena Resultados**: Selecciona columna y dirección
            4. **Exporta**: Descarga los resultados en CSV
            
            #### 📊 **Métricas Clave**
            
            - **Retorno 1A/3A/5A**: Rendimiento anualizado
            - **Sharpe Ratio**: Retorno ajustado al riesgo (>1 bueno)
            - **Alpha**: Exceso de retorno vs mercado
            - **Beta**: Sensibilidad al mercado (1 = mercado)
            - **Volatilidad**: Desviación estándar de retornos
            - **Gastos**: Costes anuales del fondo
            """)
        
        with col2:
            st.markdown("""
            #### ⚡ **Filtros Rápidos**
            
            - **Tipo**: RV, RF, Alternativo, Mixto
            - **Rating**: Calificación Morningstar (1-5 ⭐)
            - **Retorno 1A**: Filtro por rendimiento anual
            - **Gastos**: Máximo coste anual aceptable
            - **AUM**: Tamaño mínimo del fondo
            - **ESG**: Sostenibilidad (1-5 🌱)
            
            #### 💡 **Consejos Pro**
            
            - Busca Sharpe > 1 y Alpha positivo
            - Gastos < 1.5% para RV, < 0.5% para RF
            - AUM > 50M€ para mejor liquidez
            - Compara fondos similares (misma categoría)
            - Revisa retornos a 3-5 años, no solo 1 año
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px; 
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    border-radius: 16px; margin-top: 20px;'>
            <p style='color: #8b949e; font-size: 0.9em;'>
                44,341 fondos | 96 métricas | Datos actualizados
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
