# Coin Image Processor

This application automates the process of preparing coin images by removing backgrounds and combining front and back images into a single image.

## Prerequisites

*   Python 3.x
*   Node.js and npm

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd coin_processor
    ```

2.  Create a virtual environment for the Python backend:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  Install the required Python packages:
    ```bash
    pip install Flask Pillow python-dotenv watchdog rembg flask_cors
    ```

4.  Install the React frontend dependencies:
    ```bash
    cd frontend
    npm install
    ```

## Configuration

1.  Create a `.env` file in the `backend` directory. You don't need an API key for `rembg`, so the file can be empty.

## Usage

1.  Run the backend:
    ```bash
    python backend/app.py
    ```

2.  Run the frontend:
    ```bash
    cd frontend
    npm start
    ```

3.  Open the frontend in your browser (usually `http://localhost:3000`).

4.  Place images in the `input_images` directory. The processed images will appear in the `output_images` directory and in the frontend.

5.  You can delete images from the frontend.

## Directory Structure

```
coin_processor/
├── backend/
│   ├── app.py
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   ├── public/
│   │   └── index.html
│   └── package.json
├── input_images/
├── output_images/
├── temp_images/
└── README.md
```

**Note:** Ensure that `react-scripts` is listed as a dev dependency in `frontend/package.json`.