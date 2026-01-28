# Trimurti - Blood Management and Donor Reward System

## Introduction
A comprehensive platform designed to streamline blood donation processes, manage blood stock efficiently, and incentivize donors through a robust reward system. It connects donors, hospitals, and blood banks to ensure timely blood availability and foster a community of regular blood donors.

## Features

### 1. Donor Management & Engagement
*   **Donor Profiles**: Personalized profiles for donors, tracking their blood group, donation history, and eligibility.
*   **Donation Tracking**: Records individual donations, awards points, and provides insights into lives saved.
*   **Eligibility Check**: Automatically determines donor eligibility based on last donation date.
*   **Referral System**: Incentivizes new donor sign-ups through referral bonuses.
*   **Badges & Recognition**: Recognizes and rewards donors with badges based on their donation milestones.
*   **Location-Based Services**: Allows donors to share their location for efficient matching with nearby blood requests, with privacy consent.

### 2. Blood Request & Supply Management
*   **Hospital Blood Requests**: Hospitals can submit urgent blood requests with details on blood type, product, and urgency.
*   **Emergency Blood Requests**: Users can initiate emergency blood requests, triggering SMS notifications to nearby matching donors.
*   **Blood Stock Dashboard**: Real-time overview of blood stock levels across participating hospitals and blood banks.
*   **Automated Stock Ingestion**: Hospitals can integrate to automatically update blood stock levels via API, recording all transactions.
*   **Low Stock Alerts**: Proactive notifications for hospitals when blood stock falls below critical thresholds.
*   **Find Blood Banks**: Locate nearby blood banks with contact information and operating hours.
*   **Blood Needs Prediction**: Utilizes predictive analysis to forecast regional blood requirements, aiding in proactive resource allocation.
*   **Donation Drives**: Management and tracking of planned blood donation campaigns, including target collection and progress.

### 3. Reward System
*   **Points for Donations**: Donors earn points for each successful blood donation.
*   **Money Rewards**: Redeem earned points for cash through platforms like Esewa.
*   **Discount Rewards**: Unlock exclusive discounts from various businesses (restaurants, pharmacies, etc.) using points.
*   **Medicine/Healthcare Product Rewards**: Exchange points for essential medicines or healthcare products.

### 4. AI-Powered Health Assistant
*   **Interactive Chatbot**: An AI assistant (powered by Mistral AI) providing health tips, nutritional advice, and answers to blood donation-related queries, with a focus on natural remedies and Nepalese dietary context.
*   **Blood Report Analysis**: Upload blood report images or PDFs for AI-driven analysis, offering personalized health insights, dietary recommendations, lifestyle tips, and wellness advice, while strictly avoiding medical diagnoses or prescriptions.

### 5. Multi-User Architecture
*   **Donor Accounts**: Standard user accounts for blood donors.
*   **Hospital Accounts**: Dedicated accounts for hospitals to manage requests and stock.
*   **Blood Bank Accounts**: Accounts for blood banks to manage their operations.
*   **Admin Accounts**: Administrative access for platform management.

## How it Works

### Frontend (User Interface)
The frontend, built with React, provides an intuitive and responsive user experience:
*   **Dashboard**: A personalized hub for donors to view their donation history, points, badges, and recent activities.
*   **Blood Request/Find Blood**: Interfaces for requesting blood or searching for available blood/blood banks using filters and map views.
*   **AI Health**: A dedicated section for interacting with the AI chatbot and uploading blood reports for analysis.
*   **Rewards**: A catalog of available rewards (money, discounts, medicines) where users can browse and redeem their points.
*   **Profile & Settings**: Users can manage their personal information, location consent, and security settings.

### Backend (API & Business Logic)
The backend, powered by Django REST Framework, handles all data management, business logic, and third-party integrations:
*   **User & Profile Management**: Securely manages user authentication, donor profiles, and specific profiles for hospitals, blood banks, and administrators.
*   **Data Models**: Robust data models (using Django ORM) for Donors, Hospitals, Blood Banks, Donations, Blood Requests, Rewards, Stock, Transactions, and more.
*   **API Endpoints**: A comprehensive set of RESTful APIs to facilitate communication between the frontend and backend, enabling all core functionalities.
*   **SMS Service Integration**: Integrates with an SMS gateway (e.g., Twilio) to send timely notifications to potential donors for emergency blood requests, utilizing location-based matching.
*   **AI Integration**: Connects with Mistral AI for the health assistant chatbot and blood report analysis features, ensuring responsible and health-focused recommendations.
*   **Blood Stock Logic**: Manages the append-only transaction ledger and materialized blood stock views, updating in real-time as hospitals ingest data.
*   **Prediction Engine**: Processes historical data to predict future blood needs, exposed via an API endpoint.

## Getting Started

### Prerequisites
*   Python 3.8+
*   Node.js 14+
*   npm or yarn
*   PostgreSQL (recommended) or SQLite

### Setup Instructions

#### Backend
1.  Navigate to the `backend/` directory.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Set up environment variables (e.g., `DJANGO_SETTINGS_MODULE`, `DATABASE_URL`, `MISTRAL_API_KEY`, `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`).
4.  Run migrations: `python manage.py migrate`
5.  Create a superuser: `python manage.py createsuperuser`
6.  Run the development server: `python manage.py runserver`

#### Frontend
1.  Navigate to the `frontend/` directory.
2.  Install dependencies: `npm install` or `yarn install`
3.  Set up environment variables (e.g., `VITE_API_URL`).
4.  Run the development server: `npm run dev` or `yarn dev`

## Technologies Used
*   **Frontend**: React, Vite, Tailwind CSS
*   **Backend**: Django, Django REST Framework
*   **Database**: PostgreSQL/SQLite
*   **AI**: Mistral AI (for Chatbot and Report Analysis)
*   **SMS**: Twilio (for notifications)

## Contributing
*(Placeholder for contributing guidelines)*

## License
*(Placeholder for license information)*