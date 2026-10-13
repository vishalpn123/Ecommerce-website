# goCart — Full-Stack E-commerce Website

Portfolio project using **React + Vite**, **FastAPI**, **SQLAlchemy**, and **SQLite locally / PostgreSQL optionally**. Features account registration and login, JWT-protected API, product search and category filters, persistent per-user cart, inventory checks, order creation/history, and admin-only product CRUD endpoints.

> This is an educational portfolio starter, not a production store. Checkout creates a pending order only; no payment is collected. Never store card data or commit secrets.

## Run locally

### Backend (Python 3.11+)
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Optional: copy .env.example to .env and change JWT_SECRET
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000 · Interactive docs: http://127.0.0.1:8000/docs
Default database is SQLite and sample products are seeded automatically. For PostgreSQL set `DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/gocart` in `backend/.env`.

### Frontend (second terminal, Node.js 18+)
```bash
cd frontend
npm install
npm run dev
```
Open the URL Vite prints, normally http://localhost:5173.

## Demo
Register a test account, sign in, browse products, add to cart, and place a demo order. JWT is saved in browser local storage for this learning demo. Do not use this storage pattern as a blanket production recommendation; evaluate secure, HttpOnly cookie sessions for deployed apps.

## Admin products
New users are customers. To test admin routes locally, set that user's `is_admin` column to `1` in the SQLite `gocart.db` database using a database viewer. Never expose public admin self-registration.

## Key API routes
- `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- `GET /api/products?q=&category=&sort=`, `GET /api/products/{id}`
- `POST /api/products`, `PUT /api/products/{id}`, `DELETE /api/products/{id}` (admin)
- `GET /api/cart`, `POST /api/cart/items`, `PATCH /api/cart/items/{product_id}`, `DELETE /api/cart/items/{product_id}`
- `POST /api/orders`, `GET /api/orders`, `GET /api/health`

## GitHub
```bash
git init
git add .
git commit -m "Build goCart full-stack e-commerce website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/goCart.git
git push -u origin main
```

## Strong next steps for a production-quality portfolio
- Add Alembic migrations, tests, GitHub Actions CI, and deployment
- Use environment-managed JWT secrets, rate limiting, email verification and password reset
- Add admin dashboard, order status management, shipping/tax rules and inventory locking
- Integrate hosted checkout (e.g. Razorpay/Stripe test mode) and verify webhooks server-side
- Add screenshots, architecture diagram, API docs, and a short demo video to README

## License 
Free and open-source. For academic/educational use at New Technology Career Solutions.
