# -*- coding: utf-8 -*-
# 把 vm-container-k8s.html 重組成 SPA 課程站（暖色系、側邊欄、每課測驗）
import re, json

SRC = 'vm-container-k8s.html'
OUT = 'k8s-course.html'

s = open(SRC, encoding='utf-8').read()
secs = re.findall(r'<section[^>]*>.*?</section>', s, re.S)
assert len(secs) == 21, len(secs)

# ---- 從 sec12 抽出「核心迴圈」那張圖，搬到第 5 課 ----
m = re.search(r'<figure>\s*<svg viewBox="0 0 760 262"[^>]*aria-label="Kubernetes 的核心迴圈.*?</figure>', secs[12], re.S)
assert m, 'loop figure not found'
loop_fig = m.group(0)
secs[12] = secs[12].replace(loop_fig, '')

def recolor(h):
    h = h.replace('var(--teal-soft)', 'var(--gold-soft)').replace('var(--teal)', 'var(--gold)')
    h = h.replace('var(--amber-soft)', 'var(--slate-soft)').replace('var(--amber)', 'var(--slate)')
    return h

secs = [recolor(x) for x in secs]
loop_fig = recolor(loop_fig)

# ---- 內文修字：跨章引用、術語補充 ----
# kube-proxy 圖說原本說「前面 Service 那一段」，新順序 Service 在後面（第 9 課）
secs[10] = secs[10].replace(
    '那個「轉發表」（<code>kube-proxy</code>）就是前面 Service 那一段講的東西——它是一支真的在跑的程式，負責把大腦發下來的名單寫進這台機器的網路規則。',
    '那個「轉發表」（<code>kube-proxy</code>）是一支真的在跑的程式，負責把大腦發下來的名單寫進這台機器的網路規則——它就是第 9 課要講的 Service 背後的執行者。')
# 「第一部分」改成課號
secs[12] = secs[12].replace('就是第一部分講的「一台機器塞兩個服務會打架」那件事又回來了',
                            '就是第 1 課講的「一台機器塞兩個服務會打架」那件事又回來了')
secs[20] = secs[20].replace('<strong>第一、二部分（容器和 Docker）不管最後選哪一條路都要會</strong>；第三到六部分是背景知識',
                            '<strong>第 1〜4 課（容器和 Docker）不管最後選哪一條路都要會</strong>；第 5〜12 課是背景知識')
# dockershim 補年份；container runtime 補英文
secs[7] = secs[7].replace('你在文件上看到「K8s 移除 dockershim」講的就是這件事',
                          '你在文件上看到「K8s 移除 dockershim」（v1.24，2022 年）講的就是這件事')
secs[7] = secs[7].replace('kubelet 存在的理由，不是「啟動容器」——那件事 Docker 本來就會做。',
                          'kubelet 存在的理由，不是「啟動容器」——那件事容器執行環境（container runtime）本來就會做。')
# ReplicaSet 註記（加在 requests/limits 那段之後）
secs[12] = secs[12].replace(
    '<h4>Dockerfile 和 Deployment 差在哪</h4>',
    '<p class="muted">實務細節：巡邏的其實隔著一層叫 <code>ReplicaSet</code> 的中間人在數份數——Deployment 管「換版本」、ReplicaSet 管「維持份數」。下指令看狀態時會看到它，知道它是誰就好。</p>\n    <h4>Dockerfile 和 Deployment 差在哪</h4>')
# Gateway API 註記
secs[14] = secs[14].replace(
    '<h4>換成雲端託管的服務，nginx 就不見了</h4>',
    '<p class="muted">順帶一提：Ingress 的下一代規格叫 <strong>Gateway API</strong>，概念一樣（一張單子＋一個執行者），只是表格式更細。新專案的文件上會越來越常看到。</p>\n\n    <h4>換成雲端託管的服務，nginx 就不見了</h4>')

# ---- 課程設定 ----
CH5_BODY = '''  <section>
    <p class="era">一句話本質</p>
    <h3 class="head">一個一直在比對的管家</h3>
    <p>上一課結尾那四個「還沒解決的」問題——放哪台、誰重開、怎麼找、怎麼換版本——共同點是：<strong>都需要有人一直盯著、一直做決定。</strong>Kubernetes（常簡寫 K8s，因為 K 和 s 中間有 8 個字母）就是那個盯著的人。</p>
    <p>它的運作方式只有一句話：<strong>你交一張「我要什麼」的單子，它每分每秒比對現況跟單子一不一樣，不一樣就自己補到一樣。</strong></p>
''' + loop_fig + '''
    <p>這種「只講結果，不講步驟」的做法，正式名稱叫<strong>宣告式（declarative）</strong>。相對的是傳統做法：寫一堆「如果掛了就重開」「先停 A 再起 B」的腳本，一步一步下指令。</p>
    <p class="formula">你負責「說要什麼」，K8s 負責「讓現況一直是那樣」</p>
    <p class="muted">「單子交給誰」「誰在比對」「補的動作誰做」——這些角色接下來三課會一個一個拆開。這一課只要記住這個迴圈。</p>
  </section>'''

