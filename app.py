from flask import Flask
from config import Config
from extensions import db, login_manager


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------------------------
    # Initialize Extensions
    # ---------------------------------
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # ---------------------------------
    # Import Models (IMPORTANT)
    # ---------------------------------
    from models.user import User
    from models.account import Account
    from models.transaction import Transaction
    from models.loan import Loan
    from models.document import Document

    # ---------------------------------
    # Flask-Login User Loader
    # ---------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ---------------------------------
    # Register Blueprints
    # ---------------------------------
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp
    from routes.loan_routes import loan_bp
    from routes.netbanking import netbank_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(netbank_bp)

    # ---------------------------------
    # Create Database Tables
    # ---------------------------------
    with app.app_context():
        db.create_all()
        create_default_admin()

    return app


# ---------------------------------
# CREATE DEFAULT ADMIN
# ---------------------------------
def create_default_admin():

    from models.user import User
    from models.account import Account

    existing_admin = User.query.filter_by(email="admin@rmbi.com").first()

    if not existing_admin:

        admin = User(
            full_name="RMBI Super Admin",
            email="admin@rmbi.com",
            phone="9999999999",
            aadhaar="111122223333",
            role="admin"
        )

        admin.set_password("Admin@123")

        db.session.add(admin)
        db.session.commit()

        admin_account = Account(
            user_id=admin.id,
            account_number=Account.generate_account_number(),
            balance=0,
            account_type="admin"
        )

        db.session.add(admin_account)
        db.session.commit()

        print("✅ Default Admin Created Successfully")


# ---------------------------------
# Run Application
# ---------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)