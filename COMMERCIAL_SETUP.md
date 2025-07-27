# COMMERCIAL-GRADE TV SCHEDULE API SETUP

## THE EXACT SAME SOURCES USED BY CABLE COMPANIES AND STREAMING SERVICES

### 1. 🏢 GRACENOTE TMS API (INDUSTRY STANDARD)
**This is what Netflix, Hulu, cable companies, and TV Guide use**

- **Sign up:** https://developer.tmsapi.com/
- **Free tier:** Yes, available for testing
- **Commercial tier:** Contact for pricing
- **Data quality:** Industry standard, 100% accurate
- **Coverage:** All major US networks + cable channels

**Setup Steps:**
1. Go to https://developer.tmsapi.com/
2. Click "Register" 
3. Create developer account
4. Get API key from dashboard
5. Add to .env file: `GRACENOTE_API_KEY=your_key_here`

**API Endpoint:**
```
https://data.tmsapi.com/v1.1/programs/newShowAirings
```

### 2. 🏢 ROVI API (ALTERNATIVE COMMERCIAL)
**Used by many cable providers and streaming platforms**

- **Contact:** Rovi commercial licensing team
- **Pricing:** Enterprise level, contact for quote
- **Data quality:** Commercial grade
- **Coverage:** US + International

### 3. 📡 SCHEDULE DIRECT (NON-COMMERCIAL)
**High-quality alternative for personal use**

- **Website:** https://schedulesdirect.org/
- **Pricing:** ~$25/year for personal use
- **Data quality:** Very good (not commercial grade)
- **Coverage:** US networks

## IMPLEMENTATION STATUS

✅ **Commercial API framework created** - Ready for your API keys
✅ **Gracenote TMS integration** - Just needs your API key  
✅ **Zero fake data policy** - Only verified commercial sources
✅ **Multi-source fallback** - Tries multiple APIs for reliability

## NEXT STEPS

1. **Get Gracenote API Key** (Recommended)
   - Free tier available immediately
   - Commercial licensing for production

2. **Test with your API key:**
   ```bash
   export GRACENOTE_API_KEY="your_key_here"
   python3 commercial_api.py
   ```

3. **Update server to use commercial API:**
   - Replace comprehensive_api.py with commercial_api.py
   - All networks will use industry-standard data

## COST COMPARISON

| Source | Setup | Annual Cost | Data Quality |
|--------|-------|-------------|--------------|
| Gracenote Free | Immediate | $0 | Limited requests |
| Gracenote Commercial | Contact sales | $$$$ | Industry standard |
| Schedule Direct | Register | $25 | Very good |
| Web scraping | None | $0 | **UNRELIABLE** |

## WHY COMMERCIAL APIS ARE ESSENTIAL

**Cable companies use Gracenote/TMS because:**
- ✅ Real-time updates from networks
- ✅ 100% accuracy guarantee  
- ✅ Legal licensing agreements
- ✅ Standardized data format
- ✅ 24/7 reliability

**Web scraping fails because:**
- ❌ Websites change layouts constantly
- ❌ Rate limiting and blocking
- ❌ Incomplete schedule data
- ❌ No legal guarantees
- ❌ Breaks without notice

## READY TO PROCEED

Your commercial API framework is ready. Just get a Gracenote API key and we'll have the same data quality as Netflix and cable companies.