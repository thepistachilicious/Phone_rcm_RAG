import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.scss'
import { WidgetProps } from 'types/widget'
import { Widget } from 'components/Widget'
import { library } from '@fortawesome/fontawesome-svg-core'
import { API_URL } from './config'
import { fas } from '@fortawesome/free-solid-svg-icons'

const PRIMARY_COLOR = 'rgb(54, 173, 212)'
const SECONDARY_COLOR = 'rgb(38, 165, 208)'

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
library.add(fas)

export const widgetProps: WidgetProps = {
  serverApiUrl: API_URL,
  userId: undefined,
  initialPayload: '',
  //logo: 'https://gruppi-go-dev.s3.amazonaws.com/65173870df5ecb87e15438a0-image-a5d552a5-f573-4703-960e-5b54a213e6b7.png',
  logo: 'chatbot.jpg',
  botAvatar:
    'data:image/png;base64,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',
  widgetColor: PRIMARY_COLOR,
  textColor: 'white',
  userMsgBackgroundColor: 'rgb(154, 158, 182)',
  botTitle: 'Nhom_3T',
  botSubTitle: 'Trợ lí mua sắm thông minh của bạn',
  botMsgBackgroundColor: '#f3f4f6',
  chatHeaderCss: {
    textColor: '#FFF',
    backgroundColor: SECONDARY_COLOR,
    enableBotAvatarBorder: 0,
    avatarStyle: {
      borderRadius: '8px',
    },
  },
  chatHeaderTextColor: '#FFF',
  botMsgColor: '#4b5563',
  userMsgColor: '#FFF',
  buttonsCss: {
    color: '#FFF',
    backgroundColor: 'rgb(71, 178, 182)',
    borderColor: 'rgb(71, 178, 182)',
    borderWidth: '0',
    borderRadius: '999px',
    hoverBackgroundColor: 'rgb(71, 178, 182)',
    hoverColor: '#FFF',
    hoverborderWidth: '0px',
    enableHover: true,
  },
  btnColor: PRIMARY_COLOR,
  theme: {
    colors: {
      primary: PRIMARY_COLOR,
      grey: '#4b5563',
      secondary: SECONDARY_COLOR,
      red: '#e3342f',
      green: '#38c172',
    },
  },
}
root.render(
  <React.StrictMode>
    <Widget {...widgetProps} />
  </React.StrictMode>,
)
