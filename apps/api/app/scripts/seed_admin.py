from app.services.seed import get_seed_admin_user


def main() -> None:
    admin = get_seed_admin_user()
    print(f"Seed admin ready for {admin.email}")


if __name__ == "__main__":
    main()

