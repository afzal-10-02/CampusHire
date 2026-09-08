from controllers.admin import admin 
from controllers.auth import auth 
from controllers.company import company
from controllers.user import user


def register_route(app):

    app.register_blueprint(auth , url_prefix='/api/auth')
    app.register_blueprint(user , url_prefix='/api/user')
    app.register_blueprint(company , url_prefix='/api/company')
    app.register_blueprint(admin , url_prefix='/api/admin')




