import { GoogleGenerativeAI } from "@google/generative-ai";
import dotenv from "dotenv";
dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

async function testModel() {
  try {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" }); // thử "gemini-1.5-pro" nếu lỗi

    const result = await model.generateContent("Hi Gemini, what's the weather like today?");
    const response = await result.response;
    const text = response.text();

    console.log("✅ Gemini response:", text);
  } catch (error) {
    console.error("❌ Gemini Error:", error);
  }
}

testModel();
