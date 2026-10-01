import pandas as pd
import requests

def analizar_estadisticas_publicas():
    # Usamos una API pública alternativa y estable para pruebas de analítica
    url = "https://jsonplaceholder.typicode.com/users"
    print("Conectando con la base de datos pública alternativa...")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al conectar con la fuente de datos. Código: {response.status_code}")
        return
    
    data = response.json()
    
    if not isinstance(data, list):
        print("La estructura de los datos recibidos no es una lista válida.")
        return
    
    # Procesamiento y transformación con Pandas
    registros = []
    for usuario in data:
        # Extraemos datos simulados corporativos / geográficos
        company = usuario.get("company", {})
        address = usuario.get("address", {})
        
        registros.append({
            "Nombre": usuario.get("name", "N/A"),
            "Ciudad": address.get("city", "N/A"),
            "Empresa": company.get("name", "N/A"),
            "Id_Usuario": usuario.get("id", 0)
        })
        
    df = pd.DataFrame(registros)
    
    # Explotación Estadística
    print("\n" + "="*50)
    print("📊 RESULTADOS DE LA EXPLOTACIÓN ESTADÍSTICA")
    print("="*50)
    print(f"• Total de registros analizados: {len(df):,}")
    print(f"• Ciudades únicas representadas: {df['Ciudad'].nunique()}")
    print(f"• Empresas asociadas analizadas: {df['Empresa'].nunique()}")
    
    print("\n--- RESUMEN ESTADÍSTICO POR CIUDAD ---")
    resumen = df.groupby("Ciudad").agg(
        Total_Usuarios=("Id_Usuario", "count")
    ).reset_index()
    
    print(resumen.to_string(index=False))

if __name__ == "__main__":
    analizar_estadisticas_publicas()