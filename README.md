# MediSupply

**Database-driven Django website for healthcare supply chain purchase orders.**

## Overview
MediSupply is a Django application designed to streamline the purchase order process in healthcare institutions. It allows:
- Hospital Staff to create purchase orders.
- Purchasing Manager to review, approve, or reject orders.
- Suppliers to update order status (Shipped, Delivered).
- Administrators to manage users and system settings.

All core functionality is covered with automated tests to ensure correctness.

## Features
- Custom user roles: Hospital Staff, Purchasing Manager, Supplier, Administrator.
- Create, review, approve/reject, and fulfill purchase orders.
- Attach multiple order items with quantities and pricing.
- Role-based views and permissions.
- Data fixtures for initial users and sample data.
- Full BDD-style test coverage for all use cases.

## Live Demo
_Once deployed, add the public URL here._

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Toju-ik/MediSupply.git
   cd MediSupply/medisupplyproject
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations and load fixtures:
   ```bash
   python manage.py migrate
   python manage.py shell  # then run fixture commands or load via loaddata
   ```
5. Create development superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Fixtures
Initial data is provided in `mediapp/fixtures/`:
- `initial_users.json` for admin and test users.
- _(Add PurchaseOrder/OrderItem fixtures if used.)_

Load fixtures with:
```bash
python manage.py loaddata initial_users.json
```

## Running Tests
Execute the full test suite:
```bash
python manage.py test
```

## Project Structure
```
MediSupplyProject/
├── MediSupplyProject/    # Django project settings
├── mediapp/              # Main app: models, views, forms, tests, fixtures
│   ├── fixtures/         # JSON fixture files
│   ├── migrations/
│   ├── templates/mediapp/  # HTML templates
│   ├── static/           # Static assets (CSS, JS)
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── tests.py
├── Deliverable2/         # Use cases (PDF), ERD (PDF), test ZIP
├── README.md
└── requirements.txt
```

## Technologies
- Python 3.13
- Django 5.2
- Bootstrap 4

## License
MIT License. See [LICENSE](LICENSE) for details.