LESSONS = [
 dict(slug='physical', title='一台機器一個服務', mins=7,
      desc='為什麼當年一台機器只敢跑一個服務——一切的起點。',
      learn=['用「會打架」解釋為什麼一台機器只跑一個服務','說出當年上線一個服務為什麼要等兩個月'],
      keys=['兩個服務要的環境會互相蓋掉、資源會互搶，所以一台只跑一個。','機器效能大部分閒著，要多一個服務就再買一台、再等兩個月。'],
      body=[0]),
 dict(slug='vm', title='虛擬機', mins=7,
      desc='Hypervisor 把一台切成好幾台，解決了浪費，留下了「肥」。',
      learn=['說出 Hypervisor 在做什麼','講出虛擬機解決了什麼、代價是什麼'],
      keys=['Hypervisor 把一台實體機切成好幾台「看起來完整」的電腦。','解決了浪費和等待：開一台變幾分鐘、效能用得完、彼此隔開。','代價：每台都背一整套作業系統（Guest OS），肥、慢、環境還是靠人裝。'],
      body=[1]),
 dict(slug='container', title='容器', mins=9,
      desc='共用作業系統這一步，換來輕、快、到處一樣。',
      learn=['一句話說出容器和虛擬機唯一的差別','解釋為什麼金融業有些場景仍用虛擬機'],
      keys=['唯一的差別：作業系統是各背一套，還是共用一套。','少背一套系統：體積幾 GB → 幾十 MB、啟動一分鐘 → 一秒內。','隔離是「牆的厚度」問題：虛擬機隔兩道（切得徹底），容器共用一道；法遵要求硬隔離時只能用虛擬機。','三代不互相取代：實體機上跑虛擬機、虛擬機裡跑容器是常態。'],
      body=[2]),
 dict(slug='docker', title='Docker', mins=9,
      desc='食譜、成品、跑起來的那一份——三個詞講完 Docker。',
      learn=['分清 Dockerfile／映像檔／容器三個東西','解釋容器為什麼治好「在我電腦上跑得起來」'],
      keys=['Dockerfile 是食譜、映像檔（image）是不會再變的成品、容器是跑起來的那一份。','映像檔倉庫（registry）是共用的架子：推上去、別台拉下來，每台拿到同一包。','連環境一起打包，所以「在我電腦上跑得起來」治好了。','跑一個容器很爽；三百個誰管？——這就是下一課的主角。'],
      body=[3,4]),
 dict(slug='why-k8s', title='為什麼需要 Kubernetes', mins=6,
      desc='容器多到管不動之後：一個一直在比對的管家。',
      learn=['說出 K8s 的一句話本質：比對單子與現況的管家','分清「宣告式」和「一步一步下指令」的差別'],
      keys=['K8s 的核心是一個沒有停過的迴圈：比對「單子」和「現況」，不一樣就補到一樣。','你只寫「我要 3 份」，不寫「掛了要重開」的腳本——這叫宣告式（declarative）。','掛掉一份，它自己補一份回來，你不用半夜起床。'],
      body=[]),
 dict(slug='pod-node', title='Pod 與 Node', mins=10,
      desc='派工的最小單位，和它住的那台機器。',
      learn=['說出 Pod 和容器的關係、Node 的組成公式','知道一台 Node 通常跑幾個 Pod、kubelet 為什麼存在'],
      keys=['Pod 是派工單位：通常裡面就一個容器，偶爾多一個貼身小幫手（sidecar）。','一台機器＋容器執行環境（containerd）＋kubelet ＝ 一個 Node；kubelet 是聽大腦指令的聯絡窗口。','一台 Node 跑幾十個 Pod 是常態（預設上限 110 個）；一台只跑一個就白用容器了。','Pod 落在哪台不用你管，重開一次就可能換位子。'],
      body=[5,6,7]),
 dict(slug='cluster-brain', title='叢集與大腦', mins=10,
      desc='worker 跑你的程式，master 跑大腦——四個角色各自是一個 Pod。',
      learn=['分清 master／worker 的分工','講出大腦四個角色各管什麼、etcd 為什麼是命根'],
      keys=['worker node 跑你的 Pod；master node 跑大腦（Control Plane），不跑你的程式。','四個角色：櫃檯（kube-apiserver）、檔案室（etcd）、排班的（kube-scheduler）、巡邏的（kube-controller-manager）——各自是一個 Pod。','每台機器（不分 master/worker）都有三樣：containerd、kubelet、kube-proxy。','etcd 存所有單子和現況：備份 etcd ＝ 備份整個叢集。'],
      body=[8,9,10,11]),
 dict(slug='deployment', title='Deployment：下單', mins=10,
      desc='用一張 YAML 單子講「我要幾份」，換版本不停機。',
      learn=['分清 Dockerfile 和 Deployment 兩張單子','說出 requests／limits 的差別與滾動更新的原理'],
      keys=['Dockerfile 管打包（這包裡有什麼）；Deployment 管上線（跑幾份、怎麼換版本）。兩者互不相識。','requests（保留量）＝至少留這麼多、可以超；limits（上限）＝絕不准超，記憶體超了容器被殺掉重開。','滾動更新（rolling update）：一次只換一份，全程都有人服務；舊映像檔還在倉庫，隨時退回（rollback）。'],
      body=[12]),
 dict(slug='service', title='Service：找路', mins=9,
      desc='Pod 一直換位子，靠一個永遠不變的名字找到它。',
      learn=['解釋 Service 為什麼存在、本質是什麼','說出「有幾組 Pod 就有幾個 Service」'],
      keys=['Pod 的位址一直變，所以呼叫方只認名字；Service 就是那個永遠不變的名字。','它不是機器也不是 Pod，是一筆存在 etcd 的規則，由每台機器的 kube-proxy 寫進轉發表——請求不經過任何中間伺服器。','「東西住在哪」和「請求怎麼走」是兩個垂直的軸；Service 只在第二個軸上。','有幾組 Pod 就有幾個 Service，前端後端各自一個。'],
      body=[13]),
 dict(slug='ingress', title='對外入口', mins=9,
      desc='Ingress、負載平衡器、nginx——誰是單子、誰在跑。',
      learn=['分清 Ingress（單子）和 Ingress Controller（執行者）','解釋託管環境為什麼常常沒有 nginx'],
      keys=['Service 的名字只在叢集內有效；對外要靠入口依網址分流。','Ingress 是規則表（不會跑）；Ingress Controller 是真的在轉發的 Pod，通常就是 nginx。','負載平衡器分兩種：只認位址的（L4）和看得懂網址的（L7）；雲端 L7 負載平衡器自己就是執行者，所以託管環境常常不需要 nginx。','判斷請求路徑：看「打 API 的那行程式在誰的機器上執行」。'],
      body=[14,15]),
 dict(slug='pattern', title='單子與執行者', mins=5,
      desc='一個貫穿全部的模式：看懂這個，前面全部串起來。',
      learn=['用「單子＋執行者」一句話統整 K8s 的設計'],
      keys=['Deployment／Service／Ingress 都只是存在 etcd 的單子；Pod／轉發表／nginx 才是執行者。','你永遠只寫單子，K8s 負責讓執行者符合單子。','「Service 是 Node 還是 Pod」問不出答案，因為它是單子欄的東西——跟執行者不同類。'],
      body=[16]),
 dict(slug='failure', title='壞掉的時候', mins=9,
      desc='補位和選舉是兩回事——誰掛了誰救、誰救不了。',
      learn=['分清補位和選舉兩種機制','說出 master 死一台之後會發生什麼、誰負責補'],
      keys=['Pod 掛、worker 掛 → 補位（大腦生一個新的）；master 掛 → 選舉（台數不會自己變回來）。','master 要奇數台：3 台可死 1 台，2 台死 1 台就過不了半數。','補回 master 是人的工作——這就是「顧 K8s 是一份全職工作」的原因。','master 全掛：已在跑的 Pod 照跑，但叢集凍結——還在動但沒人管，反而更危險。'],
      body=[17,18]),
 dict(slug='when', title='要不要用 K8s', mins=7,
      desc='分水嶺怎麼判斷，以及大多數團隊實際落腳的中間選項。',
      learn=['用一個問題判斷該不該上 K8s','知道託管服務幫你做掉哪些事'],
      keys=['分水嶺一句話：需不需要「跨機器決定東西放哪台」。不需要就別上。','一台機器、流量穩定 → Docker Compose 就夠；需要但沒人顧 → 用託管服務（Cloud Run、ECS Fargate）。','同一個映像檔在 docker run／託管服務／K8s 都能跑——Docker 學了不會白學。'],
      body=[19,20]),
]

