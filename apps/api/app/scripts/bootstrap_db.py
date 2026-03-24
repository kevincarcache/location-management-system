from app.db.session import SessionLocal
from app.services.bootstrap import init_db


def main() -> None:
    with SessionLocal() as db:
        init_db(db=db)
    print("Database tables created and seed data applied.")


if __name__ == "__main__":
    main()
