# Founder Scraper - Complete Context & Setup Guide

**Last Updated**: 2026-05-10  
**Status**: ✅ Live & Working  
**Team**: Shareable with team via GitHub

---

## 🚀 Quick Start

```bash
cd /Users/krishnaraj/Downloads/founder_scraper
python3 main.py
```

---

## 📋 Project Overview

**What**: Extract founder names from business websites using AI  
**Why**: Build founder lists for outreach campaigns  
**Cost**: $2/mo (VPS only)  
**Speed**: 15 websites in ~5 minutes

---

## 🏗️ Architecture

```
Website URLs (input/test_websites.txt)
    ↓
crawl4ai (extract page content)
    ↓
VPS tinyproxy (proxy rotation)
    ↓
OpenAI gpt-4o-mini (extract founders)
    ↓
CSV output (results.csv, failed.csv)
```

---

## 🖥️ VPS Setup (Tinyproxy Proxy Server)

| Item | Value |
|------|-------|
| **IP Address** | 107.173.47.31 |
| **Username** | root |
| **Password** | HqD3r5us76 |
| **Proxy Port** | 8888 |
| **Service** | tinyproxy (HTTP/SOCKS proxy) |
| **Status** | ✅ LIVE & Running |
| **Uptime** | 4+ hours |
| **Cost** | $2/mo |
| **OS** | AlmaLinux 10.1 |
| **Specs** | 1 CPU, 3GB RAM, 30GB SSD |

**Test proxy:**
```bash
curl -x http://107.173.47.31:8888 https://httpbin.org/ip
```

---

## 🔧 Core Components

### 1. Web Scraper (`extractor.py`)
- **Tool**: crawl4ai (async web scraper)
- **Function**: Extract text from websites
- **Timeout**: 45 seconds
- **Proxy**: Routes through VPS tinyproxy
- **Output**: Raw markdown text

### 2. AI Analyzer (`analyzer.py`)
- **Tool**: OpenAI gpt-4o-mini
- **Function**: Extract founder names from text
- **Keywords**: founder, co-founder, ceo, owner, co-owner
- **Cost**: ~$0.01-0.05 per 100 sites

### 3. Orchestrator (`main.py`)
- **Function**: Manage scraping pipeline
- **Concurrency**: 20 parallel workers
- **Input**: `input/test_websites.txt` or `input/failed_websites.txt`
- **Output**: `output/results.csv`, `output/failed.csv`

### 4. Utilities (`utils.py`)
- Load/save CSV files
- Track completed websites
- Handle errors gracefully

---

## 🔑 API Keys & Credentials

### OpenAI
```
Key: sk-proj-YOUR-KEY-HERE
Model: gpt-4o-mini (cheap, fast)
Location: .env file (already configured)
```

---

## 📁 File Structure

```
founder_scraper/
├── main.py              # Main scraper script
├── extractor.py         # crawl4ai text extraction
├── analyzer.py          # OpenAI founder detection
├── utils.py             # CSV & utility functions
├── prompts.py           # OpenAI system prompts
├── requirements.txt     # Python dependencies
├── .env                 # API keys (KEEP PRIVATE)
├── CONTEXT.md           # This file
│
├── input/
│   ├── test_websites.txt        # 15 test websites
│   └── failed_websites.txt      # 9 failed websites (auto-generated)
│
└── output/
    ├── results.csv              # Successful results
    └── failed.csv               # Failed websites
```

---

## 🎯 Current Status

### Results So Far
- **Total processed**: 15 websites
- **Successful**: 8/15 (53%)
- **Failed**: 7/15 (47%)
- **Founder records extracted**: 14

### Successful Sites
✅ clearmediagroup.ca  
✅ leaddogad.com (4 founders)  
✅ csrhub.com  
✅ dpcrowley.com  
✅ storyclicks.us  
✅ indigocollective.group  
✅ markworth.com  
✅ newtechadvertising.com  

### Failed Sites (Need Investigation)
❌ sherrondesign.com  
❌ zeritho.com  
❌ industrial-marketing-consultants.com  
❌ farrismarketing.com  
❌ kdrom.net  
❌ hellosmdigital.com  
❌ brightspectrum.net  

---

## 🔄 How to Run

### Run Full 15 Websites
```bash
# Edit main.py line 78:
# websites = load_websites("input/test_websites.txt")

python3 main.py
```

### Re-run Failed Websites Only
```bash
# main.py line 78:
# websites = load_websites("input/failed_websites.txt")

python3 main.py
```

### Check Results
```bash
cat output/results.csv       # View successful founders
cat output/failed.csv        # View failed websites
wc -l output/results.csv     # Count results
```

---

## 🛠️ Recent Fixes & Changes

| Date | Fix | Impact |
|------|-----|--------|
| 2026-05-10 | Replaced Playwright with crawl4ai | ✅ Better text extraction |
| 2026-05-10 | Fixed model: `gpt-4.1-nano` → `gpt-4o-mini` | ✅ Valid OpenAI model |
| 2026-05-10 | Added VPS proxy support | ✅ IP rotation + reliability |
| 2026-05-10 | Increased timeout: 30s → 45s | ✅ Handles slow sites |
| 2026-05-10 | Changed wait mode: `domcontentloaded` → `networkidle` | ✅ JS rendering |
| 2026-05-10 | Updated API key to team key | ✅ Using shared credentials |

---

## 📊 Cost Breakdown

| Service | Cost/Month | Notes |
|---------|-----------|-------|
| VPS (107.173.47.31) | $2 | Includes tinyproxy |
| OpenAI API | $0.01-0.05 | ~$0.001 per site |
| **Total** | **~$2/mo** | Unlimited runs |

---

## 🔍 Troubleshooting

### [NO TEXT] Error
- Site's content not extracting
- Check: JavaScript-heavy sites, blocked access, timeout too short
- Solution: Try crawl4ai directly: `curl -x http://107.173.47.31:8888 <url>`

### [NO PEOPLE] Error
- Text extracted but no founder keywords found
- Check: Site doesn't list founders explicitly
- Solution: Improve `prompts.py` system prompt

### [TIMEOUT] Error
- VPS proxy unreachable or hanging
- Check: `sshpass -p 'HqD3r5us76' ssh root@107.173.47.31 "systemctl status tinyproxy"`
- Solution: Restart proxy or increase timeout

---

## 🚀 Next Steps

1. **Re-run failed websites** (7 sites) with improved prompt
2. **Scale to production** (full website lists)
3. **Deploy to Railway** for automated daily runs
4. **Add Supabase integration** for database storage
5. **Create GitHub repo** for team collaboration

---

## 📞 Team Notes

**Shared with**: [Add team members here]  
**Last run**: 2026-05-10 10:20 PM IST  
**Running on**: `/Users/krishnaraj/Downloads/founder_scraper/`  
**Questions**: Check CONTEXT.md (this file) or reach out to Krishna

---

## 🔗 Related Tools

- **VPS Proxy Scraper** (`/Users/krishnaraj/proxy_scraper/`) - General-purpose web scraping with VPS rotation
- **crawl4ai** - Web crawler library (https://github.com/unclecode/crawl4ai)
- **tinyproxy** - HTTP/SOCKS proxy server

---

**Version**: 1.0  
**Last Updated**: 2026-05-10  
**Auto-update**: When team makes changes, commit to GitHub
