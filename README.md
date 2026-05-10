# Founder Scraper

Extract founder names from business websites using AI-powered web scraping and OpenAI.

**Status**: ✅ Production ready  
**Cost**: $2/mo (VPS only)  
**Speed**: 15 websites in ~5 minutes  

---

## 🎯 What It Does

Scrapes business websites → extracts page content → analyzes with OpenAI GPT-4o-mini → outputs founder names with roles (Founder, Co-Founder, CEO, Owner, Co-Owner)

**Current Results**: 14 founder records extracted from 8/15 test websites (53% success rate)

---

## 🏗️ Architecture

```
Input URLs
    ↓
crawl4ai (web scraper → markdown text)
    ↓
VPS tinyproxy (IP rotation, reliability)
    ↓
OpenAI gpt-4o-mini (founder detection)
    ↓
CSV output (results.csv, failed.csv)
```

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <REPO_URL>
cd founder_scraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

**Copy `.env.example` to `.env` and add your OpenAI API key:**

```bash
OPENAI_API_KEY=sk-proj-your-key-here
```

### 3. Run

```bash
# Run all 15 test websites
python3 main.py

# Check results
cat output/results.csv
```

---

## 📁 Project Structure

```
founder_scraper/
├── main.py              # Orchestrator (20 parallel workers)
├── extractor.py         # crawl4ai web scraper
├── analyzer.py          # OpenAI founder detection
├── prompts.py           # System prompts for LLM
├── utils.py             # CSV utilities
├── requirements.txt     # Python dependencies
├── .env                 # API keys (DO NOT COMMIT)
├── CONTEXT.md           # Full technical documentation
│
├── input/
│   ├── test_websites.txt        # 15 test websites
│   └── failed_websites.txt      # Failed sites (auto-generated)
│
└── output/
    ├── results.csv              # Successful results
    └── failed.csv               # Failed websites
```

---

## 🔧 Configuration

### VPS Proxy (Optional but Recommended)

If using IP rotation through a VPS:

1. Edit `main.py` line 91:
   ```python
   extractor = WebsiteExtractor(
       timeout=45000,
       proxy="http://YOUR_VPS_IP:8888"
   )
   ```

2. Test proxy:
   ```bash
   curl -x http://YOUR_VPS_IP:8888 https://httpbin.org/ip
   ```

### API Keys

- **OpenAI**: Set `OPENAI_API_KEY` in `.env`
- Required model: `gpt-4o-mini` (cheap, fast, reliable)

---

## 📊 Current Results

From initial test run on 15 websites:

| Status | Count |
|--------|-------|
| Successful | 8/15 (53%) |
| Failed | 7/15 (47%) |
| Founders found | 14 |

**Successful sites**:
- clearmediagroup.ca, leaddogad.com, csrhub.com, dpcrowley.com, storyclicks.us, indigocollective.group, markworth.com, newtechadvertising.com

**Failed sites**:
- sherrondesign.com, zeritho.com, industrial-marketing-consultants.com, farrismarketing.com, kdrom.net, hellosmdigital.com, brightspectrum.net

See `output/results.csv` for full results.

---

## 🔄 How to Use

### Run Full Test
```bash
# main.py uses input/test_websites.txt by default
python3 main.py
```

### Re-run Failed Websites Only
```bash
# Edit main.py line 78:
# websites = load_websites("input/failed_websites.txt")
python3 main.py
```

### Add Your Own Websites
```bash
# Create input/my_websites.txt:
# https://example.com
# https://another.com
# ... one URL per line

# Edit main.py line 78:
# websites = load_websites("input/my_websites.txt")
python3 main.py
```

### Check Results
```bash
# View successful founders
cat output/results.csv

# View failed websites  
cat output/failed.csv

# Count results
wc -l output/results.csv
```

---

## 🛠️ Troubleshooting

### [NO TEXT] Error
- **Cause**: Website content not extracting
- **Solution**: 
  - Check if site has JavaScript-heavy content (crawl4ai handles this)
  - Verify proxy is working: `curl -x http://YOUR_IP:8888 https://httpbin.org/ip`
  - Increase timeout in `extractor.py` from 45s to 60s

### [NO PEOPLE] Error
- **Cause**: Text extracted but no founder keywords found
- **Solution**:
  - Site may not explicitly list founders
  - Edit `prompts.py` to improve the LLM prompt
  - Try manual analysis of the markdown output

### API Errors
- **Cause**: Invalid OpenAI key or model name
- **Solution**:
  - Verify `OPENAI_API_KEY` in `.env`
  - Check model name is `gpt-4o-mini` (not `gpt-4.1-nano`)
  - Test with: `python3 -c "import os; print(os.getenv('OPENAI_API_KEY'))"`

---

## 📦 Requirements

- Python 3.8+
- OpenAI API key (free tier $5 credit)
- ~50MB disk space
- Internet connection

---

## 💰 Cost Breakdown

| Item | Cost/Month | Notes |
|------|-----------|-------|
| VPS (tinyproxy) | $2 | Optional, for IP rotation |
| OpenAI API | $0.01-0.05 | ~$0.001 per site |
| **Total** | **~$2/mo** | Unlimited runs |

---

## 🚀 Next Steps

1. **Improve failed sites** by tweaking `prompts.py` system prompt
2. **Scale to production** with full website lists (100+, 1000+)
3. **Deploy to Railway** for automated daily runs
4. **Add Supabase** for database storage instead of CSV

See `CONTEXT.md` for full technical details.

---

## 📝 Team Collaboration

This repo is designed for team sharing. To add a teammate:

1. **GitHub**: Push to GitHub and share repo link
2. **Setup**: They clone and run `pip install -r requirements.txt`
3. **Config**: They add their own `OPENAI_API_KEY` to `.env`
4. **Run**: `python3 main.py`

`.env` is in `.gitignore` — each person uses their own key.

---

## 🔗 Related Docs

- **CONTEXT.md** — Full technical architecture, VPS setup, cost analysis
- **extractor.py** — crawl4ai configuration (timeout, proxy, wait modes)
- **analyzer.py** — OpenAI integration, allowed roles, validation
- **prompts.py** — System prompt tuning for better founder detection

---

## 📞 Support

For issues or questions:
- Check `CONTEXT.md` troubleshooting section
- Review error logs in terminal output
- Verify `.env` has valid `OPENAI_API_KEY`

---

**Version**: 1.0  
**Last Updated**: 2026-05-10  
**License**: MIT