QUIZ = {
 'physical': [
  dict(q='為什麼以前不把兩個服務裝在同一台機器上？',
       opts=['兩個服務要的環境（例如不同版本的 Java）會互相蓋掉，還會搶記憶體','一台機器的硬碟裝不下兩個服務','作業系統規定一台只能跑一個程式','兩個服務會互相抄襲程式碼'],
       exp='環境衝突＋資源互搶，一個寫爆記憶體另一個陪葬——所以當年寧可一台一個。'),
  dict(q='那個年代要上線一個新服務，時間主要花在哪？',
       opts=['採購、等機器送到、進機房、裝系統裝環境——前後約兩個月','寫程式本身','幫服務取名字','申請網址'],
       exp='瓶頸在「等一台實體機器就位」，不在寫程式。這就是虛擬機要解決的第一個痛。'),
  dict(q='一台機器只跑一個服務，最大的浪費是什麼？',
       opts=['機器效能大部分時間只用到一小部分','電費太便宜','機房空間太大','網路頻寬用不完'],
       exp='圖裡那條「效能只用了一成」的量條就是在講這件事：買了一整台，九成在發呆。'),
 ],
 'vm': [
  dict(q='Hypervisor 的工作是什麼？',
       opts=['把一台實體機的 CPU、記憶體、硬碟切成好幾份，每份看起來像一台完整的電腦','幫作業系統掃毒','加速網路連線','自動備份資料'],
       exp='中文叫「虛擬機管理程式」——就是「把一台切成好幾台」的那一層。'),
  dict(q='虛擬機最主要的代價是？',
       opts=['每一台虛擬機都要再背一整套自己的作業系統（Guest OS），又肥又慢','虛擬機不能連網路','虛擬機只能跑 Windows','一台實體機最多只能切兩台'],
       exp='底下明明已經有一套作業系統，上面每台還要再背一套 2–10 GB 的——這就是容器要省掉的那塊。'),
  dict(q='虛擬機解決了實體機時代的哪個問題？',
       opts=['效能用不完、開新機要等很久——切開之後用得滿、幾分鐘就能開一台','程式語言太舊','螢幕解析度不夠','鍵盤沒有注音'],
       exp='解決浪費與等待；但「環境靠人裝、在我電腦上跑得起來」還沒解決，留給了容器。'),
 ],
 'container': [
  dict(q='容器和虛擬機唯一的關鍵差別是？',
       opts=['作業系統是共用一套，還是各背一套','容器只能跑網頁程式','虛擬機沒有隔離能力','容器需要特殊硬體'],
       exp='就是疊層對照圖中間那塊：容器把 Guest OS 那層省掉，所以輕、快、密度高。'),
  dict(q='為什麼金融業有些場景仍堅持用虛擬機？',
       opts=['虛擬機之間隔了兩道牆、切得徹底；容器共用同一套作業系統，那道牆有漏洞就可能被跨過去','虛擬機比容器便宜','容器不能設定密碼','法規明文禁止使用容器'],
       exp='「不可能」和「很難」是兩回事。法遵要求不同客戶不能共用同一套作業系統時，容器換不了。'),
  dict(q='實體機、虛擬機、容器三代的關係是？',
       opts=['不是互相取代——最常見的組合是實體機上跑虛擬機、虛擬機裡跑容器','容器出來後虛擬機就被淘汰了','實體機已經不存在了','三選一，不能混用'],
       exp='雲端商給你的「機器」幾乎都是虛擬機，你在上面跑容器——三層疊著用才是常態。'),
 ],
 'docker': [
  dict(q='Docker 三個東西的對應，哪個正確？',
       opts=['Dockerfile 是食譜、映像檔是做好的成品、容器是跑起來的那一份','映像檔是食譜、Dockerfile 是成品','容器是成品、映像檔是跑起來的那一份','三個是同一個東西的三種叫法'],
       exp='食譜寫一次（build）→ 成品做一次 → 同一包可以同時跑（run）很多份。'),
  dict(q='容器為什麼治好了「在我電腦上跑得起來」？',
       opts=['因為搬過去的不只是程式碼，是連環境一起打包——每台跑的是同一包','因為容器會自動修改測試機的設定','因為容器裡不需要裝 Java','因為程式碼被壓縮得比較小'],
       exp='測試機裝哪版 Java 已經不重要了，容器裡自己有。你的筆電、測試機、正式機跑同一包。'),
  dict(q='映像檔倉庫（registry）是做什麼的？',
       opts=['大家共用的架子：做好的映像檔推上去，別台機器拉下來','存放程式原始碼的地方','資料庫的備份空間','自動掃描病毒的服務'],
       exp='「每台拿到同一包」靠的就是它——推一次，處處拉得到。'),
 ],
 'why-k8s': [
  dict(q='K8s 的核心運作方式是？',
       opts=['你交一張「我要什麼」的單子，它不停比對現況、不一樣就自己補到一樣','你下一步指令它做一步','它每天半夜重開所有機器','它自動幫你寫程式'],
       exp='那個比對迴圈沒有停過。掛掉一份，它發現「現況 2 份 ≠ 單子 3 份」，就自己補一份。'),
  dict(q='「宣告式（declarative）」的意思是？',
       opts=['只講結果，不講步驟——寫「我要 3 份」，而不是寫「掛了就重開」的腳本','部署前要先寫一份聲明文件','用特定的程式語言宣告變數','一次只能宣告一台機器'],
       exp='傳統腳本是「怎麼做」，K8s 的單子是「要什麼」。步驟由它自己想。'),
  dict(q='下列哪件事 Docker 自己做不到、要 K8s 接手？',
       opts=['跨機器決定容器放哪台、機器整台掛了把工作移走','把程式打包成映像檔','在一台機器上啟動容器','寫 Dockerfile'],
       exp='Docker（含 Compose）管的是「這一台」；第二台機器一出現，就沒有人幫你做決定了。'),
 ],
 'pod-node': [
  dict(q='一個 Pod 裡面通常有幾個容器？',
       opts=['一個；偶爾多一個貼身小幫手（sidecar，例如收日誌的）','固定兩個','至少五個','跟 Node 的數量一樣多'],
       exp='九成情況一對一。多包 Pod 這層是為了那一成：要用 localhost 互打、綁在一起生死的組合。'),
  dict(q='一台機器要成為 Node 的條件是？',
       opts=['機器＋容器執行環境（containerd）＋kubelet','只要有裝 Docker 就是 Node','一定要是實體機','要先裝好 nginx'],
       exp='kubelet 是關鍵：它是聽大腦指令的聯絡窗口。沒有它，就只是一台裝了 Docker 的機器。'),
  dict(q='一台 Node 上通常跑多少個 Pod？',
       opts=['幾十個很常見，K8s 預設上限是 110 個','只能跑一個','最多三個','沒有上限，通常跑上萬個'],
       exp='容器的價值就在密度。一台只跑一個容器，就跟第一代「一台機器一個服務」沒兩樣。'),
 ],
 'cluster-brain': [
  dict(q='master node 和 worker node 的分工是？',
       opts=['master 跑大腦（Control Plane），worker 跑你的 Pod','master 效能比較好，worker 比較差','worker 負責備份 master 的資料','兩種可以互相取代，沒有差別'],
       exp='master 不跑你的程式。官方現在叫它 control plane node，口語還是常講 master。'),
  dict(q='每一台機器（不分 master／worker）都有的三樣東西是？',
       opts=['容器執行環境（containerd）、kubelet、kube-proxy','etcd、scheduler、apiserver','nginx、Redis、PostgreSQL','Dockerfile、映像檔、倉庫'],
       exp='master 是在這三樣「之上」多跑四個角色；也因為 master 有 kubelet，那四個角色才能用 Pod 的形式跑。'),
  dict(q='etcd 是什麼？',
       opts=['存所有單子與現況的資料庫——備份它等於備份整個叢集','一種容器的壓縮格式','排程用的演算法','網路卡的驅動程式'],
       exp='名字來自 Linux 放設定的 /etc 加一個 d（分散式）。它沒了，機器都還在，但大腦完全失憶。'),
 ],
 'deployment': [
  dict(q='Dockerfile 和 Deployment 的分工是？',
       opts=['Dockerfile 管打包（這包裡有什麼）；Deployment 管上線（跑幾份、怎麼換版本）','兩張都是打包用的','Deployment 會產生映像檔','Dockerfile 裡要寫 K8s 的設定'],
       exp='兩個時間點、兩個對象，而且互不相識——所以同一個映像檔到哪都能用。'),
  dict(q='requests（保留量）和 limits（上限）的差別是？',
       opts=['requests 是「至少留這麼多」、可以超；limits 是「絕不准超」，記憶體超了容器會被殺掉重開','兩個數字意思一樣','limits 可以隨便超過','requests 超過容器就會被殺掉'],
       exp='requests 給排班的算位子用；limits 由機器本身執法——差別就是「超過會不會被處理」。'),
  dict(q='滾動更新（rolling update）怎麼做到換版本不停機？',
       opts=['一次只換一份，確認新的活著才換下一份——全程都有人在服務','半夜把全部關掉一起換','靠使用者自己重新整理頁面','先把舊的全刪掉再重建新的'],
       exp='每個時刻都有舊版或新版在線上。出問題就 rollback，因為舊映像檔還在倉庫裡。'),
 ],
 'service': [
  dict(q='為什麼呼叫方不直接打 Pod 的位址？',
       opts=['Pod 會重開、換位子，位址一直變；Service 的名字永遠不變','Pod 根本沒有位址','直接打的速度比較慢','防火牆規定不能直接打'],
       exp='Pod 是員工會換座位；Service 是那支永遠不變的分機號碼。'),
  dict(q='Service 的本質是什麼？',
       opts=['一筆存在 etcd 的規則，由每台機器的 kube-proxy 寫進網路轉發表——不是機器也不是 Pod','一台專門負責轉發的伺服器','一種特殊規格的 Pod','一條實體的網路線'],
       exp='請求沒有經過任何「Service 伺服器」——在呼叫方自己那台機器上，位址就當場被改寫了。所以它不會塞車、也不會單點故障。'),
  dict(q='前端那組 Pod 和後端那組 Pod，共用同一個 Service 嗎？',
       opts=['不——有幾組 Pod 就有幾個 Service，各自獨立','整個叢集只有一個 Service','Service 要手動填每個 Pod 的位址','只有後端可以有 Service'],
       exp='frontend 和 backend 是兩筆各自獨立的規則，請求一路往前走，不會繞回同一個中繼站。'),
 ],
 'ingress': [
  dict(q='Ingress 和 Ingress Controller 的關係是？',
       opts=['Ingress 是規則表（不會跑）；Ingress Controller 是真的在轉發的程式，通常是一個 nginx Pod','兩個都是硬體設備','Ingress 自己就會轉發流量','Ingress Controller 只是一份說明文件'],
       exp='跟 Deployment（單子）配 Pod（執行者）同一個模式：Ingress 是單子，Controller 是執行者。'),
  dict(q='用雲端託管服務時，為什麼常常看不到 nginx？',
       opts=['雲端的第七層（L7）負載平衡器自己就是執行者，看得懂網址、會依路徑分流——單子和執行者包在同一個產品裡','雲端環境禁止安裝 nginx','nginx 不支援雲端','因為託管環境沒有流量'],
       exp='自己架 K8s 才需要自己養執行者。負載平衡器分 L4（只認位址）和 L7（看得懂網址），雲端的 L7 把 nginx 的活包掉了。'),
  dict(q='為什麼不讓每個 Service 都直接對外？',
       opts=['一個 Service 一個對外 IP，十個服務就十個 IP，貴又難管；對外入口的價值是一個 IP 依網址分給很多 Service','Service 技術上無法對外','對外一定要經過 nginx 才合法','其實可以，而且是官方建議的做法'],
       exp='技術上可以（有一種型別會跟雲端要 IP），但管理上划不來。一個入口、依網址分路才是常態。'),
 ],
 'pattern': [
  dict(q='Deployment、Service、Ingress 的共同點是？',
       opts=['都只是存在 etcd 的「單子」，各自有真正在跑的執行者去實現它','都是會跑的程式','都是要另外採購的硬體','都只存在 worker node 上'],
       exp='單子：Deployment／Service／Ingress。執行者：Pod／每台機器的轉發表／nginx。你永遠只寫左邊。'),
  dict(q='「Service 本質是 Node 還是 Pod？」這個問題為什麼問不出答案？',
       opts=['因為 Service 是「單子」那一欄的東西，Node 和 Pod 是「執行者」那一欄——本來就不同類','因為官方文件沒有寫','因為 Service 已經被淘汰了','因為 Node 其實就是 Pod'],
       exp='把兩個欄位的東西放在一起比，怎麼比都不對。看懂單子／執行者這個模式，這類問題就消失了。'),
  dict(q='你平常「操作 K8s」，實際上在做的是？',
       opts=['改單子（YAML），讓大腦去把現況變成單子寫的樣子','登入每一台機器手動啟動容器','直接編輯 etcd 裡的資料','重灌每台機器的作業系統'],
       exp='宣告式的日常：改一行「份數：3 → 5」，交給櫃檯，剩下的是大腦的事。'),
 ],
 'failure': [
  dict(q='一個 Pod 掛了，會發生什麼？',
       opts=['巡邏的發現份數不夠，直接補一個新的（位址可能會變）','整個叢集跟著停機','要等工程師手動重開','那一份就永遠消失了'],
       exp='這是「補位」：單子說 3 份、現況 2 份，巡邏的就生一個新的。位址變了沒關係，有 Service。'),
  dict(q='master 3 台死了 1 台，會自動補回第 3 台嗎？',
       opts=['不會——補台是人的工作；剩 2 台照常運作，但已經沒有餘裕了','會，馬上自動長出一台新的','叢集會立刻全部停止','其中一台 worker 會自動升級成 master'],
       exp='worker 的 Pod 是大腦補的；master 掛了沒有更上層的東西來補——大腦自己就是壞掉的那個。'),
  dict(q='master 為什麼要擺奇數台（3 台、5 台）？',
       opts=['很多決定要「超過半數同意」：3 台可死 1 台，2 台死 1 台就過不了半數','偶數在機房裡不吉利','授權費用以奇數計價比較便宜','機架的空位剛好是奇數'],
       exp='4 台的容錯跟 3 台一樣（都只能死 1 台），多一台純浪費——所以一律奇數。'),
 ],
 'when': [
  dict(q='該不該從 Docker 轉 K8s，最根本的判斷是？',
       opts=['需不需要「跨機器決定東西放哪台」','程式碼超過多少行','團隊超過幾個人','有沒有使用 Java'],
       exp='Docker 管一台機器；第二台一出現就沒人做決定了。反過來說：一台夠用，就別上 K8s。'),
  dict(q='需要跨機器、但團隊沒有人力顧 K8s，建議是？',
       opts=['用託管服務（Cloud Run、ECS Fargate 這類）——交出映像檔，那一層雲端商幫你顧','硬著頭皮自己架 K8s','放棄，回去用實體機','乾脆不要部署'],
       exp='大多數團隊實際落腳在中間這格。代價是可調的選項變少，多數團隊願意換。'),
  dict(q='同一個映像檔可以在哪些地方跑？',
       opts=['docker run、託管服務、K8s 都可以——所以 Docker 學了不會白學','只能在打包它的那台機器上','只能在 K8s 叢集裡','只能在雲端環境'],
       exp='映像檔不知道 K8s 存在。不管最後走哪條路，Dockerfile 那一段都是必修。'),
 ],
}

