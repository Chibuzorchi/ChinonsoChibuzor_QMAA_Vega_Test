# SauceDemo Test Automation Framework

## Overview
This project implements an automated testing framework for the SauceDemo web application using Python, Playwright, and pytest.

## Documentation
- [Manual Test Cases](https://docs.google.com/spreadsheets/d/1KbOtMM8CnG6nQ-7yYZF82PqxSdnqF1Qq1aA-ugvYqVI/edit?usp=sharing)
- [Test Report](https://docs.google.com/document/d/13086aG_nCpqw4Li9CrZR99xS8R-AuXQBO3P0NSGIuIs/edit?usp=sharing)

## Features

- Page Object Model design pattern
- BDD tests using pytest-bdd
- Unit tests using pytest
- Allure reporting integration
- Screenshot capture on test failure
- Detailed logging

## Test Coverage

1. Authentication Tests
   - Standard user login
   - Locked out user validation
   - Invalid credentials handling

2. Inventory Tests
   - Product sorting
   - Add/remove items from cart
   - Cart badge updates

3. Cart Tests
   - Add/remove items
   - Cart persistence
   - Cart count validation

4. Checkout Tests
   - Complete checkout flow
   - Form validation
   - Empty cart validation
   - Order confirmation

## Prerequisites

- Python 3.9+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ChinonsoChibuzor_QMAA_Vega_Test.git
   cd ChinonsoChibuzor_QMAA_Vega_Test
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Running Tests

1. Run all tests:
   ```bash
   pytest
   ```

2. Run specific test types:
   ```bash
   # Run BDD tests
   pytest saucedemo/features/

   # Run unit tests
   pytest saucedemo/tests/

   # Run with browser visible
   pytest --headed
   ```

3. Run tests with specific markers:
   ```bash
   # Run smoke tests in headless mode
HEADLESS=true python3 -m pytest -v -m smoke

# Run regression tests in headless mode
HEADLESS=true python3 -m pytest -v -m regression

# Run negative tests in headless mode
HEADLESS=true python3 -m pytest -v -m negative
   ```

## Project Structure

```
saucedemo/
├── config/         # Configuration and constants
├── features/       # BDD feature files
├── pages/          # Page Object Models
└── tests/          # Unit tests
```

## Known Issues

1. Security/UX Issue: Direct access to inventory page possible when logged out
   - Current behavior: Can access /inventory.html without authentication
   - Expected: Should redirect to login

2. Security/UX Issue: Checkout allowed with empty cart
   - Current behavior: No validation on cart contents
   - Expected: Error message or disabled checkout

## Test Reports
- HTML reports are generated in `test-results/` directory
- Screenshots of failures are saved in `screenshots/` directory
- Test logs are available in `logs/` directory

## CI/CD Pipeline
The project uses GitHub Actions for continuous integration:
- Automated test execution on push/PR
- Parallel test execution
- Test report generation
- Artifact upload for test results

## Project Components
1. **Config**: Configuration management and constants
2. **Features**: BDD feature files
3. **Pages**: Page Object Models
4. **Tests**: Test implementation files
5. **Logs**: Test execution logs
6. **Reports**: Test execution reports

## Best Practices
- Page Object Model design pattern
- BDD approach using Gherkin syntax
- Environment variable management
- Logging and reporting
- Error handling and retries
- Type hints and documentation
- Code formatting and linting

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
[Add your contact information here]