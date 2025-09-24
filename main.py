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
        
        # FILTROS SECTION with improved names and categories
        st.markdown("### 🎯 **Filtros Inteligentes** - *Define tus criterios de búsqueda*")
        
        # Quick filters in a clear box
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        
        # First row of filters
        filter_row1 = st.columns(4)
        
        with filter_row1[0]:
            fund_types_available = ['Todos'] + df['fund_type'].dropna().unique().tolist()
            selected_fund_type = st.selectbox(
                "💼 **Categoría de Inversión**",
                options=fund_types_available,
                help="Tipo de activo del fondo"
            )
        
        with filter_row1[1]:
            selected_stars = st.selectbox(
                "⭐ **Calidad del Fondo**",
                options=['Todos', '⭐⭐⭐⭐⭐ Excelente', '⭐⭐⭐⭐ Muy Bueno', '⭐⭐⭐ Bueno', '⭐⭐ Regular', '⭐ Bajo'],
                help="Calificación Morningstar del fondo"
            )
        
        with filter_row1[2]:
            selected_return_period = st.selectbox(
                "📊 **Período de Retorno**",
                options=['1 Año', '3 Años', '5 Años', 'YTD'],
                help="Período para evaluar retornos"
            )
        
        with filter_row1[3]:
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
        
        # Second row of filters
        filter_row2 = st.columns(4)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_df = df.copy()
        
        # Apply fund type filter
        if selected_fund_type != 'Todos':
            filtered_df = filtered_df[filtered_df['fund_type'] == selected_fund_type]
        
        # Apply star rating filter
        if selected_stars != 'Todos' and 'fundStarRating_overall' in filtered_df.columns:
            star_map = {
                '⭐⭐⭐⭐⭐ Excelente': 5,
                '⭐⭐⭐⭐ Muy Bueno': 4,
                '⭐⭐⭐ Bueno': 3,
                '⭐⭐ Regular': 2,
                '⭐ Bajo': 1
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
        
        return_col = return_col_map.get(selected_return_period, 'totalReturn_1y')
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
                '> 1B€ 🏦': 1e9,
                '> 500M€': 500e6,
                '> 100M€': 100e6,
                '> 50M€': 50e6,
                '> 10M€': 10e6,
                '> 5M€': 5e6,
                '< 5M€ ⚠️': -5e6
            }
            if selected_size in size_map:
                if '<' in selected_size:
                    filtered_df = filtered_df[filtered_df['fundSize'] < 5e6]
                else:
                    filtered_df = filtered_df[filtered_df['fundSize'] > size_map[selected_size]]
        
        # Apply ESG filter
        if 'sustainabilityRating' in filtered_df.columns and selected_esg != 'Todos':
            esg_map = {
                '🌿🌿🌿🌿🌿 Líder': 5,
                '🌿🌿🌿🌿 Alto': 4,
                '🌿🌿🌿 Medio': 3,
                '🌿🌿 Básico': 2,
                '🌿 Bajo': 1
            }
            if selected_esg in esg_map:
                filtered_df = filtered_df[
                    (filtered_df['sustainabilityRating'] >= esg_map[selected_esg]) |
                    filtered_df['sustainabilityRating'].isna()
                ]
        
        # Apply volatility filter
        if 'standardDeviation_3yMonthly' in filtered_df.columns and selected_volatility != 'Todos':
            vol_value = selected_volatility.split('%')[0].split('>')[-1].split('<')[-1].strip()
            if '>' in selected_volatility:
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] > float(vol_value)]
            elif '<' in selected_volatility:
                filtered_df = filtered_df[filtered_df['standardDeviation_3yMonthly'] < float(vol_value)]
        
        # Apply Sharpe filter
        if 'sharpeRatio_3yMonthly' in filtered_df.columns and selected_sharpe != 'Todos':
            sharpe_value = selected_sharpe.split()[1] if '>' in selected_sharpe else selected_sharpe.split()[0]
            if '>' in selected_sharpe:
                threshold = float(sharpe_value)
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] > threshold]
            elif '<' in selected_sharpe:
                filtered_df = filtered_df[filtered_df['sharpeRatio_3yMonthly'] < 0]
        
        # Apply Alpha filter
        if 'alpha_3yMonthly' in filtered_df.columns and selected_alpha != 'Todos':
            alpha_value = selected_alpha.split('%')[0].split('>')[-1].split('<')[-1].strip()
            if '>' in selected_alpha:
                filtered_df = filtered_df[filtered_df['alpha_3yMonthly'] > float(alpha_value)]
            elif '<' in selected_alpha:
                filtered_df = filtered_df[filtered_df['alpha_3yMonthly'] < float(alpha_value)]
        
        # Apply age filter
        if 'fund_age_years' in filtered_df.columns and selected_age != 'Todos':
            age_map = {
                '> 10 años': 10,
                '> 5 años': 5,
                '> 3 años': 3,
                '> 1 año': 1,
                '< 1 año 🆕': -1
            }
            if selected_age in age_map:
                if '<' in selected_age:
                    filtered_df = filtered_df[filtered_df['fund_age_years'] < 1]
                else:
                    filtered_df = filtered_df[filtered_df['fund_age_years'] > age_map[selected_age]]
        
        # Apply management type filter
        if 'isIndexFund' in filtered_df.columns and selected_index != 'Todos':
            if selected_index == 'Gestión Pasiva (Indexado)':
                filtered_df = filtered_df[filtered_df['isIndexFund'] == True]
            else:
                filtered_df = filtered_df[filtered_df['isIndexFund'] == False]
        
        st.markdown("---")
        
        # SORTING SECTION
        st.markdown("### 📊 **Ordenamiento de Resultados**")
        
        sort_cols = st.columns([3, 2, 2])
        
        with sort_cols[0]:
            # Get available columns for sorting
            available_columns = filtered_df.columns.tolist()
            
            # Prioritize common sorting columns
            priority_cols = ['totalReturn_1y', 'totalReturn_3y', 'sharpeRatio_3yMonthly', 
                           'fundSize', 'ongoingCharge', 'fundStarRating_overall']
            available_priority = [col for col in priority_cols if col in available_columns]
            other_cols = [col for col in available_columns if col not in priority_cols]
            
            sort_options = available_priority + other_cols
            
            sort_by = st.selectbox(
                "🔽 Ordenar por",
                options=sort_options,
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
        st.markdown(f"### 📋 **Resultados del Screening** - *Top {min(num_results, len(sorted_df))} fondos*")
        
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
                
                # Heatmap of returns
                st.markdown("#### 🔥 **Mapa de Calor - Rendimientos Históricos**")
                fig = create_performance_heatmap(filtered_df, selected_funds)
                st.plotly_chart(fig, use_container_width=True)
                
                # Comparison table
                st.markdown("#### 📊 **Tabla Comparativa Detallada**")
                
                # Select metrics to compare
                categories_to_compare = st.multiselect(
                    "Selecciona categorías de métricas para comparar",
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
                st.markdown("#### 📈 **Análisis Visual Personalizado**")
                
                # Get numeric columns for scatter plot
                numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    x_axis = st.selectbox(
                        "📊 Eje X (Horizontal)",
                        options=numeric_cols,
                        index=numeric_cols.index('standardDeviation_3yMonthly') 
                            if 'standardDeviation_3yMonthly' in numeric_cols else 0,
                        help="Variable para el eje horizontal"
                    )
                
                with col2:
                    y_axis = st.selectbox(
                        "📈 Eje Y (Vertical)",
                        options=numeric_cols,
                        index=numeric_cols.index('totalReturn_3y') 
                            if 'totalReturn_3y' in numeric_cols else 0,
                        help="Variable para el eje vertical"
                    )
                
                with col3:
                    size_var = st.selectbox(
                        "⭕ Tamaño de burbuja",
                        options=['None'] + numeric_cols,
                        index=numeric_cols.index('fundSize') + 1 
                            if 'fundSize' in numeric_cols else 0,
                        help="Variable para determinar el tamaño"
                    )
                
                # Create scatter plot
                if x_axis and y_axis:
                    scatter_data = filtered_df.dropna(subset=[x_axis, y_axis]).copy()
                    
                    # Handle size variable
                    if size_var != 'None':
                        scatter_data[size_var] = scatter_data[size_var].fillna(scatter_data[size_var].median())
                        size_col = size_var
                    else:
                        size_col = None
                    
                    fig = px.scatter(
                        scatter_data,
                        x=x_axis,
                        y=y_axis,
                        color='fund_type',
                        size=size_col if size_col else None,
                        hover_data=['name', 'firmName', 'morningstarCategory'],
                        title=f"Análisis: {y_axis} vs {x_axis}",
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
                    
                    fig.add_hline(y=y_median, line_dash="dash", line_color="gray", opacity=0.5)
                    fig.add_vline(x=x_median, line_dash="dash", line_color="gray", opacity=0.5)
                    
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
                        xaxis=dict(gridcolor='#2d3748', zeroline=False),
                        yaxis=dict(gridcolor='#2d3748', zeroline=False)
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
               - Categoría de inversión
               - Calidad del fondo
               - Rendimientos por período
               - Comisiones y gastos
               - Patrimonio del fondo
               - Sostenibilidad ESG
               - Nivel de riesgo
               - Métricas avanzadas (Sharpe, Alpha)
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
            
            **Costes y Tamaño:**
            - Comisiones desde ultra-bajas (<0.25%) hasta altas
            - Patrimonio desde pequeños hasta mega fondos (>1B€)
            
            #### 💡 **Consejos Profesionales**
            
            - **Para conservadores**: Busca Volatilidad <10%, Sharpe >1
            - **Para agresivos**: Alpha >3%, acepta mayor volatilidad
            - **Fondos eficientes**: Gastos <1% para RV, <0.5% para RF
            - **Liquidez**: Prefiere AUM >50M€
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
