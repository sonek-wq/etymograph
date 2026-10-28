# 英語語源ネットワーク辞書 EtymoGraph 作業メモ（引き継ぎ用）

英語語源ネットワーク辞書 EtymoGraph のリポジトリ。新しい会話で作業を始めるときは、まずこのファイルと README.md を読むこと。
README.md は利用者向けの説明とデータ形式の仕様、このファイルは編集する人（Claude を含む）向けの方針と手順。

## 構成

| パス | 内容 |
|---|---|
| `index.html` | ビューア本体（vis-network 9.1.9 を CDN から読む。表示ロジックのみでデータは持たない） |
| `etymo-data.json` | データ（version 2。pie / parts / words / categories / branches） |
| `README.md` | 利用者向けの説明・データ形式 |
| `tools/` | 追加用スクリプトの例と検証スクリプト |

公開は GitHub Pages（main ブランチのルート）。main にプッシュすると数分で公開サイトに反映されるので、大きな変更はブランチで作って確認してから main に入れる。

## データ追加の方針

- **照合：** 追加・修正は、まず Online Etymology Dictionary（etymonline.com）で確認する。`src` に項目名・確認日・日本語の要約を書く（原文をそのまま写さない）。末尾に「掲載語: …」を付ける。
- **Etymonline で確認できない場合：** 他の信頼できる辞書・資料、または Claude の知識で補ってよい（2026-10-27 に利用者が了承。Etymonline に必ず従う必要はない）。
  - Claude の知識によるものは `src` の `id` を `knowledge`（`sources` に登録済み）にし、`entry`・`checked` は付けず、`note` に根拠を書く。新しく作る祖語・パーツの `status` は `unverified` にする。
  - 他の資料を使う場合は `sources` にその資料を登録し、その `id` を使う。
  - 後で Etymonline で確認できたら、`etymonline` の `src` を足して `status` を `verified` にする。
- **単語：** すべてに `ja`（和訳）と `literal`（直訳）を付ける。
- **祖語の表記：** Etymonline の表記に合わせる（例：`*spek-`、番号付きは `*pel-(5)`、ラベルは `*pel-`）。代名詞系など同綴りの区別は `*me-(pron)` のように説明的な接尾を付け、`label` は素の形にする。
- **祖語につなぐ基準：**
  - 祖語の説が一つだけなら、留保付き（perhaps など）でもつなぐ。
  - 説が競合している、または否定的な見解が併記されているなら `pie: []` にして `note` に書く。
- **祖語のないもの：**
  - 現代英語より前の形（ラテン語・ギリシア語・古フランス語・ゲルマン祖語・古英語など）が分かるなら `pie: []`（祖語未詳）で収録する。
  - 最古の形が英語（古英語・中英語）で出所の分からないものは `etym: "unknown"`（語源不明。例：boy, dog, jump, smooth）。
  - Etymonline が非印欧語起源を主な説（probably など）としているものは `etym: "nonie"`、`branch: "nonie"`（例：coffee, tea, cotton, zero）。非印欧語説が候補の一つにすぎない場合は祖語未詳にして `note` に書く（例：tower, silk）。
- **接辞の起源：** Etymonline が同じ祖語の接尾辞から（または同源と）する接辞は、その接尾辞（`*-nt-` など）を祖語ノード（カテゴリ `relation`）にしてつなぐ（例：-ing・-ent・-ence は `*-nt-`）。パーツどうしを直接つなぐ仕組みはないので、祖語の形が書かれていない同源関係（-ly と like、bench と bank、-ness と -tude など）はつながず `note` に書く。動名詞の -ing は `-ing(1)`、現在分詞の -ing は `-ing`。
- **過去分詞由来の接尾辞：** ラテン語の過去分詞の語幹（act-, fact-, script-, stat- など）は語根の異形（`forms`）に含める。英語の綴りに接尾辞として残るものはその接尾辞を付ける：-ate（ラテン語 -ātus・-ātum。Etymonline の -ate (1) にならい estate・state・status・senate も）、-ade / -ado（-āta、parade・salad・desperado）、-y(1)（フランス語 -ée など、army・country・journey・jury・party）、-ee、-ed。いずれも `*-to-` につながる。ギリシア語由来（climate・pirate）や -ītus（unite）には -ate を付けない。
- **言語のハブノードは作らない。**
- **分解：** 語根・接辞の分け方は Etymonline の説明に従う。フランス語経由の -pose（compose, propose, purpose）は `paus`（後期ラテン語 pausāre）、ラテン語 pōnere 由来（suppose, position, deposit）は `pos`。比較級の -er は `-er(2)`、行為者の -er は `-er`。

## 追加の手順

