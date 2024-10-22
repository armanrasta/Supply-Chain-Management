# Supply Chain Management (SCM) System

## Overview

This SCM project is designed to manage and optimize various aspects of supply chain processes, including demand forecasting, supplier relationship management, inventory tracking, transportation costs, and R&D investments. The system integrates **Odoo** as the main ERP panel and **FastAPI** for building additional modules and services for further backend developments.

The project includes multiple models for managing inventory, suppliers, transportation, and other SCM-specific parameters, making it robust for large-scale implementations and adaptable for a variety of industries.

## Features

1. **Demand Forecasting**:
   - Multi-period demand forecasts based on various scenarios (Best Case, Worst Case, Most Likely).
   - Constraint validation on forecasting periods and unique forecast entries.

2. **Inventory Management**:
   - Management of inventory items with parameters for tracking batches, perishable goods, capacity constraints, and stock turnover ratios.
   - Integration with Odoo’s inventory management for real-time tracking and analytics.

3. **Supplier Relationship Management**:
   - Track supplier reliability indices (SLAs, delivery rates).
   - Supplier relationship strength metrics including communication, trust, transparency, and collaboration.

4. **Supplier Product Innovation**:
   - Track supplier innovation rates based on new product introductions.
   - Monitor incremental vs. radical innovations, sustainability indices, and customer feedback post-launch.

5. **Transportation Cost Management**:
   - Track transportation costs per mode (air, road, sea, etc.), including cost per kilometer, cost per hour, and fixed costs.
   - Validation on unique entries per transport mode and carrier, as well as constraints on cost positivity and variable cost percentages.

6. **Supplier R&D Investment Tracking**:
   - Manage supplier R&D investment levels and trends, including ROI estimates, research focus areas, and collaboration with external entities.

7. **Supply Chain Network Robustness**:
   - Model robustness parameters for network design including connections to inventory items, transportation modes, and suppliers.

## Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) for RESTful services.
- **ERP System**: [Odoo](https://www.odoo.com/) for managing SCM models, panels, and views.
- **Database**: PostgreSQL (via Odoo’s ORM and SQLAlchemy in FastAPI for additional modules).
- **Testing**: Odoo’s testing framework, along with unit tests written in Python.
- **Frontend**: Odoo’s built-in UI for panel management.

## Installation and Setup

### Prerequisites

- Python 3.10 or higher.
- PostgreSQL.
- Odoo 17 or later.
- FastAPI.

### Odoo Setup

1. Install Odoo via Docker or using the source code.
2. Clone the SCM module repository to your Odoo `addons` directory:

    ```bash
    git clone https://github.com/your-repo/scm-addon.git
    ```

3. Install the module by enabling developer mode in Odoo and installing the SCM app from the Apps menu.
4. Configure basic settings such as inventory items, suppliers, and transportation modes.

### Database Configuration

In your Odoo instance, ensure the PostgreSQL database is properly configured in `odoo.conf` and accessible. FastAPI can connect to the same database or a separate one as per your requirements.

## Models

### 1. **Demand Forecasting (`scm.demand_forecast`)**

- Fields: `inventory_item_id2`, `scenario`, `period_start_date`, `period_end_date`, `forecasted_quantity`, `supplier_id3`.
- Unique constraint on inventory item, scenario, and period to avoid duplicate forecasts.

### 2. **Inventory Management**

- Inventory parameters: Reorder points, safety stock levels, ABC classification, etc.
- Model: `scm.inventory_item`.

### 3. **Supplier Relationship Strength (`scm.supplier_relationship_strength`)**

- Tracks key metrics: communication, trust, transparency, collaboration, delivery rate.

### 4. **Transportation Cost Management (`scm.mode_specific_transportation_cost`)**

- Tracks cost per transport mode and carrier with constraint checks on costs and date effectiveness.

### 5. **Supplier Product Innovation (`scm.supplier_product_innovation`)**

- Tracks supplier innovation rates and feedback, including patent filings and market impact.

### 6. **Supplier R&D Investment (`scm.supplier_rd_investment`)**

- Tracks investment amounts, periods, ROI, and research focus.

### 7. **Network Robustness (`scm.network_robustness`)**

- Connects robustness parameters with inventory, transportation modes, and suppliers.

## Testing

The project uses Odoo’s integrated testing framework for module and field validation.

To run tests for Odoo:

```bash
./odoo-bin -c ./odoo17.conf -d <database_name> -u scm -i scm --test-enable  --log-level=test --stop-after-init 
```

## Future Enhancements

- **API Integration**: To computing more complex activities.
- **Machine Learning Integration**: Use predictive models for demand forecasting.
- **IoT Integration**: Connect with IoT devices for real-time tracking of goods and inventory.
- **Blockchain for Supplier Transparency**: Implement blockchain technology for tracking transactions and building trust with suppliers.

## License

This project is licensed under the **GNU Lesser General Public License v3.0 (LGPL-3.0)**.

### LGPL-3.0 License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program. If not, see [https://www.gnu.org/licenses/lgpl-3.0.html](https://www.gnu.org/licenses/lgpl-3.0.html).

---

By following this guide, you can set up and contribute to the SCM project with ease, leveraging the power of Odoo’s ERP system along with the flexibility of FastAPI for additional services.

---
