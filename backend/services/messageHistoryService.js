import Message from '../models/Message.js';

export const getRecentHistory = async (limit = 3) => {
  const messages = await Message.find()
    .sort({ timestamp: -1 })
    .limit(limit * 2) // 1 user + 1 bot = 2 messages
    .lean();

  const history = [];
  for (let i = messages.length - 2; i >= 0; i -= 2) {
    if (messages[i].sender === 'USER' && messages[i + 1]?.sender === 'BOT') {
      history.push({
        userMessage: messages[i].message,
        botResponse: messages[i + 1].message,
      });
    }
  }

  return history;
};
