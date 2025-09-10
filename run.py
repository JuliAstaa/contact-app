from app import App


def main():
    app = App().app
    app.run(debug=True)

if __name__ == '__main__':    
    from app import db, App
    app = App()
    with app.app.app_context():
        db.create_all()
    main()