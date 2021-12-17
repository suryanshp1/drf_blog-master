from graphene.test import Client
from api.schema import schema
# from blog.schema import schema
from snapshottest import TestCase

# schema = graphene.Schema(query=Query, mutation=Mutation)

# def test_all_posts():
#     client = Client(schema)
#     executed = client.execute('''
#         {
#         allPosts {
#             id
#             title
#             body
#         }
#         }
#     ''')
#     assert executed == {
#         "data": {
#             "allPosts": [
#                 {
#                     "id": "1",
#                     "title": "First Blog",
#                     "body": "This is my first sample Blog."
#                 },
#                 {
#                     "id": "2",
#                     "title": "Second Blog",
#                     "body": "This is second blog Body."
#                 },
#                 {
#                     "id": "3",
#                     "title": "Third Blog",
#                     "body": "This is Third Blog body"
#                 },
#                 {
#                     "id": "5",
#                     "title": "Update my Title",
#                     "body": "This is a sample success post."
#                 },
#                 {
#                     "id": "6",
#                     "title": "title1",
#                     "body": "this is body"
#                 },
#                 {
#                     "id": "7",
#                     "title": "title2",
#                     "body": "this is body 2"
#                 },
#                 {
#                     "id": "9",
#                     "title": "title3",
#                     "body": "this is body 2"
#                 }]}}


# def test_post():
#     client = Client(schema)
#     executed = client.execute('''
#         {
#         post(id: 2){
#         id
#         title
#         body
#         }
#         }
#     ''')
#     assert executed == {
#         "data": {
#             "post": {
#                 "id": "2",
#                 "title": "Second Blog",
#                 "body": "This is second blog Body."
#             }}}


# def test_all_comments():
#     client = Client(schema)
#     executed = client.execute('''
#         {
#         allComments{
#             id
#             body
#     	    post {
#     	    id
#     	    }
#         }
#         }
#     ''')
#     assert executed == {
#         "data": {
#             "allComments": [
#                 {
#                     "id": "1",
#                     "body": "Good",
#                     "post": {
#                         "id": "1"
#                     }
#                 },
#                 {
#                     "id": "2",
#                     "body": "Best",
#                     "post": {
#                         "id": "2"
#                     }
#                 },
#                 {
#                     "id": "3",
#                     "body": "Better",
#                     "post": {
#                         "id": "3"
#                     }
#                 },
#                 {
#                     "id": "6",
#                     "body": "Well done.",
#                     "post": {
#                         "id": "2"
#                     }
#                 },
#                 {
#                     "id": "8",
#                     "body": "good",
#                     "post": {
#                         "id": "7"
#                     }
#                 },
#                 {
#                     "id": "9",
#                     "body": "This is a graphene post comment.",
#                     "post": {
#                         "id": "6"
#                     }
#                 }]}}


# def test_comment():
#     client = Client(schema)
#     executed = client.execute('''
#     {
#     comment(id: 6){
#       id
#       body
#     	post {
#     	  id
#     	}
#         }
#         }
#     ''')

#     assert executed == {
#         "data": {
#             "comment": {
#                 "id": "6",
#                 "body": "Well done.",
#                 "post": {
#                     "id": "2"
#                 }
#             }}}

class APITestCase(TestCase):
    def test_all_posts(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''{
        allPosts {
            id
            title
            body
        }
        }'''))

    def test_post(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
        post(id: 2){
        id
        title
        body
        }
        }'''))

    def test_all_comments(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
        allComments{
            id
            body
    	    post {
    	    id
    	    }
          }
        }'''))

    def test_comment(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        query getComment($id: ID) {
          comment(id: $id) {
            id
            body
    	      post {
    	      id
    	    }
          }
        }''',
        variables={'id': 6}))
