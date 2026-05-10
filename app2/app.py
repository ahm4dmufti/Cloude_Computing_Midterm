from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>DevOpsHub Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 60px auto; background: #f4f6f9; }}
    .card {{ background: white; padding: 32px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
    h1 {{ color: #2c3e50; margin-bottom: 24px; }}
    .stat {{ display: flex; justify-content: space-between; align-items: center; padding: 16px 0; border-bottom: 1px solid #eee; }}
    .stat:last-child {{ border-bottom: none; }}
    .label {{ font-size: 16px; color: #555; }}
    .value {{ font-size: 28px; font-weight: bold; color: #3498db; }}
    .footer {{ margin-top: 16px; font-size: 12px; color: #aaa; text-align: right; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Dashboard</h1>
    <div class="stat">
      <span class="label">Total Messages Collected</span>
      <span class="value">{messages}</span>
    </div>
    <div class="stat">
      <span class="label">Total Page Visits (App 1)</span>
      <span class="value">{visits}</span>
    </div>
    <p class="footer">Data refreshes on every page load</p>
  </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
    messages = r.llen('messages')
    visits = r.get('visit_count') or 0
    return HTML.format(messages=messages, visits=visits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
