
# """
# 이번에 사용하는 구글의 Oauth는 Authorization Code Grant Type 방식이며 요약하면 다음과 같습니다.
# 1. 리다이렉트할 uri, 사용자에게 앱에서 사용하도록 요청할 정보 범위 등을 포함한 flow 객체를 만듭니다.
# 2. 이 flow 객체가 만들어낸 구글 로그인 uri를 사용자에게 보냅니다.

# 3. 사용자가 위 구글 로그인 uri에서 요청 정보 범위, 앱 이름 등을 확인합니다.
# 4. 구글에서 이를 1에서 지정했던 uri로 리다이렉트하면서 정보 요청 코드를 보냅니다.
# 5. 이 코드를 통해 구글에 데이터를 요청합니다.
# 6. 구글에서 받아온 데이터를 서버 데이터와 조회해 로그인 처리를 합니다.
# 7. 구글 api 사용을 요청한 경우 6 과정에서 받은 access token과 refresh 토큰으로 api를 사용할 수 있습니다.
# """

# """
# scope : 필수 입력 항목으로 사용자에게 요청할 정보 범위 입니다. 여기에 전체 목록이 나와있습니다.

# state : 추천 입력 항목입니다. 구글이 리다이렉트하면서 동일한 값을 파라미터로 보내는 값이며 리다이렉트했을 때 이 권한 요청을 앱 서버에서 보낸 것이 맞는 지 확인할 수 있습니다.

# access_type : 추천 입력 사용자가 로그아웃한 상태에서도(=브라우저를 종료한 상태)에서도 access_token을 쓸 수 있는지 없는지를 나타냅니다. 기본은 online으로 로그인 된 상태에서의 접근만이 허용됩니다.
# 그 외 여러 항목들이 있으며 자세한 것은 여기서 볼 수 있습니다.
# 이렇게 만들어진 authorization_url을 사용자에게 보내서 접속하게 합니다.
# """

from django.shortcuts import render
from django.http import HttpResponse
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req


def index(request):
    # return HttpResponse("Hello, World.")
    context = { 'result': 'Hello, World.' }
    return render(request, 'oauth/index.html', context)



flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'E:\ssl_workspace\python\oauth\client_secret.json',
    scopes = ['openid',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ],
    state = '12345678910',
)

flow.redirect_uri = 'http://localhost:8000/oauth/page'

authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true')



def google_oauth_redirect(request):

    context = { 'result': authorization_url}
    return render(request, 'oauth/google.html', context)


def page(request):

    context = { 'result': '리다이렉트 페이지'}
    return render(request, 'oauth/page.html', context)



# from __future__ import print_function
# import datetime
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     service = build('calendar', 'v3', credentials=creds)

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])


# if __name__ == '__main__':
#     main()