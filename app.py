from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample dataset
emails = [
    "Dear user, your account has been compromised. Click here to reset your password.",
    "Win a $1000 gift card now! Click here to claim your prize.",
    "Your Amazon order has been shipped. Track your package here.",
    "Congratulations! You've won a free vacation. Click to claim now.",
    "Your bank account has been suspended. Please verify your identity.",
    "Meeting at 10 AM tomorrow. Please confirm your attendance.",
    "Your subscription has been renewed successfully.",
    "Reminder: Your appointment is scheduled for next week.",
    "Thank you for your purchase. Your order will be delivered soon.",
    "Join us for a webinar on data science next week."
]

labels = [1, 1, 0, 1, 1, 0, 0, 0, 0, 0]  # 1 for phishing, 0 for non-phishing

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(emails, labels, test_size=0.2, random_state=42)

# Create a pipeline with a CountVectorizer and MultinomialNB
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Sample names and times
names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Davis"]

def random_name(email_id):
    return random.choice(names)

def random_time(email_id):
    now = datetime.now()
    time_diff = timedelta(minutes=random.randint(0, 120))
    email_time = now - time_diff
    return email_time.strftime('%Y-%m-%d %H:%M')

@app.route('/')
def index():
    return render_template('index.html', emails=emails, enumerate=enumerate, random_name=random_name, random_time=random_time)

@app.route('/email/<int:email_id>')
def email_detail(email_id):
    email_text = emails[email_id]
    prediction = model.predict([email_text])[0]
    if prediction == 1:
        return render_template('phishing_warning.html', email=email_text)
    else:
        return render_template('email_detail.html', email=email_text)

if __name__ == '__main__':
    app.run(debug=True)
