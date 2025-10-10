# vue-music-app

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Running the Application Locally

To run the full application (backend and frontend), follow these steps:

### 1. Backend Setup (Python FastAPI)

1.  **Navigate to the project root directory**:
    ```sh
    cd /Users/mfrost/learning/ai/gemini/music
    ```
2.  **Create and activate a Python virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install backend dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
4.  **Run the FastAPI application**:
    ```sh
    ./venv/bin/uvicorn main:app --reload
    ```
    The backend server will typically run on `http://127.0.0.1:8000`.

### 2. Frontend Setup (Vue.js)

1.  **Navigate to the frontend directory**:
    ```sh
    cd /Users/mfrost/learning/ai/gemini/music/vue-music-app
    ```
2.  **Install frontend dependencies**:
    ```sh
    npm install
    ```
3.  **Run the Vue.js development server**:
    ```sh
    npm run dev
    ```
    The frontend application will typically run on `http://localhost:5173`.

Once both the backend and frontend servers are running, you can access the application in your web browser at the frontend's address (e.g., `http://localhost:5173`).