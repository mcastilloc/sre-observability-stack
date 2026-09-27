import time
import random
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Métricas de Prometheus (Golden Signals)
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total de peticiones HTTP', ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'Latencia de las peticiones HTTP en segundos', ['endpoint']
)

@app.route('/')
def home():
    start_time = time.time()
    
    # Simular latencia y errores ocasionales
    latency = random.uniform(0.1, 0.8)
    time.sleep(latency)
    
    status_code = 200
    if random.random() < 0.15:  # 15% de probabilidad de error 500
        status_code = 500
        REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=status_code).inc()
        REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
        return "Internal Server Error", 500

    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=status_code).inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)
    return "API SRE/DevOps funcionando perfectamente!"

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)