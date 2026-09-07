# -*- coding: utf-8 -*-
# 把 rescue/distributed-lock-redis.artifact.html 剝殼、換暖色，寫成 content/redis/
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / 'content' / 'redis' / '01-distributed-lock'

s = (HERE / 'distributed-lock-redis.artifact.html').read_text(encoding='utf-8')
body = s[s.find('<title>'):]                       # 剝掉 artifact 發佈系統的外殼
secs = re.findall(r'<section[^>]*>.*?</section>', body, re.S)
assert len(secs) == 9, len(secs)

# 第 9 段：公司內容改寫成一般化例子（Tim 拍板）
secs[8] = '''<section>
    <p class="era">回到現實</p>
    <h3 class="head">放登入資訊沒問題，想當鎖要三思</h3>
    <p>一個常見的用法：把登入者的身份與權限暫存在 Redis（雲端上就是 GCP 的 Memorystore、AWS 的 ElastiCache 這類託管服務）。<strong>這個用途沒有上面的問題</strong>——換主機時真的掉了幾筆，使用者頂多重新登入一次。</p>
    <p>要留意的是<strong>哪天想拿 Redis 來當鎖</strong>的時候，例如「同一份文件不要被兩個人同時送出審核」。那種情境屬於上面的「不能重複」，建議先看資料庫的唯一索引擋不擋得住，擋得住就不用架鎖。</p>
  </section>'''

def warm(h):
    h = h.replace('var(--brass)', 'var(--gold)')
    h = h.replace('class="tag"', 'class="era"')
    h = re.sub(r'<h2(\s[^>]*)?>', '<h3 class="head">', h)
    h = h.replace('</h2>', '</h3>')
    return h

secs = [warm(x) for x in secs]

LEARN = ['說出鎖搬到多台機器後為什麼失效、分散式鎖怎麼補救',
         '看懂 SET … NX EX 這行指令，講出用 Redis 當鎖的三個坑',
         '分清四種擺法差在哪，以及為什麼哨兵和叢集也救不了鎖']
KEYS = ['機器變多，各自記憶體裡的鎖就互相看不到，等於沒鎖。',
        '分散式鎖就是把鎖搬到一個大家都看得到的地方，Redis 是常見選擇。',
        'Redis 四種擺法差在「裝得下多少」和「主機掛了誰來救」：單機沒人救、主從要人工救、哨兵自動救、叢集自動救而且裝得更多。',
        '但四種都救不了鎖——因為複製是非同步的，換主機的瞬間鎖會憑空消失。',
        '先問「重複做一次會怎樣」。沒差就用 Redis；不能重複就加遞增編號，或乾脆用資料庫、etcd。']

HEADER = '<!-- 來源：rescue/distributed-lock-redis.artifact.html（舊對話救回的 artifact，已剝殼）· 收錄日期：2026-09-04 -->'

def box(cls, label, items):
    return ('<div class="%s"><p class="lbl">%s</p><ul>%s</ul></div>'
            % (cls, label, ''.join('<li>%s</li>' % x for x in items)))

OUT.mkdir(parents=True, exist_ok=True)
parts = [HEADER, box('learn', '讀完這課你會', LEARN)] + secs + [box('keys', '重點整理', KEYS)]
(OUT / 'lesson.html').write_text('\n'.join(parts) + '\n', encoding='utf-8')

