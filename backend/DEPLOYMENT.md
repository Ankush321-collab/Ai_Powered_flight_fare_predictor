# Deployment Guide (Backend)

1) MongoDB Atlas
 - Create a free cluster, whitelist your IP or use 0.0.0.0/0 during testing.
 - Create database user and copy connection string to `MONGO_URI` in backend `.env`.

2) Railway / Render
 - Push repo to GitHub.
 - Create a new service on Railway or Render, connect GitHub repo.
 - Set environment variables: `MONGO_URI`, `OPENAI_API_KEY`, `PORT`.
 - Use `npm run start` as start command.

3) Environment
 - Ensure `OPENAI_API_KEY` is set for LLM features.
 - For scheduled jobs, either use Railway's cron or remote scheduler to call the scraper webhook.

Security notes
 - Never commit `.env` to repo.
 - Use minimal DB user permissions (readWrite only on the specific DB).
