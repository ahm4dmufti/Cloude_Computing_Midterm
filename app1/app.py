from flask import Flask, request, redirect, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Message Collector</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 60px auto; background: #f4f6f9; }}
    .card {{ background: white; padding: 32px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    h1 {{ color: #2c3e50; margin-bottom: 4px; }}
    .badge {{ display: inline-block; background: #3498db; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; margin-bottom: 24px; }}
    textarea {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; font-size: 15px; box-sizing: border-box; }}
    button {{ margin-top: 12px; padding: 10px 28px; background: #2ecc71; color: white; border: none; border-radius: 6px; font-size: 15px; cursor: pointer; }}
    button:hover {{ background: #27ae60; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>DevOpsHub Feedback</h1>
    <span class="badge">Page visits: {visits}</span>
    <form method="POST" action="/submit">
      <textarea name="message" rows="4" placeholder="Enter your message, feedback or suggestion..." required></textarea>
      <br>
      <button type="submit">Submit Message</button>
    </form>
  </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    visits = r.incr('visit_count')
    return HTML.format(visits=visits)

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form.get('message', '').strip()
    if message:
        r.rpush('messages', message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
