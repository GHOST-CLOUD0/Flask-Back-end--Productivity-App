from server.controllers.auth_controller import auth_bp
from server.controllers.task_controller import task_bp

def register_routes(app):
    """
    Register API blueprints using the paths expected by the JWT client.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)