QUIZ = [
 dict(q='鎖在程式裡是為了防止什麼？',
      opts=['同一份資料同一時間被兩個人改——例如同時扣款、扣成一次', '程式碼被別人偷看',
            '伺服器被關機', '資料庫被塞滿'],
      exp='跟廁所門閂一樣：一個人進去、閂上，其他人只能在外面等。'),
 dict(q='程式複製成三台之後，原本的鎖為什麼失效？',
      opts=['鎖是記在各自記憶體裡的旗子，A 台舉的旗子 B 台看不到——三把鎖各鎖各的',
            '三台機器的時鐘不同步', '網路太慢', '記憶體不夠大'],
      exp='每台機器的記憶體互相獨立，等於沒鎖——所以要把鎖搬到大家都看得到的地方。'),
 dict(q='SET 訂單123 我的名字 NX EX 30 這行裡的 NX 是什麼意思？',
      opts=['「這個名字目前沒人用，才寫得進去」——第一個寫進去的人贏，其他人收到失敗',
            '把資料加密', '30 秒後這筆自動消失', '通知其他機器來搶'],
      exp='NX 就是「搶鎖」的關鍵：只有一個人能寫成功。「30 秒後自動消失」是 EX 30 的事。'),
 dict(q='為什麼鎖一定要設過期時間（EX）？',
      opts=['拿到鎖的機器如果當場斷電，鎖會永遠留在那裡，後面全部卡死',
            'Redis 規定不設就不能用', '設了可以加快讀取速度', '為了省記憶體'],
      exp='三個坑的第一個：沒有 EX，一次意外就把整條路堵死。'),
 dict(q='解鎖前為什麼要先確認「鎖上寫的是不是我的名字」，而且確認和刪除要一氣呵成？',
      opts=['我的鎖可能已經過期、換別人拿到了——不確認就刪，刪掉的是別人的鎖；分兩步做，中間可能被插隊',
            'Redis 會拒絕沒署名的刪除', '為了留下操作紀錄', '名字寫錯會被扣款'],
      exp='實務上用 Lua 腳本讓「確認＋刪除」整段在 Redis 裡一起跑，中間不會被插隊。'),
 dict(q='四種擺法裡，哪一種能裝的資料量可以靠加機器一直往上加？',
      opts=['叢集（Cluster）——資料切成 16384 個號碼段，分給好幾組主從各管一段',
            '單機（Standalone）', '主從複製（Master–Replica）', '哨兵（Sentinel）'],
      exp='前三種能裝的都是「一台的量」；哨兵解決的是「掛了誰救」，不是容量。'),
 dict(q='架成哨兵或叢集之後，鎖為什麼還是會破？',
      opts=['主機複製資料給從機是非同步的——鎖剛給出去、還沒複製過去主機就掛了，升上來的新主機根本沒看過那把鎖',
            '設定檔寫錯了才會破，設對就不會', '哨兵會定期清掉所有的鎖', '叢集不支援 SET 指令'],
      exp='這不是設定錯，是這種複製方式本來就這樣——「架成哨兵就安全了」剛好想反了。'),
 dict(q='「絕對不能重複執行」的場景，建議的做法是？',
      opts=['別用 Redis 當鎖——改用 etcd 或 ZooKeeper（寫入要多數節點點頭才算成功），或先看資料庫的唯一索引擋不擋得住',
            '把 Redis 的過期時間設成一年', '多架幾台 Redis 就安全了', '在程式裡多睡一秒再執行'],
      exp='判斷起點是「鎖破了會怎樣」：重做沒差就直接用 Redis；不能重複但想留 Redis 就加遞增編號（fencing token）；絕對不行就換工具或讓資料庫擋。'),
]
(OUT / 'quiz.json').write_text(
    json.dumps({'questions': QUIZ}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

module = dict(
    title='分散式鎖與 Redis',
    intro='機器一多，好好的鎖為什麼失效；Redis 四種擺法差在哪、什麼時候別用它當鎖。',
    kick='分散式鎖 / REDIS',
    overview_intro=('「分散式」就是同一套程式同時跑在好幾台機器上。機器一多，原本好好的鎖就失效了。'
                    '這個模組講為什麼，以及 Redis 的四種擺法差在哪。'),
    footer_note='圖裡的號碼段 0–16383 是 Redis 叢集固定的切法；其餘數字（30 秒、幾十秒）是常見的量級，實際依設定而定。',
    lessons=[dict(dir='01-distributed-lock', slug='distributed-lock',
                  title='一把鑰匙，很多台機器在搶',
                  desc='為什麼鎖會破、一行指令怎麼當鎖、三個坑、四種擺法，以及該不該用 Redis 當鎖。',
                  mins=9, group='')])
(ROOT / 'content' / 'redis' / 'module.json').write_text(
    json.dumps(module, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

# modules.json 加上 redis
mj = ROOT / 'content' / 'modules.json'
site = json.loads(mj.read_text(encoding='utf-8'))
if 'redis' not in [m['id'] for m in site['modules']]:
    site['modules'].append({'id': 'redis', 'icon': '🔐'})
mj.write_text(json.dumps(site, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('content/redis/ 完成')
