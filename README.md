Online Retail Customer Analysis



Project Overview



This project analyses an online retail dataset to uncover sales trends, product performance, customer purchasing behaviour, and revenue patterns.



The objective is to transform raw transactional data into actionable business insights using Python, Pandas, and data visualisation.



Dataset



Source: UCI Online Retail Dataset



Original records: 541,909



Cleaned records: 392,692



Unique customers: 4,338



Unique products: 3,665



Countries represented: 37



Tools and Technologies



Python



Pandas



Matplotlib



Excel



Power BI (planned dashboard stage)



Data Cleaning



The following steps were performed:



Investigated missing values.



Identified and removed 5,268 exact duplicate records.



Removed records with missing Customer IDs or product descriptions.



Excluded cancelled transactions.



Removed transactions with non-positive quantities or unit prices.



Calculated revenue using quantity multiplied by unit price.



Analysis Performed



Sales Performance



Monthly revenue trends.



Top-performing products.



Revenue by country.



International revenue excluding the United Kingdom.



Customer Analysis



Top customers by revenue.



Repeat customer analysis.



Recency, Frequency, and Monetary (RFM) analysis.



Customer segmentation.



Key Findings



Total cleaned revenue: £8,887,208.89.



Repeat customer rate: 65.58%.



November 2011 recorded the highest monthly revenue at approximately £1.16 million.



The United Kingdom generated approximately £7.29 million in revenue.



Champions generated approximately £6.48 million, representing about 72.9% of total revenue.



At Risk customers accounted for approximately £1.05 million in historical revenue.



Customer Segmentation



Customers were classified into six groups:



Champions



Loyal Customers



Potential Loyalists



At Risk



Lost Customers



Other Customers



Segmentation was based on RFM scores calculated from customer purchasing behaviour.



Project Structure



Customer\_Analysis/

│

├── data/

├── charts/

├── customer\_analysis.py

└── README.md



Outputs



The project generates:



Cleaned transaction dataset.



Customer RFM and segmentation dataset.



Monthly revenue summary.



Country revenue summary.



Product revenue summary.



Sales and customer segmentation charts.



Business Recommendations



Retain Champions through loyalty programmes and personalised offers.



Develop targeted re-engagement campaigns for At Risk customers.



Encourage repeat purchases among Potential Loyalists.



Investigate opportunities for growth in international markets.



Monitor monthly revenue trends to support sales planning.



Limitations



December 2011 contains incomplete monthly data, so it should not be compared directly with full months.



Revenue represents historical transaction value, not profit.



Customer segmentation uses simplified RFM classification rules.



Author



Data Analysis Portfolio Project

