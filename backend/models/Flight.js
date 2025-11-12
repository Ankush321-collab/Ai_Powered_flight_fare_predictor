const mongoose = require('mongoose');

const PricePointSchema = new mongoose.Schema({
  date: { type: Date, required: true },
  price: { type: Number, required: true }
}, { _id: false });

const FlightSchema = new mongoose.Schema({
  from: { type: String, required: true },
  to: { type: String, required: true },
  airline: { type: String, required: true },
  date: { type: Date, required: true },
  price: { type: Number, required: true },
  duration: { type: String },
  timestamp: { type: Date, default: Date.now },
  history: [PricePointSchema]
});

module.exports = mongoose.model('Flight', FlightSchema);
