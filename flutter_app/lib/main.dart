import 'package:flutter/material.dart';

import 'models/recommendation.dart';
import 'services/recommendation_service.dart';

void main() {
  runApp(const RecommendationApp());
}

class RecommendationApp extends StatelessWidget {
  const RecommendationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Product Recommendations',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const RecommendationHomePage(),
    );
  }
}

class RecommendationHomePage extends StatefulWidget {
  const RecommendationHomePage({super.key});

  @override
  State<RecommendationHomePage> createState() => _RecommendationHomePageState();
}

class _RecommendationHomePageState extends State<RecommendationHomePage> {
  static const apiUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  final service = RecommendationService(baseUrl: apiUrl);
  final users = const ['U001', 'U002', 'U003', 'U004', 'U005', 'U006'];

  String selectedUser = 'U001';
  bool loading = false;
  String? error;
  List<Recommendation> recommendations = const [];

  Future<void> loadRecommendations() async {
    setState(() {
      loading = true;
      error = null;
    });

    try {
      final result = await service.getRecommendations(selectedUser, topN: 5);
      if (!mounted) return;
      setState(() {
        recommendations = result;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        error = 'Unable to load recommendations. Check that the API is running.';
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Recommended For You')),
      body: RefreshIndicator(
        onRefresh: loadRecommendations,
        child: ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text('Product Recommendation Engine', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 6),
            Text('Flutter → FastAPI → Hybrid ML', style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 24),
            DropdownButtonFormField<String>(
              value: selectedUser,
              decoration: const InputDecoration(
                labelText: 'Customer',
                border: OutlineInputBorder(),
              ),
              items: users.map((user) => DropdownMenuItem(value: user, child: Text(user))).toList(),
              onChanged: (value) {
                if (value != null) setState(() => selectedUser = value);
              },
            ),
            const SizedBox(height: 12),
            FilledButton.icon(
              onPressed: loading ? null : loadRecommendations,
              icon: const Icon(Icons.auto_awesome),
              label: const Text('Get Recommendations'),
            ),
            const SizedBox(height: 24),
            if (loading)
              const Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
            else if (error != null)
              Card(child: Padding(padding: const EdgeInsets.all(16), child: Text(error!)))
            else if (recommendations.isEmpty)
              const Card(child: Padding(padding: EdgeInsets.all(16), child: Text('Select a customer and load recommendations.')))
            else
              ...recommendations.asMap().entries.map((entry) => RecommendationCard(index: entry.key + 1, item: entry.value)),
          ],
        ),
      ),
    );
  }
}

class RecommendationCard extends StatelessWidget {
  final int index;
  final Recommendation item;

  const RecommendationCard({super.key, required this.index, required this.item});

  @override
  Widget build(BuildContext context) {
    final match = (item.score * 100).clamp(0, 100).toStringAsFixed(0);

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            CircleAvatar(child: Text('$index')),
            const SizedBox(width: 12),
            Expanded(child: Text(item.name, style: Theme.of(context).textTheme.titleMedium)),
          ]),
          const SizedBox(height: 10),
          Text('${item.brand} • ${item.category}'),
          const SizedBox(height: 4),
          Text('₹${item.price.toStringAsFixed(0)}', style: Theme.of(context).textTheme.titleSmall),
          const SizedBox(height: 10),
          LinearProgressIndicator(value: item.score.clamp(0, 1)),
          const SizedBox(height: 6),
          Text('$match% recommendation score'),
          const SizedBox(height: 8),
          Text(item.reason, style: Theme.of(context).textTheme.bodySmall),
        ]),
      ),
    );
  }
}
