// routes/chatRoutes.js

import express from 'express';
import Message from '../models/Message.js';
import { getGeminiResponse } from '../services/geminiService.js';
import { getRecentHistory } from '../services/messageHistoryService.js';
import { buildGeminiMessages } from '../utils/promptBuilder.js';

const router = express.Router();

// ✅ POST: Lưu tin nhắn vào MongoDB
router.post('/messages', async (req, res) => {
  try {
    const { sender, message, messageType } = req.body;

    const newMessage = new Message({
      sender,
      message,
      messageType,
      timestamp: new Date(),
    });

    await newMessage.save();
    res.status(201).json(newMessage);
  } catch (error) {
    console.error('❌ Lỗi khi lưu tin nhắn:', error);
    res.status(500).json({ error: 'Lỗi khi lưu tin nhắn' });
  }
});

// ✅ GET: Gọi Gemini API và lưu lịch sử
router.get('/answer', async (req, res) => {
  const userQuestion = req.query.answer;

  try {
    // Lấy 3 câu gần nhất từ lịch sử MongoDB
    const history = await getRecentHistory(3); // trả về dạng [{ userMessage, botResponse }, ...]

    // Tạo structured message array cho Gemini
    const messages = buildGeminiMessages({ historyArray: history, currentQuestion: userQuestion });

    // Gọi Gemini để lấy phản hồi
    const botResponse = await getGeminiResponse(messages);

    // ✅ Lưu user message
    const userMsg = new Message({
      sender: 'USER',
      message: userQuestion,
      messageType: 'text',
      timestamp: new Date(),
    });
    await userMsg.save();

    // ✅ Lưu bot response
    const botMsg = new Message({
      sender: 'BOT',
      message: botResponse,
      messageType: 'text',
      timestamp: new Date(),
    });
    await botMsg.save();

    // Trả kết quả về client
    res.json({ bot_response: botResponse });
  } catch (err) {
    console.error('❌ Lỗi từ Gemini:', err);
    res.status(500).json({ error: 'Lỗi khi lấy phản hồi từ Gemini' });
  }
});

export default router;
