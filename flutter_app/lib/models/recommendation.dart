class Recommendation {
  final String productId;
  final String name;
  final String category;
  final String brand;
  final double price;
  final double score;
  final double contentScore;
  final double collaborativeScore;
  final String reason;

  const Recommendation({
    required this.productId,
    required this.name,
    required this.category,
    required this.brand,
    required this.price,
    required this.score,
    required this.contentScore,
    required this.collaborativeScore,
    required this.reason,
  });

  factory Recommendation.fromJson(Map<String, dynamic> json) {
    return Recommendation(
      productId: json['product_id'] as String,
      name: json['name'] as String,
      category: json['category'] as String,
      brand: json['brand'] as String,
      price: (json['price'] as num).toDouble(),
      score: (json['score'] as num).toDouble(),
      contentScore: (json['content_score'] as num? ?? 0).toDouble(),
      collaborativeScore: (json['collaborative_score'] as num? ?? 0).toDouble(),
      reason: json['reason'] as String? ?? 'Recommended for you.',
    );
  }
}