CSS = '''
:root{
  --paper:#F7F0E3; --surface:#FFFFFF; --sunk:#F1E9D9;
  --ink:#22242A; --ink2:#55575E; --mut:#8B8D94; --line:#E4DCCB;
  --gold:#B5730F; --gold-deep:#8A5809; --gold-soft:#F6E9D2;
  --slate:#5E7A9B; --slate-soft:#E2E8F2;
  --danger:#B0402F; --ok:#4F7A57; --ok-soft:#E8F0E6;
  --code:#F1E9D9; --shadow:0 1px 3px rgba(90,70,35,.07);
}
/* 亮暖色是這個站的定調：不跟著系統切深色 */
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;
  font-size:16.5px;line-height:1.85;-webkit-font-smoothing:antialiased}

/* ── 頂欄 ── */
.topbar{position:fixed;top:0;left:0;right:0;height:54px;z-index:40;
  background:var(--paper);border-bottom:1px solid var(--line);
  display:flex;align-items:center;gap:12px;padding:0 16px}
.topbar .burger{display:none;background:none;border:1px solid var(--line);border-radius:6px;
  width:36px;height:36px;font-size:17px;color:var(--ink);cursor:pointer}
.topbar .brand{font-family:"Chivo","Noto Sans TC",sans-serif;font-weight:900;font-size:16.5px;
  letter-spacing:.01em;text-decoration:none;color:var(--ink)}
.topbar .brand b{color:var(--gold)}

/* ── 側邊欄 ── */
.sidebar{position:fixed;top:54px;left:0;bottom:0;width:272px;z-index:30;
  background:var(--paper);border-right:1px solid var(--line);
  overflow-y:auto;padding:14px 0 30px}
.sidebar a{display:flex;align-items:baseline;gap:9px;padding:9px 18px 9px 16px;
  color:var(--ink2);text-decoration:none;font-size:14.5px;line-height:1.5;
  border-left:3px solid transparent}
.sidebar a:hover{background:var(--gold-soft);color:var(--ink)}
.sidebar a.active{background:var(--gold-soft);border-left-color:var(--gold);
  color:var(--ink);font-weight:700}
.sidebar a .n{font-family:"JetBrains Mono",monospace;font-size:12px;color:var(--gold);
  min-width:20px;text-align:right;flex:none}
.sidebar a .tick{margin-left:auto;flex:none;color:var(--ok);font-weight:700;font-size:13px}
.sidebar .group{font-family:"JetBrains Mono",monospace;font-size:10.5px;letter-spacing:.18em;
  color:var(--mut);padding:16px 18px 5px}
.sidebar .ov{font-weight:700;color:var(--ink)}
.scrim{display:none;position:fixed;inset:54px 0 0 0;background:rgba(25,21,17,.45);z-index:25}

/* ── 主內容 ── */
.main{margin-left:272px;padding:78px clamp(18px,4.5vw,56px) 90px;max-width:848px}
@media (max-width:960px){
  .topbar .burger{display:block}
  .sidebar{transform:translateX(-105%);transition:transform .2s ease;box-shadow:4px 0 18px rgba(0,0,0,.15)}
  @media (prefers-reduced-motion:reduce){.sidebar{transition:none}}
  .sidebar.open{transform:none}
  .scrim.show{display:block}
  .main{margin-left:0}
}
article[hidden]{display:none}

/* ── 課程頁頭 ── */
.crumb{font-size:13px;color:var(--mut);margin:0 0 10px}
.crumb a{color:var(--gold);text-decoration:none}
.crumb a:hover{text-decoration:underline}
h1.lt{font-family:"Chivo","Noto Sans TC",sans-serif;font-weight:900;
  font-size:clamp(27px,5vw,38px);line-height:1.25;margin:0 0 10px;letter-spacing:-.01em;text-wrap:balance}
.meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 8px}
.meta .chip{font-family:"JetBrains Mono",monospace;font-size:11.5px;padding:3px 10px;
  border-radius:99px;border:1px solid var(--line);background:var(--surface);color:var(--ink2)}
.meta .chip.g{border-color:var(--gold);color:var(--gold);background:var(--gold-soft)}
p.sub{color:var(--ink2);font-size:16.5px;margin:0 0 20px}
.learn{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--gold);
  border-radius:6px;padding:14px 20px;margin:0 0 30px;box-shadow:var(--shadow)}
.learn .lbl{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.16em;
  color:var(--gold);margin:0 0 4px;font-weight:600}
.learn ul{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:4px}
.learn li{font-size:15px}

/* ── 內文（沿用原本的段落樣式） ── */
section{display:flex;flex-direction:column;gap:16px;margin:0 0 44px}
.era{font-family:"JetBrains Mono",monospace;font-size:11.5px;letter-spacing:.16em;color:var(--gold);margin:0}
h3.head{font-family:"Chivo","Noto Sans TC",sans-serif;font-weight:900;
  font-size:clamp(21px,3.6vw,27px);line-height:1.35;margin:0;letter-spacing:-.005em;text-wrap:balance}
h4{font-weight:700;font-size:17.5px;margin:8px 0 0}
h5{margin:0;font-size:12.5px;font-family:"JetBrains Mono",monospace;letter-spacing:.1em;font-weight:600}
p{margin:0}
.muted{color:var(--ink2)}
.hot{color:var(--danger);font-weight:700}
.win{color:var(--gold-deep);font-weight:700}
code{font-family:"JetBrains Mono",monospace;font-size:.85em;background:var(--code);
  padding:2px 6px;border-radius:3px}
p.q{font-size:17px;font-weight:700;background:var(--sunk);border-left:4px solid var(--ink2);
  border-radius:0 4px 4px 0;padding:11px 17px;margin-top:6px}
p.formula{font-family:"Chivo","Noto Sans TC",sans-serif;font-size:clamp(15px,2.3vw,18px);
  font-weight:700;color:var(--gold-deep);background:var(--gold-soft);border-radius:6px;
  padding:13px 20px;text-align:center;max-width:none}
ul.plainlist{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:8px}
ul.plainlist li{line-height:1.8}
.ledger{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:15px}
.box{border:1px solid var(--line);border-radius:6px;background:var(--surface);
  padding:16px 19px;display:flex;flex-direction:column;gap:8px;box-shadow:var(--shadow)}
.box.solved{border-top:4px solid var(--gold)}
.box.left{border-top:4px solid var(--danger)}
.box.solved h5{color:var(--gold-deep)}
.box.left h5{color:var(--danger)}
.box ul{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:6px}
.box li{font-size:14.5px;line-height:1.7}
figure{margin:0;display:flex;flex-direction:column;gap:10px}
figure svg{display:block;width:100%;height:auto;background:var(--surface);
  border:1px solid var(--line);border-radius:6px;padding:10px;box-shadow:var(--shadow)}
svg text{font-family:"Noto Sans TC","PingFang TC",sans-serif;fill:currentColor}
svg .mono{font-family:"JetBrains Mono",monospace}
figcaption{font-size:13.5px;color:var(--ink2);line-height:1.7;
  border-left:2px solid var(--line);padding-left:12px}
.terms{display:grid;grid-template-columns:repeat(auto-fit,minmax(225px,1fr));gap:13px}
.term{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--slate);
  border-radius:5px;padding:13px 15px;display:flex;flex-direction:column;gap:3px;box-shadow:var(--shadow)}
.term b{font-family:"Chivo","Noto Sans TC",sans-serif;font-size:15.5px}
.term span{font-size:14px;line-height:1.65;color:var(--ink2)}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--surface);box-shadow:var(--shadow)}
table{border-collapse:collapse;width:100%;min-width:620px;font-size:14px}
th,td{text-align:left;padding:11px 15px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.1em;
  color:var(--ink2);font-weight:600;white-space:nowrap}
tbody th{font-weight:700;white-space:nowrap}
td.num{font-family:"JetBrains Mono",monospace;font-variant-numeric:tabular-nums}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:0}

/* ── 重點整理 ── */
.keys{background:var(--surface);border:1px solid var(--line);border-top:4px solid var(--gold);
  border-radius:6px;padding:18px 22px;margin:8px 0 36px;box-shadow:var(--shadow)}
.keys .lbl{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.16em;
  color:var(--gold);font-weight:600;margin:0 0 8px}
.keys ul{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:7px}
.keys li{font-size:15px}

/* ── 測驗 ── */
.quiz{background:var(--surface);border:1px solid var(--line);border-radius:12px;
  padding:clamp(16px,3vw,26px);margin:0 0 34px;box-shadow:var(--shadow)}
.quiz .qhead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 4px}
.quiz .qtag{font-family:"JetBrains Mono",monospace;font-size:11px;letter-spacing:.18em;color:var(--gold)}
.quiz .qtitle{font-family:"Chivo","Noto Sans TC",sans-serif;font-weight:900;font-size:19px}
.quiz .qnote{font-size:13.5px;color:var(--ink2);margin:0 0 14px}
.qq{margin:0 0 18px}
.qq .qt{font-weight:700;font-size:15.5px;margin:0 0 8px}
.qq .qt .qn{font-family:"JetBrains Mono",monospace;color:var(--gold);margin-right:6px}
.opts{display:flex;flex-direction:column;gap:7px}
.opt{display:flex;gap:9px;align-items:flex-start;border:1px solid var(--line);border-radius:6px;
  padding:9px 13px;background:#FFFFFF;cursor:pointer;font-size:14.5px;line-height:1.65;
  color:var(--ink);text-align:left;width:100%;font-family:inherit}
.opt:hover{border-color:var(--gold)}
.opt .dot{flex:none;width:16px;height:16px;border-radius:50%;border:2px solid var(--mut);margin-top:4px}
.opt.sel{border-color:var(--gold);background:var(--gold-soft)}
.opt.sel .dot{border-color:var(--gold);background:var(--gold)}
.opt:disabled{cursor:default}
.opt.right{border-color:var(--ok);background:var(--ok-soft)}
.opt.right .dot{border-color:var(--ok);background:var(--ok)}
.opt.wrongpick{border-color:var(--danger);background:var(--sunk)}
.opt.wrongpick .dot{border-color:var(--danger);background:var(--danger)}
.exp{font-size:13.5px;color:var(--ink2);border-left:3px solid var(--ok);
  padding:6px 12px;margin:8px 0 0;background:var(--ok-soft);border-radius:0 4px 4px 0}
.exp.bad{border-left-color:var(--danger);background:var(--sunk)}
.qact{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:4px}
.qbtn{font-family:inherit;font-size:15px;font-weight:700;padding:9px 22px;border-radius:6px;
  border:none;background:var(--gold);color:#FFFFFF;cursor:pointer}
.qbtn:hover{background:var(--gold-deep)}
.qbtn:disabled{background:var(--mut);cursor:not-allowed}
.qmsg{font-size:14px;color:var(--ink2)}
.qmsg.pass{color:var(--ok);font-weight:700}
.qmsg.fail{color:var(--danger);font-weight:700}

/* ── 上一課／下一課 ── */
.pager{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding-top:20px}
.pager a{display:flex;flex-direction:column;gap:2px;text-decoration:none;color:var(--ink);
  border:1px solid var(--line);border-radius:8px;padding:12px 18px;max-width:46%;background:var(--surface);box-shadow:var(--shadow)}
.pager a:hover{border-color:var(--gold)}
.pager a .dir{font-size:12px;color:var(--mut)}
.pager a .t{font-weight:700;font-size:15px;color:var(--gold-deep)}
.pager a.next{margin-left:auto;text-align:right}

/* ── 總覽 ── */
.ov-hero{margin:0 0 26px}
.ov-hero .kick{font-family:"JetBrains Mono",monospace;font-size:11.5px;letter-spacing:.2em;color:var(--gold);margin:0 0 8px}
.ov-hero h1{font-family:"Chivo","Noto Sans TC",sans-serif;font-weight:900;
  font-size:clamp(30px,6vw,46px);line-height:1.2;margin:0 0 12px;letter-spacing:-.01em}
.ov-hero p{color:var(--ink2)}
.ov-progress{font-size:14.5px;color:var(--ink2);margin:14px 0 0}
.ov-progress b{color:var(--gold-deep)}
.lesson-list{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:12px;
  background:var(--surface);overflow:hidden;box-shadow:var(--shadow)}
.lesson-list a{display:flex;gap:14px;align-items:baseline;padding:15px 20px;
  text-decoration:none;color:var(--ink);border-bottom:1px solid var(--line)}
.lesson-list a:last-child{border-bottom:0}
.lesson-list a:hover{background:var(--gold-soft)}
.lesson-list .n{font-family:"JetBrains Mono",monospace;color:var(--gold);font-size:14px;min-width:22px;text-align:right;flex:none}
.lesson-list .tt{display:flex;flex-direction:column;gap:1px;min-width:0}
.lesson-list .tt b{font-size:16px}
.lesson-list .tt span{font-size:13.5px;color:var(--ink2)}
.lesson-list .mins{margin-left:auto;flex:none;font-family:"JetBrains Mono",monospace;
  font-size:12px;color:var(--ink2);background:var(--sunk);border-radius:99px;padding:3px 10px}
.lesson-list .done{flex:none;color:var(--ok);font-weight:700}
footer.site{margin-top:36px;border-top:1px solid var(--line);padding-top:15px;
  font-size:12.5px;color:var(--mut)}
a{color:var(--gold)}
*:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
'''

