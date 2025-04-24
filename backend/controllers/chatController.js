const Message = require('../models/Message')
const axios = require('axios') // dùng gọi Gemini API
require('dotenv').config()

const GOOGLE_API_KEY = process.env.GEMINI_API_KEY

exports.getBotAnswer = async (req, res) => {
  const { answer } = req.query
  const { chatId } = req.params

  try {
    // Lưu tin nhắn của user
    const userMessage = await Message.create({
      chatId,
      sender: 'USER',
      text: answer,
      ts: new Date().toISOString(),
    })

    // Gọi Gemini API
    const geminiResponse = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GOOGLE_API_KEY}`,
      {
        contents: [{ parts: [{ text: answer }] }]
      }
    )

    const botText = geminiResponse?.data?.candidates?.[0]?.content?.parts?.[0]?.text

    // Lưu phản hồi từ bot
    const botMessage = await Message.create({
      chatId,
      sender: 'BOT',
      text: botText,
      ts: new Date().toISOString(),
    })

    res.send(`'user_message':'${userMessage._id}', 'bot_response':'${botText}', 'bot_response_id':'${botMessage._id}'`)
  } catch (error) {
    console.error(error)
    res.status(500).send("Bot Error")
  }
}
