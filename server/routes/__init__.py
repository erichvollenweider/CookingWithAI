from .login_register import login_register_bp
from .recipes import recipes_bp

def init_routes(app):
    app.register_blueprint(login_register_bp)
    app.register_blueprint(recipes_bp)
