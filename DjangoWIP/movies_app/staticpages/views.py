# staticpages/views.py
from django.http import HttpResponse

def home(request):
    """Vista que devuelve HTML fijo - sin base de datos"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>📄 Mi Primera Página Django</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; background: white; 
                        padding: 30px; border-radius: 10px; }
            nav a { margin-right: 15px; text-decoration: none; color: #007cba; }
        </style>
    </head>
    <body>
        <div class="container">
            <nav>
                <a href="/static-pages/">🏠 Home</a>
                <a href="/static-pages/about/">ℹ️ About</a>
                <a href="/static-pages/contact/">📧 Contact</a>
            </nav>
            
            <h1>🪑 ¡Bienvenido a Furniture Catalog!</h1>
            <p><strong>¿Qué es contenido estático?</strong></p>
            <ul>
                <li>✅ HTML completamente fijo</li>
                <li>✅ No consulta base de datos</li>
                <li>✅ Respuesta muy rápida</li>
                <li>✅ Ideal para landing pages</li>
            </ul>
            
            <p><em>Esta página está definida directamente en el código Python.</em></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def about(request):
    """Página About estática"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📋 Acerca de</title>
        <style>body { font-family: Arial; margin: 40px; }</style>
    </head>
    <body>
        <h1>📋 Acerca del Catálogo de Muebles</h1>
        <p>Esta es una página estática creada con Django.</p>
        <p><strong>Características:</strong></p>
        <ul>
            <li>No usa base de datos</li>
            <li>HTML fijo definido en views.py</li>
            <li>Respuesta inmediata</li>
        </ul>
        <a href="/static-pages/">← Volver al Home</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def contact(request):
    """Formulario de contacto estático"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📧 Contacto</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .form-group { margin: 15px 0; }
            input, textarea { width: 300px; padding: 8px; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; }
        </style>
    </head>
    <body>
        <h1>📧 Contacto</h1>
        <p><strong>⚠️ Formulario estático</strong> - No procesa datos realmente.</p>
        
        <form>
            <div class="form-group">
                <label>Nombre:</label><br>
                <input type="text" placeholder="Tu nombre">
            </div>
            <div class="form-group">
                <label>Email:</label><br>
                <input type="email" placeholder="tu@email.com">
            </div>
            <div class="form-group">
                <label>Mensaje:</label><br>
                <textarea rows="4" placeholder="Tu mensaje..."></textarea>
            </div>
            <button type="button" onclick="alert('¡Formulario estático!')">
                📤 Enviar
            </button>
        </form>
        
        <p><a href="/static-pages/">← Volver al Home</a></p>
    </body>
    </html>
    """
    return HttpResponse(html_content)