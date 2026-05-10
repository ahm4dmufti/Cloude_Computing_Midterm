from flask import Flask, request, redirect, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DevOpsHub – Feedback</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: "Segoe UI", Arial, sans-serif;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 30px 16px;
    }}

    .logo {{
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 3px;
      color: #e94560;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}

    .card {{
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 40px 44px;
      width: 100%;
      max-width: 520px;
      box-shadow: 0 24px 60px rgba(0,0,0,0.4);
    }}

    h1 {{
      font-size: 26px;
      color: #fff;
      margin-bottom: 6px;
      font-weight: 700;
    }}

    .subtitle {{
      font-size: 13.5px;
      color: rgba(255,255,255,0.45);
      margin-bottom: 28px;
    }}

    .visits-bar {{
      display: flex;
      align-items: center;
      gap: 10px;
      background: rgba(233,69,96,0.15);
      border: 1px solid rgba(233,69,96,0.3);
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 28px;
    }}

    .visits-dot {{
      width: 8px; height: 8px;
      background: #e94560;
      border-radius: 50%;
      animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.5; transform: scale(1.3); }}
    }}

    .visits-text {{
      font-size: 13px;
      color: rgba(255,255,255,0.7);
    }}

    .visits-text strong {{
      color: #e94560;
      font-size: 15px;
    }}

    label {{
      display: block;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: rgba(255,255,255,0.5);
      margin-bottom: 8px;
    }}

    textarea {{
      width: 100%;
      background: rgba(255,255,255,0.07);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 10px;
      padding: 14px 16px;
      font-size: 14px;
      color: #fff;
      resize: vertical;
      outline: none;
      transition: border-color 0.2s;
      font-family: inherit;
    }}

    textarea::placeholder {{ color: rgba(255,255,255,0.25); }}

    textarea:focus {{ border-color: #e94560; }}

    button {{
      margin-top: 18px;
      width: 100%;
      padding: 14px;
      background: #e94560;
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      letter-spacing: 0.5px;
      transition: background 0.2s, transform 0.1s;
    }}

    button:hover {{ background: #c73652; }}
    button:active {{ transform: scale(0.98); }}

    .footer {{
      margin-top: 20px;
      font-size: 11.5px;
      color: rgba(255,255,255,0.25);
      text-align: center;
    }}

    .footer a {{ color: #e94560; text-decoration: none; }}
  </style>
</head>
<body>
  <div class="logo">DevOpsHub</div>
  <div class="card">
    <h1>Share Your Feedback</h1>
    <p class="subtitle">Your message goes straight to our team via Redis.</p>

    <div class="visits-bar">
      <div class="visits-dot"></div>
      <span class="visits-text">Page visited <strong>{visits}</strong> time(s) since launch</span>
    </div>

    <form method="POST" action="/submit">
      <label for="msg">Your Message</label>
      <textarea id="msg" name="message" rows="5"
        placeholder="Write your feedback, suggestion or comment here..." required></textarea>
      <button type="submit">Send Message &rarr;</button>
    </form>

    <p class="footer">View stats on the <a href="http://localhost:5001">Dashboard &rarr;</a></p>
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
