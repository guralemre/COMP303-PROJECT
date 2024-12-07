import pyrebase

#firebase bağlantısı
firebaseConfig = { 'apiKey': "AIzaSyC2neSPwNwg_ZQxYzKcyoh6qPqlhNOlaH0",
  'authDomain': "comp303-project-3871f.firebaseapp.com",
  'databaseURL': "https://comp303-project-3871f-default-rtdb.firebaseio.com",
  'projectId': "comp303-project-3871f",
  'storageBucket': "comp303-project-3871f.firebasestorage.app",
  'messagingSenderId': "103364531587",
  'appId': "1:103364531587:web:e0ac5e619c0dc2fc6a92b6",
  'measurementId': "G-C61LSWEHR5"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def signup():
    email=input("Enter your email: ")
    password=input("Enter your password: ")
    user=auth.create_user_with_email_and_password(email, password)
    print("User created successfully")

signup()

    