1. **調べる：** WebSearch「etymonline WORD etymology」で URL を得て、WebFetch で本文を確認する（検索結果に出ていない URL を直接 WebFetch すると拒否されることがある）。
2. **既存のノードを確認する：** 祖語の id・パーツの id が既にあるか、衝突しないかを調べる。
3. **スクリプトを書く：** `tools/batch_example.py` の形式に従う。
   - 新しい祖語・パーツは衝突を assert で確認する。
   - パーツは種類ごとの末尾に挿入する。
   - 既存パーツへの出典・異形の追加は `addsrc()` で行う。
   - 書き出しは1要素1行のブロック形式（差分が見やすい）。
   - 例のスクリプトはそのまま再実行しないこと（同じ語を二重に足そうとして assert で止まる）。
4. **バックアップしてから実行する：**
   ```
   cp etymo-data.json etymo-data.vNNpre.json && (python3 tools/batchNN.py || cp etymo-data.vNNpre.json etymo-data.json)
   ```
   `etymo-data.v*.json` は .gitignore 済み。
5. **検証する（下記）。**
6. **README を更新する：** 機能を変えたときは「画面の使い方」、データ形式を変えたときは該当する節を直す。

## 検証

最初に一度だけ：`cd tools && npm install`（ブラウザのテストで vis-network をローカルから読むため）。
ブラウザのテストの前に、リポジトリのルートで `python3 -m http.server 8782` を起動しておく。

| コマンド | 内容 |
|---|---|
| `echo "inspect gate" \| python3 tools/showdec.py` | 単語の分解（綴りのどこが各パーツか）を表示 |
| `python3 tools/cover.py` | 綴りの被覆率が低い語・語根を持たない語の一覧（末尾が件数） |
| `python3 tools/test23.py` | ページを開いて統計・警告・道探索を確認。`errors: []` なら正常 |
| `python3 tools/pwall.py` | 全単語の分解を JS 側で計算（Python 側との不一致確認用） |
| `python3 tools/test_fav.py` | 登録機能・登録一覧・道探索（接辞も経由）のテスト |
| `python3 tools/test_lbl.py` | ノード名の表示切り替えと登録ノードの強調のテスト |
| `python3 tools/test_mobile.py` | スマホ幅（390×844・360×640）と PC 幅のスクリーンショット（`tools/mob_*.png`） |
| `python3 tools/test_search_mobile.py` | スマホでの検索（検索ボタン・Enter・変換確定・候補の選択）と PC の Enter 検索 |
| `python3 tools/test_case.py` | 大文字・小文字だけが違う語（Miss / miss など）の検索と、id を変えた語（mister → Mister）の旧リンク・登録の引き継ぎ |

画面の見た目を変えたときは、テストが保存するスクリーンショット（`tools/*.png`、.gitignore 済み）を目で確認する。

## 画面まわりのメモ

- 登録（☆）と各種設定はブラウザの localStorage に保存する（`etymo-favs-v1`、`etymo-via-affix`、`etymo-fav-sort`、`etymo-label`）。キー名を変えると利用者の登録が消えるので変えないこと。
- 道探索で「接辞も経由」がオフのとき、繋がらなければ `fewestAffixPaths()`（通る接辞が最少の道）に切り替えて、その旨を表示する。
- スマホの検索補助（変換確定後の検索・候補選択での検索）は `TOUCH`（`pointer: coarse`）のときだけ動かす。「検索」ボタンは `type="button"`（submit にすると、PC で Enter による送信の挙動が変わる恐れがある）。
- スマホ対応はすべて `@media (max-width:720px)` の中と、`fitNodes()`・`showHome()` の幅による分岐で行っている。PC の見た目を変えないこと（変更後は PC 幅のスクリーンショットも比べる）。
- 登録したノードの表示：単語は本体と文字を黄色（#facc15）にし、祖語・語根・接辞は名前を黄色にして★印を `afterDrawing` で描く。
- 単語の id は大文字・小文字を区別する（固有名詞・敬称は大文字：March と march、Miss と miss）。検索は大文字・小文字まで一致する語を優先する。既存の語の id を変えたときは、`index.html` の `RENAMED`（登録の引き継ぎ）に旧 id → 新 id を足す。旧リンク（`#f=word:旧id`）は大文字・小文字の違いだけなら自動で新 id に開く。

## 名称と検索での表示

- 正式な表記は「英語語源ネットワーク辞書 EtymoGraph」（日本語名が先、英字名が後。間は半角スペース）。`<title>`・`og:title`・`og:site_name`・画面の見出し・README で揃える。
- 公開 URL が決まったら、トップページに WebSite の構造化データ（JSON-LD）を追加する：`name` に正式名、`alternateName` に「EtymoGraph」「英語語源ネットワーク辞書」、`url` にトップページの URL。あわせて `og:url`・`og:image`・`<link rel="canonical">` も入れる。
- Google の「サイト名」表示はドメイン・サブドメイン単位で、`ユーザー名.github.io/etymograph/` のようなサブディレクトリでは使われない。サイト名まで正式名で出すには独自ドメイン（例：etymograph.jp）が必要。
