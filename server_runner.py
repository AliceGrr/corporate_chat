from server import app, db, manager, migrate

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
