# Dove
Dividend Income Calculator
# Dove - Dividend Income Calculator: Complete File Structure

```
dove_app/
│
├── app.py                      # Main application file
│
├── modules/                    # Modular components folder
│   ├── __init__.py             # Makes modules a package
│   ├── data.py                 # Data initialization and loading
│   ├── calculations.py         # Calculation functions
│   ├── visualizations.py       # Chart and visualization functions
│   ├── projections.py          # Projection calculation functions
│   ├── ui_components.py        # UI rendering functions with header/footer
│   └── about.py                # About page content with Dove branding
│
└── requirements.txt            # Dependencies list
```

## File Contents Overview

### app.py
The main application file that orchestrates all components. It:
- Sets up the Streamlit page configuration
- Initializes data on first run
- Displays the header and footer
- Creates the tab structure
- Handles main application flow

### modules/__init__.py
Makes the modules directory a proper Python package, allowing imports between modules.

### modules/data.py
Handles all data operations:
- Initializes default data (stock/ETF information)
- Stores and updates share quantities
- Calculates initial income values
- Provides data access functions

### modules/calculations.py
Contains core calculation logic:
- Calculates monthly income distribution
- Computes portfolio metrics
- Handles dividend calculations across different payment schedules

### modules/visualizations.py
Creates data visualizations:
- Monthly income distribution charts
- Asset allocation pie charts
- Income source visualizations
- Formatting functions for currency display

### modules/projections.py
Handles future income projections:
- Projects future income with growth rates
- Calculates DRIP (Dividend Reinvestment Plan) effects
- Creates projection visualization charts
- Models portfolio growth over time

### modules/ui_components.py
Manages UI elements:
- Renders the portfolio editor interface
- Creates projection control panels
- Displays metrics and KPIs
- Provides the branded header and footer
- Handles CSS styling

### modules/about.py
Contains the About page content:
- Dove product information
- AvaResearch LLC branding
- Educational content about dividend investing
- Portfolio explanation

### requirements.txt
Lists all Python package dependencies:
- streamlit
- pandas
- numpy
- matplotlib
- plotly