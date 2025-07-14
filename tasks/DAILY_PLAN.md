# Daily Planning Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `PLAN.md` file using the VPA-Strategist methodology. The agent must follow these steps sequentially to ensure accurate, verifiable analysis based on the multi-stage protocol.

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

```bash
# Check for required input files
ls REPORT.md REPORT_week.md LEADER.md GROUP.md
ls vpa_data/ market_data/
```

**Actions**:
- Verify `REPORT.md` exists and contains recent daily signals
- Verify `REPORT_week.md` exists with weekly analysis (reflects last completed trading week)
- Verify `vpa_data/` directory exists with individual ticker VPA files
- Verify `market_data/` directory exists with individual ticker CSV files
- Verify `LEADER.md` exists with industry context analysis
- Verify `GROUP.md` exists with ticker-to-industry mappings

**Success Criteria**: All core input files are present and accessible

### Step 2: Previous PLAN.md Analysis
**Objective**: Understand current ticker states and positions

**Actions**:
- Read existing `PLAN.md` to identify all tickers in each category:
  - Top List (tickers in "Top 1x Cơ Hội Giao Dịch")
  - Potential List (tickers in "Danh Sách Cổ Phiếu Tiềm Năng")
  - Downgraded (tickers in "Danh Sách Cổ Phiếu Bị Hạ Ưu Tiên")
  - Unlisted (any other tickers mentioned in reports)

**Output**: Create internal ticker state map for Stage 0 processing

### Step 3: STAGE 0 - Data Verification & Fact Sheet Creation
**Objective**: Create verified internal fact sheets for ALL tickers to prevent data contamination

**Parallel Processing Approach**: Use Task tool to process tickers concurrently in batches of 5-10 tickers.

**Critical Process**: For EVERY ticker from previous PLAN.md AND any new tickers from reports, create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "previous_state": "Top List/Potential List/Downgraded/Unlisted",
  "current_price": "Latest close from market_data/{TICKER}_*.csv",
  "most_recent_daily_signal": {
    "signal": "Effort to Rise/No Demand/SOS/etc.",
    "date": "YYYY-MM-DD"
  },
  "daily_narrative_context": "1-sentence summary from vpa_data/{TICKER}.md last 3-5 days",
  "weekly_context": {
    "signal": "SOS Bar/Upthrust/etc.",
    "week_ending_date": "YYYY-MM-DD"
  },
  "industry_group": "Industry name from GROUP.md",
  "industry_status": "Dẫn dắt Đồng Thuận/Yếu/Phân Phối from LEADER.md"
}
```

**File Reading Strategy for Each Ticker**:
1. Read `vpa_data/{TICKER}.md` for daily VPA narrative (last 10 entries)
2. Read `market_data/{TICKER}_*.csv` for current price (last row)
3. Cross-reference with `REPORT.md` and `REPORT_week.md` for signals
4. Map industry using `GROUP.md` and get status from `LEADER.md`

**Data Extraction Rules**:
- Extract daily signals ONLY from `REPORT.md` with exact dates
- Extract weekly signals ONLY from `REPORT_week.md` with week ending dates
- Extract VPA narrative context from individual `vpa_data/{TICKER}.md` files
- Extract current prices from individual `market_data/{TICKER}_*.csv` files (latest entry)
- Map industries using exact matches from `GROUP.md`
- Get industry status from `LEADER.md` analysis

**Parallel Processing Strategy**:
- Use Task tool to process multiple tickers concurrently
- Read ticker-specific files (vpa_data/{TICKER}.md, market_data/{TICKER}_*.csv) for focused context
- Avoid reading large consolidated files (VPA.md, market_data.txt)

**Quality Control**: These fact sheets become the SOLE source of truth for all subsequent stages

**Example Task Tool Usage**:
```
Task 1: "Process tickers TCB,VND,ACB,HPG,VHM for fact sheet creation. For each ticker: 1) Read vpa_data/{TICKER}.md last 10 entries 2) Read market_data/{TICKER}_*.csv last price 3) Extract recent signals from REPORT.md 4) Return fact sheet JSON for each ticker"

