import requests
import json
from datetime import datetime

# Token obtenido del login
TOKEN = "eyJhbGciOiJIUzI1NiIsImtpZCI6IjJwa1FadlNNaHB5dHV0ZEoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3poa3VocHFvZW1vcHdicXl3YWd0LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI3MGZiNmMzYy0yODJiLTRmMTAtYThmNy00NjFmYmZjNjgyZTYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzU3NDI4MzE2LCJpYXQiOjE3NTc0MjQ3MTYsImVtYWlsIjoiam9oYW5zdGl2ZW5yZW5naWZvQG91dGxvb2suY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJlbWFpbCIsInByb3ZpZGVycyI6WyJlbWFpbCJdfSwidXNlcl9tZXRhZGF0YSI6eyJhcGVsbGlkb3MiOiJSZW5naWZvIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5vbWJyZSI6IkpvaGFuIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NTc0MjQ3MTZ9XSwic2Vzc2lvbl9pZCI6IjQ4NDk5N2RlLTg2MjktNDdhZC1hY2YyLWViMmY4YzgyY2IyYSIsImlzX2Fub255bW91cyI6ZmFsc2V9.Zq1E3z_lhdSstB43wPjaI_I09lCt4qbpqEWkTWEGk08"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Lista de endpoints para probar
ENDPOINTS = [
    # Autenticación
    {"method": "GET", "url": "/api/v1/auth/me", "name": "Obtener usuario actual"},
    {"method": "POST", "url": "/api/v1/auth/refresh", "name": "Renovar token"},
    
    # Usuarios
    {"method": "GET", "url": "/api/v1/usuarios/", "name": "Listar usuarios"},
    {"method": "GET", "url": "/api/v1/usuarios/activos", "name": "Listar usuarios activos"},
    
    # Pacientes
    {"method": "GET", "url": "/api/v1/pacientes/", "name": "Listar pacientes"},
    
    # Médicos
    {"method": "GET", "url": "/api/v1/medicos/", "name": "Listar médicos"},
    {"method": "GET", "url": "/api/v1/medicos/detalles", "name": "Listar médicos con especialidad"},
    {"method": "GET", "url": "/api/v1/medicos/disponibles", "name": "Obtener médicos disponibles"},
    
    # Especialidades
    {"method": "GET", "url": "/api/v1/especialidades/", "name": "Listar especialidades"},
    {"method": "GET", "url": "/api/v1/especialidades/activas", "name": "Listar especialidades activas"},
    
    # Consultorios
    {"method": "GET", "url": "/api/v1/consultorios/", "name": "Listar consultorios"},
    {"method": "GET", "url": "/api/v1/consultorios/activos", "name": "Listar consultorios activos"},
    
    # Citas
    {"method": "GET", "url": "/api/v1/citas/", "name": "Listar citas"},
    {"method": "GET", "url": "/api/v1/citas/detalles", "name": "Listar citas con detalles"},
    {"method": "GET", "url": "/api/v1/citas/pendientes-pago", "name": "Obtener citas pendientes de pago"},
    
    # Calificaciones
    {"method": "GET", "url": "/api/v1/calificaciones/", "name": "Listar calificaciones"},
    {"method": "GET", "url": "/api/v1/calificaciones/detalles", "name": "Listar calificaciones con detalles"},
    
    # Notificaciones
    {"method": "GET", "url": "/api/v1/notificaciones/", "name": "Listar notificaciones"},
]

def test_endpoint(endpoint):
    """Probar un endpoint específico"""
    url = f"http://localhost:8000{endpoint['url']}"
    
    try:
        if endpoint["method"] == "GET":
            response = requests.get(url, headers=HEADERS)
        elif endpoint["method"] == "POST":
            response = requests.post(url, headers=HEADERS)
        elif endpoint["method"] == "PUT":
            response = requests.put(url, headers=HEADERS)
        elif endpoint["method"] == "DELETE":
            response = requests.delete(url, headers=HEADERS)
        
        return {
            "name": endpoint["name"],
            "method": endpoint["method"],
            "url": endpoint["url"],
            "status_code": response.status_code,
            "success": response.status_code == 200,
            "error": response.text if response.status_code != 200 else None
        }
        
    except Exception as e:
        return {
            "name": endpoint["name"],
            "method": endpoint["method"],
            "url": endpoint["url"],
            "status_code": 0,
            "success": False,
            "error": str(e)
        }

def main():
    """Probar todos los endpoints"""
    print("=" * 80)
    print("REPORTE DE PRUEBAS DE ENDPOINTS")
    print("=" * 80)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Token: {TOKEN[:50]}...")
    print("=" * 80)
    
    results = []
    successful = 0
    failed = 0
    
    for endpoint in ENDPOINTS:
        result = test_endpoint(endpoint)
        results.append(result)
        
        if result["success"]:
            successful += 1
            print(f"✅ {result['method']} {result['url']} - {result['name']}")
        else:
            failed += 1
            print(f"❌ {result['method']} {result['url']} - {result['name']}")
            print(f"   Status: {result['status_code']}")
            if result['error']:
                print(f"   Error: {result['error'][:100]}...")
    
    print("=" * 80)
    print(f"RESUMEN:")
    print(f"Total endpoints: {len(ENDPOINTS)}")
    print(f"Exitosos: {successful}")
    print(f"Fallidos: {failed}")
    print(f"Tasa de éxito: {(successful/len(ENDPOINTS)*100):.1f}%")
    print("=" * 80)
    
    # Guardar reporte en archivo
    with open("endpoint_test_report.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(ENDPOINTS),
                "successful": successful,
                "failed": failed,
                "success_rate": successful/len(ENDPOINTS)*100
            },
            "results": results
        }, f, indent=2, ensure_ascii=False)
    
    print("Reporte guardado en: endpoint_test_report.json")

if __name__ == "__main__":
    main()