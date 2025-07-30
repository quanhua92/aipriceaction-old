# Tasks Directory - AI Agent Task System

## Overview

This directory contains AI agent task protocols for the **AIPriceAction** Vietnamese stock market analysis system. These tasks orchestrate a sophisticated multi-timeframe analysis workflow with comprehensive error handling and quality assurance.

## System Architecture

### 🎯 **Core Analysis Engines (4 files)**

#### **`DAILY_VPA.md`** - Daily Volume Price Analysis
- **Purpose**: Primary daily VPA analysis using Wyckoff methodology
- **Features**: 8-batch parallel processing, manual analysis focus
- **Output**: Updates `vpa_data/` with daily analysis
- **Dependencies**: market_data/, merge_vpa.py

#### **`WEEKLY_VPA.md`** - Weekly Volume Price Analysis  
- **Purpose**: Weekly timeframe VPA analysis with Monday-dated logic
- **Features**: Same structure as daily but weekly-focused
- **Output**: Updates `vpa_data_week/` with weekly analysis
- **Dependencies**: market_data_week/, merge_vpa.py --week

#### **`DAILY_PLAN.md`** - Trading Plan Generation
- **Purpose**: Generate PLAN.md using VPA-Strategist methodology
- **Features**: Natural language analysis, Vietnamese financial terminology
- **Output**: Creates comprehensive trading plan in PLAN.md
- **Dependencies**: REPORT.md, REPORT_week.md, LEADER.md, GROUP.md

#### **`WEEKLY_LEADER.md`** - Sector Leadership Analysis
- **Purpose**: Generate LEADER.md with sector leadership analysis
- **Features**: Manual scoring framework, sector health classification
- **Output**: Creates sector leadership analysis in LEADER.md
- **Dependencies**: GROUP.md, REPORT_week.md, vpa_data_week/

### 🛡️ **Quality Control & Verification (3 files)**

#### **`CHECK_VPA.md`** - VPA Analysis Verification
- **Purpose**: Systematic verification of VPA analysis accuracy
- **Features**: Market data verification, duplicate resolution, emergency procedures
- **Critical**: Prevents costly trading errors from bad data
- **Dependencies**: vpa_data/, market_data/, CSV verification

#### **`CHECK_PLAN.md`** - Price Verification for PLAN.md
- **Purpose**: Verify all price and volume data in PLAN.md
- **Features**: Zero tolerance for price/volume errors
- **Critical**: Prevents trading losses from incorrect prices
- **Dependencies**: PLAN.md, market_data/

#### **`CHECK_HOLD.md`** - Portfolio Holdings Verification
- **Purpose**: Verify portfolio P&L calculations and analysis accuracy
- **Features**: P&L verification, sector allocation checks
- **Critical**: Portfolio accuracy prevents trading losses
- **Dependencies**: hold.md, calculate_pnl_correct.py, GROUP.md

### 💼 **Portfolio Management (1 file)**

#### **`DAILY_HOLD.md`** - Portfolio Management Protocol
- **Purpose**: Generate hold.md for portfolio management decisions
- **Features**: Manual P&L calculations, Vietnamese formatting, sector allocation
- **Output**: Creates portfolio recommendations in hold.md
- **Dependencies**: calculate_pnl_correct.py, GROUP.md, REPORT.md

### 🔧 **Supporting Tasks (4 files)**

#### **`FIX_VPA.md`** - VPA Error Correction
- **Purpose**: Systematic approach to fix VPA analysis errors
- **Features**: Sub-agent deployment, verification workflow
- **Dependencies**: verify_vpa.py, vpa_data/, market_data/

#### **`dividends_plan.md`** - Dividend Processing
- **Purpose**: Handle dividend-adjusted VPA files
- **Features**: Price adjustment logic, automatic detection
- **Dependencies**: market_data_check_dividends/

#### **`task_generate_vpa_analysis.md`** - Daily VPA Task Template
- **Purpose**: Task template for sub-agents performing daily VPA analysis
- **Usage**: Called by DAILY_VPA.md for sub-agent instructions
- **Features**: Detailed file operation requirements

#### **`task_generate_vpa_analysis_week.md`** - Weekly VPA Task Template
- **Purpose**: Task template for sub-agents performing weekly VPA analysis
- **Usage**: Called by WEEKLY_VPA.md for sub-agent instructions
- **Features**: Weekly-specific task specifications

### 🌐 **Web Development Project (5 files)**

