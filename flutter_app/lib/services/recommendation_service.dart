import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/recommendation.dart';

class RecommendationService {
  final String baseUrl;
  final http.Client client;

  RecommendationService({required this.baseUrl, http.Client? client})
      : client = client ?? http.Client();

  Future<List<Recommendation>> getRecommendations(String userId, {int topN = 5}) async {
    final uri = Uri.parse('$baseUrl/recommendations/$userId?top_n=$topN');
    final response = await client.get(uri).timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      throw Exception('Recommendation API returned ${response.statusCode}.');
    }

    final decoded = jsonDecode(response.body);
    if (decoded is! Map<String, dynamic> || decoded['recommendations'] is! List) {
      throw const FormatException('Invalid recommendation response.');
    }

    return (decoded['recommendations'] as List)
        .map((item) => Recommendation.fromJson(item as Map<String, dynamic>))
        .toList();
  }
}
