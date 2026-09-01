# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how ML recommendation techniques can be integrated into an e-commerce application.

## Current Version: V6.1

The project includes a hybrid ML engine, a FastAPI REST service, and a polished Flutter mobile client.

## Architecture

```text
                 Flutter App
                     │
                     │ HTTP / JSON
                     ↓
                 FastAPI API
                     │
                     ↓
           Hybrid Recommendation
              ┌──────┴──────┐
              ↓             ↓
        Content-Based  Collaborative
              └──────┬──────┘
                     ↓
                Recommendations
```

## Recommendation Engine

The engine combines content-based filtering and user-based collaborative filtering. The default blend is 60% content and 40% collaborative, with scores normalized before blending.

## V5 — FastAPI

REST endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| GET | `/recommendations/{user_id}` | Get recommendations |

## V6 — Flutter Client

The Flutter application consumes the Python recommendation API and presents the results as a simple e-commerce-style mobile experience.

## V6.1 — Client Polish

The mobile client now includes:

- Automatic recommendation loading on startup
- Customer selection with automatic refresh
- Pull-to-refresh
- Explicit refresh action
- Loading, error, retry, and empty states
- Configurable API URL through `--dart-define`
- Material 3 UI
- Recommendation score visualization
- Content and collaborative component scores
- Human-readable recommendation explanations
- Reusable recommendation card and state widgets
- Network timeout and response validation

### Flutter Structure

```text
flutter_app/
├── lib/
│   ├── main.dart
│   ├── models/
│   │   └── recommendation.dart
│   └── services/
│       └── recommendation_service.dart
├── pubspec.yaml
└── README.md
```

### Run FastAPI

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api:app --reload
```

### Run Flutter

From `flutter_app/`:

```bash
flutter pub get
flutter run
```

Android emulator:

```bash
flutter run --dart-define=API_URL=http://10.0.2.2:8000
```

iOS simulator:

```bash
flutter run --dart-define=API_URL=http://127.0.0.1:8000
```

For a physical device, replace the API host with the machine's LAN IP address.

## Stack

### ML / Backend

- Python
- Pandas
- scikit-learn
- FastAPI
- Uvicorn
- pytest

### Mobile

- Flutter
- Dart
- Material 3
- HTTP/REST

## Roadmap

- [x] V1: Content-based recommendation
- [x] V2: Interaction weighting + explainable recommendations
- [x] V3: User-based collaborative filtering
- [x] V4: Hybrid recommendation
- [x] V5: FastAPI recommendation API
- [x] V6: Flutter client
- [x] V6.1: Client polish
- [ ] V7: React Native/Web client