def esc(t): return t

# ---- 組頁面 ----
parts = []
parts.append('<title>從一台機器到一堆貨櫃</title>\n')
parts.append('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n')
parts.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chivo:wght@600;900&family=JetBrains+Mono:wght@400;600&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">\n')
parts.append('<style>'+CSS+'</style>\n')

# 頂欄 + 側欄
parts.append('''<header class="topbar">
  <button class="burger" id="burger" aria-label="開關章節選單">☰</button>
  <a class="brand" href="#/">從一台機器到<b>一堆貨櫃</b></a>
</header>
<div class="scrim" id="scrim"></div>
<nav class="sidebar" id="sidebar" aria-label="章節選單">
  <a href="#/" data-nav="ov" class="ov">📖&nbsp; 課綱總覽</a>
  <div class="group">歷史：為什麼會有容器</div>
''')
groups = {0:'', 3:'  <div class="group">DOCKER：一台機器上的事</div>\n',
          4:'  <div class="group">K8S：由小到大</div>\n',
          12:'  <div class="group">判斷</div>\n'}
for i,L in enumerate(LESSONS):
    if i in groups and groups[i]: parts.append(groups[i])
    parts.append('  <a href="#/lesson/%s" data-nav="%s"><span class="n">%d.</span><span>%s</span><span class="tick" data-tick hidden>✓</span></a>\n'
                 % (L['slug'], L['slug'], i+1, L['title']))
