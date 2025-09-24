import streamlit as st
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
               'sharpeRatio_3yMonthly', 'ongoingCharge', 'fundStarRating_overall'],
    
    'Performance': ['name', 'totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m',
                   'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 
                   'totalReturn_ytd', 'sharpeRatio_3yMonthly'],
    
    'Riesgo': ['name', 'standardDeviation_1yMonthly', 'standardDeviation_3yMonthly',
              'beta_3yMonthly', 'sharpeRatio_3yMonthly', 'alpha_3yMonthly',
              'morningstarRiskRating_overall'],
    
    'ESG': ['name', 'fund_type', 'sustainabilityRating', 'fundStarRating_overall',
           'totalReturn_1y', 'ongoingCharge'],
    
    'Completo': ['name', 'fund_type', 'morningstarCategory', 'totalReturn_1y', 
                'totalReturn_3y', 'sharpeRatio_3yMonthly', 'standardDeviation_3yMonthly', 
                'alpha_3yMonthly', 'beta_3yMonthly', 'ongoingCharge', 'fundSize', 
                'fundStarRating_overall', 'sustainabilityRating']
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
        
        # Quick filters in a clear box
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        
        filter_cols = st.columns(6)
        
        with filter_cols[0]:
            fund_types_available = ['Todos'] + df['fund_type'].dropna().unique().tolist()
            selected_fund_type = st.selectbox(
                "🏷️ Tipo de Fondo",
                options=fund_types_available,
                help="Filtra por tipo de fondo"
            )
        
        with filter_cols[1]:
            selected_stars = st.selectbox(
                "⭐ Rating Mínimo",
                options=[0, 3, 4, 5],
                format_func=lambda x: "Todos" if x == 0 else f"≥ {x} estrellas",
                help="Fondos con este rating o superior"
            )
        
        with filter_cols[2]:
            selected_return = st.selectbox(
                "📈 Retorno 1A",
                options=['Todos', '> 0%', '> 10%', '> 20%', '< 0%'],
                help="Filtra por retorno anual"
            )
        
        with filter_cols[3]:
            selected_expense = st.selectbox(
                "💰 Gastos Máximos",
                options=['Todos', '< 0.5%', '< 1%', '< 1.5%', '< 2%'],
                help="Fondos con gastos menores a"
            )
        
        with filter_cols[4]:
            selected_size = st.selectbox(
                "📊 AUM Mínimo",
                options=['Todos', '> 10M€', '> 50M€', '> 100M€', '> 500M€'],
                help="Tamaño mínimo del fondo"
            )
        
        with filter_cols[5]:
            selected_esg = st.selectbox(
                "🌱 ESG Mínimo",
                options=[0, 3, 4, 5],
                format_func=lambda x: "Todos" if x == 0 else f"≥ {x} hojas",
                help="Rating ESG mínimo"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply each filter with clear logic
        if selected_fund_type != 'Todos':
            filtered_df = filtered_df[filtered_df['fund_type'] == selected_fund_type]
        
        if selected_stars > 0 and 'fundStarRating_overall' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['fundStarRating_overall'] >= selected_stars) |
                filtered_df['fundStarRating_overall'].isna()
            ]
        
        if 'totalReturn_1y' in filtered_df.columns:
            if selected_return == '> 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] > 0]
            elif selected_return == '> 10%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] > 10]
            elif selected_return == '> 20%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] > 20]
            elif selected_return == '< 0%':
                filtered_df = filtered_df[filtered_df['totalReturn_1y'] < 0]
        
        if 'ongoingCharge' in filtered_df.columns:
            if selected_expense == '< 0.5%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 0.5]
            elif selected_expense == '< 1%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 1]
            elif selected_expense == '< 1.5%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 1.5]
            elif selected_expense == '< 2%':
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < 2]
        
        if 'fundSize' in filtered_df.columns:
            if selected_size == '> 10M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 10e6]
            elif selected_size == '> 50M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 50e6]
            elif selected_size == '> 100M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 100e6]
            elif selected_size == '> 500M€':
                filtered_df = filtered_df[filtered_df['fundSize'] > 500e6]
        
        if selected_esg > 0 and 'sustainabilityRating' in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df['sustainabilityRating'] >= selected_esg) |
                filtered_df['sustainabilityRating'].isna()
            ]
        
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
            
            # Apply translations
            column_translations = {}
            for category, cols in COLUMN_DEFINITIONS.items():
                column_translations.update(cols)
            
            rename_dict = {col: column_translations.get(col, col) for col in display_df.columns}
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
            
            selected_funds = st.multiselect(
                "📌 Selecciona fondos para comparar (máximo 10)",
                options=fund_names,
                max_selections=10,
                help="Elige hasta 10 fondos para comparación detallada"
            )
            
            if selected_funds:
                comparison_df = filtered_df[filtered_df['name'].isin(selected_funds)]
                
                # Heatmap of returns
                st.markdown("#### 🔥 **Mapa de Calor - Retornos**")
                fig = create_performance_heatmap(filtered_df, selected_funds)
                st.plotly_chart(fig, use_container_width=True)
                
                # Comparison table
                st.markdown("#### 📊 **Tabla Comparativa**")
                
                # Select metrics to compare
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
                    index_translations = {}
                    for category, cols in COLUMN_DEFINITIONS.items():
                        index_translations.update(cols)
                    
                    comp_display.index = comp_display.index.map(lambda x: index_translations.get(x, x))
                    
                    st.dataframe(comp_display, use_container_width=True, height=400)
                
                # Scatter plot configuration
                st.markdown("---")
                st.markdown("#### 📈 **Gráfico de Dispersión Configurable**")
                
                # Get numeric columns for scatter plot
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
                
                # Create friendly names for the columns
                friendly_names = {}
                for col in numeric_cols:
                    if col in ALL_COLUMN_TRANSLATIONS:
                        friendly_names[col] = ALL_COLUMN_TRANSLATIONS[col]
                    else:
                        # Create a friendly name for columns not in translations
                        friendly_name = col.replace('_', ' ').replace('[', ' ').replace(']', '')
                        friendly_name = friendly_name.replace('Monthly', ' Mensual')
                        friendly_name = friendly_name.replace('Return', 'Retorno')
                        friendly_name = friendly_name.replace('totalReturn', 'Retorno')
                        friendly_name = friendly_name.replace('standardDeviation', 'Volatilidad')
                        friendly_name = friendly_name.replace('sharpeRatio', 'Ratio Sharpe')
                        friendly_names[col] = friendly_name.title()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Default to volatility if available
                    default_x = 'standardDeviation_3yMonthly' if 'standardDeviation_3yMonthly' in numeric_cols else numeric_cols[0] if numeric_cols else None
                    
                    x_axis = st.selectbox(
                        "📊 Eje X",
                        options=numeric_cols,
                        format_func=lambda x: friendly_names.get(x, x),
                        index=numeric_cols.index(default_x) if default_x in numeric_cols else 0,
                        help="Selecciona la métrica para el eje horizontal"
                    )
                
                with col2:
                    # Default to return if available
                    default_y = 'totalReturn_3y' if 'totalReturn_3y' in numeric_cols else numeric_cols[0] if numeric_cols else None
                    
                    y_axis = st.selectbox(
                        "📈 Eje Y",
                        options=numeric_cols,
                        format_func=lambda x: friendly_names.get(x, x),
                        index=numeric_cols.index(default_y) if default_y in numeric_cols else 0,
                        help="Selecciona la métrica para el eje vertical"
                    )
                
                with col3:
                    # Size variable with None option
                    size_options = ['Ninguno'] + numeric_cols
                    default_size = 'fundSize' if 'fundSize' in numeric_cols else 'Ninguno'
                    
                    size_var = st.selectbox(
                        "⭕ Tamaño de punto",
                        options=size_options,
                        format_func=lambda x: 'Sin tamaño variable' if x == 'Ninguno' else friendly_names.get(x, x),
                        index=size_options.index(default_size),
                        help="Variable para determinar el tamaño de los puntos (opcional)"
                    )
                
                # Create scatter plot
                if x_axis and y_axis:
                    scatter_data = filtered_df.dropna(subset=[x_axis, y_axis]).copy()
                    
                    # Handle size variable
                    if size_var != 'Ninguno':
                        scatter_data[size_var] = scatter_data[size_var].fillna(scatter_data[size_var].median())
                        size_col = size_var
                    else:
                        size_col = None
                    
                    # Get friendly names for axis labels
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
                        xaxis=dict(
                            gridcolor='#2d3748',
                            zeroline=False,
                            title=x_label
                        ),
                        yaxis=dict(
                            gridcolor='#2d3748',
                            zeroline=False,
                            title=y_label
                        ),
                        hoverlabel=dict(
                            bgcolor="#1a1f2e",
                            font_size=12,
                            font_family="Arial"
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
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
