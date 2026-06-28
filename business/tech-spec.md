# test‑wright Technical Specification – v1

---

## 1. Stack

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| **Runtime** | Node.js | 20.x LTS | Mature ecosystem, native ES modules, excellent async I/O |
| **Language** | TypeScript | 5.4 | Strong typing for safety, auto‑completion, and future‑proofing |
| **Web Framework** | Express.js | 4.18 | Minimal, battle‑tested, easy to extend with middleware |
| **Testing Engine** | Jest | 29.x | Built‑in snapshot support, parallel workers, good TypeScript integration |
| **AI Integration** | OpenAI SDK | 4.x | Native support for GPT‑4, fine‑tuned prompts for test generation |
| **Database** | PostgreSQL | 15.x | ACID, JSONB support for test metadata, open‑source |
| **ORM** | Prisma | 5.x | Type‑safe, auto‑generated client, migration tooling |
| **Container Runtime** | Docker | 25.x | Reproducible builds, easy deployment to any cloud |
| **CI/CD** | GitHub Actions | – | Native to repo, free for public, supports self‑hosted runners |
| **Observability** | OpenTelemetry | 1.26 | Unified tracing, metrics, and logs |
| **Monitoring** | Prometheus + Grafana | – | Time‑series metrics, alerting |
| **Logging** | Loki + Grafana | – | Structured logs, easy query via Grafana |

> **Why this stack?**  
> • Node/TS gives us rapid iteration and a huge ecosystem.  
> • Express + Jest are industry standards for REST APIs and unit testing.  
> • PostgreSQL + Prisma provide a type‑safe data layer with powerful JSON support for test artifacts.  
> • Docker + GitHub Actions keep the build pipeline simple and reproducible.  
> • OpenTelemetry + Prometheus/Grafana give us a single observability stack that scales from local dev to production.

---

## 2. Hosting

| Platform | Tier | Key Features | Why |
|----------|------|--------------|-----|
| **Render** | Free | Static sites, web services, PostgreSQL, auto‑deploy from GitHub | First‑tier free, instant HTTPS, automatic scaling |
| **Fly.io** | Free | Global edge, Docker support, PostgreSQL add‑on | Low latency for dev teams worldwide |
| **Railway** | Free | One‑click Postgres, Docker, environment variables | Quick prototyping, built‑in CI integration |

> **Deployment Flow**  
> 1. Docker image built via GitHub Actions.  
> 2. Pushed to Render’s container registry.  
> 3. Render auto‑deploys to the free tier.  
> 4. Fly.io or Railway used for staging or edge‑optimized deployments.

---

## 3. Data Model

> All tables are in a single `public` schema. Primary keys are UUIDs.  
> Timestamps are UTC, `created_at` & `updated_at` are automatically populated.

| Table | Key Fields | Description |
|-------|------------|-------------|
| **users** | `id` (PK), `email`, `password_hash`, `role`, `created_at`, `updated_at` | Authenticated developers. `role` can be `admin` or `user`. |
| **projects** | `id` (PK), `user_id` (FK), `name`, `description`, `created_at`, `updated_at` | Logical grouping of tests. |
| **tests** | `id` (PK), `project_id` (FK), `name`, `description`, `prompt_template` (JSONB), `created_at`, `updated_at` | Test definitions that drive AI generation. |
| **test_runs** | `id` (PK), `test_id` (FK), `status` (`queued`, `running`, `completed`, `failed`), `started_at`, `ended_at`, `metadata` (JSONB) | Execution records. |
| **results** | `id` (PK), `run_id` (FK), `output` (JSONB), `score` (numeric), `created_at` | AI‑generated test output and evaluation. |
| **audit_logs** | `id` (PK), `user_id` (FK), `action`, `entity`, `entity_id`, `timestamp` | Immutable audit trail. |

> **Indexes**  
> • `users.email` unique.  
> • `projects.user_id`.  
> • `tests.project_id`.  
> • `test_runs.test_id`.  
> • `results.run_id`.

---

## 4. API Surface