parts.append('</nav>\n<main class="main" id="main">\n')

# ---- 總覽頁 ----
ov = ['<article id="pg-ov">\n<div class="ov-hero">\n<p class="kick">實體機 → 虛擬機 → 容器 → KUBERNETES</p>\n<h1>從一台機器到一堆貨櫃</h1>\n']
ov.append('<p>一份從零開始的教材，共 13 課，照學習順序排列：先懂歷史（每一代解決了上一代的什麼痛），再把 Kubernetes 由小到大一層層拆開。每課末有 3 題隨堂測驗，全對就在側邊欄打勾；進度只存在你這台瀏覽器裡。</p>\n')
ov.append('<p class="ov-progress" id="ovProgress"></p>\n</div>\n<div class="lesson-list">\n')
for i,L in enumerate(LESSONS):
    ov.append('<a href="#/lesson/%s"><span class="n">%d</span><span class="tt"><b>%s</b><span>%s</span></span><span class="done" data-ovtick="%s" hidden>✓</span><span class="mins">%d 分</span></a>\n'
              % (L['slug'], i+1, L['title'], L['desc'], L['slug'], L['mins']))
ov.append('</div>\n<footer class="site">圖裡的時間與數量（40 秒、110 個、2–10 GB）都是預設值或常見量級，不是硬規定。</footer>\n</article>\n')
parts.append(''.join(ov))

