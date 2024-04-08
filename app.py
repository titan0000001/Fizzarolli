#IMPORTACIONES

import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image

# Importaciones para análisis exploratorio de datos (EDA)
import pandas as pd
import numpy as np

# Importaciones para visualización de datos
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


#FUNCIONES
#Funcion para nuestra animacion
def load_lottieurl(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  return r.json()

#globales
#ANIMACION DEL INICIO
lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_0yfsb3a1.json")
st.set_page_config(
    page_title="Fizzarolli",    
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 5%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 5%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

#DATA
data_pm = pd.read_csv('pm_cleaned.csv')
data_dem = pd.read_csv('demolicion_cleaned.csv')
data_rcd = pd.read_csv('residuosdeconstruccionydemolicion_rcd_2021(cleaned).csv')
data_pesos = pd.read_csv('registro-gral.-de-pesos-residuos-siremu(cleaned) (1).csv')
data_temp = pd.read_excel('limpio_ bolivia-temperatura-media-por-principales-ciudades-1990-2022.xlsx')
data_temp['LA PAZ'] = data_temp['LA PAZ'].fillna(data_temp['LA PAZ'].mean())
average_temp_by_year = data_temp.groupby('AÑO')['LA PAZ'].mean()
colors = plt.cm.viridis(np.linspace(0, 1, len(average_temp_by_year)))
data_co = pd.read_excel('limpio_concent_2019-22.xlsx')


#VISUALIZACIONES

data_pm_limited = data_pm.iloc[3828:]
pm_rcd = px.line(data_pm_limited, x='FECHA', y='PM 10', labels={'PM 10': 'PM 10'})
pm_rcd.add_scatter(x=data_dem['FECHA'], y=data_dem['TOTAL m3'], mode='lines', name='TOTAL m3', line=dict(dash='dash'))
pm_rcd.update_layout(title='Comportamiento de PM 10 y TOTAL m3 a lo largo del tiempo', xaxis_title='Fecha', yaxis_title='Valor')


v_instituciones_residuos = px.bar(data_rcd, x='NOMBRE/INSTITUCIÓN',
             labels={'Suma': 'Suma de Valores', 'Variable': 'Variables'},
             title='Suma de Valores en las Variables de Material',
             color='NOMBRE/INSTITUCIÓN')

v_temperatura_ = plt.figure(figsize=(15, 8))
average_temp_by_year.plot(kind='bar', color=colors)
plt.title('Average Temperature in La Paz by Year (1990-2022)')
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.grid(axis='y')
#plt.show()

v_temperatura = px.bar(
    x=average_temp_by_year.index,
    y=average_temp_by_year.values,
    labels={'x': 'Year', 'y': 'Average Temperature (°C)'},
    title='Average Temperature in La Paz by Year (1990-2022)',
    color_discrete_sequence=['olive']
)

co_plotly_line = px.line(data_co, x='FECHA', y='CO ', title='CO Concentration Over Time', labels={'CO': 'CO Concentration'})
co_plotly_histogram = px.histogram(data_co, x='CO ', nbins=20, title='Distribution of CO Concentration', labels={'CO': 'CO Concentration'})

pm_plotly_line = px.line(data_pm, x='FECHA', y='PM 10', title='PM 10 Concentration Over Time', labels={'PM 10': 'PM 10 Concentration'})

pm_plotly_histogram = px.histogram(data_pm, x='PM 10', nbins=20, title='Distribution of PM 10 Concentration', labels={'PM 10': 'PM 10 Concentration'})


co_heatmap_data = data_co[['CO ']].T
pm_heatmap_data = data_pm[['PM 10']].T

co_heatmap_ = sns.heatmap(co_heatmap_data, cmap='YlGnBu', cbar_kws={'label': 'CO Concentration'})

pm_heatmap_ = sns.heatmap(pm_heatmap_data, cmap='YlGnBu', cbar_kws={'label': 'PM 10 Concentration'})

co_heatmap = px.imshow(co_heatmap_data, color_continuous_scale='YlGnBu', labels={'color': 'CO Concentration'})
pm_heatmap = px.imshow(pm_heatmap_data, color_continuous_scale='YlGnBu', labels={'color': 'PM 10 Concentration'})


#co_jointplot = px.scatter(data_co, x='FECHA', y='CO ', marginal_x="histogram", marginal_y="histogram", color='CO ', color_continuous_scale='blues', title='CO Concentration Over Time')

#pm_jointplot = px.scatter(data_pm, x='FECHA', y='PM 10', marginal_x="histogram", marginal_y="histogram", color='PM 10', color_continuous_scale='greens', title='PM 10 Concentration Over Time')
co_jointplot = px.scatter(
    data_co,
    x='FECHA',
    y='CO ',
    marginal_x="histogram",
    marginal_y="histogram",
    color_continuous_scale=['orange', 'yellow'],
    title='CO Concentration Over Time'
)
co_jointplot.update_layout(coloraxis_colorbar=dict(title='CO Concentration'))

# Scatter plot con histogramas marginales para PM 10
pm_jointplot = px.scatter(
    data_pm,
    x='FECHA',
    y='PM 10',
    marginal_x="histogram",
    marginal_y="histogram",
    color_continuous_scale=['yellow', 'orange'],
    title='PM 10 Concentration Over Time'
)
pm_jointplot.update_layout(coloraxis_colorbar=dict(title='PM 10 Concentration'))


#plot_comunes_kg_ = sns.barplot(x="MES", y="COMUNES KG", data=data_pesos, ci=None)
#plot_papel_carton_kg_ = sns.lineplot(x="MES", y="PAPEL Y CARTON KG", data=data_pesos, marker="o")
#plot_vidrio_kg_ = sns.scatterplot(x="MES", y="VIDRIO KG", data=data_pesos)


plot_comunes_kg = px.bar(data_pesos, x="MES", y="COMUNES KG", title="Bar Chart - Comunes KG")
plot_papel_carton_kg = px.line(data_pesos, x="MES", y="PAPEL Y CARTON KG", markers=True, title="Line Chart - Papel y Carton KG")
plot_vidrio_kg = px.scatter(data_pesos, x="MES", y="VIDRIO KG", title="Scatter Plot - Vidrio KG")

strip_plot_patogenos = px.strip(
    data_pesos,
    x='MES',
    y='PATOGENOS KG',
    title="Strip Plot for PATOGENOS KG",
)
bar_plot_patogenos = px.bar(
    data_pesos,
    x='MES',
    y='PATOGENOS KG',
    color_discrete_sequence=['green'],  # Establecer el color de todas las barras a verde
    title="Bar Plot for PATOGENOS KG"
)
macrodistrito_residuos = px.bar(data_dem, x='MACRODISTRITO DONDE SE ENTREGO', y='TOTAL m3', title='Relación entre Macrodistrito y Total m3', color_discrete_sequence=['pink'],
                          labels={'MACRODISTRITO DONDE SE ENTREGO': 'Macrodistrito',  'TOTAL m3': 'Total m3'})
macrodistrito_residuos.update_layout(xaxis_title='Macrodistrito', yaxis_title='Total m3')

linetime_rcd = px.line(data_dem, x='FECHA', y="TOTAL m3", color_discrete_sequence=['green'] )
linetime_pm = px.line(data_pm, x='FECHA', y="PM 10",  color_discrete_sequence=['brown'])


columnas_sumar = ['GRAVA m3', 'GRAVILLA m3', 'ARENA m3', 'PIEDRAS m3', 'TIERRA m3']
suma_valores = data_dem[columnas_sumar].sum()
df_suma = pd.DataFrame({'Variable': suma_valores.index, 'Suma': suma_valores.values})
df_suma = df_suma.sort_values(by='Suma', ascending=False)
tipos_residuo = px.bar(df_suma, x='Variable', y='Suma',
             labels={'Suma': 'Suma de Valores', 'Variable': 'Variables'},
             color='Variable',
             title='Suma de Valores en las Variables de Material')
tipos_residuo.update_layout(xaxis_title='tipos', yaxis_title='año 2022')



#CONTAINERS
def main():

  #col = st.columns((1.5, 4.5, 2), gap='medium')

  with st.container():

    st.subheader("¡Bienvenido al Dashboard de Análisis de Datos Atmosféricos y Residuos de La Paz - Bolivia!")
    col = st.columns((4, 4), gap='medium')
    with col[0]:
      st.write("Este espacio interactivo te invita a explorar las complejas relaciones entre los datos atmosféricos y la generación de residuos. ¿Cómo afecta la calidad del aire al manejo de residuos? ¿Existen patrones estacionales en la producción de residuos? Descubre estas respuestas y más a través de visualizaciones dinámicas y análisis detallados.")
      st.title("ANÁLISIS DE DATOS ")

    with col[1]:
      st_lottie(lottie_coding, height=300, key="coding")
    st.write("---")

  with st.container():
    st.subheader("Correlación Temporal entre Residuos de Demoliciones (m3) y Partículas Sólidas PM")
    col = st.columns((4, 4), gap='medium')
    with col[0]:    
      st.plotly_chart(linetime_rcd)
    with col[1]:
      st.plotly_chart(linetime_pm)
    
    
    st.plotly_chart(pm_rcd)
    col2 = st.columns((4, 4), gap='medium')
    with col2[0]:
      st.subheader("Relación entre la Cantidad de Días y el CO: Mapa de Calor")
      st.plotly_chart(co_heatmap, use_container_width=True)
    with col2[1]:
      st.subheader("Mapa de Calor de la Relación entre la Cantidad de Días y las Partículas Sólidas PM")
      st.plotly_chart(pm_heatmap, use_container_width=True)
    st.write("---")


  with st.container():
    col = st.columns((4, 4), gap='medium')
    with col[0]:
      st.subheader("Gráfica de Barras sobre la Cantidad de Residuos de Construcción por Tipo de Institución")
      st.plotly_chart(v_instituciones_residuos)
    
    with col[1]:
      st.subheader("Gráfica de Barras sobre el Tipo de Residuos de Construcción en el Año 2022")
      st.plotly_chart(tipos_residuo)
    col = st.columns((4, 4), gap='medium')
    with col[0]:
      st.subheader("Visualización de la Tendencia al Cambio en los Residuos a lo Largo del Tiempo")
      st.plotly_chart(plot_vidrio_kg)
    with col[1]:
      st.plotly_chart(plot_comunes_kg)

    
    st.subheader("Gráfica del Conteo entre la Relación entre Macrodistrito y Total m3")
    st.plotly_chart(macrodistrito_residuos)
    st.write("---")

  with st.container():
    col = st.columns((4, 4), gap='medium')
    
    with col[0]:
      st.subheader("Visualizaciones del Comportamiento del Monóxido de Carbono (CO) en el Paso del Tiempo")
      st.plotly_chart(co_plotly_line)
    with col[1]:
      st.plotly_chart(co_plotly_histogram)
    st.write("---")

    col = st.columns((4, 4), gap='medium')
    with col[0]:
      st.subheader("Visualizaciones del Comportamiento de las Partículas Sólidas PM en el Paso del Tiempo")
      st.plotly_chart(pm_plotly_line)
    with col[1]:
      st.plotly_chart(pm_plotly_histogram)
    st.write("---")
    col = st.columns((4, 4), gap='medium')
    with col[0]:
      st.write("Observa la Dispersión de las Partículas Sólidas PM y el Monóxido de Carbono (CO) a lo largo del Tiempo")
      st.plotly_chart(co_jointplot)
    with col[1]:
      st.plotly_chart(pm_jointplot)
    st.write("---")

  with st.container():
    
    st.subheader("Variación de la Temperatura Promedio en La Paz por Año")
    st.plotly_chart(v_temperatura)
    st.write("---")

  with st.container():
    # st.subheader("Temperatura Promedio en La Paz por Año")

    # st.plotly_chart(plot_papel_carton_kg)

    st.subheader('Distribución de Residuos Patogénicos a lo largo de los Meses: Gráfica Strip')
    st.plotly_chart(strip_plot_patogenos)

    st.subheader('Cantidad de Residuos Patogénicos para Cada Mes: Gráfica de Barras')

    st.plotly_chart(bar_plot_patogenos)
    st.write("---")
  
  
  
  with st.container():

    left_column, right_column = st.columns(2)
    with left_column:

      st.write(
        """
        Hicimos un exhaustivo análisis de datos y gracias a ello ahora les presentamos una iniciativa innovadora de economia circular centrada en la recoleccion de residuos solidos para mejorar la calidad del aire.
          Siéntete libre de pasar por las diapositivas para ver los detalles de nuestra propuesta!
        """
      )
      st.header("Revisa nuestra propuesta a traves de este enlace")
      st.write("[Fizzarolli >](https://drive.google.com/drive/folders/1-jMNTWFKCDnF1vIOLF3c2fB6RMyOynvVXXX)")
    with right_column:
      st_lottie(lottie_coding, height=300, key="coding2")
    st.write("---")



if __name__ == "__main__":
    print('running...')
    main()


