# EtymoGraph 作業メモ（引き継ぎ用）

英語語源ネットワーク辞書（EtymoGraph）のリポジトリ。新しい会話で作業を始めるときは、まずこのファイルと README.md を読むこと。
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

- **照合：** 追加・修正はすべて Online Etymology Dictionary（etymonline.com）で確認する。`src` に項目名・確認日・日本語の要約を書く（原文をそのまま写さない）。末尾に「掲載語: …」を付ける。
- **単語：** すべてに `ja`（和訳）と `literal`（直訳）を付ける。
- **祖語の表記：** Etymonline の表記に合わせる（例：`*spek-`、番号付きは `*pel-(5)`、ラベルは `*pel-`）。代名詞系など同綴りの区別は `*me-(pron)` のように説明的な接尾を付け、`label` は素の形にする。
- **祖語につなぐ基準：**
  - 祖語の説が一つだけなら、留保付き（perhaps など）でもつなぐ。
  - 説が競合している、または否定的な見解が併記されているなら `pie: []` にして `note` に書く。
- **祖語のないもの：**
  - 現代英語より前の形（ラテン語・ギリシア語・古フランス語・ゲルマン祖語・古英語など）が分かるなら `pie: []`（祖語未詳）で収録する。
  - 最古の形が英語（古英語・中英語）で出所の分からないものは `etym: "unknown"`（語源不明。例：boy, dog, jump, smooth）。
  - Etymonline が非印欧語起源を主な説（probably など）としているものは `etym: "nonie"`、`branch: "nonie"`（例：coffee, tea, cotton, zero）。非印欧語説が候補の一つにすぎない場合は祖語未詳にして `note` に書く（例：tower, silk）。
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

画面の見た目を変えたときは、テストが保存するスクリーンショット（`tools/*.png`、.gitignore 済み）を目で確認する。

## 画面まわりのメモ

- 登録（☆）と各種設定はブラウザの localStorage に保存する（`etymo-favs-v1`、`etymo-via-affix`、`etymo-fav-sort`、`etymo-label`）。キー名を変えると利用者の登録が消えるので変えないこと。
- 道探索で「接辞も経由」がオフのとき、繋がらなければ `fewestAffixPaths()`（通る接辞が最少の道）に切り替えて、その旨を表示する。
- 登録したノードの表示：単語は本体と文字を黄色（#facc15）にし、祖語・語根・接辞は名前を黄色にして★印を `afterDrawing` で描く。
