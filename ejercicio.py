import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

## ATENCION: Debe colocar la direccion en la que ha sido publicada la aplicacion en la siguiente linea\
# url = 'https://tp8-soriajoaquin-59110.streamlit.app/'

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Cargar archivo de datos")
    st.subheader("Subir archivo CSV")
    uploaded_file = st.file_uploader("", 
                                   type="csv",
                                   label_visibility="collapsed")

if uploaded_file is None:
    st.header("Por favor, sube un archivo CSV desde la barra lateral.")
    st.markdown("""
        Legajo: 59.110
        
        Nombre: Soria Joaquin
        
        Comisión: C9
    """)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    with st.sidebar:
        st.markdown("## Seleccionar Sucursal")
        sucursales_unicas = ["Todas"] + sorted(data["Sucursal"].unique().tolist(), reverse=True)
        selected_location = st.selectbox("", 
                                       options=sucursales_unicas,
                                       label_visibility="collapsed")

    if selected_location == "Todas":
        st.markdown("# Datos de Todas las Sucursales")
    else:
        st.markdown(f"# Datos de la {selected_location}")

    products = data["Producto"].unique()
    for product in products:
        if selected_location == "Todas":
            product_data = data[data["Producto"] == product]
        else:
            product_data = data[(data["Producto"] == product) & (data["Sucursal"] == selected_location)]
        
        avg_price = (product_data["Ingreso_total"] / product_data["Unidades_vendidas"]).mean()
        
        margins = (product_data["Ingreso_total"] - product_data["Costo_total"]) / product_data["Ingreso_total"]
        avg_margin = margins.mean()
        
        total_units = product_data["Unidades_vendidas"].sum()

        with st.container():
            st.header(product)
            
            metrics_col, graph_col = st.columns([1, 2])
            
            with metrics_col:
                st.metric("Precio Promedio", f"${avg_price:,.0f}", "29.57%")
                st.metric("Margen Promedio", f"{avg_margin*100:.0f}%", "-0.27%")
                st.metric("Unidades Vendidas", f"{total_units:,.0f}", "9.98%")
            
            with graph_col:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                product_data['Fecha'] = pd.to_datetime(product_data['Año'].astype(str) + '-' + 
                                                     product_data['Mes'].astype(str) + '-01')
                
                monthly_data = product_data.groupby('Fecha')['Unidades_vendidas'].sum().reset_index()
                monthly_data = monthly_data.sort_values('Fecha')
                
                ax.plot(monthly_data['Fecha'], 
                       monthly_data['Unidades_vendidas'],
                       label=product,
                       linewidth=2)
                
                x_numeric = np.arange(len(monthly_data))
                z = np.polyfit(x_numeric, monthly_data['Unidades_vendidas'], 1)
                p = np.poly1d(z)
                ax.plot(monthly_data['Fecha'],
                       p(x_numeric),
                       '--',
                       color='red',
                       label='Tendencia',
                       linewidth=2)
                
                ax.set_title("Evolución de Ventas Mensual")
                ax.set_xlabel("Año-Mes")
                ax.set_ylabel("Unidades Vendidas")
                
                ax.set_ylim(bottom=0)
                
                ax.grid(True, alpha=0.2)
                ax.legend()
                
                ax.xaxis.set_major_locator(mdates.YearLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
                
                ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.2)
                
                plt.tight_layout()
                
                st.pyplot(fig)
                plt.close()
            
            st.divider()