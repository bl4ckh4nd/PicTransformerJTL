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

4.  Create a Vite-based React frontend:
    ```bash
    npm create vite@latest frontend --template react
    cd frontend
    npm install
    ```

5.  Install the necessary TypeScript types for React:
    ```bash
    cd frontend
    npm install @types/react @types/react-dom
    ```

6.  Add `"jsx": "react-jsx"` to the `compilerOptions` section of `frontend/tsconfig.json`.

7.  Modify `frontend/src/main.ts` to render the React application:
    ```typescript
    import React from 'react'
    import ReactDOM from 'react-dom/client'
    import App from './App.jsx'
    import './index.css'

    ReactDOM.createRoot(document.getElementById('app')).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
    )
    ```

8.  Rename `frontend/src/App.js` to `frontend/src/App.jsx`.

9.  Create a `vite.config.js` file in the `frontend` directory with the following content:
    ```javascript
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'

    // https://vitejs.dev/config/
    export default defineConfig({
      plugins: [react()],
      server: {
        proxy: {
          '/images': 'http://localhost:5000', // Proxy /images requests to the backend
        }
      }
    })
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
    npm run dev
    ```

3.  Open the frontend in your browser (usually `http://localhost:5173`).

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
│   │   ├── App.jsx
│   │   └── App.css
│   ├── public/
│   │   └── index.html
│   └── package.json
├── input_images/
├── output_images/
├── temp_images/
└── README.md