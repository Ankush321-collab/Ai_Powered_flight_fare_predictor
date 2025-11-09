const Flight = require('../models/Flight');

// GET /api/flights?from=DEL&to=DXB
const getFlights = async (req, res) => {
  const { from, to } = req.query;
  try {
    const query = {};
    if (from) query.from = from;
    if (to) query.to = to;
    const flights = await Flight.find(query).sort({ timestamp: -1 }).limit(100);
    res.json({ success: true, data: flights });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// GET /api/flights/trends?from=DEL&to=DXB
const getTrends = async (req, res) => {
  const { from, to, days = 30 } = req.query;
  try {
    const match = {};
    if (from) match.from = from;
    if (to) match.to = to;
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - Number(days));

    const pipeline = [
      { $match: { ...match, timestamp: { $gte: cutoff } } },
      { $group: { _id: { date: { $dateToString: { format: '%Y-%m-%d', date: '$timestamp' } }, airline: '$airline' }, avgPrice: { $avg: '$price' } } },
      { $sort: { '_id.date': 1 } }
    ];

    const data = await Flight.aggregate(pipeline);
    res.json({ success: true, data });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = { getFlights, getTrends };
