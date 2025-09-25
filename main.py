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
    bool_cols = ['hasPerformanceFee', 'isIndexFund', 'isPrimaryShareClassInMarket']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({'True': True, 'False': False, True: True, False: False})
    
    # Convert date column
    if 'inceptionDate' in df.columns:
        df['inceptionDate'] = pd.to_datetime(df['inceptionDate'], errors='coerce')
    
    # Calculate fund age if inception date exists
    if 'inceptionDate' in df.columns:
        df['fund_age_years'] = (pd.Timestamp.now() - df['inceptionDate']).dt.days / 365.25
    
    # Handle fund type column - could be 'fund_type' or 'broadCategoryGroup'
    type_translations = {
        'Equity': 'Renta Variable',
        'Fixed Income': 'Renta Fija',
        'Alternative': 'Alternativo',
        'Other/Mixed': 'Mixto/Otro',
        'Allocation': 'Mixto/Otro',
        'Commodities': 'Alternativo',
        'Convertible': 'Mixto/Otro',
        'Miscellaneous': 'Mixto/Otro'
    }
    
    # Check for fund_type or broadCategoryGroup and create/rename to fund_type
    if 'broadCategoryGroup' in df.columns:
        df['fund_type'] = df['broadCategoryGroup'].map(type_translations).fillna(df['broadCategoryGroup'])
    elif 'fund_type' in df.columns:
        df['fund_type'] = df['fund_type'].map(type_translations).fillna(df['fund_type'])
    else:
        # Create a default fund_type column if neither exists
        df['fund_type'] = 'Mixto/Otro'
    
    # Translate distribution types to Spanish
    if 'distributionFundType' in df.columns:
        dist_translations = {
            'Accumulation': 'Acumulación',
            'Distribution': 'Distribución',
            'Income': 'Reparto',
            'Acc': 'Acumulación',
            'Dist': 'Distribución'
        }
        df['distributionFundType'] = df['distributionFundType'].map(dist_translations).fillna(df['distributionFundType'])
    
    # Translate dividend frequency to Spanish
    if 'dividendDistributionFrequency' in df.columns:
        freq_translations = {
            'Annual': 'Anual',
            'Quarterly': 'Trimestral',
            'Monthly': 'Mensual',
            'Semi-Annual': 'Semestral',
            'None': 'Sin Distribución'
        }
        df['dividendDistributionFrequency'] = df['dividendDistributionFrequency'].map(freq_translations).fillna(df['dividendDistributionFrequency'])
    
    return df

# Column definitions with categories and Spanish translations
COLUMN_DEFINITIONS = {
    'Identificación': {
        'name': 'Nombre',
        'isin': 'ISIN',
        'fundID': 'ID Fondo',
        'firmName': 'Gestora',
        'domicile': 'Domicilio',
        'baseCurrency': 'Divisa',
        'primaryBenchmark': 'Índice Referencia'
    },
    'Clasificación': {
        'fund_type': 'Tipo de Fondo',
        'broadCategoryGroup': 'Categoría General',
        'morningstarCategory': 'Categoría Morningstar',
        'investmentType': 'Tipo de Inversión',
        'isIndexFund': 'Fondo Indexado',
        'isPrimaryShareClassInMarket': 'Clase Principal',
        'distributionFundType': 'Tipo Distribución',
        'dividendDistributionFrequency': 'Frecuencia Dividendos',
        'universe': 'Universo'
    },
    'Retornos': {
        'totalReturn_1d': 'Retorno 1 Día %',
        'totalReturn_1w': 'Retorno 1 Semana %',
        'totalReturn_1m': 'Retorno 1 Mes %',
        'totalReturn_2m': 'Retorno 2 Meses %',
        'totalReturn_3m': 'Retorno 3 Meses %',
        'totalReturn_6m': 'Retorno 6 Meses %',
        'totalReturn_9m': 'Retorno 9 Meses %',
        'totalReturn_1y': 'Retorno 1 Año %',
        'totalReturn_2y': 'Retorno 2 Años %',
        'totalReturn_3y': 'Retorno 3 Años %',
        'totalReturn_4y': 'Retorno 4 Años %',
        'totalReturn_5y': 'Retorno 5 Años %',
        'totalReturn_6y': 'Retorno 6 Años %',
        'totalReturn_7y': 'Retorno 7 Años %',
        'totalReturn_8y': 'Retorno 8 Años %',
        'totalReturn_9y': 'Retorno 9 Años %',
        'totalReturn_10y': 'Retorno 10 Años %',
        'totalReturn_15y': 'Retorno 15 Años %',
        'totalReturn_20y': 'Retorno 20 Años %',
        'totalReturn_ytd': 'Retorno YTD %',
        'totalReturn_qtd': 'Retorno Trimestre %'
    },
    'Riesgo': {
        'standardDeviation_1yMonthly': 'Volatilidad 1 Año %',
        'standardDeviation_3yMonthly': 'Volatilidad 3 Años %',
        'standardDeviation_5yMonthly': 'Volatilidad 5 Años %',
        'standardDeviation_10yMonthly': 'Volatilidad 10 Años %',
        'standardDeviation_15yMonthly': 'Volatilidad 15 Años %',
        'standardDeviation_20yMonthly': 'Volatilidad 20 Años %',
        'beta_1yMonthly': 'Beta 1 Año',
        'beta_3yMonthly': 'Beta 3 Años',
        'beta_5yMonthly': 'Beta 5 Años',
        'beta_10yMonthly': 'Beta 10 Años',
        'beta_15yMonthly': 'Beta 15 Años',
        'beta_20yMonthly': 'Beta 20 Años',
        'rSquared_3yMonthly': 'R-Cuadrado 3 Años',
        'rSquared_5yMonthly': 'R-Cuadrado 5 Años'
    },
    'Riesgo Ajustado': {
        'sharpeRatio_1yMonthly': 'Ratio Sharpe 1 Año',
        'sharpeRatio_3yMonthly': 'Ratio Sharpe 3 Años',
        'sharpeRatio_5yMonthly': 'Ratio Sharpe 5 Años',
        'sharpeRatio_10yMonthly': 'Ratio Sharpe 10 Años',
        'sharpeRatio_15yMonthly': 'Ratio Sharpe 15 Años',
        'sharpeRatio_20yMonthly': 'Ratio Sharpe 20 Años',
        'alpha_1yMonthly': 'Alpha 1 Año %',
        'alpha_3yMonthly': 'Alpha 3 Años %',
        'alpha_5yMonthly': 'Alpha 5 Años %',
        'alpha_10yMonthly': 'Alpha 10 Años %',
        'alpha_15yMonthly': 'Alpha 15 Años %',
        'alpha_20yMonthly': 'Alpha 20 Años %',
        'informationRatio_3y': 'Ratio Información 3 Años',
        'informationRatio_5y': 'Ratio Información 5 Años'
    },
    'Costes': {
        'ongoingCharge': 'Gastos Corrientes %',
        'maximumEntryCost': 'Comisión Entrada Máx %',
        'maximumExitCost': 'Comisión Salida Máx %',
        'maximumManagementFee': 'Comisión Gestión Máx %',
        'hasPerformanceFee': 'Comisión de Éxito'
    },
    'Ratings': {
        'fundStarRating_overall': '⭐ Rating General',
        'fundStarRating_3y': '⭐ Rating 3 Años',
        'fundStarRating_5y': '⭐ Rating 5 Años',
        'fundStarRating_10y': '⭐ Rating 10 Años',
        'sustainabilityRating': '🌱 Rating ESG',
        'morningstarRiskRating_overall': 'Rating Riesgo General',
        'morningstarRiskRating_3y': 'Rating Riesgo 3 Años',
        'morningstarRiskRating_5y': 'Rating Riesgo 5 Años',
        'morningstarRiskRating_10y': 'Rating Riesgo 10 Años',
        'medalistRating_overall': '🏅 Rating Analista',
        'corporateSustainabilityScore_environmental': 'ESG Medioambiental',
        'corporateSustainabilityScore_social': 'ESG Social',
        'corporateSustainabilityScore_governance': 'ESG Gobernanza',
        'corporateSustainabilityScore_total': 'ESG Total'
    },
    'Características': {
        'fundSize': 'Patrimonio Fondo €',
        'totalNetAssetsForShareClass': 'Patrimonio Clase €',
        'fund_age_years': 'Antigüedad (años)',
        'minimumInitialInvestment': 'Inversión Mínima €',
        'returnRankCategory_1y': 'Percentil Categoría 1 Año',
        'returnRankCategory_3y': 'Percentil Categoría 3 Años',
        'returnRankCategory_5y': 'Percentil Categoría 5 Años',
        'returnRankCategory_10y': 'Percentil Categoría 10 Años',
        'distributionYield': 'Rentabilidad por Dividendo %',
        'averageManagerTenure_fund': 'Antigüedad Gestor (años)',
        'averageManagerTenure_firm': 'Antigüedad en Gestora (años)',
        'inceptionDate': 'Fecha de Inicio'
    },
    'Estilos': {
        'fundEquityStyleBox': 'Estilo Renta Variable',
        'fundFixedIncomeStyleBox': 'Estilo Renta Fija',
        'fundAlternativeStyleBox': 'Estilo Alternativo'
    }
}

