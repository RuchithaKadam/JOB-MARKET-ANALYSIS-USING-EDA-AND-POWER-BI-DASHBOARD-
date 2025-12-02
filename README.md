💼 Job Market Analysis Dashboard – WorkIndia

📘 Project Overview
This project focuses on analyzing the Indian job market using data collected from WorkIndia, a job listing platform. Through web scraping, data cleaning, and visualization, this project provides key insights into salary trends, job demand, company-wise opportunities, and city-level analysis.
An interactive Power BI dashboard was built to visualize metrics such as total companies, job roles, salary averages, and top-paying organizations across major cities.

🎯 Objectives
- To analyze the job market landscape across major Indian cities.
- To identify salary variations and hiring patterns by company and role.
- To visualize top-paying companies and job distribution for better market insights.
- To assist job seekers and recruiters in understanding current market demand.

⚙️ Project Workflow
Data Collection:
- Scraped job data from WorkIndia.com - using Python, Requests, and BeautifulSoup.
- Extracted details such as job title, company name, location, salary range, experience, education, gender preference, and English communication requirement.
Data Cleaning & Transformation:
- Cleaned company names, standardized education and experience fields.
- Extracted Min_Salary and Max_Salary using regular expressions.
- Handled missing values and converted salary columns into numeric formats.
- Created new feature Avg_Salary for analysis.
Exploratory Data Analysis (EDA):
- Conducted univariate and bivariate analysis on salaries, roles, and experience.
- Analyzed city-wise and company-wise job distribution.
- Explored correlations between salary, education, experience, and communication skills.
Dashboard Creation (Power BI):
- Built an interactive dashboard visualizing total companies, job roles, and salary insights.
- Displayed top-paying companies, city-wise job distribution, and average salary ranges.
- Used charts, KPIs, and filters for dynamic insights.

🧩 Key Insights
- Mumbai, Bengaluru, and Hyderabad have nearly equal job shares (~33% each).
- Average Minimum Salary: ₹19.61K | Average Maximum Salary: ₹30.54K.
- Everest Fleet Pvt Ltd, Disha Skill Training, and Propoint Manpower are among the top-paying companies.
- Strong English communication and higher education levels correlate with better salaries.
- Most job opportunities cater to freshers or 1–2 years of experience.

🧰 Tools & Technologies
- Python – Data collection and cleaning
- Libraries: Requests, BeautifulSoup, Pandas, NumPy, Matplotlib, Seaborn
- Power BI – Dashboard design and visualization
- Jupyter Notebook – Exploratory data analysis and preprocessing

📊 Dashboard Highlights
- Total Companies: 934
- Total Roles: 1455
- Average Min Salary: ₹19.61K
- Average Max Salary: ₹30.54K
- Top Paying Companies: Everest Fleet Pvt Ltd, Disha Skill Training, Propoint Manpower
