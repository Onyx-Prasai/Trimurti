from django.http import JsonResponse


def api_root(request):
    """Root view showing API information"""
    return JsonResponse({
        'message': 'Blood Hub Nepal API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api': {
                'donors': '/api/donors/',
                'hospitals': '/api/hospitals/',
                'bloodbanks': '/api/bloodbanks/',
                'store': '/api/store/',
                'ai-health': '/api/ai-health/',
            }
        },
        'frontend': 'http://localhost:3000',
        'documentation': 'See README.md for API documentation'
    })

