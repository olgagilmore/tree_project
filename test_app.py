import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Tree, Owner


class TreeAppTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trees4life'   # "test_trees4life"
        self.database_path = "postgres://hlwfabhgudlimb:68b67af396085639ed6c33dba4f0af2f3fc9527faa1d878f342557d816a37ad3@ec2-18-232-143-90.compute-1.amazonaws.com:5432/d6cn808tp1t9mn"
        # "postgres://{}:{}@{}/{}".format('postgres', 'dbadmin',
        # 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_tree = {
            'type': 'mahogany',
            'owner_id': '1',
            'latitude': '33.7490',
            'longitude': '84.3880',
            'plantedDate': '6-16-2020'
            }
#         self.another_tree = {
#             'type': "other",
#             'owner_id': "1",
#             'lat': "33.7490",
#             'long': "-84.3880",
#             'date': "6/16/2020"
#             }
        self.notoken = ''
        self.assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdLa2t2ajJJb1h5dUJsWUFvSUQ2XyJ9.eyJpc3MiOiJodHRwczovL29naWxtb3JlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWJhM2Y3YjRmNjllMTIyNTZmYzFhZDgiLCJhdWQiOiJUcmVlczRMaWZlIiwiaWF0IjoxNTkyNTEyMTc4LCJleHAiOjE1OTI1OTg1NzgsImF6cCI6InpYejhOTWZLR3ZRaHRXeW1CWDExdG1xTVZvc2pPWDFYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6b3duZXJzIiwiZ2V0OnRyZWVzIl19.pvPND-pD9y1TSBbpgskN7MjMOHpLyQ6J4-7T1kOvXF8svTB16fakS2tuxu0eXRQTEHMkejVIc2KUlfT_9Bfs1BHAD-zhS5UNLpwwxGAnlocsUCjcBjKx3_dCcD1R618sub--IwTObdDobScJFikEkIWPgabQULh1fdkfi73cIenllH4MFtjQ9YoT2F4RHIctGTHPat9sTIULNcg2mH5aLR55etiukZx10Hu142iPKdQtXbQrId0qiaSBSpkJCKbzdHMY3vV1OeDHuGQp_pqv2rRfOG6KpOjSgFlGQtfPhOpWFjtIU95intTklIUR_ymfFmvjCG1wCHvSvUcUpIFMyA'

        self.admin = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdLa2t2ajJJb1h5dUJsWUFvSUQ2XyJ9.eyJpc3MiOiJodHRwczovL29naWxtb3JlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWFmN2IxOTFjYzFhYzBjMTQ4MWQ0ZTYiLCJhdWQiOiJUcmVlczRMaWZlIiwiaWF0IjoxNTkyNTExODkzLCJleHAiOjE1OTI1OTgyOTMsImF6cCI6InpYejhOTWZLR3ZRaHRXeW1CWDExdG1xTVZvc2pPWDFYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6dHJlZSIsImdldDpvd25lcnMiLCJnZXQ6dHJlZXMiLCJwYXRjaDp0cmVlIiwicG9zdDp0cmVlcyJdfQ.i_07jVMnRmizpgTobsQ3HbGiORhxzPVLDww70auA8gHTxxE0oLgeuP_QQ9MGuRK49lkskUTS2q14J9SPuqMQONUdyu_cdr6WpdGbvoN1-vWBi4bzfA8Bic_DfOssxxJnbG4X4irn7CkEV6Rw5vQoFOm-L4bp8ClufFAG3gzdvnRa7vCEecgt-9BdZf-CQPt7EVI7WMApi-sc8z-PUvJDmZC3yxkyNcBitCO9cUXdDklmM9Dq5dJx8icQ-fYtHZuMPX0xJqiJrQM871n8K2wGa6PQZNB0hWQ_oV0vcZQPq6q6_adJJ7ANGYbM4tvGnr65qgRDGK71WQWpaJfXhYk1pg'

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    DONE
    Write at least one test for each test for successful operation and
    for expected errors.
    """
    def test_get_trees(self):
        response = self.client().get('/trees')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_trees'])
        self.assertTrue(len(data['trees']))

    def test_404_invalid_trees_route(self):
        response = self.client().get('/tree', json={'type': "Nothing"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_get_owners(self):
        response = self.client().get('/owners', headers={
            "Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_owners'])
        self.assertTrue(len(data['owners']))

    def test_401_unauthorized__owners_route(self):
        response = self.client().get('/owners')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], {
            'code': 'authorization_header_missing', 'description':
            'Authorization header is expected.'})

#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], "resource not found")
    def test_get_trees_per_owner(self):
        response = self.client().get('owners/2/trees', headers={
            "Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_trees'])
        self.assertEqual(data['total_trees'], 2)
        self.assertTrue(len(data['trees']))

    def test_add_tree_delete_tree(self):
        # combining both so the tests can run multiple times
        response = self.client().post('/trees', headers={
            "Authorization": "Bearer {}".format(self.admin)},
            json=self.new_tree)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

        self.assertTrue(data['total_trees'])
        self.assertTrue(len(data['trees']))
        self.created_tree_id = data['created']

    # def test_delete_tree(self):

        response = self.client().delete('/trees/' + str(self.created_tree_id),
                                        headers={
                                        "Authorization":
                                            "Bearer {}".format(self.admin)})
        data = json.loads(response.data)

        tree = Tree.query.filter(Tree.id == self.created_tree_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(self.created_tree_id))
        self.assertEqual(tree, None)
        self.assertTrue(data['total_trees'])
        self.assertTrue(len(data['trees']))

    def test_delete_trees_out_of_bounds(self):
        response = self.client().delete('/trees/1000', headers={
            "Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(response.data)

        tree = Tree.query.filter(Tree.id == 1000).one_or_none()

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_trees_unauthorized(self):
        response = self.client().delete('/trees/1000', headers={
            "Authorization": "Bearer {}".format(self.assistant)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], {
            'code': 'unauthorized', 'description':
            'Permission not found.'})

    def test_post_not_allowed(self):
        response = self.client().post('/trees/42', headers={
            "Authorization": "Bearer {}".format(self.admin)},
            json=self.new_tree)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_patch_with_success(self):
        response = self.client().patch('/trees/1', headers={
            "Authorization": "Bearer {}".format(self.admin)},
            json={'type': 'elm'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['trees'])
        self.assertTrue(len(data['trees']))

    def test_patch_failure(self):
        response = self.client().patch('/trees/1', headers={
            "Authorization": "Bearer {}".format(self.admin)},
            json={'type': 'wwwww'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

        self.assertEqual(data['message'], 'unprocessable')

    def test_patch_unauthorized(self):
        response = self.client().patch('/trees/1', headers={
            "Authorization": "Bearer {}".format(self.assistant)},
             json={'type': 'wwwww'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], {
            'code': 'unauthorized', 'description':
            'Permission not found.'})

#     def test_post_not_allowed(self):
#         response= self.client().post('/questions/42', json=self.new_question)
#         data= json.loads(response.data)
#
#         self.assertEqual(response.status_code, 405)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'method not allowed')
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
