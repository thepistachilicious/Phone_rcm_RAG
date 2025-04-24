import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

type MarkdownTextProps = {
  text: string
}

export const MarkdownText = ({ text }: MarkdownTextProps) => {
  // Xử lý text nếu cần, ví dụ bỏ dấu **
  const cleanText = text.replace(/\*\*/g, ''); // Loại bỏ dấu **

  return <ReactMarkdown children={cleanText} remarkPlugins={[remarkGfm]} />
}