# ---- 各課 ----
N = len(LESSONS)
for i,L in enumerate(LESSONS):
    a = ['<article id="pg-%s" hidden>\n' % L['slug']]
    a.append('<p class="crumb"><a href="#/">課綱總覽</a> › 第 %d 課 / 共 %d 課</p>\n' % (i+1, N))
    a.append('<h1 class="lt">%s</h1>\n' % L['title'])
    a.append('<div class="meta"><span class="chip g">第 %d 課 / 共 %d 課</span><span class="chip">約 %d 分鐘</span></div>\n' % (i+1, N, L['mins']))
    a.append('<p class="sub">%s</p>\n' % L['desc'])
    a.append('<div class="learn"><p class="lbl">讀完這課你會</p><ul>%s</ul></div>\n'
             % ''.join('<li>%s</li>' % x for x in L['learn']))
    if L['slug'] == 'why-k8s':
        a.append(CH5_BODY + '\n')
    for si in L['body']:
        a.append(secs[si] + '\n')
    a.append('<div class="keys"><p class="lbl">重點整理</p><ul>%s</ul></div>\n'
             % ''.join('<li>%s</li>' % x for x in L['keys']))
    a.append('<div class="quiz" data-quiz="%s"></div>\n' % L['slug'])
    # pager
    a.append('<nav class="pager">')
    if i > 0:
        P = LESSONS[i-1]
        a.append('<a href="#/lesson/%s"><span class="dir">← 上一課</span><span class="t">%s</span></a>' % (P['slug'], P['title']))
    if i < N-1:
        Nx = LESSONS[i+1]
        a.append('<a class="next" href="#/lesson/%s"><span class="dir">下一課 →</span><span class="t">%s</span></a>' % (Nx['slug'], Nx['title']))
    else:
        a.append('<a class="next" href="#/"><span class="dir">回到</span><span class="t">課綱總覽</span></a>')
    a.append('</nav>\n</article>\n')
    parts.append(''.join(a))

