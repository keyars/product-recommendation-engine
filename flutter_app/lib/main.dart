import 'package:flutter/material.dart';

import 'models/recommendation.dart';
import 'services/recommendation_service.dart';

void main() => runApp(const RecommendationApp());

class RecommendationApp extends StatelessWidget {
  const RecommendationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Recommendations',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF7F7FA),
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

  late final RecommendationService service;
  final users = const ['U001', 'U002', 'U003', 'U004', 'U005', 'U006'];
  String selectedUser = 'U001';
  bool loading = false;
  String? error;
  List<Recommendation> recommendations = const [];

  @override
  void initState() {
    super.initState();
    service = RecommendationService(baseUrl: apiUrl);
    loadRecommendations();
  }

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
    } catch (_) {
      if (!mounted) return;
      setState(() {
        recommendations = const [];
        error = 'Could not connect to the recommendation service.';
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Recommendations'),
        actions: [
          IconButton(
            tooltip: 'Refresh',
            onPressed: loading ? null : loadRecommendations,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: loadRecommendations,
        child: ListView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
          children: [
            _Header(recommendationCount: recommendations.length),
            const SizedBox(height: 20),
            DropdownButtonFormField<String>(
              value: selectedUser,
              decoration: const InputDecoration(
                labelText: 'Customer',
                prefixIcon: Icon(Icons.person_outline),
                border: OutlineInputBorder(),
              ),
              items: users.map((user) => DropdownMenuItem(value: user, child: Text(user))).toList(),
              onChanged: loading
                  ? null
                  : (value) {
                      if (value != null) {
                        setState(() => selectedUser = value);
                        loadRecommendations();
                      }
                    },
            ),
            const SizedBox(height: 20),
            if (loading)
              const _LoadingState()
            else if (error != null)
              _ErrorState(message: error!, onRetry: loadRecommendations)
            else if (recommendations.isEmpty)
              const _EmptyState()
            else
              ...recommendations.asMap().entries.map(
                    (entry) => RecommendationCard(index: entry.key + 1, item: entry.value),
                  ),
          ],
        ),
      ),
    );
  }
}

class _Header extends StatelessWidget {
  final int recommendationCount;

  const _Header({required this.recommendationCount});

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Text('Recommended For You', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w700)),
      const SizedBox(height: 6),
      Text('Personalized using a hybrid ML recommendation engine.', style: Theme.of(context).textTheme.bodyLarge),
      const SizedBox(height: 12),
      Wrap(spacing: 8, children: [
        const Chip(avatar: Icon(Icons.auto_awesome, size: 16), label: Text('Hybrid ML')),
        if (recommendationCount > 0) Chip(label: Text('$recommendationCount recommendations')),
      ]),
    ]);
  }
}

class RecommendationCard extends StatelessWidget {
  final int index;
  final Recommendation item;

  const RecommendationCard({super.key, required this.index, required this.item});

  @override
  Widget build(BuildContext context) {
    final score = item.score.clamp(0.0, 1.0);
    final match = (score * 100).toStringAsFixed(0);

    return Card(
      margin: const EdgeInsets.only(bottom: 14),
      elevation: 0,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [
            CircleAvatar(child: Text('$index')),
            const SizedBox(width: 12),
            Expanded(child: Text(item.name, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w600))),
            Text('₹${item.price.toStringAsFixed(0)}', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
          ]),
          const SizedBox(height: 10),
          Wrap(spacing: 6, runSpacing: 6, children: [
            Chip(label: Text(item.brand)),
            Chip(label: Text(item.category)),
          ]),
          const SizedBox(height: 8),
          Row(children: [
            Expanded(child: ClipRRect(borderRadius: BorderRadius.circular(8), child: LinearProgressIndicator(value: score, minHeight: 8))),
            const SizedBox(width: 10),
            Text('$match%', style: Theme.of(context).textTheme.labelLarge?.copyWith(fontWeight: FontWeight.w700)),
          ]),
          const SizedBox(height: 8),
          Text(item.reason, style: Theme.of(context).textTheme.bodyMedium),
          if (item.contentScore > 0 || item.collaborativeScore > 0) ...[
            const SizedBox(height: 10),
            Text(
              'Content ${item.contentScore.toStringAsFixed(2)}  •  Similar customers ${item.collaborativeScore.toStringAsFixed(2)}',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ]),
      ),
    );
  }
}

class _LoadingState extends StatelessWidget {
  const _LoadingState();

  @override
  Widget build(BuildContext context) => const Center(
        child: Padding(padding: EdgeInsets.all(40), child: CircularProgressIndicator()),
      );
}

class _ErrorState extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;

  const _ErrorState({required this.message, required this.onRetry});

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(children: [
            const Icon(Icons.cloud_off, size: 40),
            const SizedBox(height: 10),
            Text(message, textAlign: TextAlign.center),
            const SizedBox(height: 12),
            OutlinedButton.icon(onPressed: onRetry, icon: const Icon(Icons.refresh), label: const Text('Try Again')),
          ]),
        ),
      );
}

class _EmptyState extends StatelessWidget {
  const _EmptyState();

  @override
  Widget build(BuildContext context) => const Card(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Center(child: Text('No recommendations available.')),
        ),
      );
}
