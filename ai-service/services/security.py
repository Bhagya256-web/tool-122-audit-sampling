from flask import Flask


def apply_security_headers(app: Flask):
    """
    Apply security headers to all responses.
    These fix common OWASP ZAP findings.
    """

    @app.after_request
    def add_security_headers(response):
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Enable XSS protection in older browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Restrict browser features
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        # Force HTTPS (enable in production)
        # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Remove server header to hide tech stack
        response.headers.pop("Server", None)

        return response

    return app