import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

## ATENCION: Debe colocar la direccion en la que ha sido publicada la aplicacion en la siguiente linea\
# url = 'https://tp8-555555.streamlit.app/'

# Configuración de la página
st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    st.header("Cargar archivo de datos")
    st.subheader("Subir archivo CSV")
    uploaded_file = st.file_uploader("", 
                                   type="csv",
                                   label_visibility="collapsed")

# Contenido principal - solo se muestra si no hay archivo cargado
if uploaded_file is None:
    st.header("Por favor, sube un archivo CSV desde la barra lateral.")
    st.markdown("""
        Legajo: 59.110
        
        Nombre: Soria Joaquin
        
        Comisión: C9
    """)

# Procesar datos si se carga un archivo
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    with st.sidebar:
        st.markdown("## Seleccionar Sucursal")
        sucursales_unicas = ["Todas"] + sorted(data["Sucursal"].unique().tolist(), reverse=True)
        selected_location = st.selectbox("", 
                                       options=sucursales_unicas,
                                       label_visibility="collapsed")

    # Main dashboard area
    if selected_location == "Todas":
        st.markdown("# Datos de Todas las Sucursales")
    else:
        st.markdown(f"# Datos de la {selected_location}")

    # Calculate metrics for each product
    products = data["Producto"].unique()
    for product in products:
        # Cálculos de métricas
        if selected_location == "Todas":
            product_data = data[data["Producto"] == product]
        else:
            product_data = data[(data["Producto"] == product) & (data["Sucursal"] == selected_location)]
        
        avg_price = product_data["Ingreso_total"].sum() / product_data["Unidades_vendidas"].sum()
        avg_margin = (product_data["Ingreso_total"].sum() - product_data["Costo_total"].sum()) / product_data["Ingreso_total"].sum()
        total_units = product_data["Unidades_vendidas"].sum()

        # Contenedor principal para cada producto
        with st.container():
            st.header(product)
            
            # Crear dos columnas: métricas y gráfico
            metrics_col, graph_col = st.columns([1, 2])
            
            # Columna de métricas
            with metrics_col:
                st.metric("Precio Promedio", f"${avg_price:,.3f}", "29.57%")
                st.metric("Margen Promedio", f"{avg_margin*100:.0f}%", "-0.27%")
                st.metric("Unidades Vendidas", f"{total_units:,.0f}", "9.98%")
            
            # Columna del gráfico
            with graph_col:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Crear fecha combinando año y mes
                product_data['Fecha'] = pd.to_datetime(product_data['Año'].astype(str) + '-' + 
                                                     product_data['Mes'].astype(str) + '-01')
                
                # Agrupar por fecha y calcular la suma de unidades vendidas
                monthly_data = product_data.groupby('Fecha')['Unidades_vendidas'].sum().reset_index()
                monthly_data = monthly_data.sort_values('Fecha')
                
                # Graficar datos
                ax.plot(monthly_data['Fecha'], 
                       monthly_data['Unidades_vendidas'],
                       label=product,
                       linewidth=2)
                
                # Línea de tendencia
                x_numeric = np.arange(len(monthly_data))
                z = np.polyfit(x_numeric, monthly_data['Unidades_vendidas'], 1)
                p = np.poly1d(z)
                ax.plot(monthly_data['Fecha'],
                       p(x_numeric),
                       '--',
                       color='red',
                       label='Tendencia',
                       linewidth=2)
                
                # Configuración del gráfico
                ax.set_title("Evolución de Ventas Mensual")
                ax.set_xlabel("Año-Mes")
                ax.set_ylabel("Unidades Vendidas")
                
                # Asegurar que el eje Y comience en 0
                ax.set_ylim(bottom=0)
                
                # Agregar cuadrícula
                ax.grid(True, alpha=0.2)
                ax.legend()
                
                # Formatear eje X para mostrar años
                ax.xaxis.set_major_locator(mdates.YearLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                
                # Agregar líneas de cuadrícula verticales para los años
                ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.2)
                
                # Ajustar márgenes
                plt.tight_layout()
                
                # Mostrar gráfico
                st.pyplot(fig)
                plt.close()
            
            # Separador entre productos
            st.divider()