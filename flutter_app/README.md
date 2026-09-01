# Flutter Client

A simple Flutter client for the Product Recommendation Engine.

## Architecture

```text
Flutter UI
    ↓
RecommendationService
    ↓ HTTP GET
FastAPI
    ↓
Hybrid Recommendation Engine
    ↓
JSON Recommendations
    ↓
Flutter Cards
```

## Run

From this directory:

```bash
flutter pub get
flutter run
```

The default Android emulator API URL is:

```text
http://10.0.2.2:8000
```

For another environment, override it with:

```bash
flutter run --dart-define=API_URL=http://YOUR_HOST:8000
```

For an iOS simulator, a typical local API URL is:

```bash
flutter run --dart-define=API_URL=http://127.0.0.1:8000
```

Make sure the FastAPI server is running first:

```bash
uvicorn src.api:app --reload
```

## What the App Demonstrates

- Customer selection
- REST API integration
- JSON model parsing
- Loading and error states
- Recommendation ranking
- Recommendation score visualization
- Explainable recommendation text
- Pull-to-refresh