#### **`web/`** - Complete React Frontend Implementation
- **Purpose**: 5-stage plan for building React web frontend
- **Status**: Independent web project, not part of core analysis system
- **Technology**: React + TypeScript, Vercel deployment
- **Stages**: 
  1. Project setup
  2. Data services
  3. Core components
  4. Page components
  5. Deployment & testing

## Workflow Overview

### **Daily Analysis Flow**
```
1. DAILY_VPA.md → Generate daily VPA analysis → vpa_data/
2. CHECK_VPA.md → Verify analysis accuracy → Error correction if needed
3. DAILY_PLAN.md → Generate trading plan → PLAN.md
4. CHECK_PLAN.md → Verify plan accuracy → Emergency procedures if errors
5. DAILY_HOLD.md → Generate portfolio recommendations → hold.md
6. CHECK_HOLD.md → Verify portfolio calculations → Final validation
```

### **Weekly Analysis Flow**
```
1. WEEKLY_VPA.md → Generate weekly VPA analysis → vpa_data_week/
2. CHECK_VPA.md → Verify weekly analysis accuracy
3. WEEKLY_LEADER.md → Generate sector leadership → LEADER.md
4. DAILY_PLAN.md → Integrate weekly insights into daily plan
```

### **Error Handling Flow**
```
CHECK_*.md → Detect errors → FIX_VPA.md → Sub-agent correction → Verification
```

## Key Features

### **🔄 Parallel Processing**
- 8-batch concurrent analysis for efficiency
- Coordinated multi-timeframe analysis (daily + weekly)

### **🎯 Manual Intelligence Focus**
- Emphasis on human analysis over pure automation
- Professional trader methodology (Wyckoff, VPA-Strategist)

### **🛡️ Data Accuracy Priority**
- Multiple verification layers prevent trading errors
- Zero tolerance for price/volume inaccuracies
- Emergency procedures for data issues

### **🇻🇳 Vietnamese Market Specialization**
- Tailored for Vietnamese stock market
- Vietnamese financial terminology and formatting
- Local market conventions and practices

### **📊 Production Quality**
- Comprehensive error handling
- Quality assurance measures
- Risk management protocols

## Usage Instructions

### **Running Daily Analysis**
1. Execute `DAILY_VPA.md` for daily analysis
2. Run `CHECK_VPA.md` to verify accuracy
3. Execute `DAILY_PLAN.md` for trading plan
4. Run `CHECK_PLAN.md` to verify plan
5. Execute `DAILY_HOLD.md` for portfolio management
6. Run `CHECK_HOLD.md` for final verification

### **Running Weekly Analysis**
1. Execute `WEEKLY_VPA.md` for weekly analysis
2. Run `WEEKLY_LEADER.md` for sector analysis
3. Integrate results into daily workflow

### **Error Correction**
- Use `FIX_VPA.md` when CHECK_*.md tasks detect errors
- Use `dividends_plan.md` for dividend-related price adjustments

## File Dependencies

### **Core Data Dependencies**
- `market_data/` - Daily market data
- `market_data_week/` - Weekly market data  
- `vpa_data/` - Daily VPA analysis results
- `vpa_data_week/` - Weekly VPA analysis results

### **Configuration Files**
- `GROUP.md` - Sector groupings
- `TICKERS.csv` - Stock symbols list
- `ticker_group.json` - Industry classifications

### **Output Files**
- `PLAN.md` - Trading plan
- `LEADER.md` - Sector leadership analysis
- `hold.md` - Portfolio recommendations
- `REPORT.md` - Daily market report
- `REPORT_week.md` - Weekly market report

## Technical Notes

### **Agent Coordination**
- Tasks use sub-agents for parallel processing
- Task templates provide consistent instructions
- Error handling includes emergency procedures

### **Data Integrity**
- Multiple verification layers
- Manual verification requirements
- Automatic duplicate detection and resolution

### **Vietnamese Localization**
- All outputs in Vietnamese
- Local financial terminology
- Vietnamese market conventions

## Maintenance

### **Regular Tasks**
- Daily: Run full daily analysis workflow
- Weekly: Run weekly analysis and sector leadership
- As needed: Error correction and dividend adjustments

### **Quality Assurance**
- All CHECK_*.md tasks must pass before proceeding
- Manual verification required for critical data
- Emergency procedures for data accuracy issues

This task system represents a **production-ready, professional-grade** stock analysis workflow with comprehensive quality controls and risk management measures specifically designed for the Vietnamese stock market.