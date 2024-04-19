from unittest import TestCase
from app import app, databs
from models import Cupcake

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

databs.drop_all()
databs.create_all()


class CupcakeTests(TestCase):
    def setUp(self):
        with app.app_context():
            self.cupcake_1 = Cupcake(
                flavor="Chocolate", size="Small", rating=5, image="http://example.com/chocolate.jpg"
            )
            self.cupcake_2 = Cupcake(
                flavor="Vanilla", size="Medium", rating=7, image="http://example.com/vanilla.jpg"
            )

            databs.session.add_all([self.cupcake_1, self.cupcake_2])
            databs.session.commit()

    def tearDown(self):
        with app.app_context():
            databs.session.rollback()
            databs.drop_all()

    def list_cupcakes_test(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(len(data['cupcakes']), 2)

    def get_cupcake_test(self):
        with app.test_client() as client:
            resp = client.get(f"/api/cupcakes/{self.cupcake_1.id}")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data['cupcake']['flavor'], "Chocolate")

    def create_cupcake_test(self):
        with app.test_client() as client:
            resp = client.post(
                "/api/cupcakes",
                json={
                    "flavor": "Strawberry",
                    "size": "Large",
                    "rating": 8,
                    "image": "http://example.com/strawberry.jpg",
                },
            )

            self.assertEqual(resp.status_code, 201)

            data = resp.json
            self.assertEqual(data['cupcake']['flavor'], "Strawberry")

    def update_cupcake_test(self):
        with app.test_client() as client:
            resp = client.patch(
                f"/api/cupcakes/{self.cupcake_1.id}",
                json={"flavor": "NewFlavor"},
            )

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data['cupcake']['flavor'], "NewFlavor")

    def delete_cupcake_test(self):
        with app.test_client() as client:
            resp = client.delete(f"/api/cupcakes/{self.cupcake_1.id}")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {"message": "Deleted"})
