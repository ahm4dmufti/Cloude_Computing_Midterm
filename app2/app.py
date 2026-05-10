from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DevOpsHub – Dashboard</title>
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

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 32px;
    }}

    h1 {{
      font-size: 26px;
      color: #fff;
      font-weight: 700;
    }}

    .live-badge {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(46,213,115,0.15);
      border: 1px solid rgba(46,213,115,0.3);
      border-radius: 20px;
      padding: 4px 12px;
      font-size: 11.5px;
      color: #2ed573;
      font-weight: 600;
    }}

    .live-dot {{
      width: 7px; height: 7px;
      background: #2ed573;
      border-radius: 50%;
      animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(1.4); }}
    }}

    .stats {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 28px;
    }}

    .stat-card {{
      border-radius: 12px;
      padding: 20px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .stat-card.messages {{
      background: rgba(52,152,219,0.15);
      border: 1px solid rgba(52,152,219,0.25);
    }}

    .stat-card.visits {{
      background: rgba(233,69,96,0.15);
      border: 1px solid rgba(233,69,96,0.25);
    }}

    .stat-label {{
      font-size: 13px;
      color: rgba(255,255,255,0.55);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      font-weight: 600;
    }}

    .stat-desc {{
      font-size: 12px;
      color: rgba(255,255,255,0.3);
    }}

    .stat-value {{
      font-size: 48px;
      font-weight: 800;
      line-height: 1;
    }}

    .stat-card.messages .stat-value {{ color: #3498db; }}
    .stat-card.visits   .stat-value {{ color: #e94560; }}

    .divider {{
      height: 1px;
      background: rgba(255,255,255,0.07);
      margin-bottom: 20px;
    }}

    .footer {{
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
    <div class="card-header">
      <h1>Dashboard</h1>
      <div class="live-badge">
        <div class="live-dot"></div>
        LIVE
      </div>
    </div>

    <div class="stats">
      <div class="stat-card messages">
        <div>
          <div class="stat-label">Messages Collected</div>
          <div class="stat-desc">Total submitted via App 1</div>
        </div>
        <div class="stat-value">{messages}</div>
      </div>

      <div class="stat-card visits">
        <div>
          <div class="stat-label">Page Visits</div>
          <div class="stat-desc">Total loads of App 1</div>
        </div>
        <div class="stat-value">{visits}</div>
      </div>
    </div>

    <div class="divider"></div>
    <p class="footer">Refreshes on every load &nbsp;·&nbsp; Data stored in Redis &nbsp;·&nbsp;
      <a href="http://localhost:5000">Go to Collector &rarr;</a></p>
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