| Method | Path | Purpose | Auth | Notes |
|--------|------|---------|------|-------|
| POST | `/auth/signup` | Create new user | None | Returns JWT |
| POST | `/auth/login` | Login | None | Returns JWT |
| GET | `/projects` | List user’s projects | JWT | Pagination |
| POST | `/projects` | Create project | JWT | |
| GET | `/projects/:id` | Get project details | JWT | |
| DELETE | `/projects/:id` | Delete project | JWT | Soft delete |
| POST | `/projects/:id/tests` | Create test | JWT | Accepts `prompt_template` |
| GET | `/projects/:id/tests` | List tests | JWT | |
| GET | `/tests/:id` | Get test definition | JWT | |
| POST | `/tests/:id/run` | Trigger AI test run | JWT | Returns run ID |
| GET | `/runs/:id` | Get run status | JWT | Polling endpoint |
| GET | `/runs/:id/results` | Get run results | JWT | |
| GET | `/metrics` | Prometheus scrape endpoint | None | Exposes internal metrics |
| POST | `/webhooks/test-completed` | Receive async completion | HMAC | For CI integration |

> **Rate Limiting** – 100 req/min per user, enforced via Redis.  
> **Pagination** – `limit`/`offset` query params, default 20/0.  
> **Error Handling** – Standard JSON `{error: string, code: number}`.

---

## 5. Security Model

| Area | Implementation |
|------|----------------|
| **Auth** | JWT signed with HS256, 15‑min expiry, refresh token (30‑day) |
| **Secrets** | Stored in Render/Fly.io env vars, accessed via `process.env` |
| **IAM** | Role‑based access control: `admin` can view all projects, `user` only own |
| **Transport** | TLS everywhere (HTTPS enforced) |
| **Data at Rest** | PostgreSQL encrypted via `pgcrypto` for sensitive fields |
| **API Security** | CSRF protection on state‑changing endpoints, CORS restricted to known domains |
| **Audit** | Immutable `audit_logs` table, write‑only via trigger |
| **HMAC** | Webhook payloads signed with shared secret, verified in `/webhooks/test-completed` |

> **Compliance** – Meets SOC 2 Type II baseline (encryption, audit, access control).

---

## 6. Observability

| Category | Tool | Metrics/Logs |
|----------|------|--------------|
| **Tracing** | OpenTelemetry (Node SDK) | Span for each request, AI call, DB query |
| **Metrics** | Prometheus | `http_requests_total`, `db_query_duration_seconds`, `ai_response_time_seconds`, `test_run_duration_seconds`, `error_rate` |
| **Logs** | Loki | Structured JSON logs (`level`, `msg`, `request_id`) |
| **Dashboards** | Grafana | Service health, latency, error rates, AI cost per run |
| **Alerting** | Prometheus Alertmanager | `high_error_rate`, `high_latency`, `db_connection_failures` |
| **Tracing UI** | Jaeger (optional) | Visual trace exploration |

> **Cost Control** – AI usage logged with `ai_cost_usd`; alerts if monthly spend > $200.

---

## 7. Build / CI

| Stage | Tool | Action |
|-------|------|--------|
| **Lint** | ESLint + Prettier | `npm run lint` |
| **Type Check** | TypeScript | `npm run type-check` |
| **Unit Tests** | Jest | `npm test` (coverage ≥ 80%) |
| **Integration Tests** | Jest + Supertest | `npm run test:integration` |
| **Static Analysis** | SonarCloud | Pull‑request scan |
| **Docker Build** | Dockerfile | `docker build -t test-wright:${{ github.sha }} .` |
| **Push** | Docker Hub / Render Registry | `docker push` |
| **Deploy** | Render CLI | `render deploy` |
| **Release** | Semantic Release | Auto‑bump, changelog, tag |
| **Post‑Deploy Smoke** | Cypress | End‑to‑end smoke test on staging |

> **GitHub Actions Workflow**  
> ```yaml
> name: CI
> on: [push, pull_request]
> jobs:
>   build:
>     runs-on: ubuntu-latest
>     steps:
>       - uses: actions/checkout@v4
>       - uses: actions/setup-node@v4
>         with: { node-version: 20 }
>       - run: npm ci
>       - run: npm run lint
>       - run: npm run type-check
>       - run: npm test -- --coverage
>       - run: docker build -t test-wright:${{ github.sha }} .
>       - run: docker push test-wright:${{ github.sha }}
> ```

> **Self‑hosted Runners** – For AI cost control, we run the `ai-runner` job on a dedicated GPU instance (AWS G4dn.xlarge) to avoid hitting public rate limits.

---

**End of v1 Technical Specification**