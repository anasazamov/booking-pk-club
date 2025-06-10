<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>PC-Club Booking Backend</title>
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
    h1, h2, h3 { color: #333; }
    pre { background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }
    code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }
    ul { margin-left: 20px; }
    table { border-collapse: collapse; width: 100%; margin: 10px 0; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    th { background: #eee; }
  </style>
</head>
<body>
  <h1>PC-Club Booking Backend</h1>
  <p>Bu loyiha — kompyuter klubi o‘rnini bron qilish tizimi backend qismi.</p>

  <h2>📁 Loyihaning tuzilishi</h2>
  <pre><code>
booking-pk-club/
├── alembic/
│   └── versions/
├── core/
│   ├── api/           FastAPI router’lari
│   │   └── v1/
│   ├── crud/          CRUD-funktsiyalar
│   ├── database/      DB helper va model’lar
│   ├── schemas/       Pydantic sxemalar
│   ├── services/      auth, OTP-servis
│   └── tasks/         Celery vazifalari
├── tests/             pytest testlari
├── Dockerfile
├── docker-compose.yml
├── main.py            FastAPI entry-point
├── README.md
└── requirements.txt
  </code></pre>

  <h2>🚀 Texnologiyalar</h2>
  <ul>
    <li>Python 3.11+</li>
    <li>FastAPI</li>
    <li>SQLAlchemy (async) + Alembic</li>
    <li>PostgreSQL (prod), SQLite (test)</li>
    <li>Celery + Redis</li>
    <li>JWT (python-jose) + passlib/bcrypt</li>
    <li>Pydantic v2</li>
    <li>Docker & docker-compose</li>
    <li>pytest & httpx</li>
  </ul>

  <h2>🗄️ Model’lar qisqacha</h2>
  <table>
    <tr><th>Model</th><th>Asosiy maydonlar</th></tr>
    <tr><td><code>User</code></td><td>id, first_name, last_name, phone_number, password_hash, is_active, is_verified, role, balance, created_at, updated_at</td></tr>
    <tr><td><code>Branch</code></td><td>id, name, address</td></tr>
    <tr><td><code>Zone</code></td><td>id, branch_id, name</td></tr>
    <tr><td><code>Place</code></td><td>id, zone_id, name</td></tr>
    <tr><td><code>Booking</code></td><td>id, user_id, place_id, start_datetime, end_datetime, status, amount, idempotency_key, created_at, updated_at</td></tr>
    <tr><td><code>BalanceTransaction</code></td><td>id, user_id, booking_id, type, amount, idempotency_key, created_at</td></tr>
  </table>

  <h2>🛠️ Ishga tushirish</h2>
  <ol>
    <li><strong>Klon qiling:</strong>
      <pre><code>git clone &lt;repo_url&gt; booking-pk-club
cd booking-pk-club</code></pre>
    </li>
    <li><strong>`.env` faylini yarating:</strong>
      <pre><code>ENV=development
DEBUG=true
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/booking
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=1440
REFRESH_TOKEN_EXPIRE_DAYS=7
OTP_EXPIRE_MINUTES=5
SMS_AUTH_URL=https://notify.eskiz.uz/api/auth/login
SMS_SEND_URL=https://notify.eskiz.uz/api/message/sms/send
SMS_USERNAME=your_eskiz_user
SMS_PASSWORD=your_eskiz_pass
SMS_SENDER=BookingClub
ICAFE_API_URL=https://dev.icafecloud.com/api
ICAFE_API_KEY=...
ICAFE_API_SECRET=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
</code></pre>
    </li>
    <li><strong>Docker-kompazini ishga tushiring:</strong>
      <pre><code>docker-compose up --build -d</code></pre>
    </li>
    <li><strong>Migratsiyalarni qo‘llang:</strong>
      <pre><code>docker-compose exec web alembic upgrade head</code></pre>
    </li>
    <li><strong>Swagger UI:</strong> <a href="http://localhost/docs">http://localhost/docs</a></li>
  </ol>

  <h2>📑 API End-pointlar</h2>
  <h3>🔐 Auth</h3>
  <ul>
    <li><code>POST /auth/register</code></li>
    <li><code>POST /auth/verify</code></li>
    <li><code>POST /auth/login</code></li>
    <li><code>POST /auth/refresh</code></li>
    <li><code>POST /auth/otp</code></li>
  </ul>

  <h3>👤 Users</h3>
  <ul>
    <li><code>GET /users</code></li>
    <li><code>GET /users/{id}</code></li>
    <li><code>PATCH /users/{id}</code></li>
  </ul>

  <h3>🏢 Branches/Zones/Places</h3>
  <ul>
    <li><code>GET /branches</code>, <code>POST /branches</code>, <code>PUT /branches/{id}</code>, <code>DELETE /branches/{id}</code></li>
    <li><code>GET /zones?branch_id={id}</code>, <code>POST /zones</code>, <code>PUT /zones/{id}</code>, <code>DELETE /zones/{id}</code></li>
    <li><code>GET /places?zone_id={id}</code>, <code>POST /places</code>, <code>PUT /places/{id}</code>, <code>DELETE /places/{id}</code></li>
  </ul>

  <h3>🪑 Bookings</h3>
  <ul>
    <li><code>POST /bookings</code></li>
    <li><code>GET /bookings</code></li>
    <li><code>PATCH /bookings/{id}</code></li>
    <li><code>DELETE /bookings/{id}</code></li>
  </ul>

  <h3>💰 Balance</h3>
  <ul>
    <li><code>GET /balance</code></li>
    <li><code>POST /balance/topup</code></li>
  </ul>

  <h3>📜 Transactions</h3>
  <ul>
    <li><code>GET /transactions</code></li>
  </ul>

  <h2>✅ Testlar</h2>
  <p>Asinxron pytest + httpx yordamida barcha endpointlar testlandi, shuningdek load-test skript mavjud.</p>
  <pre><code>pytest -q
python tests/test_api.py  # load-test</code></pre>

  <hr/>
  <p>© 2025 PC-Club Booking</p>
</body>
</html>
