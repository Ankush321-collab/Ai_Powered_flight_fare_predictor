const mongoose = require('mongoose');

const ReviewSchema = new mongoose.Schema({
  airline: { type: String, required: true },
  review_text: { type: String, required: true },
  sentiment: { type: String, enum: ['positive','neutral','negative'], required: true },
  score: { type: Number, min: 0, max: 1 },
  category: { type: String },
  source: { type: String },
  created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Review', ReviewSchema);