parts.append('</main>\n')

# ---- JS ----
quiz_json = json.dumps(QUIZ, ensure_ascii=False)
slugs_json = json.dumps([L['slug'] for L in LESSONS], ensure_ascii=False)

parts.append('<script>\n(function(){\n')
parts.append('var QUIZ=' + quiz_json + ';\n')
parts.append('var SLUGS=' + slugs_json + ';\n')
parts.append('''var KEY='k8s-course-done';
function loadDone(){try{return JSON.parse(localStorage.getItem(KEY))||{};}catch(e){return {};}}
function saveDone(d){try{localStorage.setItem(KEY,JSON.stringify(d));}catch(e){}}
function refreshTicks(){
  var d=loadDone(),n=0;
  SLUGS.forEach(function(s){ if(d[s])n++; });
  document.querySelectorAll('[data-tick]').forEach(function(el){
    var slug=el.closest('a').getAttribute('data-nav');
    el.hidden=!d[slug];
  });
  document.querySelectorAll('[data-ovtick]').forEach(function(el){
    el.hidden=!d[el.getAttribute('data-ovtick')];
  });
  var p=document.getElementById('ovProgress');
  if(p) p.innerHTML='已完成 <b>'+n+'</b> / '+SLUGS.length+' 課'+(n===SLUGS.length?'——全部打勾了 🎉':'');
}
function shuffle(a){
  for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}
  return a;
}
function renderQuiz(slug){
  var host=document.querySelector('[data-quiz="'+slug+'"]');
  if(!host||!QUIZ[slug])return;
  var qs=QUIZ[slug];
  host.innerHTML='';
  var head=document.createElement('div');
  head.innerHTML='<div class="qhead"><span class="qtag">QUIZ · 隨堂測驗</span><span class="qtitle">檢查你學會了沒</span></div>'
    +'<p class="qnote">共 '+qs.length+' 題，選項順序每次都會重排。全部選好後按「對答案」；全對就在側邊欄打勾。</p>';
  host.appendChild(head);
  var picks=qs.map(function(){return null;});
  var graded=false;
  qs.forEach(function(q,qi){
    var wrap=document.createElement('div');wrap.className='qq';
    var qt=document.createElement('p');qt.className='qt';
    qt.innerHTML='<span class="qn">Q'+(qi+1)+'</span>'+q.q;
    wrap.appendChild(qt);
    var opts=document.createElement('div');opts.className='opts';
    var order=shuffle(q.opts.map(function(_,k){return k;}));
    order.forEach(function(oi){
      var b=document.createElement('button');b.type='button';b.className='opt';
      b.setAttribute('data-oi',oi);
      b.innerHTML='<span class="dot"></span><span>'+q.opts[oi]+'</span>';
      b.addEventListener('click',function(){
        if(graded)return;
        picks[qi]=oi;
        opts.querySelectorAll('.opt').forEach(function(x){x.classList.remove('sel');});
        b.classList.add('sel');
        btn.disabled=picks.some(function(p){return p===null;});
        msg.textContent=btn.disabled?'請先回答全部 '+qs.length+' 題':'都選好了，按「對答案」';
        msg.className='qmsg';
      });
      opts.appendChild(b);
    });
    wrap.appendChild(opts);
    var exp=document.createElement('p');exp.className='exp';exp.hidden=true;
    exp.setAttribute('data-exp',qi);
    wrap.appendChild(exp);
    host.appendChild(wrap);
  });
  var act=document.createElement('div');act.className='qact';
  var btn=document.createElement('button');btn.className='qbtn';btn.textContent='對答案';btn.disabled=true;
  var msg=document.createElement('span');msg.className='qmsg';msg.textContent='請先回答全部 '+qs.length+' 題';
  act.appendChild(btn);act.appendChild(msg);host.appendChild(act);
  btn.addEventListener('click',function(){
    if(graded){renderQuiz(slug);return;}
    graded=true;var allRight=true;
    qs.forEach(function(q,qi){
      var opts=host.querySelectorAll('.qq')[qi].querySelectorAll('.opt');
      opts.forEach(function(b){
        b.disabled=true;
        var oi=+b.getAttribute('data-oi');
        if(oi===0)b.classList.add('right');
        else if(picks[qi]===oi)b.classList.add('wrongpick');
      });
      var exp=host.querySelector('[data-exp="'+qi+'"]');
      var right=picks[qi]===0;
      if(!right)allRight=false;
      exp.hidden=false;
      exp.className='exp'+(right?'':' bad');
      exp.innerHTML=(right?'✓ 答對。':'✗ 正確答案是打勾那一個。')+' '+q.exp;
    });
    btn.textContent='再測一次';btn.disabled=false;
    if(allRight){
      var d=loadDone();d[slug]=true;saveDone(d);refreshTicks();
      msg.textContent='✓ 全對！已在側邊欄打勾';msg.className='qmsg pass';
    }else{
      msg.textContent='有幾題再想想——看完解析可以「再測一次」';msg.className='qmsg fail';
    }
  });
}
/* 路由 */
var sidebar=document.getElementById('sidebar'),scrim=document.getElementById('scrim');
document.getElementById('burger').addEventListener('click',function(){
  sidebar.classList.toggle('open');scrim.classList.toggle('show');
});
scrim.addEventListener('click',function(){sidebar.classList.remove('open');scrim.classList.remove('show');});
sidebar.addEventListener('click',function(e){
  if(e.target.closest('a')){sidebar.classList.remove('open');scrim.classList.remove('show');}
});
function route(){
  var h=location.hash||'#/';
  var m=h.match(/^#\\/lesson\\/([a-z0-9-]+)$/);
  var slug=m&&SLUGS.indexOf(m[1])>=0?m[1]:null;
  document.querySelectorAll('main > article').forEach(function(a){a.hidden=true;});
  var pg=document.getElementById(slug?('pg-'+slug):'pg-ov');
  if(!pg){pg=document.getElementById('pg-ov');slug=null;}
  pg.hidden=false;
  document.querySelectorAll('.sidebar a').forEach(function(a){
    a.classList.toggle('active',a.getAttribute('data-nav')===(slug||'ov'));
  });
  if(slug)renderQuiz(slug);
  refreshTicks();
  window.scrollTo(0,0);
  try{localStorage.setItem('k8s-course-last',h);}catch(e){}
}
window.addEventListener('hashchange',route);
/* 回到上次看的課 */
if(!location.hash){
  var last=null;try{last=localStorage.getItem('k8s-course-last');}catch(e){}
  if(last&&last!=='#/')location.hash=last;
}
route();
})();
</script>\n''')

open(OUT,'w',encoding='utf-8').write(''.join(parts))
print('written', OUT)