# Preset configurations
PRESET_CONFIGS = {
    'Básico': ['name', 'fund_type', 'isPrimaryShareClassInMarket', 'morningstarCategory', 
               'totalReturn_1y', 'sharpeRatio_3yMonthly', 'ongoingCharge', 'fundStarRating_overall'],
    
    'Performance': ['name', 'totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m',
                   'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 
                   'totalReturn_ytd', 'sharpeRatio_3yMonthly'],
    
    'Riesgo': ['name', 'standardDeviation_1yMonthly', 'standardDeviation_3yMonthly',
              'beta_3yMonthly', 'sharpeRatio_3yMonthly', 'alpha_3yMonthly',
              'morningstarRiskRating_overall'],
    
    'ESG': ['name', 'fund_type', 'sustainabilityRating', 'fundStarRating_overall',
           'totalReturn_1y', 'ongoingCharge'],
    
    'Distribución': ['name', 'distributionFundType', 'dividendDistributionFrequency', 
                    'distributionYield', 'totalReturn_1y', 'ongoingCharge', 
                    'fundSize', 'isPrimaryShareClassInMarket'],
    
    'Completo': ['name', 'fund_type', 'isPrimaryShareClassInMarket', 'morningstarCategory', 
                'totalReturn_1y', 'totalReturn_3y', 'sharpeRatio_3yMonthly', 
                'standardDeviation_3yMonthly', 'alpha_3yMonthly', 'beta_3yMonthly', 
                'ongoingCharge', 'fundSize', 'fundStarRating_overall', 'sustainabilityRating']
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

def create_configurable_heatmap(df, fund_names, metric_type='returns'):
    """Create a configurable heatmap for different metrics"""
    
    # Define metric groups
    metric_groups = {
        'returns': {
            'columns': ['totalReturn_1m', 'totalReturn_3m', 'totalReturn_6m', 
                       'totalReturn_1y', 'totalReturn_3y', 'totalReturn_5y', 'totalReturn_10y'],
            'labels': ['1M', '3M', '6M', '1A', '3A', '5A', '10A'],
            'title': 'Retornos por Período',
            'suffix': '%',
            'colorbar_title': 'Retorno (%)'
        },
        'risk': {
            'columns': ['standardDeviation_1yMonthly', 'standardDeviation_3yMonthly', 'standardDeviation_5yMonthly',
                       'beta_1yMonthly', 'beta_3yMonthly', 'beta_5yMonthly'],
            'labels': ['Vol 1A', 'Vol 3A', 'Vol 5A', 'Beta 1A', 'Beta 3A', 'Beta 5A'],
            'title': 'Métricas de Riesgo',
            'suffix': '',
            'colorbar_title': 'Valor'
        },
        'risk_adjusted': {
            'columns': ['sharpeRatio_1yMonthly', 'sharpeRatio_3yMonthly', 'sharpeRatio_5yMonthly',
                       'alpha_1yMonthly', 'alpha_3yMonthly', 'alpha_5yMonthly'],
            'labels': ['Sharpe 1A', 'Sharpe 3A', 'Sharpe 5A', 'Alpha 1A', 'Alpha 3A', 'Alpha 5A'],
            'title': 'Rendimiento Ajustado al Riesgo',
            'suffix': '',
            'colorbar_title': 'Valor'
        },
        'ratings': {
            'columns': ['fundStarRating_overall', 'fundStarRating_3y', 'fundStarRating_5y',
                       'sustainabilityRating', 'morningstarRiskRating_overall'],
            'labels': ['⭐ General', '⭐ 3A', '⭐ 5A', '🌱 ESG', 'Riesgo'],
            'title': 'Calificaciones',
            'suffix': '',
            'colorbar_title': 'Rating'
        },
        'costs': {
            'columns': ['ongoingCharge', 'maximumEntryCost', 'maximumExitCost'],
            'labels': ['Gastos Corrientes', 'Com. Entrada', 'Com. Salida'],
            'title': 'Estructura de Costes',
            'suffix': '%',
            'colorbar_title': 'Coste (%)'
        }
    }
    
    metric_config = metric_groups.get(metric_type, metric_groups['returns'])
    
    matrix = []
    fund_labels = []
    
    for fund_name in fund_names[:10]:
        fund_data = df[df['name'] == fund_name].iloc[0]
        values = [fund_data.get(col, np.nan) for col in metric_config['columns']]
        matrix.append(values)
        fund_labels.append(fund_name[:30] + '...' if len(fund_name) > 30 else fund_name)
    
    # Adjust colorscale based on metric type
    if metric_type == 'costs':
        colorscale = [
            [0.0, '#10b981'],
            [0.25, '#84cc16'],
            [0.5, '#fbbf24'],
            [0.75, '#f59e0b'],
            [1.0, '#ef4444']
        ]  # Inverted for costs (lower is better)
    else:
        colorscale = [
            [0.0, '#ef4444'],
            [0.25, '#f59e0b'],
            [0.5, '#fbbf24'],
            [0.75, '#84cc16'],
            [1.0, '#10b981']
        ]
    
    # Format text for display
    text_matrix = []
    for row in matrix:
        text_row = []
        for val in row:
            if pd.isna(val):
                text_row.append("N/D")
            elif metric_config['suffix']:
                text_row.append(f"{val:.1f}{metric_config['suffix']}")
            else:
                text_row.append(f"{val:.2f}")
        text_matrix.append(text_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=metric_config['labels'],
        y=fund_labels,
        colorscale=colorscale,
        text=text_matrix,
        texttemplate="%{text}",
        textfont={"size": 10},
        colorbar=dict(
            title=metric_config['colorbar_title'],
            thickness=15,
            len=0.7
        )
    ))
    
    fig.update_layout(
        title=f"Mapa de Calor - {metric_config['title']}",
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1f2e',
        font=dict(color='#fafafa'),
        height=400,
        xaxis=dict(title="Métrica", side="bottom"),
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
        
        # FILTROS SECTION with improved names and categories
        st.markdown("### 🎯 **Filtros Inteligentes** - *Define tus criterios de búsqueda*")
        
        # Quick filters in a clear box
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        
        # First row of filters
        filter_row1 = st.columns(5)
        
        with filter_row1[0]:
            # Broad Category Group filter
            if 'broadCategoryGroup' in df.columns:
                broad_categories = ['Todas'] + sorted(df['broadCategoryGroup'].dropna().unique().tolist())
            else:
                broad_categories = ['Todas']
            
            selected_broad_category = st.selectbox(
                "🏢 **Grupo Categoría**",
                options=broad_categories,
                help="Categoría amplia del fondo (Equity, Fixed Income, etc.)"
            )
        
        with filter_row1[1]:
            # Morningstar Category filter
            if 'morningstarCategory' in df.columns:
                # Filter categories based on selected broad category if applicable
                if selected_broad_category != 'Todas' and 'broadCategoryGroup' in df.columns:
                    filtered_cats_df = df[df['broadCategoryGroup'] == selected_broad_category]
                    categories = ['Todas'] + sorted(filtered_cats_df['morningstarCategory'].dropna().unique().tolist())
                else:
                    categories = ['Todas'] + sorted(df['morningstarCategory'].dropna().unique().tolist())
            else:
                categories = ['Todas']
            
            selected_category = st.selectbox(
                "📂 **Cat. Morningstar**",
                options=categories,
                help="Categoría específica según Morningstar"
            )
        
        with filter_row1[2]:
            selected_stars = st.selectbox(
                "⭐ **Rating**",
                options=['Todos', '⭐⭐⭐⭐⭐', '⭐⭐⭐⭐+', '⭐⭐⭐+', '⭐⭐+', '⭐+'],
                help="Calificación mínima del fondo"
            )
        
        with filter_row1[3]:
            selected_return_period = st.selectbox(
                "📊 **Período**",
                options=['1 Año', '3 Años', '5 Años', 'YTD'],
                help="Período para retornos"
            )
        
        with filter_row1[4]:
            return_options = {
                '1 Año': ['Todos', '> 20%', '> 10%', '> 5%', '> 0%', '< 0%'],
                '3 Años': ['Todos', '> 15%', '> 10%', '> 5%', '> 0%', '< 0%'],
                '5 Años': ['Todos', '> 10%', '> 7%', '> 5%', '> 0%', '< 0%'],
                'YTD': ['Todos', '> 15%', '> 10%', '> 5%', '> 0%', '< 0%']
            }
            selected_return = st.selectbox(
                f"📈 **Retorno**",
                options=return_options[selected_return_period],
                help=f"Filtro de retorno {selected_return_period}"
            )
        
        # Info banner showing current period for time-based metrics
        st.info(f"⏱️ **Período activo: {selected_return_period}** - Los filtros de Volatilidad, Sharpe y Alpha usan datos de este período")
        
        # Second row of filters
        filter_row2 = st.columns(4)
        
        with filter_row2[0]:
            return_options = {
                '1 Año': ['Todos', '> 20% 🚀', '> 15%', '> 10%', '> 5%', '> 0%', '0% a -5%', '< -5% ⚠️'],
                '3 Años': ['Todos', '> 15% 🚀', '> 10%', '> 5%', '> 0%', '< 0% ⚠️'],
                '5 Años': ['Todos', '> 10% 🚀', '> 7%', '> 5%', '> 0%', '< 0% ⚠️'],
                'YTD': ['Todos', '> 15% 🚀', '> 10%', '> 5%', '> 0%', '< 0% ⚠️']
            }
            selected_return = st.selectbox(
                f"📈 **Rendimiento ({selected_return_period})**",
                options=return_options[selected_return_period],
                help=f"Filtro de retorno para {selected_return_period}"
            )
        
        with filter_row2[0]:
            selected_expense = st.selectbox(
                "💰 **Comisiones Anuales**",
                options=['Todos', '< 0.25% 💎', '< 0.5%', '< 0.75%', '< 1%', '< 1.5%', '< 2%', '> 2% ⚠️'],
                help="Gastos corrientes del fondo"
            )
        
        with filter_row2[1]:
            selected_size = st.selectbox(
                "💼 **Patrimonio del Fondo**",
                options=['Todos', '> 1B€ 🏦', '> 500M€', '> 100M€', '> 50M€', '> 10M€', '> 5M€', '< 5M€ ⚠️'],
                help="Activos bajo gestión (AUM)"
            )
        
        with filter_row2[2]:
            selected_esg = st.selectbox(
                "🌍 **Sostenibilidad ESG**",
                options=['Todos', '🌿🌿🌿🌿🌿 Líder', '🌿🌿🌿🌿 Alto', '🌿🌿🌿 Medio', '🌿🌿 Básico', '🌿 Bajo'],
                help="Calificación de sostenibilidad"
            )
        
        with filter_row2[3]:
            selected_volatility = st.selectbox(
                "📉 **Nivel de Riesgo (Volatilidad)**",
                options=['Todos', '< 5% 🟢 Bajo', '< 10% 🟡', '< 15% 🟠', '< 20% 🔴', '> 20% ⚫ Muy Alto'],
                help="Volatilidad anual del fondo"
            )
        
        # Third row of filters
        filter_row3 = st.columns(4)
        
        with filter_row3[0]:
            selected_sharpe = st.selectbox(
                "🎯 **Ratio Sharpe (3A)**",
                options=['Todos', '> 2.0 💎 Excepcional', '> 1.5 Excelente', '> 1.0 Bueno', '> 0.5', '> 0', '< 0 ⚠️'],
                help="Retorno ajustado al riesgo"
            )
        
        with filter_row3[1]:
            selected_alpha = st.selectbox(
                "🔥 **Alpha (3A)**",
                options=['Todos', '> 5% 🚀', '> 3%', '> 1%', '> 0%', '< 0% ⚠️'],
                help="Exceso de retorno vs benchmark"
            )
        
        with filter_row3[2]:
            selected_age = st.selectbox(
                "⏳ **Antigüedad del Fondo**",
                options=['Todos', '> 10 años', '> 5 años', '> 3 años', '> 1 año', '< 1 año 🆕'],
                help="Años desde el inicio del fondo"
            )
        
        with filter_row3[3]:
            selected_index = st.selectbox(
                "🤖 **Tipo de Gestión**",
                options=['Todos', 'Gestión Activa', 'Gestión Pasiva (Indexado)'],
                help="Estrategia de gestión del fondo"
            )
        
        # Fourth row of filters for share class and distribution characteristics
        filter_row4 = st.columns(4)
        
        with filter_row4[0]:
            selected_share_class = st.selectbox(
                "🎯 **Clase**",
                options=['Todas', 'Solo Principales', 'Solo Secundarias'],
                help="Filtra por clase principal del fondo"
            )
        
        with filter_row4[1]:
            dist_types = ['Todos']
            if 'distributionFundType' in df.columns:
                dist_types += df['distributionFundType'].dropna().unique().tolist()
            selected_distribution = st.selectbox(
                "💵 **Distribución**",
                options=dist_types,
                help="Acumulación vs Distribución"
            )
        
        with filter_row4[2]:
            freq_options = ['Todas']
            if 'dividendDistributionFrequency' in df.columns:
                freq_options += df['dividendDistributionFrequency'].dropna().unique().tolist()
            selected_frequency = st.selectbox(
                "📅 **Dividendos**",
                options=freq_options,
                help="Frecuencia de reparto"
            )
        
        with filter_row4[3]:
            selected_min_investment = st.selectbox(
                "💸 **Inv. Mínima**",
                options=['Todos', '< 1K€', '< 10K€', '< 50K€', '< 100K€', '> 100K€'],
                help="Inversión inicial requerida"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply broad category group filter
        if selected_broad_category != 'Todas' and 'broadCategoryGroup' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['broadCategoryGroup'] == selected_broad_category]
        
        # Apply Morningstar category filter
        if selected_category != 'Todas' and 'morningstarCategory' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['morningstarCategory'] == selected_category]
        
        # Apply star rating filter
        if selected_stars != 'Todos' and 'fundStarRating_overall' in filtered_df.columns:
            star_map = {
                '⭐⭐⭐⭐⭐': 5,
                '⭐⭐⭐⭐+': 4,
                '⭐⭐⭐+': 3,
                '⭐⭐+': 2,
                '⭐+': 1
            }
            if selected_stars in star_map:
                filtered_df = filtered_df[
                    (filtered_df['fundStarRating_overall'] >= star_map[selected_stars]) |
                    filtered_df['fundStarRating_overall'].isna()
                ]
        
        # Apply return filter based on selected period
        return_col_map = {
            '1 Año': 'totalReturn_1y',
            '3 Años': 'totalReturn_3y',
            '5 Años': 'totalReturn_5y',
            'YTD': 'totalReturn_ytd'
        }
        
        # Map period to metric suffixes for other metrics
        period_suffix_map = {
            '1 Año': '_1yMonthly',
            '3 Años': '_3yMonthly',
            '5 Años': '_5yMonthly',
            'YTD': '_1yMonthly'  # Use 1Y metrics for YTD
        }
        
        return_col = return_col_map.get(selected_return_period, 'totalReturn_1y')
        period_suffix = period_suffix_map.get(selected_return_period, '_3yMonthly')
        
        if return_col in filtered_df.columns and selected_return != 'Todos':
            return_value = selected_return.split('%')[0].split('>')[-1].split('<')[-1].strip()
            
            if '>' in selected_return:
                threshold = float(return_value)
                filtered_df = filtered_df[filtered_df[return_col] > threshold]
            elif '<' in selected_return:
                threshold = float(return_value)
                filtered_df = filtered_df[filtered_df[return_col] < threshold]
            elif 'a' in selected_return:  # Range like "0% a -5%"
                parts = selected_return.split('a')
                upper = float(parts[0].replace('%', '').strip())
                lower = float(parts[1].split('%')[0].strip())
                filtered_df = filtered_df[(filtered_df[return_col] <= upper) & (filtered_df[return_col] >= lower)]
        
        # Apply expense filter
        if 'ongoingCharge' in filtered_df.columns and selected_expense != 'Todos':
            if '>' in selected_expense:
                filtered_df = filtered_df[filtered_df['ongoingCharge'] > 2]
            else:
                expense_value = float(selected_expense.split('%')[0].split('<')[1].strip())
                filtered_df = filtered_df[filtered_df['ongoingCharge'] < expense_value]
        
        # Apply size filter
        if 'fundSize' in filtered_df.columns and selected_size != 'Todos':
            size_map = {
                '> 1B€': 1e9,
                '> 500M€': 500e6,
                '> 100M€': 100e6,
                '> 50M€': 50e6,
                '> 10M€': 10e6,
                '< 10M€': -10e6
            }
            if selected_size in size_map:
                if '<' in selected_size:
                    filtered_df = filtered_df[filtered_df['fundSize'] < 10e6]
                else:
                    filtered_df = filtered_df[filtered_df['fundSize'] > size_map[selected_size]]
        
        # Apply ESG filter
        if 'sustainabilityRating' in filtered_df.columns and selected_esg != 'Todos':
            esg_map = {
                '5 🌿': 5,
                '4+ 🌿': 4,
                '3+ 🌿': 3,
                '2+ 🌿': 2,
                '1+ 🌿': 1
            }
            if selected_esg in esg_map:
                filtered_df = filtered_df[
                    (filtered_df['sustainabilityRating'] >= esg_map[selected_esg]) |
                    filtered_df['sustainabilityRating'].isna()
                ]
        
        # Apply volatility filter - NOW USING SELECTED PERIOD
        volatility_col = f'standardDeviation{period_suffix}'
        if volatility_col in filtered_df.columns and selected_volatility != 'Todos':
            vol_value = selected_volatility.split('%')[0].split('>')[-1].split('<')[-1].strip()
            if '>' in selected_volatility:
                filtered_df = filtered_df[filtered_df[volatility_col] > float(vol_value)]
            elif '<' in selected_volatility:
                filtered_df = filtered_df[filtered_df[volatility_col] < float(vol_value)]
        
        # Apply Sharpe filter - NOW USING SELECTED PERIOD
        sharpe_col = f'sharpeRatio{period_suffix}'
        if sharpe_col in filtered_df.columns and selected_sharpe != 'Todos':
            sharpe_value = selected_sharpe.split()[1] if '>' in selected_sharpe or '<' in selected_sharpe else selected_sharpe
            if '>' in selected_sharpe:
                threshold = float(sharpe_value)
                filtered_df = filtered_df[filtered_df[sharpe_col] > threshold]
            elif '<' in selected_sharpe:
                filtered_df = filtered_df[filtered_df[sharpe_col] < 0]
        
        # Apply Alpha filter - NOW USING SELECTED PERIOD
        alpha_col = f'alpha{period_suffix}'
        if alpha_col in filtered_df.columns and selected_alpha != 'Todos':
            alpha_value = selected_alpha.split('%')[0].split('>')[-1].split('<')[-1].strip()
            if '>' in selected_alpha:
                filtered_df = filtered_df[filtered_df[alpha_col] > float(alpha_value)]
            elif '<' in selected_alpha:
                filtered_df = filtered_df[filtered_df[alpha_col] < float(alpha_value)]
        
        # Apply age filter
        if 'fund_age_years' in filtered_df.columns and selected_age != 'Todos':
            age_map = {
                '> 10 años': 10,
                '> 5 años': 5,
                '> 3 años': 3,
                '> 1 año': 1,
                '< 1 año': -1
            }
            if selected_age in age_map:
                if '<' in selected_age:
                    filtered_df = filtered_df[filtered_df['fund_age_years'] < 1]
                else:
                    filtered_df = filtered_df[filtered_df['fund_age_years'] > age_map[selected_age]]
        
        # Apply management type filter
        if 'isIndexFund' in filtered_df.columns and selected_index != 'Todos':
            if selected_index == 'Pasiva (Indexado)':
                filtered_df = filtered_df[filtered_df['isIndexFund'] == True]
            else:
                filtered_df = filtered_df[filtered_df['isIndexFund'] == False]
        
        # Apply share class filter
        if 'isPrimaryShareClassInMarket' in filtered_df.columns and selected_share_class != 'Todas':
            if selected_share_class == 'Solo Principales':
                filtered_df = filtered_df[filtered_df['isPrimaryShareClassInMarket'] == True]
            else:  # Solo Secundarias
                filtered_df = filtered_df[filtered_df['isPrimaryShareClassInMarket'] == False]
        
        # Apply distribution type filter
        if 'distributionFundType' in filtered_df.columns and selected_distribution != 'Todos':
            filtered_df = filtered_df[filtered_df['distributionFundType'] == selected_distribution]
        
        # Apply dividend frequency filter
        if 'dividendDistributionFrequency' in filtered_df.columns and selected_frequency != 'Todas':
            filtered_df = filtered_df[filtered_df['dividendDistributionFrequency'] == selected_frequency]
        
        # Apply minimum investment filter
        if 'minimumInitialInvestment' in filtered_df.columns and selected_min_investment != 'Todos':
            if selected_min_investment == '< 1K€':
                filtered_df = filtered_df[filtered_df['minimumInitialInvestment'] < 1000]
            elif selected_min_investment == '< 10K€':
                filtered_df = filtered_df[filtered_df['minimumInitialInvestment'] < 10000]
            elif selected_min_investment == '< 50K€':
                filtered_df = filtered_df[filtered_df['minimumInitialInvestment'] < 50000]
            elif selected_min_investment == '< 100K€':
                filtered_df = filtered_df[filtered_df['minimumInitialInvestment'] < 100000]
            elif selected_min_investment == '> 100K€':
                filtered_df = filtered_df[filtered_df['minimumInitialInvestment'] >= 100000]
        
        st.markdown("---")
        
        # SORTING SECTION
        st.markdown("### 📊 **Ordenamiento de Resultados**")
        
        sort_cols = st.columns([3, 2, 2])
        
        with sort_cols[0]:
            # Get available columns for sorting with friendly names
            available_columns = filtered_df.columns.tolist()
            
            # Create friendly name mapping for sorting
            sort_translations = {}
            for category, cols in COLUMN_DEFINITIONS.items():
                for col_key, col_name in cols.items():
                    if col_key in available_columns:
                        sort_translations[col_name] = col_key
            
            # Prioritize common sorting options
            priority_options = [
                '📈 Retorno 1 Año %', 
                '📊 Retorno 3 Años %', 
                '💰 Retorno 5 Años %',
                '🎯 Ratio Sharpe 3 Años',
                '💼 Patrimonio Fondo €', 
                '💵 Gastos Corrientes %', 
                '⭐ Rating General',
                '🌱 Rating ESG', 
                '📉 Volatilidad 3 Años %', 
                '🔥 Alpha 3 Años %',
                '📊 Percentil Categoría 1 Año',
                '💎 Inversión Mínima €'
            ]
            
            # Map priority options to actual columns
            priority_mapping = {
                '📈 Retorno 1 Año %': 'totalReturn_1y',
                '📊 Retorno 3 Años %': 'totalReturn_3y',
                '💰 Retorno 5 Años %': 'totalReturn_5y',
                '🎯 Ratio Sharpe 3 Años': 'sharpeRatio_3yMonthly',
                '💼 Patrimonio Fondo €': 'fundSize',
                '💵 Gastos Corrientes %': 'ongoingCharge',
                '⭐ Rating General': 'fundStarRating_overall',
                '🌱 Rating ESG': 'sustainabilityRating',
                '📉 Volatilidad 3 Años %': 'standardDeviation_3yMonthly',
                '🔥 Alpha 3 Años %': 'alpha_3yMonthly',
                '📊 Percentil Categoría 1 Año': 'returnRankCategory_1y',
                '💎 Inversión Mínima €': 'minimumInitialInvestment'
            }
            
            # Build available sort options
            available_priority = [opt for opt in priority_options if priority_mapping.get(opt) in available_columns]
            
            # Add other columns with friendly names
            other_options = []
            for name, col in sort_translations.items():
                display_name = name
                if col not in priority_mapping.values():
                    other_options.append((display_name, col))
            
            # Combine all options
            all_sort_options = available_priority + [opt[0] for opt in other_options]
            
            selected_sort = st.selectbox(
                "🔽 Ordenar por",
                options=all_sort_options,
                index=0 if all_sort_options else None,
                help="Selecciona la columna para ordenar"
            )
            
            # Get actual column name for sorting
            if selected_sort:
                if selected_sort in priority_mapping:
                    sort_by = priority_mapping[selected_sort]
                else:
                    sort_by = sort_translations.get(selected_sort, selected_sort)
        
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
        st.markdown(f"### 📋 **Resultados del Screening** - *Top {min(num_results, len(sorted_df))} fondos*")
        
        # Prepare display dataframe
        display_cols = [col for col in selected_columns if col in sorted_df.columns]
        
        if display_cols:
            display_df = sorted_df[display_cols].copy()
            
            # Format columns
            for col in display_df.columns:
                if col == 'fundSize':
                    display_df[col] = display_df[col].apply(lambda x: format_number(x, 1, '€'))
                elif col == 'totalNetAssetsForShareClass':
                    display_df[col] = display_df[col].apply(lambda x: format_number(x, 1, '€'))
                elif col == 'minimumInitialInvestment':
                    display_df[col] = display_df[col].apply(lambda x: format_number(x, 0, '€'))
                elif 'totalReturn' in col or 'return' in col.lower():
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                elif 'distributionYield' in col:
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                elif 'ongoingCharge' in col or 'maximum' in col.lower():
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                elif any(metric in col.lower() for metric in ['sharpe', 'alpha', 'beta', 'standard']):
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/D")
                elif col in ['isIndexFund', 'hasPerformanceFee', 'isPrimaryShareClassInMarket']:
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
        st.markdown("### ⚖️ **Comparador Avanzado de Fondos**")
        
        # Fund selection
        if len(filtered_df) > 0:
            st.info("💡 Los fondos disponibles para comparar están basados en los filtros aplicados en el Screener")
            
            fund_names = sorted(filtered_df['name'].dropna().unique())
            
            selected_funds = st.multiselect(
                "📌 **Selecciona fondos para análisis comparativo** (máximo 10)",
                options=fund_names,
                max_selections=10,
                help="Elige hasta 10 fondos para comparación detallada"
            )
            
            if selected_funds:
                comparison_df = filtered_df[filtered_df['name'].isin(selected_funds)]
                
                # Configurable heatmap
                st.markdown("#### 🔥 **Mapa de Calor Configurable**")
                
                heatmap_col1, heatmap_col2 = st.columns([1, 3])
                
                with heatmap_col1:
                    heatmap_type = st.selectbox(
                        "📊 Tipo de Métrica",
                        options=[
                            ('📈 Retornos', 'returns'),
                            ('📉 Riesgo', 'risk'),
                            ('🎯 Riesgo Ajustado', 'risk_adjusted'),
                            ('⭐ Calificaciones', 'ratings'),
                            ('💰 Costes', 'costs')
                        ],
                        format_func=lambda x: x[0],
                        help="Selecciona qué métricas mostrar en el mapa de calor"
                    )
                
                with heatmap_col2:
                    fig = create_configurable_heatmap(filtered_df, selected_funds, heatmap_type[1])
                    st.plotly_chart(fig, use_container_width=True)
                
                # Enhanced comparison table with individual metric selection
                st.markdown("---")
                st.markdown("#### 📊 **Tabla Comparativa Personalizada**")
                
                # Create list of all available metrics with friendly names
                all_metrics = []
                metric_mapping = {}
                
                for category, cols in COLUMN_DEFINITIONS.items():
                    for col_key, col_name in cols.items():
                        if col_key in comparison_df.columns and col_key != 'name':
                            display_name = f"{category} - {col_name}"
                            all_metrics.append(display_name)
                            metric_mapping[display_name] = col_key
                
                # Default selection
                default_metrics = [
                    'Retornos - 1 Año %',
                    'Retornos - 3 Años %',
                    'Riesgo Ajustado - Sharpe 3A',
                    'Riesgo - Vol 3A %',
                    'Costes - Gastos %',
                    'Ratings - ⭐ Rating'
                ]
                
                available_defaults = [m for m in default_metrics if m in all_metrics]
                
                selected_metrics = st.multiselect(
                    "Selecciona métricas específicas para comparar (máximo 20)",
                    options=all_metrics,
                    default=available_defaults[:10] if available_defaults else all_metrics[:10],
                    max_selections=20,
                    help="Elige hasta 20 métricas para la tabla comparativa"
                )
                
                if selected_metrics:
                    # Build comparison dataframe with selected metrics
                    comparison_metrics = ['name'] + [metric_mapping[m] for m in selected_metrics]
                    comp_display = comparison_df[comparison_metrics].copy()
                    
                    # Format values for display
                    for col in comp_display.columns:
                        if col == 'name':
                            continue
                        elif col == 'fundSize':
                            comp_display[col] = comp_display[col].apply(lambda x: format_number(x, 1, '€'))
                        elif col == 'totalNetAssetsForShareClass':
                            comp_display[col] = comp_display[col].apply(lambda x: format_number(x, 1, '€'))
                        elif col == 'minimumInitialInvestment':
                            comp_display[col] = comp_display[col].apply(lambda x: format_number(x, 0, '€'))
                        elif 'totalReturn' in col or 'return' in col.lower():
                            comp_display[col] = comp_display[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                        elif 'distributionYield' in col:
                            comp_display[col] = comp_display[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                        elif 'ongoingCharge' in col or 'maximum' in col.lower():
                            comp_display[col] = comp_display[col].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else "N/D")
                        elif any(metric in col.lower() for metric in ['sharpe', 'alpha', 'beta', 'standard']):
                            comp_display[col] = comp_display[col].apply(lambda x: f"{x:.2f}" if not pd.isna(x) else "N/D")
                        elif col in ['isIndexFund', 'hasPerformanceFee', 'isPrimaryShareClassInMarket']:
                            comp_display[col] = comp_display[col].apply(lambda x: '✓' if x else '✗' if not pd.isna(x) else "N/D")
                        elif 'Rating' in col or 'rating' in col:
                            comp_display[col] = comp_display[col].apply(lambda x: f"{x:.0f}" if not pd.isna(x) else "N/D")
                    
                    # Transpose for comparison view
                    comp_display = comp_display.set_index('name').T
                    
                    # Apply friendly names to index
                    index_translations = {}
                    for metric_name, col_key in metric_mapping.items():
                        if col_key in comp_display.index:
                            index_translations[col_key] = metric_name.split(' - ')[1]
                    
                    comp_display.index = comp_display.index.map(lambda x: index_translations.get(x, x))
                    
                    # Display with styling
                    st.dataframe(
                        comp_display,
                        use_container_width=True,
                        height=min(400, 50 + len(comp_display) * 35)
                    )
                    
                    # Export comparison button
                    csv = comp_display.to_csv()
                    st.download_button(
                        label="📥 Descargar Comparación CSV",
                        data=csv,
                        file_name=f"comparacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                # Scatter plot configuration
                st.markdown("---")
                st.markdown("#### 📈 **Análisis Visual Personalizado**")
                
                # Get numeric columns for scatter plot with friendly names
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
                
                # Create friendly names for scatter plot axes
                scatter_options = {}
                for col in numeric_cols:
                    for category, cols in COLUMN_DEFINITIONS.items():
                        if col in cols:
                            scatter_options[f"{cols[col]} ({category})"] = col
                            break
                    else:
                        scatter_options[col] = col
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    x_axis_display = st.selectbox(
                        "📊 Eje X (Horizontal)",
                        options=list(scatter_options.keys()),
                        index=list(scatter_options.values()).index('standardDeviation_3yMonthly') 
                            if 'standardDeviation_3yMonthly' in scatter_options.values() else 0,
                        help="Variable para el eje horizontal"
                    )
                    x_axis = scatter_options[x_axis_display]
                
                with col2:
                    y_axis_display = st.selectbox(
                        "📈 Eje Y (Vertical)",
                        options=list(scatter_options.keys()),
                        index=list(scatter_options.values()).index('totalReturn_3y') 
                            if 'totalReturn_3y' in scatter_options.values() else 0,
                        help="Variable para el eje vertical"
                    )
                    y_axis = scatter_options[y_axis_display]
                
                with col3:
                    size_options = {'Ninguno': None}
                    size_options.update(scatter_options)
                    
                    size_var_display = st.selectbox(
                        "⭕ Tamaño de burbuja",
                        options=list(size_options.keys()),
                        index=list(size_options.values()).index('fundSize') 
                            if 'fundSize' in size_options.values() else 0,
                        help="Variable para determinar el tamaño"
                    )
                    size_var = size_options[size_var_display]
                
                # Create scatter plot
                if x_axis and y_axis:
                    scatter_data = filtered_df.dropna(subset=[x_axis, y_axis]).copy()
                    
                    # Handle size variable - ensure positive values for Plotly
                    if size_var:
                        scatter_data[size_var] = scatter_data[size_var].fillna(scatter_data[size_var].median())
                        # Ensure all size values are positive
                        min_size = scatter_data[size_var].min()
                        if min_size < 0:
                            # Shift all values to be positive, maintaining relative differences
                            scatter_data[f'{size_var}_size'] = scatter_data[size_var] - min_size + 1
                            size_col = f'{size_var}_size'
                        else:
                            # Add small offset to avoid zero sizes
                            scatter_data[f'{size_var}_size'] = scatter_data[size_var] + 0.1
                            size_col = f'{size_var}_size'
                    else:
                        size_col = None
                    
                    # Create scatter plot with safe fund_type handling
                    color_col = 'fund_type' if 'fund_type' in scatter_data.columns else None
                    
                    if color_col:
                        color_map = {
                            'Renta Variable': '#3b82f6',
                            'Renta Fija': '#10b981',
                            'Alternativo': '#f59e0b',
                            'Mixto/Otro': '#8b5cf6'
                        }
                    else:
                        color_map = None
                    
                    fig = px.scatter(
                        scatter_data,
                        x=x_axis,
                        y=y_axis,
                        color=color_col,
                        size=size_col if size_col else None,
                        hover_data=['name', 'firmName', 'morningstarCategory'],
                        title=f"Análisis: {y_axis_display} vs {x_axis_display}",
                        color_discrete_map=color_map
                    )
                    
                    # Add median lines
                    x_median = scatter_data[x_axis].median()
                    y_median = scatter_data[y_axis].median()
                    
                    fig.add_hline(y=y_median, line_dash="dash", line_color="gray", opacity=0.5)
                    fig.add_vline(x=x_median, line_dash="dash", line_color="gray", opacity=0.5)
                    
                    # Add quadrant labels
                    fig.add_annotation(x=scatter_data[x_axis].max(), y=scatter_data[y_axis].max(),
                                     text="Alto/Alto", showarrow=False,
                                     xanchor="right", yanchor="top", opacity=0.3)
                    fig.add_annotation(x=scatter_data[x_axis].min(), y=scatter_data[y_axis].max(),
                                     text="Bajo/Alto", showarrow=False,
                                     xanchor="left", yanchor="top", opacity=0.3)
                    fig.add_annotation(x=scatter_data[x_axis].max(), y=scatter_data[y_axis].min(),
                                     text="Alto/Bajo", showarrow=False,
                                     xanchor="right", yanchor="bottom", opacity=0.3)
                    fig.add_annotation(x=scatter_data[x_axis].min(), y=scatter_data[y_axis].min(),
                                     text="Bajo/Bajo", showarrow=False,
                                     xanchor="left", yanchor="bottom", opacity=0.3)
                    
                    # Highlight selected funds
                    if selected_funds:
                        selected_data = scatter_data[scatter_data['name'].isin(selected_funds)]
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
                            hovertemplate='<b>%{text}</b><extra></extra>',
                            text=selected_data['name']
                        ))
                    
                    fig.update_layout(
                        paper_bgcolor='#0e1117',
                        plot_bgcolor='#1a1f2e',
                        font=dict(color='#fafafa'),
                        height=600,
                        xaxis=dict(gridcolor='#2d3748', zeroline=False, title=x_axis_display),
                        yaxis=dict(gridcolor='#2d3748', zeroline=False, title=y_axis_display)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👆 Selecciona fondos arriba para comenzar la comparación")
        else:
            st.warning("⚠️ Aplica filtros primero en la pestaña SCREENER para ver fondos disponibles")
    
    with main_tabs[2]:  # GUIDE TAB
        st.markdown("### 📖 **Guía Completa de Uso**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🔍 **Cómo usar el Screener**
            
            1. **Configura la Vista**: Elige qué columnas quieres ver
            2. **Aplica Filtros Inteligentes**: 
               - Categoría de inversión (tipo de activo)
               - Categoría Morningstar (clasificación específica)
               - Calidad del fondo (rating estrellas)
               - Rendimientos por período
               - Comisiones y gastos
               - Patrimonio del fondo
               - Sostenibilidad ESG
               - Nivel de riesgo
               - Métricas avanzadas (Sharpe, Alpha)
               - Clases y distribución
            3. **Ordena Resultados**: Por cualquier métrica
            4. **Exporta**: Descarga en formato CSV
            
            #### 📊 **Métricas Clave Explicadas**
            
            - **Retorno**: Rendimiento anualizado del período
            - **Sharpe Ratio**: Retorno ajustado al riesgo (>1 es bueno, >2 excelente)
            - **Alpha**: Exceso de retorno vs benchmark (positivo = supera al mercado)
            - **Beta**: Sensibilidad al mercado (1 = igual que el mercado)
            - **Volatilidad**: Desviación estándar de retornos (menor = más estable)
            - **Gastos**: Costes anuales totales del fondo
            - **ESG**: Calificación de sostenibilidad (1-5 hojas)
            """)
        
        with col2:
            st.markdown("""
            #### ⚡ **Filtros Avanzados**
            
            **Rendimiento por Período:**
            - Analiza retornos a 1, 3, 5 años o YTD
            - Múltiples rangos de rendimiento
            
            **Calidad y Riesgo:**
            - Rating Morningstar (1-5 estrellas)
            - Volatilidad en rangos específicos
            - Sharpe Ratio para retorno ajustado
            - Alpha para exceso de retorno
            
            **Costes y Tamaño:**
            - Comisiones desde ultra-bajas (<0.25%) hasta altas
            - Patrimonio desde pequeños hasta mega fondos (>1B€)
            - Inversión mínima requerida
            
            **Clases y Distribución:**
            - **Clase Principal**: Filtra solo las clases principales
            - **Tipo Distribución**: Acumulación vs Distribución
            - **Frecuencia Dividendos**: Anual, Trimestral, etc.
            
            #### 💡 **Consejos Profesionales**
            
            - **Clases Principales**: Usa el filtro para ver solo las clases más líquidas
            - **Para conservadores**: Busca Volatilidad <10%, Sharpe >1
            - **Para rentas**: Selecciona tipo Distribución con frecuencia deseada
            - **Para agresivos**: Alpha >3%, acepta mayor volatilidad
            - **Fondos eficientes**: Gastos <1% para RV, <0.5% para RF
            - **Liquidez**: Prefiere AUM >50M€ y clases principales
            - **Sostenibles**: ESG ≥4 hojas
            - **Track record**: Antigüedad >3 años
            - **Comparación justa**: Compara fondos de la misma categoría
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px; 
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    border-radius: 16px; margin-top: 20px;'>
            <p style='color: #8b949e; font-size: 0.9em;'>
                44,341 fondos | 96 métricas | Análisis profesional
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
