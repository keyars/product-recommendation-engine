# Product Recommendation Engine

A small, practical product recommendation engine demonstrating how ML recommendation techniques can be integrated into an e-commerce application.

## Current Version: V6

The project now includes a Flutter mobile client consuming the FastAPI recommendation service.

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

The engine combines:

- **Content-based filtering** — products similar to the customer's own interaction history.
- **User-based collaborative filtering** — products supported by similar customer behaviour.

Default blend:

- Content-based: **60%**
- Collaborative: **40%**

Scores are normalized before blending.

## V5 — FastAPI

REST endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Service information |
| GET | `/health` | Health check |
| GET | `/recommendations/{user_id}` | Get recommendations |

## V6 — Flutter Client

The Flutter application demonstrates a real mobile integration with the Python ML service.

It includes:

- Customer selection
- REST API integration using `http`
- JSON model parsing
- Loading state
- Error state
- Pull-to-refresh
- Recommendation ranking cards
- Score visualization
- Human-readable recommendation explanations

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
- [ ] V7: React Native/Web client
