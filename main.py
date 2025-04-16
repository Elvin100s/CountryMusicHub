from app import app

if __name__ == "__main__":
    # Configure for large file uploads
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host="0.0.0.0", port=5000, debug=True, 
            threaded=True,
            request_handler=WSGIRequestHandler)