Task 2: "Process tickers FPT,MWG,GAS,CTG,STB for fact sheet creation. Same process as Task 1."
```

**File Size Benefits**:
- Individual VPA files: ~50-200 lines each vs VPA.md: ~15,000+ lines
- Individual CSV files: ~200 rows each vs market_data.txt: ~25,000+ rows
- Better context focus, faster processing, reduced token usage

### Step 4: STAGE 1 - Ticker State Assessment
**Objective**: Determine new state for each ticker using verified fact sheets

**Process**: Apply state transition rules in exact order using ONLY fact sheet data:

#### For Previous "Top List" Tickers (WEEKLY PRIORITY + STABILITY):
- **Primary Assessment (Weekly Context)**: Weekly trend status takes precedence
  - Weekly SOS/Effort to Rise = Strong foundation (maintain high confidence)
  - Weekly No Supply/Test for Supply = Neutral (monitor daily for direction)
  - Weekly SOW/Upthrust = Warning (reduce confidence, monitor for confirmation)
- **Secondary Assessment (Daily Confirmation)**:
  - **If Weekly Strong**: Daily weakness reduces confidence (95%→85%→75%) but doesn't remove
  - **If Weekly Neutral**: Daily SOS can boost confidence, daily SOW for 3+ days may downgrade
  - **If Weekly Weak**: Daily confirmation needed for removal
- **VERY HIGH THRESHOLD for Removal**: Weekly bearish + 3+ consecutive daily bearish + industry "Yếu"
- **Decision**: Weekly context dominates, daily fine-tunes confidence scores

**Examples of What NOT to Remove**:
- Ticker up 10 days → 1 day SOW → KEEP (reduce confidence 95% → 85%)
- Strong weekly SOS → daily "Test for Supply" → KEEP (normal consolidation)
- Industry still "Dẫn dắt" → single "No Demand" → KEEP (temporary pause)
- After breakout → pullback to support → KEEP (healthy retest)

#### For Previous "Potential List" Tickers (WEEKLY PRIORITY + RESPONSIVE TO DAILY SOS):
- **Promotion Assessment (Weekly + Daily Balance)**:
  - **Weekly Strong + Daily Strong**: Immediate promotion to Top List (95% confidence)
  - **Weekly Neutral/Weak + Daily SOS**: Add to Top List with lower confidence (75-85%) - don't miss breakouts!
  - **Weekly Strong + Daily Neutral**: Promote if industry "Dẫn dắt" (85% confidence)
  - **Entry Point Check**: Ensure reasonable entry levels, not overextended
- **Demotion Assessment (More Lenient)**:
  - **Weekly Bearish + Daily confirms 2+ days**: Move to Downgraded
  - **Allow temporary weakness**: Single day bad signals okay if weekly intact
- **Unlisted Conditions**: Both weekly and daily neutral + industry "Yếu"
- **Decision**: Balance weekly foundation with daily opportunity capture

#### For Previous "Downgraded" Tickers (RESPONSIVE TO RECOVERY):
- **Fast Recovery Assessment (Daily Priority for Reversals)**:
  - **Daily SOS + Weekly supportive/neutral**: Fast track to Potential List (don't miss reversals!)
  - **Daily SOS + Weekly still bearish**: Monitor for 2-3 days confirmation before promoting
  - **Multiple daily bullish signals**: Consider promotion even if weekly lagging
- **Weekly Recovery Assessment**:
  - **Weekly SOS/Effort to Rise**: Immediate promotion to Potential List regardless of daily
  - **Weekly No Supply after SOW**: Move to Potential if industry improving
- **Removal Criteria (More Patient)**:
  - **Both weekly and daily bearish for 2+ weeks**: Consider removal
  - **Industry remains "Yếu" + continued distribution**: Remove
- **Decision**: Prioritize capturing reversals while avoiding false breakouts

#### For Previous "Unlisted" Tickers (WEEKLY PRIORITY + DAILY SOS CAPTURE):
- **Entry Assessment (Responsive to Opportunities)**:
  - **Daily SOS + Weekly neutral/positive**: Fast entry to Potential List
  - **Daily SOS + Weekly negative**: Monitor for 2-3 day confirmation
  - **Weekly SOS + Daily any**: Immediate entry to Potential List
  - **Industry factor**: Even "Đồng Thuận" sectors acceptable if signals strong
- **Risk Tolerance**: Higher for Potential list - capture emerging trends early
- **Decision**: Prioritize opportunity capture over perfection

### Step 5: STAGE 2 - PLAN.md Generation
**Objective**: Generate complete PLAN.md using verified fact sheets and final states

#### 5.1 VNINDEX Analysis Section
```markdown
## 1. Phân Tích Trạng Thái VNINDEX & Chiến Lược

