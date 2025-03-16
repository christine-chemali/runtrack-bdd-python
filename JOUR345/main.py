
from application import Application
from database import Database

def main():
    db = Database()
    app = Application(db)
    app.mainloop()
    db.close()

if __name__ == "__main__":
    main()