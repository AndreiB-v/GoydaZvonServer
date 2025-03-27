from requests import get, post

# print(post('http://localhost:5000/api/users',
#            json={'nickname': 'GooDnes',
#                  'phone': '79011093769',
#                  'real_name': 'Андрей',
#                  'password': '123456'}).json())
# print(post('http://localhost:5000/api/users',
#            json={'nickname': 'Polina',
#                  'phone': '79011093768',
#                  'real_name': 'Полина',
#                  'password': '123456'}).json())
# print(post('http://localhost:5000/api/chats',
#            json={'user_id1': 1,
#                  'user_id2': 2}).json())
# print(post('http://localhost:5000/api/messages',
#            json={'chat_id': 1,
#                  'user_id': 2,
#                  'message': 'what the hell'}).json())
# print(post('http://localhost:5000/api/contacts',
#            json={'user_id': 1,
#                  'user_contact_id': 2,
#                  'description_contact': 'челик'}).json())
print(get('http://localhost:5000/api/users/1').json())
print(get('http://localhost:5000/api/chats/1').json())
print(get('http://localhost:5000/api/messages/1').json())
print(get('http://localhost:5000/api/contacts/1').json())
