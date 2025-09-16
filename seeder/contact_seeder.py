from faker import Faker
from app import App
from app.services.contact_services import ContactServices

fake = Faker()

def seeder_contact(n=10000):
    service = ContactServices()
    for _ in range(n):
        service.create_contact(
            phone_number=fake.phone_number(),
            f_name=fake.first_name(),
            l_name=fake.last_name(),
            email=fake.email()
        )
    print(f"{n} data created ✅")


if __name__ == "__main__":
    app = App().app
    with app.app_context():
        seeder_contact(10000)