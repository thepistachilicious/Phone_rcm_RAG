import { useAppContext } from 'hooks/useAppContext'
import { MarkdownText } from 'components/MarkdownText'
import { formattedTs } from 'utils/dates'
import { Icon } from 'components/ui/Icon'
import { useTheme } from 'hooks/useTheme'
import { memo } from 'react'
import { Message } from 'types/state'

type TextMessageProps = {
  messageItem: Message
  text: string
  startsSequence?: boolean
  endsSequence?: boolean
  showBotAvatar?: boolean
  ts: string
}

export const TextMessage = memo(
  ({ text, startsSequence, endsSequence, showBotAvatar, ts }: TextMessageProps) => {
    const { botMsgColor, botMsgBackgroundColor } = useAppContext()
    const { colors } = useTheme()

    // Determine position of the message bubble
    const position = [
      'message',
      startsSequence ? 'start' : '',
      endsSequence ? 'end' : ''
    ].join(' ').trim()

    // Dynamic border styles
    let borderStyle
    switch (position) {
      case 'message start end':
        borderStyle = 'tw-rounded-[20px]'
        break
      case 'message start':
        borderStyle = 'tw-rounded-tl-[20px] tw-rounded-br-[20px] tw-rounded-tr-[20px] tw-rounded-bl-[5px]'
        break
      case 'message end':
        borderStyle = 'tw-rounded-tl-[5px] tw-rounded-br-[20px] tw-rounded-tr-[20px] tw-rounded-bl-[20px]'
        break
      case 'message':
        borderStyle = 'tw-rounded-tl-[5px] tw-rounded-bl-[5px] tw-rounded-br-[20px] tw-rounded-tr-[20px]'
        break
      default:
        borderStyle = ''
    }

    return (
      <div className="tw-flex tw-space-x-2 tw-items-start">
        {/* Bot Avatar */}
        {showBotAvatar && (
          <div className="tw-flex tw-w-8 tw-items-center">
            <Icon
              className="tw-h-8 tw-w-8 tw-rounded-full"
              icon={['fas', 'robot']}
              color={colors.primary}
            />
          </div>
        )}
        {/* Message Content */}
        <div className="tw-flex tw-flex-col tw-space-y-2 tw-max-w-[75%]">
          <div
            className={`tw-px-4 tw-py-3 ${borderStyle} tw-bg-white tw-shadow-md tw-text-sm tw-break-words tw-whitespace-pre-line`}
            style={{ color: botMsgColor, backgroundColor: botMsgBackgroundColor }}
            dir="auto"
          >
            <MarkdownText text={text} />
          </div>
          {/* Timestamp */}
          {showBotAvatar && (
            <div className="tw-text-[10px] tw-italic tw-text-gray-500">
              <span>{formattedTs(ts)}</span>
            </div>
          )}
        </div>
      </div>
    )
  }
)
TextMessage.displayName = 'TextMessage'
