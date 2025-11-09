# Shufersal Online E-Commerce Automation Testing Framework

A comprehensive end-to-end testing framework for Shufersal Online (https://www.shufersal.co.il/online/he) built with Python, Playwright, and pytest. This framework implements the Page Object Model (POM) design pattern for maintainable and scalable test automation.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [Browser Configuration](#browser-configuration)
- [Known Limitations & Assumptions](#known-limitations--assumptions)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## ✨ Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Multi-Test Suite Coverage**:
  - End-to-End purchase flow tests
  - Functional tests for cart operations
  - Multiple product handling tests
  - Negative scenario and edge case tests
- **Hebrew Language Support**: Handles RTL (Right-to-Left) text and Hebrew locale
- **Flexible Configuration**: Environment-based settings via `.env` file
- **Detailed Logging**: Comprehensive test execution logs
- **Pytest Integration**: Powerful test runner with custom markers and fixtures

---

**Key Components:**
- **Base Page**: Common methods shared across all pages
- **Page Objects**: Encapsulate page-specific selectors and actions
- **Test Suites**: Business logic and test scenarios
- **Utilities**: Helper functions, settings, and configuration management

---

## 📦 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager
- **Operating System**: Windows, macOS, or Linux

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd shufersal_online_automation
```

### 2. Create a Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

This will download the Chromium browser binaries required for test execution.

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Browser Settings
HEADLESS=false
SLOW_MO=500
BROWSER_TIMEOUT=30000

# Test Environment
TEST_ENV=dev
BASE_URL=https://www.shufersal.co.il/online/he

# Delivery Address (for modal handling)
DELIVERY_CITY=תל אביב
DELIVERY_STREET=דיזנגוף
DELIVERY_STREET_NUMBER=1
DELIVERY_APARTMENT=1

# Delivery Time Slot (format: YYYYMMDD and HH:MM)
DELIVERY_DATE=20251104
DELIVERY_TIME=14:00

# Reporting
SCREENSHOT_ON_FAILURE=true
VIDEO_ON_FAILURE=false
```

---

## ⚙️ Configuration

### Environment Variables Explained

| Variable | Description | Default |
|----------|-------------|---------|
| `HEADLESS` | Run browser in headless mode (true/false) | `false` |
| `SLOW_MO` | Slow down operations by X milliseconds | `500` |
| `BROWSER_TIMEOUT` | Default timeout for browser operations (ms) | `30000` |
| `TEST_ENV` | Test environment identifier | `dev` |
| `BASE_URL` | Shufersal Online base URL | `https://www.shufersal.co.il/online/he` |
| `DELIVERY_CITY` | City for delivery address | `תל אביב` |
| `DELIVERY_STREET` | Street for delivery address | `דיזנגוף` |
| `DELIVERY_STREET_NUMBER` | Street number | `1` |
| `DELIVERY_APARTMENT` | Apartment number | `1` |
| `DELIVERY_DATE` | Delivery date (YYYYMMDD format) | `20251104` |
| `DELIVERY_TIME` | Delivery time (HH:MM format) | `14:00` |
| `SCREENSHOT_ON_FAILURE` | Capture screenshot on test failure | `true` |
| `VIDEO_ON_FAILURE` | Record video on test failure | `false` |

---

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Suite

```bash
# End-to-End tests
pytest tests/test_end_to_end.py

# Functional tests
pytest tests/test_functionality.py

# Multiple products tests
pytest tests/test_multiple_products.py

# Negative scenario tests
pytest tests/test_negative_scenarios.py
```

### Run Tests by Marker

```bash
# Run only smoke tests
pytest -m smoke

# Run only cart-related tests
pytest -m cart

# Run only negative scenario tests
pytest -m negative

# Run end-to-end tests
pytest -m e2e
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test

```bash
pytest tests/test_functionality.py::TestFunctionality::test_add_and_remove_single_item -v
```

### Generate HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

### Available Pytest Markers

- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.functional` - Functional tests
- `@pytest.mark.cart` - Shopping cart tests
- `@pytest.mark.search` - Search functionality tests
- `@pytest.mark.negative` - Negative/edge case tests
- `@pytest.mark.checkout` - Checkout process tests

---

## 📂 Test Structure

### Test Suites Overview

#### 1. **End-to-End Tests** (`test_end_to_end.py`)
Complete user journey from search to checkout:
- Homepage navigation
- Product search with relevance verification
- Add to cart with address modal handling
- Cart verification (product, quantity, price)
- Checkout flow (stops at login wall)

#### 2. **Functional Tests** (`test_functionality.py`)
Core functionality validation:
- Add and remove single items
- Checkout button state changes
- Cart badge updates
- Product price retrieval

#### 3. **Multiple Products Tests** (`test_multiple_products.py`)
Bulk operations:
- Add multiple products from search
- Update product quantities in cart
- Verify batch operations

#### 4. **Negative Scenarios** (`test_negative_scenarios.py`)
Error handling and edge cases:
- Search for non-existent products
- Empty cart checkout validation
- Remove non-existent products
- Special character search handling
- Empty string search
- Very long search strings

---

## 🌐 Browser Configuration

### Browser Used: **Chromium**

This framework uses **Chromium** (via Playwright) as the default browser engine.

**Why Chromium?**
- ✅ **Stability**: Consistent behavior across platforms
- ✅ **Performance**: Fast execution and rendering
- ✅ **Playwright Integration**: Native support with automatic browser management
- ✅ **Headless Support**: Runs efficiently in CI/CD environments
- ✅ **DevTools Protocol**: Advanced debugging capabilities

### Browser Settings

```python
# From conftest.py
browser = playwright.chromium.launch(
    headless=Settings.HEADLESS,      # false = visible browser
    slow_mo=Settings.SLOW_MO,        # 500ms delay for visibility
)

context = browser.new_context(
    viewport={"width": 1920, "height": 1080},
    locale="he-IL",                  # Hebrew locale
    timezone_id="Asia/Jerusalem",    # Israel timezone
)
```

### Switching Browsers

To use a different browser, modify `conftest.py`:

```python
# For Firefox
browser = playwright.firefox.launch(...)

# For WebKit (Safari)
browser = playwright.webkit.launch(...)
```

---

## ⚠️ Known Limitations & Assumptions

### 1. **Address Modal Handling**

**Current Implementation:**
- The framework handles the delivery address modal that appears when adding the first product to cart
- Uses a `handle_address_modal` boolean parameter in `add_products_to_cart()` method
- When `handle_address_modal=False` (default in tests), the modal is closed without filling details

**Production Environment Assumption:**
In a **staging/production test environment**, this would be handled differently:
- **Test Database Integration**: Use a dedicated test SQL database with pre-configured addresses
- **API Mocking**: Mock address validation endpoints to return fixed, known-good responses
- **Test Accounts**: Utilize test user accounts with saved delivery addresses
- **Fixed Test Data**: Address and time slot data would come from a controlled test dataset

**Code Example:**
```python
# Current: Close modal without filling
result = search_page.add_products_to_cart(
    num_products=1, 
    handle_address_modal=False  # Just close the modal
)

# Production Test Environment: Would use API mocking
# The test database would have:
# - Pre-validated addresses for test users
# - Fixed delivery slots that never expire
# - Mock API responses for address verification
```

### 2. **Delivery Time Slot Selection**

**Current State:** 
- Time slot selection logic is implemented but mocked with environment variables
- Uses hardcoded date/time from `.env` file
- Fallback: If requested slot unavailable, selects first available slot

**Production Assumption:**
- In staging environments, delivery slots would be mocked via backend API
- Test database would maintain a set of always-available test slots
- No dependency on real delivery logistics

### 3. **Login/Authentication**

**Limitation:** 
- Tests stop at the login wall and do NOT complete actual purchases
- No real authentication is performed
- Tests verify login prompt appears, confirming checkout flow works

**Reason:** 
- Prevents accidental real orders
- No need for real user credentials
- Checkout validation is sufficient for UI/UX testing

### 4. **Payment Processing**

**Limitation:** 
- No actual payment methods are tested
- Payment gateway integration is NOT covered

**Reason:** 
- Payment testing would require sandbox/test payment environments
- Out of scope for UI automation
- Should be covered by payment provider's own test suite

### 5. **Product Availability**

**Assumption:** 
- Tests assume search term "חלב" (milk) returns results
- Product availability may vary in production
- Tests may fail if search yields no results

**Mitigation:** 
- Use common, always-available product categories
- Implement retry logic or fallback search terms

### 6. **Network Dependency**

**Limitation:** 
- Tests require active internet connection
- Dependent on Shufersal website availability
- No offline mode or mock server

**Impact:** 
- Tests may fail due to network issues
- Website downtime affects test execution

### 7. **Hebrew Language & RTL Support**

**Assumption:** 
- All selectors assume Hebrew (RTL) UI
- Tests are configured for Israeli locale (`he-IL`)
- May not work correctly if website switches to English

### 8. **Browser Compatibility**

**Tested On:** 
- Chromium (via Playwright)
- Windows 11, macOS, Linux

**Not Tested:** 
- Real Chrome, Firefox, Safari browsers
- Mobile browsers
- Older browser versions

### 9. **Test Data Isolation**

**Limitation:** 
- Cart state is not isolated between some tests
- Uses session-scoped fixtures for functional tests
- May have side effects if tests fail mid-execution

**Mitigation:** 
- Cleanup steps in tests (clear cart)
- Use fresh browser contexts for E2E tests

---

## 📁 Project Structure

```
shufersal_online_automation/
│
├── pages/                          # Page Object Model
│   ├── __init__.py
│   ├── base_page.py               # Base class with common methods
│   ├── home_page.py               # Homepage interactions
│   ├── search_results_page.py     # Search results & product selection
│   ├── cart_page.py               # Shopping cart sidebar
│   ├── checkout_page.py           # Checkout/login verification
│   └── address_modal_page.py      # Address & delivery slot modal
│
├── tests/                          # Test suites
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and configuration
│   ├── test_end_to_end.py         # E2E purchase flow tests
│   ├── test_functionality.py      # Functional tests
│   ├── test_multiple_products.py  # Bulk operations tests
│   └── test_negative_scenarios.py # Negative/edge case tests
│
├── utils/                          # Utilities
│   ├── __init__.py
│   ├── helpers.py                 # Helper functions (logging)
│   └── settings.py                # Configuration management
│
├── reports/                        # Test reports (generated)
│   └── report.html
│
├── temp/                           # Temporary files & logs
│   └── test_runs/                 # Test execution logs
│
├── .env                            # Environment variables (create this)
├── requirements.txt                # Python dependencies
├── pyproject.toml                 # Project metadata
└── README.md                       # This file
```

---

## 🤝 Contributing

### Code Style Guidelines

1. **Follow PEP 8**: Python style guide
2. **Page Object Model**: Keep page logic in page objects, test logic in tests
3. **Descriptive Names**: Use clear, meaningful variable and method names
4. **Documentation**: Add docstrings to all classes and methods
5. **Type Hints**: Use type annotations where applicable

### Adding New Tests

1. Identify the test category (functional, e2e, negative)
2. Create test method in appropriate test class
3. Use existing page objects or create new ones if needed
4. Add appropriate pytest markers
5. Include cleanup steps to avoid side effects

### Adding New Page Objects

1. Inherit from `BasePage`
2. Define selectors as class constants
3. Implement page-specific methods
4. Add comprehensive docstrings
5. Use logger for debugging information

---

## 📊 Test Execution Logs

Logs are automatically generated in `temp/test_runs/` with timestamp:
```
temp/test_runs/test_run_06-11-2025_14-30-45.log
```

Each log contains:
- Test execution steps
- Page navigation events
- Element interactions
- Errors and warnings

---

## 🔧 Troubleshooting

### Common Issues

**1. Browser not found**
```bash
playwright install chromium
```

**2. Tests fail with timeout**
- Increase `BROWSER_TIMEOUT` in `.env`
- Check internet connection
- Verify Shufersal website is accessible

**3. Hebrew characters not displaying**
- Ensure terminal supports UTF-8 encoding
- Check locale settings in `conftest.py`

**4. Address modal doesn't close**
- Verify selectors in `address_modal_page.py`
- Check if website UI has changed
- Increase wait timeouts


**Last Updated:** November 6, 2025  
**Framework Version:** 1.0.0  
**Playwright Version:** Latest  
**Python Version:** 3.8+
