🚚 Factory-to-Customer Shipping Route Efficiency Analysis
📌 Project Overview

This project analyzes shipping and logistics performance using the Nassau Candy Distributor dataset to identify inefficiencies, delays, and regional bottlenecks.

The goal is to enable data-driven decision-making by providing insights into delivery performance across regions, states, and shipping methods.

An interactive dashboard was developed to monitor key performance metrics and support operational optimization.

🎯 Objectives
Analyze shipping performance across regions and states
Identify high-delay routes and geographic bottlenecks
Compare efficiency across different shipping methods
Define and track key performance indicators (KPIs)
Build an interactive dashboard for business insights
📊 Key Features
📈 KPI Monitoring
Average Lead Time
Delay Frequency (%)
Efficiency Score
🗺 Geographic Analysis
State-level shipping efficiency heatmap
Regional bottleneck identification
🚚 Ship Mode Comparison
Lead time comparison across shipping methods
Delay distribution analysis
🛣 Route Drill-Down
State-level performance insights
On-time vs delayed shipment tracking
📦 Order-Level Timeline
Shipment tracking from order to delivery
Delay classification
📓 Exploratory Data Analysis (EDA)

The analytical foundation of this project is documented in the Jupyter Notebook:

👉 notebooks/Nassau_factory_to_customer_project.ipynb

🔍 Notebook Covers:
Data cleaning and preprocessing
Lead time calculation (Order Date → Ship Date)
KPI creation (Delay %, Efficiency Score)
Regional and state-level analysis
Shipping mode comparison
Insight generation
🧠 Key Insights
Significant variation in shipping performance across regions
Certain states consistently act as logistics bottlenecks
Standard Class shipments show the highest delay frequency
Faster shipping modes (Same Day, First Class) are more reliable
Data visibility enables proactive logistics optimization
🛠 Tech Stack
Python
Pandas
Streamlit
Plotly
⚙️ How to Run the Project
Clone the repository:
git clone https://github.com/your-username/your-repo-name.git
Navigate to the project folder:
cd your-repo-name
Install dependencies:
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py
📁 Dataset

The dataset includes:

Order Date
Ship Date
Region
State/Province
Ship Mode
Order ID
📈 Business Impact

This project helps:

Improve logistics efficiency
Reduce shipping delays
Identify operational bottlenecks
Enable data-driven decision-making
Enhance supply chain visibility

👨‍💼 Author
Zaid Shaikh
Business Analyst Intern

Guided by: Ankit
Internship: Unified Mentor
