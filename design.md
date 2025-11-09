# Architecture & Design Document
## Shufersal Online E-Commerce Automation Testing Framework

**Version:** 1.0.0  
**Last Updated:** November 6, 2025  
**Author:** Test Automation Team

---

## Table of Contents

1. [Overview](#overview)
2. [Infrastructure & Automation Design](#infrastructure--automation-design)
3. [Test Automation Flow](#test-automation-flow)
4. [Page Object Model Architecture](#page-object-model-architecture)
5. [CI/CD Integration](#cicd-integration)
6. [Data Flow Diagram](#data-flow-diagram)
7. [Technology Stack](#technology-stack)
8. [Design Decisions](#design-decisions)

---

## Overview

This document provides comprehensive architectural diagrams and design explanations for the Shufersal Online E-Commerce automation testing framework. The framework is built using the **Page Object Model (POM)** design pattern with **Playwright** and **pytest** for robust, maintainable end-to-end testing.

---

## Infrastructure & Automation Design

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TEST AUTOMATION FRAMEWORK                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
        │  Test Suites  │   │  Page Objects │   │   Utilities   │
        └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
                │                   │                   │
                │                   │                   │
    ┌───────────┼───────────┐       │       ┌───────────┼───────────┐
    │           │           │       │       │           │           │
    ▼           ▼           ▼       ▼       ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  E2E   │ │Functnl │ │Multiple│ │Base│ │Settings│ │Helpers │ │Fixtures│
│ Tests  │ │ Tests  │ │Product │ │Page│ │Manager │ │ Logger │ │ Pytest │
└────────┘ └────────┘ └────────┘ └──┬─┘ └────────┘ └────────┘ └────────┘
    │           │           │        │        │           │           │
    └───────────┴───────────┴────────┼────────┴───────────┴───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   Playwright Engine    │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │   Chromium Browser     │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  Shufersal Online      │
                        │  (Target Application)  │
                        └────────────────────────┘
```

### Component Descriptions

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Test Suites** | Contains all test cases organized by functionality | pytest |
| **Page Objects** | Encapsulates page-specific elements and actions | Python Classes |
| **Base Page** | Common methods inherited by all page objects | Python Base Class |
| **Utilities** | Settings, helpers, and logging functionality | Python modules |
| **Fixtures** | Browser setup, context, and page initialization | pytest fixtures |
| **Playwright Engine** | Browser automation and control | Playwright |
| **Chromium Browser** | Headless/headed browser for test execution | Chromium |

---

## Test Automation Flow

### End-to-End Test Execution Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                     TEST EXECUTION WORKFLOW                          │
└──────────────────────────────────────────────────────────────────────┘

    START
      │
      ▼
┌─────────────────────┐
│  1. pytest init     │ ◄───── conftest.py loads
│  - Load fixtures    │        - Settings from .env
│  - Setup browser    │        - Browser config
└──────────┬──────────┘        - Test markers
           │
           ▼
┌─────────────────────┐
│  2. Create Browser  │
│  - Launch Chromium  │
│  - Set viewport     │
│  - Set locale (he)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. Create Context  │
│  - New session      │
│  - Isolated cookies │
│  - Fresh state      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. Create Page     │
│  - New tab          │
│  - Set timeout      │
│  - Ready for test   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  5. Execute Test                        │
│  ┌─────────────────────────────────┐   │
│  │ a. Initialize Page Objects      │   │
│  │    - HomePage(page)              │   │
│  │    - SearchResultsPage(page)     │   │
│  │    - CartPage(page)              │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐   │
│  │ b. Navigate to Application      │   │
│  │    - home_page.navigate()        │   │
│  │    - Wait for page load          │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐   │
│  │ c. Perform Actions               │   │
│  │    - Search for product          │   │
│  │    - Add to cart                 │   │
│  │    - Handle modals               │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐   │
│  │ d. Verify Results                │   │
│  │    - Assert product in cart      │   │
│  │    - Assert prices               │   │
│  │    - Assert UI states            │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐   │
│  │ e. Cleanup                       │   │
│  │    - Clear cart                  │   │
│  │    - Reset state                 │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
           │
           ▼
      ┌────────┐
      │ PASS?  │
      └───┬────┘
          │
    ┌─────┴─────┐
    │           │
   YES         NO
    │           │
    ▼           ▼
┌────────┐  ┌────────────────┐
│ Report │  │ Screenshot     │
│ Success│  │ + Error Log    │
└────────┘  └────────────────┘
    │           │
    └─────┬─────┘
          │
          ▼
┌─────────────────────┐
│  6. Teardown        │
│  - Close page       │
│  - Close context    │
│  - Close browser    │
└──────────┬──────────┘
           │
           ▼
         END
```

### Detailed Test Flow Explanation

1. **Initialization Phase**
   - pytest loads `conftest.py`
   - Environment variables loaded from `.env`
   - Browser fixtures created (session/function scope)
   - Custom markers registered

2. **Browser Setup Phase**
   - Chromium browser launched (headless or headed based on config)
   - Browser context created with:
     - 1920x1080 viewport
     - Hebrew locale (he-IL)
     - Israel timezone (Asia/Jerusalem)

3. **Test Execution Phase**
   - Page objects instantiated
   - Test steps executed sequentially
   - Actions performed via page object methods
   - Assertions validate expected behavior

4. **Reporting Phase**
   - Test results logged
   - HTML report generated
   - Screenshots captured on failure
   - Logs written to `temp/test_runs/`

5. **Cleanup Phase**
   - Browser resources released
   - Temporary files managed
   - Context isolated for next test

---

## Page Object Model Architecture

### POM Structure Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PAGE OBJECT MODEL LAYERS                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  TEST LAYER (tests/*.py)                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  E2E Tests   │  │  Functional  │  │   Negative   │         │
│  │              │  │    Tests     │  │   Scenarios  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │ Uses             │ Uses             │ Uses
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  PAGE OBJECT LAYER (pages/*.py)                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │  Home   │  │ Search  │  │  Cart   │  │Checkout │          │
│  │  Page   │  │ Results │  │  Page   │  │  Page   │          │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘          │
└───────┼────────────┼────────────┼────────────┼─────────────────┘
        │            │            │            │
        │ Inherits   │ Inherits   │ Inherits   │ Inherits
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────┐
│  BASE PAGE LAYER (pages/base_page.py)                           │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Common Methods:                                       │     │
│  │  • navigate_to(url)                                    │     │
│  │  • click_element(selector)                             │     │
│  │  • fill_input(selector, text)                          │     │
│  │  • wait_for_element(selector)                          │     │
│  │  • is_visible(selector)                                │     │
│  │  • get_text(selector)                                  │     │
│  └───────────────────────────────────────────────────────┘     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ Uses
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  PLAYWRIGHT LAYER                                                │
│  • Browser automation                                            │
│  • Element interactions                                          │
│  • Wait strategies                                               │
│  • Network interception                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Page Object Responsibilities

#### **Base Page** (`base_page.py`)
```python
Responsibilities:
├── Common navigation methods
├── Element interaction helpers
├── Wait and visibility checks
├── Logger initialization
└── Screenshot capture
```

#### **Home Page** (`home_page.py`)
```python
Responsibilities:
├── Navigate to homepage
├── Search for products
├── Verify homepage loaded
└── Open cart sidebar
```

#### **Search Results Page** (`search_results_page.py`)
```python
Responsibilities:
├── Get product listings
├── Add products to cart
├── Get product prices
├── Verify search relevance
└── Handle address modal
```

#### **Cart Page** (`cart_page.py`)
```python
Responsibilities:
├── Open/close cart sidebar
├── Get cart item count
├── Verify products in cart
├── Update quantities
├── Remove items
├── Clear cart
├── Check checkout button state
└── Get total price
```

#### **Checkout Page** (`checkout_page.py`)
```python
Responsibilities:
└── Verify login wall displayed
```

#### **Address Modal** (`address_modal_page.py`)
```python
Responsibilities:
├── Detect modal visibility
├── Fill address details
├── Select delivery time slot
└── Close modal
```

---

## CI/CD Integration

### GitHub Actions Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE WORKFLOW                       │
└──────────────────────────────────────────────────────────────────┘

    TRIGGER EVENTS
         │
    ┌────┴────┬────────────┬───────────────┬────────────────┐
    │         │            │               │                │
    ▼         ▼            ▼               ▼                ▼
┌────────┐ ┌──────┐ ┌──────────┐ ┌──────────────┐ ┌──────────────┐
│ Push   │ │  PR  │ │ Schedule │ │   Manual     │ │   Workflow   │
│ (main) │ │      │ │ (Daily)  │ │   Trigger    │ │   Dispatch   │
└────────┘ └──────┘ └──────────┘ └──────────────┘ └──────────────┘
    │         │            │               │                │
    └─────────┴────────────┴───────────────┴────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   GitHub Actions VM    │
              │   (Ubuntu Latest)      │
              └────────────┬───────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Python   │   │ Python   │   │ Python   │
    │  3.9     │   │  3.10    │   │  3.11    │
    └─────┬────┘   └─────┬────┘   └─────┬────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  1. SETUP PHASE        │
            │  ├─ Checkout code      │
            │  ├─ Setup Python       │
            │  ├─ Cache pip deps     │
            │  └─ Install deps       │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  2. BROWSER SETUP      │
            │  ├─ Install Chromium   │
            │  └─ Install deps       │
            └────────────┬───────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  3. TEST EXECUTION     │
            │  ├─ Run smoke tests    │
            │  └─ Run all tests      │
            └────────────┬───────────┘
                         │
                ┌────────┴────────┐
                │                 │
              PASS              FAIL
                │                 │
                ▼                 ▼
    ┌────────────────────┐  ┌─────────────────────┐
    │  4. REPORTING      │  │  4. ERROR HANDLING  │
    │  ├─ Upload reports │  │  ├─ Upload reports  │
    │  └─ Archive HTML   │  │  ├─ Upload screenshots│
    └─────────┬──────────┘  │  └─ Send notification│
              │             └──────────┬────────────┘
              │                        │
              └────────────┬───────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  5. ARTIFACTS  │
                  │  Retention:    │
                  │  Reports: 30d  │
                  │  Screens: 7d   │
                  └────────────────┘
                           │
                           ▼
                         END
```

### CI/CD Workflow Configuration

**File:** `.github/workflows/tests.yml`

**Key Features:**

1. **Multi-Trigger Support**
   - Push to `main` or `develop` branches
   - Pull requests to `main`
   - Daily scheduled run at 2 AM UTC
   - Manual workflow dispatch

2. **Matrix Strategy**
   - Tests run on Python 3.9, 3.10, and 3.11
   - Parallel execution for faster feedback
   - Ensures compatibility across Python versions

3. **Optimizations**
   - Pip dependency caching for faster builds
   - Artifact retention policies (reports: 30 days, screenshots: 7 days)
   - Conditional uploads (screenshots only on failure)

4. **Test Stages**
   ```
   Stage 1: Smoke Tests (Critical paths only)
            ↓ (if pass)
   Stage 2: Full Test Suite (All tests)
   ```

5. **Reporting**
   - HTML reports generated for each run
   - Artifacts uploaded and downloadable from GitHub Actions
   - Failure notifications with warnings

### CI/CD Environment Variables

For CI execution, add these secrets to your GitHub repository:

```yaml
# Repository Settings → Secrets → Actions

HEADLESS=true                    # Run browser in headless mode
SLOW_MO=0                        # No delay in CI (faster execution)
BROWSER_TIMEOUT=30000            # 30 second timeout
DELIVERY_CITY=תל אביב            # Mock delivery data
DELIVERY_STREET=דיזנגוף
DELIVERY_STREET_NUMBER=1
DELIVERY_APARTMENT=1
DELIVERY_DATE=20251104
DELIVERY_TIME=14:00
```

### CI/CD Best Practices Implemented

✅ **Isolated Environments** - Each test run uses fresh browser context  
✅ **Parallel Execution** - Matrix strategy for multiple Python versions  
✅ **Caching** - Pip dependencies cached to speed up builds  
✅ **Artifact Management** - Reports and screenshots preserved  
✅ **Failure Handling** - Screenshots captured and notifications sent  
✅ **Scheduled Runs** - Daily automated test execution  
✅ **Manual Triggers** - On-demand test execution capability

---

## Data Flow Diagram

### Test Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                       │
└──────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   .env      │  Configuration
    │   file      │  Variables
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  Settings   │  Loads & Validates
    │   Manager   │  Environment Config
    └──────┬──────┘
           │
           ▼
    ┌─────────────┐
    │  conftest   │  Creates Fixtures
    │   .py       │  with Config
    └──────┬──────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
    ┌─────────────┐      ┌─────────────┐
    │  Browser    │      │   Page      │
    │  Context    │      │  Objects    │
    └──────┬──────┘      └──────┬──────┘
           │                     │
           └──────────┬──────────┘
                      │
                      ▼
              ┌───────────────┐
              │  Test Cases   │
              └───────┬───────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    ┌───────┐    ┌───────┐    ┌───────┐
    │Search │    │ Add   │    │Verify │
    │Product│───▶│ Cart  │───▶│ State │
    └───────┘    └───────┘    └───────┘
        │             │             │
        │             │             │
        ▼             ▼             ▼
    ┌──────────────────────────────────┐
    │      Shufersal Online            │
    │      (Target Application)        │
    └────────────────┬─────────────────┘
                     │
                     │ Response
                     ▼
              ┌─────────────┐
              │ Assertions  │
              └──────┬──────┘
                     │
            ┌────────┴────────┐
            │                 │
           PASS              FAIL
            │                 │
            ▼                 ▼
    ┌──────────────┐  ┌──────────────┐
    │ Test Report  │  │ Screenshots  │
    │ (HTML)       │  │ + Error Logs │
    └──────────────┘  └──────────────┘
```

---

## Technology Stack

### Framework Components

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY STACK                         │
└─────────────────────────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════╗
║  AUTOMATION LAYER                                         ║
╠═══════════════════════════════════════════════════════════╣
║  • Playwright 1.40.0  - Browser automation                ║
║  • Python 3.9+        - Programming language              ║
╚═══════════════════════════════════════════════════════════╝
                           │
╔═══════════════════════════════════════════════════════════╗
║  TESTING FRAMEWORK                                        ║
╠═══════════════════════════════════════════════════════════╣
║  • pytest 7.4.3       - Test runner & framework           ║
║  • pytest-html 4.1.1  - HTML reporting                    ║
║  • pytest-xdist 3.5.0 - Parallel execution                ║
║  • allure-pytest      - Advanced reporting (optional)     ║
╚═══════════════════════════════════════════════════════════╝
                           │
╔═══════════════════════════════════════════════════════════╗
║  CONFIGURATION & UTILITIES                                ║
╠═══════════════════════════════════════════════════════════╣
║  • python-dotenv 1.0.0  - Environment configuration       ║
║  • logging (stdlib)     - Test execution logs             ║
║  • pathlib (stdlib)     - File path management            ║
╚═══════════════════════════════════════════════════════════╝
                           │
╔═══════════════════════════════════════════════════════════╗
║  CI/CD INTEGRATION                                        ║
╠═══════════════════════════════════════════════════════════╣
║  • GitHub Actions       - CI/CD pipeline                  ║
║  • Ubuntu Latest        - CI runner environment           ║
║  • Chromium (Headless)  - Browser for CI                  ║
╚═══════════════════════════════════════════════════════════╝
                           │
╔═══════════════════════════════════════════════════════════╗
║  BROWSER ENGINE                                           ║
╠═══════════════════════════════════════════════════════════╣
║  • Chromium             - Default browser                 ║
║  • Viewport: 1920x1080  - Standard desktop resolution     ║
║  • Locale: he-IL        - Hebrew language support         ║
║  • Timezone: Asia/Jerusalem  - Israel timezone            ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Design Decisions

### 1. **Why Page Object Model (POM)?**

**Decision:** Implement POM design pattern

**Rationale:**
- ✅ **Maintainability** - UI changes require updates only in page objects
- ✅ **Reusability** - Page methods can be used across multiple tests
- ✅ **Readability** - Tests read like business workflows
- ✅ **Separation of Concerns** - Test logic separated from page interactions

**Example:**
```python
# Without POM (Not Recommended)
page.click("button.js-add-to-cart")
page.fill("input#cityInput", "תל אביב")

# With POM (Recommended)
home_page.search_product("חלב")
cart_page.add_to_cart()
```

---

### 2. **Why Playwright over Selenium?**

**Decision:** Use Playwright as the automation engine

**Rationale:**
- ✅ **Modern Architecture** - Built for modern web apps
- ✅ **Auto-wait** - Automatically waits for elements to be actionable
- ✅ **Fast Execution** - Faster than Selenium WebDriver
- ✅ **Better Debugging** - Built-in debugging tools and traces
- ✅ **Multi-browser Support** - Chromium, Firefox, WebKit out of the box
- ✅ **Network Interception** - Can mock APIs and responses

---

### 3. **Why pytest over unittest?**

**Decision:** Use pytest as the testing framework

**Rationale:**
- ✅ **Fixtures** - Powerful setup/teardown mechanism
- ✅ **Markers** - Easy test categorization (@pytest.mark.smoke)
- ✅ **Plugins** - Rich ecosystem (pytest-html, pytest-xdist)
- ✅ **Assertions** - Clear, readable assertion messages
- ✅ **Parameterization** - Data-driven testing support

---

### 4. **Why Chromium as Default Browser?**

**Decision:** Use Chromium as the default browser

**Rationale:**
- ✅ **Stability** - Consistent behavior across platforms
- ✅ **Performance** - Fast rendering and execution
- ✅ **Headless Support** - Ideal for CI/CD environments
- ✅ **DevTools Protocol** - Advanced debugging capabilities
- ✅ **Market Share** - Chrome-based browsers dominate the market

---

### 5. **Why Session vs Function Scope Fixtures?**

**Decision:** Use both session and function scope fixtures

**Rationale:**
- **Session Scope** (`test_functionality.py`)
  - ✅ Faster execution - browser created once
  - ✅ Tests share state for related operations
  - ✅ Good for functional test suites

- **Function Scope** (`test_end_to_end.py`)
  - ✅ Complete isolation between tests
  - ✅ Fresh browser state for each test
  - ✅ Good for E2E tests that modify state

---

### 6. **Why Environment Variables (.env)?**

**Decision:** Use .env files for configuration

**Rationale:**
- ✅ **Security** - Sensitive data not in code
- ✅ **Flexibility** - Easy to change configs per environment
- ✅ **CI/CD Integration** - Easy to override in pipelines
- ✅ **Developer Experience** - Local overrides without code changes

---

### 7. **Why Separate Test Suites?**

**Decision:** Organize tests into separate files by category

**File Structure:**
```
tests/
├── test_end_to_end.py         # Complete user journeys
├── test_functionality.py      # Individual feature tests
├── test_multiple_products.py  # Bulk operations
└── test_negative_scenarios.py # Error handling
```

**Rationale:**
- ✅ **Organization** - Easy to find specific test types
- ✅ **Selective Execution** - Run only needed test suites
- ✅ **Parallel Execution** - Different suites can run in parallel
- ✅ **Maintenance** - Clear responsibility boundaries

---

### 8. **Why Mock Address/Delivery Slots?**

**Decision:** Handle address modal with mock data

**Rationale:**
- ✅ **Test Isolation** - No dependency on real delivery logistics
- ✅ **Reliability** - Tests don't fail due to unavailable slots
- ✅ **Speed** - No wait time for real API responses
- ✅ **Production Safety** - No risk of real orders

**Production Approach:**
In a staging environment, this would integrate with:
- Test database with fixed addresses
- Mocked API endpoints for address validation
- Dedicated test delivery slots that never expire

---

### 9. **Why Hebrew Locale Configuration?**

**Decision:** Configure browser with Hebrew locale (he-IL)

**Rationale:**
- ✅ **Accuracy** - Tests match production user experience
- ✅ **RTL Support** - Proper handling of right-to-left text
- ✅ **Localization Testing** - Validates Hebrew UI elements
- ✅ **Timezone** - Tests run in Israel timezone context

---

### 10. **Why Logs in temp/ Directory?**

**Decision:** Store test execution logs in `temp/test_runs/`

**Rationale:**
- ✅ **Debugging** - Detailed execution traces available
- ✅ **Audit Trail** - Historical test run information
- ✅ **Timestamp** - Each run has unique timestamped log
- ✅ **Git Ignore** - Logs not committed to repository

---

## Summary

This framework implements a **robust, scalable, and maintainable** test automation solution using:

- 🏗️ **Page Object Model** for clean architecture
- 🚀 **Playwright** for modern web automation
- 🧪 **pytest** for powerful testing capabilities
- 🔄 **GitHub Actions** for continuous integration
- 📊 **HTML Reports** for comprehensive test results
- 🌐 **Hebrew/RTL Support** for localized testing

The design prioritizes **maintainability**, **reliability**, and **developer experience** while ensuring comprehensive test coverage of the Shufersal Online e-commerce platform.

---

**Document Version:** 1.0.0  
**Last Review Date:** November 6, 2025  
**Next Review Date:** December 6, 2025
