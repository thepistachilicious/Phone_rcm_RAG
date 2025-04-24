import { DateTime } from 'luxon';
import axios from 'axios';
import { store } from '../store';
import { endBotResponse, selectChatId, startBotResponse, streamBotResponse } from 'store/messages';
import ObjectID from 'bson-objectid';
import { t } from 'i18next';
import { addMessage } from '../store/messages';

// ✅ BASE URL của backend (nếu cần, có thể chuyển vào .env và import từ đó)
const BASE_URL = 'http://localhost:5000';

// Gửi tin nhắn người dùng hoặc bot vào MongoDB
export const sendMessageToMongo = async (
  sender: 'USER' | 'BOT',
  message: string,
  messageType: 'text' | 'image' | 'video' = 'text'
): Promise<void> => {
  try {
    await axios.post(`${BASE_URL}/api/messages`, {
      sender,
      message,
      messageType,
    });
  } catch (error) {
    console.error('❌ Lỗi khi lưu tin nhắn vào MongoDB:', error);
  }
};

// Tạo object tin nhắn người dùng để hiển thị
export const createUserMessage = (message: string) => {
  return {
    text: message,
    sender: 'USER',
    messageType: 'text',
    ts: DateTime.now().toISO(),
  };
};

// Gọi backend để lấy phản hồi từ Gemini và cập nhật UI
export const getBotResponseV2 = async ({ message }: { message?: string }) => {
  const state = store.getState();
  const chatId = selectChatId(state);
  const botMessageId = String(ObjectID());

  try {
    // 1. Bắt đầu phản hồi từ bot
    store.dispatch(startBotResponse());

    // 3. Gọi API backend để lấy câu trả lời từ Gemini
    const { data } = await axios.get(`${BASE_URL}/api/answer`, {
      params: { answer: message },
    });

    if (!data || !data.bot_response) {
      throw new Error("❌ Không nhận được phản hồi từ Gemini.");
    }

    const botResponse = data.bot_response;

    // 4. Cập nhật UI với phản hồi bot
    store.dispatch(streamBotResponse({
      botMessageId,
      partialResponse: botResponse,
    }));

    store.dispatch(endBotResponse({
      botMessageId,
      botResponse,
      botDatabaseId: null,
      userMessageId: null,
    }));

    // 5. Gửi phản hồi vào MongoDB
    await sendMessageToMongo('BOT', botResponse, 'text');

    return botResponse;
  } catch (error) {
    console.error('❌ Lỗi khi gọi Gemini:', error);

    const fallback = t('genericError') || 'Bot gặp lỗi, vui lòng thử lại sau.';

    // 6. Thông báo lỗi UI
    store.dispatch(endBotResponse({
      botMessageId,
      botResponse: fallback,
      botDatabaseId: null,
      userMessageId: null,
    }));

    return fallback;
  }
};
