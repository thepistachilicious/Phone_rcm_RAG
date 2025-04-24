import mongoose from 'mongoose';

const messageSchema = new mongoose.Schema({
  sender: {
    type: String,
    enum: ['USER', 'BOT'],
    required: true,
  },
  message: {
    type: String,
    required: true,
  },
  messageType: {
    type: String,
    default: 'text',
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

export default mongoose.model('Message', messageSchema);
