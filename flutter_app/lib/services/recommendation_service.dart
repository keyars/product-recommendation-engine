import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/recommendation.dart';

class RecommendationService {
  final String baseUrl;
  final http.Client client;

  RecommendationService({
    required this.baseUrl,
    http.Client? client,
  }) : client = client ?? http.Client();

  Future<List<Recommendation>> getRecommendations(
    String userId, {
    int topN = 5,
  }) async {
    final uri = Uri.parse('$baseUrl/recommendations/$userId?top_n=$topN');
    final response = await client.get(uri);

    if (response.statusCode != 200) {
      throw Exception('Recommendation API returned ${response.statusCode}.');
    }

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    final items = body['recommendations'] as List<dynamic>;

    return items
        .map((item) => Recommendation.fromJson(item as Map<String, dynamic>))
        .toList();
  }
}
