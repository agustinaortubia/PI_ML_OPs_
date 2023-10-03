from fastapi import FastAPI
import pandas as pd


# Carga el dataset
df_consulta1 = pd.read_csv('C:/Users/Susana y Juan/OneDrive/Escritorio/Henry/PI_ML_Ops/Archivos/Consultas/df_consulta1_a.csv')  # Ruta al primer archivo CSV
df_consulta2 = pd.read_csv('C:/Users/Susana y Juan/OneDrive/Escritorio/Henry/PI_ML_Ops/Archivos/Consultas/df_consulta2.csv')  # Ruta al segundo archivo CSV


# Supongamos que tienes un DataFrame llamado df_consulta1
df_consulta2 = pd.DataFrame({
    'Nombre': ['Alice', 'Bob', 'Charlie'],
    'Edad': [25, 30, 22]
})

app = FastAPI()

#127.0.0.1:8000
@app.get('/') #ruta de prueba
def index():
    return {'message' : 'holi2'}

# Endpoint 1: Obtener el año con más horas jugadas para un género dado
@app.get('/playtime_genre')
async def playtime_genre(Genres: str):
    # Filtrar el DataFrame por género
    df_filtered = df_consulta1[df_consulta1['Genres'] == Genres]

    if df_filtered.empty:
        raise HTTPException(status_code=404, detail=f"No se encontraron datos para el género {Genres}")

    # Encontrar el año con más horas jugadas
    year_max_playtime = df_filtered.loc[df_filtered['Playtime_Forever'].idxmax()]['Release_Date']

    return {"Año de lanzamiento con más horas jugadas para Género X": year_max_playtime}
    
# ENDPOINT 2 -----------------------------------------------------------------------------------

# Endpoint 1: Obtener el usuario con más horas jugadas y acumulación de horas por año para un género dado
@app.route('/user_for_genre')
def UserForGenre():
    genero = request.args.get('Genres')  # Obtén el género de la consulta

    # Filtrar el DataFrame por género
    df_filtered = df_consulta2[df_consulta2['Genres'] == genero]

    if df_filtered.empty:
        return jsonify({"error": f"No se encontraron datos para el género {genero}"}), 404

    # Encontrar el usuario con más horas jugadas
    usuario_max_horas = df_filtered.loc[df_filtered['Playtime_Forever'].idxmax()]['User_Id']

    # Calcular la acumulación de horas jugadas por año
    df_filtered['Year'] = pd.to_datetime(df_filtered['Release_Date']).dt.year
    acumulacion_horas_por_ano = df_filtered.groupby('Year')['Playtime_Forever'].sum().reset_index()
    horas_por_ano = [{"Año": row['Year'], "Horas": row['Playtime_Forever']} for _, row in acumulacion_horas_por_ano.iterrows()]

    resultado = {
        "Usuario con más horas jugadas para Género X": usuario_max_horas,
        "Horas jugadas": horas_por_ano
    }

    return jsonify(resultado)

    
    
    