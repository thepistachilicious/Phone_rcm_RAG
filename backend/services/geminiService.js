// services/geminiService.js

import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

export const getGeminiResponse = async (messages) => {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });

    const chat = model.startChat({
      history: messages, // Không có system role ở đây
    });

    const result = await chat.sendMessage(messages[messages.length - 1].parts[0].text);
    const response = result.response.text();

    return response;
  } catch (error) {
    console.error("❌ Lỗi khi gọi Gemini API:", error);
    throw error;
  }
};
