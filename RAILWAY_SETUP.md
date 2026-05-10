# Railway Deployment Guide

Deploy founder_scraper to Railway for 24/7 scraping with automatic GitHub sync.

---

## 🚀 Quick Setup (5 minutes)

### 1. Push to GitHub

```bash
cd /Users/krishnaraj/Downloads/founder_scraper
git remote add origin https://github.com/YOUR_USERNAME/founder-scraper.git
git push -u origin main
```

### 2. Connect to Railway

1. Go to https://railway.app
2. Sign in with GitHub
3. Create new project
4. Select "Deploy from GitHub repo"
5. Choose `founder-scraper` repo
6. Railway auto-detects Dockerfile

### 3. Set Environment Variables

In Railway dashboard:
- Go to **Variables** tab
- Add `OPENAI_API_KEY` = your OpenAI key
- Add `INPUT_FILE` = `input/test_websites.txt` (or `input/failed_websites.txt`)

### 4. Deploy

- Railway auto-deploys on git push
- View logs in **Logs** tab
- Scraper runs continuously, exits when done

---

## 📊 How It Works

```
GitHub repo
    ↓ (automatic sync)
Railway builder
    ↓
Docker container (Dockerfile)
    ↓
main.py runs
    ↓
Rotating proxies (VPS + ProxyMesh + Direct)
    ↓
OpenAI API
    ↓
output/results.csv
```

---

## ⚙️ Configuration

### Input File
- `input/test_websites.txt` — 15 test websites (default)
- `input/failed_websites.txt` — retry only failed sites
- `input/your_websites.txt` — your own list

Set via `INPUT_FILE` environment variable in Railway.

### Proxy Rotation
Automatically cycles through:
1. **VPS tinyproxy** — 107.173.47.31:8888 ($2/mo)
2. **ProxyMesh** — us-ca.proxymesh.com:31280 (10GB/mo)
3. **Direct IP** — datacenter, no rotation

Each request uses next proxy in cycle.

### Concurrency
- Default: 20 parallel workers
- Adjust in `main.py` line 14: `CONCURRENCY = 20`

---

## 📈 Monitoring

### View Logs
```bash
# In Railway dashboard: Logs tab
# Or via CLI:
railway logs --tail
```

### Check Results
- Results stored in `output/results.csv`
- Use Railway **File Explorer** or pull via:
  ```bash
  railway run cat output/results.csv
  ```

### Metrics
- Websites scraped: Check logs for `[SCRAPING]` count
- Success rate: `[SUCCESS]` / total
- Failed sites: Listed in `output/failed.csv`

---

## 🔄 Continuous Runs

### Option A: One-time execution
- Railway runs scraper once
- Exits when all websites processed
- Restart manually via dashboard

### Option B: Scheduled runs (every 24h)
```bash
# Use Cron jobs in Railway (paid feature)
# Or deploy with cron wrapper:
# while true; do python3 main.py; sleep 86400; done
```

### Option C: Manual batch runs
```bash
# Via Railway CLI:
railway run python3 main.py

# Edit input file between runs:
# input/test_websites.txt → more URLs
# Push to GitHub, redeploy
```

---

## 🛠️ Troubleshooting

### Scraper exits immediately
- Check `INPUT_FILE` exists in `input/`
- View logs: "Remaining websites: 0"
- Solution: Add URLs to `input/test_websites.txt`

### API key error
- Verify `OPENAI_API_KEY` in Railway Variables
- Test locally: `python3 main.py` with `.env` file
- Check key validity: https://platform.openai.com/api-keys

### Low success rate
- Check proxy rotation in logs: `[SCRAPING] ... (proxy: ...)`
- ProxyMesh may be hitting bandwidth limit (10GB/mo)
- VPS may be down (test: `curl http://107.173.47.31:8888`)
- Direct IP may be blocked by sites

### Out of memory
- Reduce `CONCURRENCY` from 20 to 5-10
- Edit `main.py` line 14
- Redeploy

---

## 📦 Production Checklist

- [ ] OpenAI API key added to Railway Variables
- [ ] INPUT_FILE set correctly
- [ ] GitHub repo public (for Railway to access)
- [ ] Dockerfile builds successfully
- [ ] Test run on 5 websites first
- [ ] Monitor logs for [SUCCESS] entries
- [ ] Check `output/results.csv` for results

---

## 💰 Cost Estimation

| Service | Cost/Month |
|---------|-----------|
| Railway (hobby tier) | $5 (free for small apps) |
| VPS tinyproxy | $2 |
| ProxyMesh 10GB | $10 |
| OpenAI API | $0.01-0.05 per 100 sites |
| **Total** | **~$17/mo** |

*Note: Railway hobby tier is free for first 100 hours/month (~3 hours/day)*

---

## 🚀 Scaling

To scale scraping:

1. **Increase concurrency**: `CONCURRENCY = 50` (Railway memory allows)
2. **Add more proxies**: Edit `main.py` line 19 PROXIES list
3. **Buy more VPS**: Add IPs to rotation
4. **Upgrade ProxyMesh**: Buy higher tier (50GB, 100GB)

---

## 📞 Support

- Railway docs: https://docs.railway.app
- For scraper issues: Check CONTEXT.md
- For proxy issues: Test locally with `curl`

---

**Version**: 1.0  
**Last Updated**: 2026-05-11
