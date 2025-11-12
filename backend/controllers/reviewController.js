const Review = require('../models/Review');

// GET /api/reviews
const getReviews = async (req, res) => {
  const { airline } = req.query;
  try {
    const query = {};
    if (airline) query.airline = airline;
    const reviews = await Review.find(query).sort({ created_at: -1 }).limit(500);
    res.json({ success: true, data: reviews });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// GET /api/reviews/sentiment/:airline
const getSentimentStats = async (req, res) => {
  const { airline } = req.params;
  try {
    const match = airline ? { airline } : {};
    const pipeline = [
      { $match: match },
      { $group: { _id: '$sentiment', avgScore: { $avg: '$score' }, count: { $sum: 1 } } }
    ];
    const stats = await Review.aggregate(pipeline);
    res.json({ success: true, data: stats });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = { getReviews, getSentimentStats };
