import googlemaps

# Inicializar el cliente con tu clave de API
gmaps = googlemaps.Client(key='TU_CLAVE_API')

# Coordenadas de ejemplo (Monte Everest)
location = (27.9881, 86.9250)

# Solicitar elevación
elevation_result = gmaps.elevation(location)

# Mostrar resultado
for result in elevation_result:
    print(f"Elevación: {result['elevation']} metros")
