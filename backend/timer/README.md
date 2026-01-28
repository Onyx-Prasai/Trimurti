# Time-at-Risk (TaR) Timer Feature

This document explains how to use the TaR Timer feature.

## Setup

1.  **Environment Variables:** Make sure you have the following environment variable in your `.env` file:

    ```
    OPENWEATHERMAP_API_KEY=<your_openweathermap_api_key>
    ```

    You can get a free API key from [OpenWeatherMap](https://openweathermap.org/api). The key `f59eb3fc9bfc508396f0b1f5e4365f42` is provided for testing purposes.

## API Endpoints

### 1. Pickup a Blood Packet

This endpoint is called when a courier picks up a blood packet. It starts the TaR timer.

*   **URL:** `/api/timer/pickup/`
*   **Method:** `POST`
*   **Authentication:** `Token <user_token>`
*   **Body:**

    ```json
    {
        "blood_request_id": <id_of_the_blood_request>,
        "initial_temperature": <initial_temperature_in_celsius> // optional, defaults to 4.0
    }
    ```

*   **Success Response (201 Created):**

    ```json
    {
        "message": "TaR Timer started.",
        "blood_packet": { ... },
        "tar_timer": { ... }
    }
    ```

### 2. Update Courier Location

This endpoint is called by the courier's app periodically to update its location. It also checks for traffic jams and sends notifications if the TaR threshold is reached.

*   **URL:** `/api/timer/update-location/`
*   **Method:** `POST`
*   **Authentication:** `Token <user_token>`
*   **Body:**

    ```json
    {
        "latitude": <courier_latitude>,
        "longitude": <courier_longitude>,
        "traffic_jam_detected": <true_or_false> // optional, defaults to false
    }
    ```

*   **Success Response (200 OK):**

    ```json
    {
        "message": "Location updated successfully."
    }
    ```

*   **Success Response with Notification (200 OK):**

    ```json
    {
        "message": "Location updated. Critical notifications sent.",
        "notifications": [
            { ... }
        ]
    }
    ```

## How it Works

1.  When a courier picks up a blood packet, the `pickup_packet` endpoint is called.
2.  The backend fetches the current ambient temperature for Kathmandu from OpenWeatherMap.
3.  It then uses a simplified thermal decay algorithm to predict how long it will take for the blood packet to reach a critical temperature.
4.  The courier's app periodically calls the `update_location` endpoint.
5.  If a traffic jam is detected (by setting `traffic_jam_detected` to `true`), the backend recalculates the TaR with a higher simulated ambient temperature.
6.  If the time since pickup exceeds the critical threshold, a notification is logged. In a full implementation, this would trigger a push notification to the courier's device.
