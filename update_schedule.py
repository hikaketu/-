from datetime import datetime
import json
import re
from bs4 import BeautifulSoup
import requests


def fetch_nhk_cinema():
  url = 'https://www.nhk.jp/p/ts/19X124K35K/schedule/'
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      )
  }

  movies = []

  try:
    res = requests.get(url, headers=headers, timeout=10)
    res.encoding = 'utf-8'

    if res.status_code == 200:
      soup = BeautifulSoup(res.text, 'html.parser')

      # NHKサイトの各番組カードを取得（HTML構造に合わせて調整可能）
      items = soup.find_all('article') or soup.find_all(
          'div', class_=re.compile(r'schedule|card|item')
      )

      for item in items:
        title_el = item.find(['h2', 'h3', 'a'])
        date_el = item.find(['time', 'p', 'span'])
        desc_el = item.find('p')

        if title_el and title_el.text.strip():
          movies.append({
              'title': title_el.text.strip(),
              'date': date_el.text.strip() if date_el else '日時不明',
              'description': desc_el.text.strip() if desc_el else '',
          })

  except Exception as e:
    print(f'取得エラー: {e}')

  # 取得できない場合のサンプルデータ補完（テスト用）
  if not movies:
    movies = [
        {
            'title': 'プレミアムシネマ 放送予定',
            'date': 'NHK公式サイトにてご確認ください',
            'description': '※自動更新スクリプトの実行結果を表示中',
        }
    ]

  # JSONに書き出し
  data = {
      'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      'movies': movies,
  }

  with open('schedule.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
  fetch_nhk_cinema()

