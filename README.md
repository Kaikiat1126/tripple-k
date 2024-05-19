# Analyzing Fraudulent E-commerce Transaction by Triple K
This project is a web-based dashboard for analyzing transaction data to identify fraudulent activities. The dashboard uses Chart.js to visualize data and display insights from different hypotheses.

## Table of Contents
- [Inspiration](#inspiration)
- [Objectives](#objectives)
- [Installation](#installation)
- [Implementation](#implementation)
  - [Dataset](#dataset)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Contributing](#contributing)
- [License](#license)


## Inspiration
Since the onset of COVID-19, e-commerce transactions have surged dramatically, accompanied by a corresponding spike in fraudulent activities. In response to the growing demand for enhanced security on e-commerce platforms, **Triple K** has embarked on a project aimed at identifying the primary factors contributing to fraud and developing effective prevention strategies. Our mission is to fortify the e-commerce environment, safeguarding users from financial losses and ensuring a secure, trustworthy shopping experience.

## Objectives
**"Analyzing Fraudulent E-commerce Transactions by Triple K"** leverages advanced data analysis to identify patterns indicative of fraudulent activities. Our system processes transaction data, cleans and prepares it, and shares insights through an interactive web interface. This allows stakeholders to visualize and understand potential fraud patterns and take preventive measures.

## Installation
Follow the installation instructions in the backend [README.md](./backend/README.md) and frontend [README.md](./frontend/README.md) file.

## Implementation
### Dataset
We began by obtaining a synthetic dataset designed to simulate realistic e-commerce transactions. 
The dataset is retrieved from Kaggle [🚨 Fraudulent E-Commerce Transactions 💳](https://www.kaggle.com/datasets/shriyashjagtap/fraudulent-e-commerce-transactions )

### Backend
Using Python, we performed extensive data cleaning to ensure the dataset was free of inconsistencies and ready for analysis. FastAPI, a modern web framework for building APIs with Python, was used to develop an API that serves the cleaned data to the front end.

### Frontend
The front end, built with HTML, CSS, and JavaScript, uses Chart.js to create interactive visualizations that display transaction patterns and potential fraud indicators. 