![Weekly Chart](reports_week/VNINDEX/VNINDEX_candlestick_chart.png) | ![Daily Chart](reports/VNINDEX/VNINDEX_candlestick_chart.png)

**Bối Cảnh Tuần**: [Synthesize weekly context from REPORT_week.md]

**Hành Động Gần Đây**: [Describe how recent daily action from REPORT.md confirms/contradicts weekly picture]

**Vùng Tốt Nhất Để Gia Tăng Tỷ Trọng**: [Define specific support/resistance levels with justification]
```

#### 5.2 Top List Generation (STABILITY-FOCUSED)
**Rules**:
- Include ONLY tickers with final state = `Top List`
- **Confidence Score Strategy**: Adjust scores (95% → 85% → 75%) for temporary weakness rather than removing
- **Ranking Priority**: Multi-timeframe confirmation clarity and trend sustainability
- **Mid-Term Focus**: Prioritize consistent performers over short-term momentum
- Format: `[**TCB**](#TCB) (Ngân Hàng - Dẫn dắt đồng thuận) - (Độ tin cậy: 95%)`
- **Score Guidelines**: 
  - 95%: Perfect weekly/daily alignment with strong industry
  - 85%: Minor daily weakness but weekly trend intact
  - 75%: Temporary consolidation but fundamentally sound

#### 5.3 Potential List Generation (OPPORTUNITY FOCUSED)
**Rules**:
- Include ONLY tickers with final state = `Potential List`
- **Higher capacity**: Maximum 15 tickers to capture more opportunities
- **Lower confidence threshold**: >70% confidence to include emerging signals
- **Daily SOS Priority**: Highlight tickers with recent daily SOS signals
- **Fast-track indicators**: Mark tickers ready for Top List promotion
- Format with reasoning emphasizing weekly foundation + daily catalyst

#### 5.4 Downgraded List Generation
**Rules**:
- Include ONLY tickers with final state = `Downgraded`
- Include demotion date and confidence score for keeping reasoning
- Cite specific signals that triggered demotion

#### 5.5 Detailed Analysis for Top Tickers
For EVERY ticker in Top List, provide:
- Chart links (daily and weekly)
- Weekly VPA narrative with exact dates
- Daily VPA narrative with exact dates  
- Industry context from LEADER.md
- Synthesis explaining high-conviction setup
- Best entry zones with technical justification

#### 5.6 Audit Log Creation
**Mandatory documentation** of ALL state changes with precise justifications:

```markdown
## 6. Nhật Ký Thay Đổi Kế Hoạch (AUDIT LOG)

### Cổ Phiếu Được Nâng Lên "Top 1x":
- **ABC**: Từ `Potential List`. Lý do: REPORT.md ghi nhận **'SOS' ngày YYYY-MM-DD**, xác nhận **'SOS' tuần kết thúc YYYY-MM-DD**. LEADER.md xác nhận ngành 'Dẫn dắt Đồng Thuận'.

### Cổ Phiếu Được Thêm Vào "Potential List":
- **XYZ**: Từ `Unlisted`. Lý do: **'SOS' ngày YYYY-MM-DD** với biểu đồ tuần trong vùng Tích Lũy.

### Cổ Phiếu Bị Giáng Xuống "Hạ Ưu Tiên":
- **FPT**: Từ `Top List`. Lý do: **'Sign of Weakness' ngày YYYY-MM-DD** sau 'Upthrust' tuần kết thúc YYYY-MM-DD.

### Cổ Phiếu Bị Loại Bỏ Hoàn Toàn:
- **GEX**: Từ `Downgraded`. Lý do: **'No Demand' ngày YYYY-MM-DD** xác nhận xu hướng giảm.
```

### Step 6: Quality Verification
**Objective**: Ensure PLAN.md accuracy and completeness

**Verification Checklist**:
- [ ] All assertions cite specific signals and dates from fact sheets
- [ ] No ticker appears in multiple categories
- [ ] All Top List tickers have detailed analysis sections
- [ ] Audit log documents every state change with justification
- [ ] VNINDEX analysis synthesizes both daily and weekly timeframes
- [ ] Chart links use correct file paths
- [ ] Vietnamese text is grammatically correct
- [ ] Confidence scores are justified

### Step 7: File Output
**Objective**: Generate final PLAN.md file

```bash
# Generate new PLAN.md (git handles version control)
# [Output complete PLAN.md content]
```

## Quality Control Standards

### Data Accuracy Requirements
- **Zero Tolerance**: No signal assertions without fact sheet verification
- **Date Precision**: All signals must include exact dates
- **Source Attribution**: Every claim must trace back to input files
- **Cross-Verification**: Weekly and daily signals must align logically

### Vietnamese Language Standards
- Use proper financial terminology
- Maintain professional tone and grammar
- Ensure decimal formatting uses dots (.), not commas (,)
- Use consistent industry naming from GROUP.md

### Technical Requirements
- **Chart Links**: Verify all image paths exist
- **Markdown Formatting**: Ensure proper headers, links, and structure
- **Confidence Scores**: Base on objective signal strength and industry context
- **Audit Trail**: Document reasoning for every decision

## Error Handling

### Missing Input Files
- Document missing files in summary
- Use available data and note limitations
- Flag areas requiring manual review

### Data Inconsistencies  
- Cross-reference multiple sources
- Prioritize most recent and reliable data
- Document conflicts in audit log

### Signal Interpretation Disputes
- Apply conservative Wyckoff methodology
- Err on side of caution for state changes
- Provide detailed reasoning for controversial decisions

## Success Metrics

- **Accuracy**: All fact sheets match source data exactly
- **Completeness**: Every ticker assessed and categorized
- **Traceability**: All decisions can be verified from audit log
- **Actionability**: Top List provides clear trading opportunities
- **Consistency**: Analysis follows Wyckoff methodology strictly

## Templates

### Fact Sheet Template
```json
{
  "ticker": "",
  "previous_state": "",
  "most_recent_daily_signal": {"signal": "", "date": ""},
  "daily_narrative_context": "",
  "weekly_context": {"signal": "", "week_ending_date": ""},
  "industry_group": "",
  "industry_status": ""
}
```

### Top Ticker Analysis Template
```markdown
### [TICKER_NAME]

- ![Weekly Chart](reports_week/TICKER/TICKER_candlestick_chart.png) | ![Daily Chart](reports/TICKER/TICKER_candlestick_chart.png) | [View Report](REPORT.md#TICKER)
- **Phân Tích Cốt Lõi:**
  - **Weekly VPA Narrative:** Bối cảnh tuần kết thúc [DATE] cho thấy [SIGNAL]...
  - **Daily VPA Narrative:** Ngày [DATE] có tín hiệu [SIGNAL]. [VPA context]...
  - **Industry Context:** Ngành [INDUSTRY] ở trạng thái [STATUS]...
  - **Synthesis:** [Why this creates high-conviction setup]
- **Vùng Tham Gia Tốt Nhất:** [Technical levels with reasoning]
```
