export const buildGeminiMessages = ({ historyArray, currentQuestion }) => {
  const messages = [];

  historyArray.forEach(item => {
    messages.push({ role: "user", parts: [{ text: item.userMessage }] });
    messages.push({ role: "model", parts: [{ text: item.botResponse }] });
  });

  messages.push({ role: "user", parts: [{ text: currentQuestion }] });

  return messages;
};
