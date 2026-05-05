---
name: jiecc
description: |
  PLCプログラム実装依頼を、エンジニアリングツール（GX Works3、Sysmac Studio、
  KV STUDIO、CODESYS等）にインポート可能な IEC 61131-10 XML で納品するためのSkill。
  メインターゲットは三菱電機 GX Works3。
  jiecc.exe はこのSkillに同梱されており、追加インストール不要で動作する。

  ## メーカー別の対応言語

  | メーカー | 対応言語（XMLインポート可能なもの） |
  |---|---|
  | 三菱 GX Works3 | **ST、FB、関数（FUN）のみ** |
  | オムロン Sysmac Studio | ST、FB、関数、LD（ラダー） |
  | キーエンス KV STUDIO | ST、FB、関数、LD（ラダー） |
  | CODESYS | ST、FB、関数、SFC |
  | 標準（汎用） | 全言語（ST/FB/FUN/LD/FBD/SFC/IL） |

  ## 起動する依頼パターン

  ### 1. 三菱(GX Works3)向け新規実装 — ST/FB/FUN のみ
  - 「STで〜書いて」「ST言語で実装」「STロジック」
  - 「FB作って」「ファンクションブロック作って」
  - 「FUN作って」「関数を書いて」
  - 「カウンタFB」「タイマーFB」「制御FB」など機能名+FB/FUNの組合せ
  - 「GX Works3で動くST」「三菱で動くFB」など

  ### 2. 他メーカー(オムロン/キーエンス/CODESYS)向け新規実装 — 各社の対応言語すべて
  各メーカーの対応範囲内であれば、ラダー/SFCを含めて起動する：
  - 「オムロンでラダー書いて」「Sysmac StudioのLDで」「Sysmac StudioのFB」
  - 「キーエンスのKVでラダー」「KV STUDIOのSTで」
  - 「CODESYSのSFC組んで」「CODESYSのST」「CODESYSの関数」

  ### 3. メーカー間の移植・変換（入力言語は何でもOK）
  既存資産を別メーカーに持っていく案件は、入力言語に制限なく起動する：
  - 「オムロンのラダーを三菱に移植」（→出力はSTへの翻訳が必要）
  - 「キーエンスのSTを三菱に持っていきたい」
  - 「CODESYSのSFCを別メーカーに移植」
  - 「他社PLCのプログラムをGX Works3に取り込みたい」
  - エンジニアリングツールから書き出したXMLの読み込み・テキスト化

  ### 4. XMLレビュー・差分管理
  - 既存PLCopen XML（IEC 61131-10 XML）のテキスト化
  - 「このXMLの中身を確認したい」「Gitで管理したい」
  - 入力XMLにラダー/FBD/SFCが含まれていてもOK（逆変換時は言語制約なし）

  ### 5. キーワード明示時
  - 「Jiecc」「jiecc.exe」「IEC 61131-3」「IEC 61131-10」

  ### 6. 標準（standard）ターゲット
  メーカー特定なし、または明示的に IEC 61131-10 規格準拠を求められた場合は
  全言語対応可能。

  ## 起動してはいけない依頼パターン

  ### 三菱(GX Works3)向けの新規ラダー/FBD/SFC/IL実装
  GX Works3 はこれらの言語の XMLインポートに対応していない。
  - 「三菱でラダー書いて」「GX Works3でラダー回路」
  - 「三菱のFBDで」「GX Works3でSFC組んで」「GX Works3でIL」
  - 「三菱で（言語不明）の制御プログラム書いて、ラダーで」
  → 本Skillで対応不可。代替手段（GX Works3で直接編集、または別Skill）を案内すること

  ⚠️ ただし**移植案件は例外**: 「オムロンのラダーを三菱に移植」のような場合は
  起動する（入力ラダー → 出力STへの変換作業は本Skillで対応）。

  ### FBDの新規実装（standard以外）
  standard以外のメーカーは FBD の XMLインポートに対応していない。
  → 撤退対応または standard ターゲットでの実装を案内

  ### CODESYS向けのラダー/IL新規実装
  CODESYSはLD/ILのXMLインポートに対応していない（SFC/STは対応）。
  → 撤退対応または ST への置き換えを提案

  ## 言語が不明な依頼の扱い

  「PLCプログラム作って」「制御ロジック書いて」等、言語が指定されていない依頼：
  - **三菱がターゲット**: STでの実装を前提に進める。ユーザーが明示的にラダー等を
    希望した時点で撤退対応。
  - **他メーカーがターゲット**: ヒアリングで言語を確認し、各メーカーの対応範囲内
    なら継続。
  - **メーカー不明**: メーカーを聞いてから上記を判断。

  ## メーカー独自フォーマットの議論

  PLCがメーカー独自フォーマット（mwp, smc, kpr, project等）の議論をしている場合は、
  XMLインポート可否を案内する起点として本Skillを参照する。
---

# Jiecc — PLCプログラム実装の納品Skill

## このSkillの守備範囲

メーカーごとに対応する言語が異なる：

| メーカー | ST | FB / 関数 | LD（ラダー） | FBD | SFC | IL |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 三菱 GX Works3 | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| オムロン Sysmac Studio | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| キーエンス KV STUDIO | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| CODESYS | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ |
| 標準（standard） | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**ST/FB/関数 は全メーカー対応**、ラダー/SFCはメーカーによる、FBDは標準のみ。

メインターゲットは三菱（GX Works3）。

---

## jiecc.exe の場所（重要）

`jiecc.exe` は**このSkillの `scripts/jiecc.exe` に同梱されている**。
追加インストール不要。

Claude Code がコマンド実行する際は、このSKILL.md が置かれている
ディレクトリ（`<SKILL_DIR>`）からの相対パス、または絶対パス
`<SKILL_DIR>/scripts/jiecc.exe` で `jiecc.exe` を呼び出す。

例えばSkillが `~/.claude/skills/jiecc/SKILL.md` にある場合、
`jiecc.exe` の絶対パスは `~/.claude/skills/jiecc/scripts/jiecc.exe`。

以下、SKILL.md内のコマンド例では便宜上 `jiecc.exe` と短く書くが、
**実行時は必ず同梱版（scripts配下）の絶対パスに置き換えて呼び出す**こと。

### 動作確認（最初の変換実行前に1度だけ）

```bash
# 例（Skillが ~/.claude/skills/jiecc/ にある場合）
~/.claude/skills/jiecc/scripts/jiecc.exe --version
```

PowerShell の場合：

```powershell
& "$HOME\.claude\skills\jiecc\scripts\jiecc.exe" --version
```

### 動作要件

- Windows 7 以降の 64bit OS
- WSL や Linux ネイティブからは直接呼び出せない（cmd.exe 経由が必要）

---

## ユーザーの依頼パターン → 対応する例

### 三菱（GX Works3）向け
> 「GX Works3で動くカウンタFBをSTで作って」  
> 「STで温度制御アルゴリズム書いて」  
> 「PIDのファンクションブロックを実装して」

→ ST/FB/関数で実装してXML化。

### 他メーカー向け
> 「オムロンでラダーを書いて」  
> 「Sysmac Studio で使えるFBを作って」  
> 「キーエンスのKVでラダー処理を実装して」  
> 「CODESYSでSFCを使った状態遷移を組んで」

→ 各メーカーの対応範囲内で実装してXML化。

### 移植・変換
> 「オムロンのラダーを三菱に移植したい」  
> 「他社PLCで動いてたSTプログラムを GX Works3 で動かしたい」  
> 「CODESYSのプロジェクトをオムロンに変換したい」

→ 入力XMLを逆変換 → 必要に応じて言語変換（ラダー→ST等）→ ターゲットメーカー向けに再変換。

### XMLレビュー
> 「このXMLの中身を確認したい」「Gitで差分見たい」

→ 逆変換でテキスト化。入力XMLの言語は問わない。

---

## ユーザーの依頼パターン → 撤退する例

### 三菱(GX Works3)向け新規実装でラダー/FBD/SFC/IL希望
> 「GX Works3でラダー書いて」  
> 「三菱でFBD組んで」  
> 「GX Works3でSFC使って状態遷移」

このようなケースでは、**本Skillでは対応しない**。以下のように案内する：

```
申し訳ありません、三菱 GX Works3 はST言語・FB・関数のXMLインポートのみに
対応しており、ラダー/FBD/SFC/IL は本Skillの対応範囲外です。

以下のいずれかの方法をご検討ください：

1. GX Works3 で直接編集する（ラダー編集はGX Works3の本来の使い方）
2. ロジック自体をST言語に置き換えて実装する場合は、改めてSTでのご依頼として
   承ります（ロジックの表現力はSTでも十分）
```

ユーザーが「ではSTで」と切り替えた場合は、通常のST実装フローに進む。

### CODESYS向け新規実装でラダー/IL希望
CODESYSは LD/IL のXMLインポートに対応していない（SFC/STは対応）。同様に撤退または
ST/SFCへの切り替えを案内する。

### standard以外でFBD希望
FBDは standard ターゲットのみ対応。ユーザーが特定メーカーでのFBD実装を希望する
場合は撤退、または standard でXML生成して手動でメーカー側に取り込む方法を案内。

---

## 三菱(GX Works3)向けの実装ポイント（最頻ターゲット）

三菱向けの詳細仕様は **`references/mitsubishi.md`** に集約。
変換前にまず読むこと。要点：

### 三菱固有データ型（STからも参照可能）

IEC 61131-3 標準には無い、GX Works3 固有のデータ型：

| 型 | 用途 |
|---|---|
| `TIMER` / `LTIMER` | 標準タイマー（32bit / 64bit） |
| `RETENTIVETIMER` / `LRETENTIVETIMER` | 積算タイマー（停電保持） |
| `COUNTER` / `LCOUNTER` | カウンタ（32bit / 64bit） |
| `POINTER` | ポインタ |

これらは三菱のラダー命令（OUT_T、OUT_C等）と組み合わせて使われるが、
**ST言語からも変数として宣言・参照可能**。例えばラダー部で動かすタイマーの
プリセット値をSTで計算する、といった連携パターンに使える。

### キーワードは大文字出力が原則

GX Works3 はキーワードを大文字で扱う。jieccのデフォルトは小文字なので、
変換時に `--retro_caps` オプションを必ず付ける：

```bash
jiecc.exe --retro_caps input.txt -t mitsubishi -o output.xml
```

または IEC 61131-3 テキスト内のプラグマで指定：

```iec
//{retro_caps: true}
```

### ST POU の「プログラムファイル」への配置

GX Works3 ではプログラムを「初期/スキャン/待機/定周期/イベント/実行種別なし」の
6種類のファイルに分けて配置する。configuration定義で指定する：

```iec
configuration config1
    resource MainScan: prgFile
        // (*{ResourceExecutionType.type: "scan"}*)  // スキャン実行
        program ProgramScan with tsk1: ProgramScan_pou();
    end_resource
end_configuration
```

`type` の値: `initial`, `scan`, `standby`, `fixedScan`, `event`, `noExecution`

### 公式サンプルの参照

`samples/mitsubishi/_official_complete_sample.xml` に三菱電機公式の
完全サンプルXMLが配置されている。POU、FB、関数、構造体、コンフィグレーション、
グローバル変数、各種プロパティのすべての要素が網羅されている。

**三菱向けXML生成時は、このファイルを必ず参照する**。
未知の要素や属性が出てきたら、まずこのサンプルで使われ方を確認する。

---

## 標準ワークフロー

### ステップ1: 要件ヒアリング

**最初に必ずメーカーと言語を確認する**。組合せが対応外なら撤退対応に切り替える。

| 確認事項 | デフォルト |
|---|---|
| **ターゲットメーカー** | 不明なら聞く。メイン環境なら mitsubishi 提案 |
| **言語**（メーカーの対応範囲外なら撤退） | メーカーで使える言語の中で確認 |
| 機能要件 | 必須。曖昧なら具体化を聞く |
| 入出力デバイス（X0、Y10 等） | あれば取り込む。なければ仮の名前で書いて指定可能にする |
| ヘッダーコメント・著作情報 | あれば取り込む |
| エンジニアリングツールのバージョン | 各メーカーの最低バージョン要件を満たすか |

### ステップ2: IEC 61131-3 テキスト記述

`references/language.md` を参照しつつ、IEC 61131-3 文法でテキストを書く。
**`samples/<target>/<feature>.txt` に類似機能のサンプルがあれば必ず先に見る**。
書き方の精度が大幅に上がる。

メーカー別の方言は `references/targets.md` を参照。
三菱向けは `references/mitsubishi.md` と
`samples/mitsubishi/_official_complete_sample.xml` を参照。

最低限の構造（三菱向けFB）：

```iec
//{retro_caps: true}
//{company-name: あなたの会社名}
//{product-name: あなたのプロダクト名}

function_block {FbPouProperties.isEnEno: false} CounterFB
var_input
    Enable: bool;
    Reset:  bool;
end_var
var_output
    Count: int;
end_var
var
    PrevEnable: bool;
end_var
//{st}
if Reset then
    Count := 0;
elsif Enable and not PrevEnable then
    Count := Count + 1;
end_if;
PrevEnable := Enable;
//{end}
end_function_block
```

ST本体を `//{st}` ～ `//{end}` で囲むのを忘れない（最頻発エラー）。

### ステップ3: XML変換

```bash
# 三菱向け（大文字キーワード必須）
<SKILL_DIR>/scripts/jiecc.exe counter.txt -t mitsubishi --retro_caps -o counter.xml
```

`<SKILL_DIR>` はSKILL.mdが置かれているディレクトリの絶対パス。

エラーが出たら `references/targets.md` `references/mitsubishi.md` で確認。

### ステップ4: 納品

ユーザーには以下のような形で渡す：

> `counter.xml` を生成しました。GX Works3 で「プロジェクト → IEC 61131-10 XML 形式の
> ファイルからインポート」を選び、このファイルを取り込んでください。
> ソースは `counter.txt` に保存してあります（Git管理用）。

エンジニアリングツールごとのインポート手順の概略：

| ツール | 必要バージョン | インポート方法 |
|---|---|---|
| GX Works3 | Ver.1.110Q 以降 | プロジェクト → 開く → ファイル種別をXMLに切替、または「XMLファイルからインポート」 |
| Sysmac Studio | Ver.1.30 以降 | プロジェクト → ライブラリ → IEC 61131-10 XML をインポート |
| KV STUDIO | Version 12 以降 | プロジェクト → ファイル → IEC 61131-10 XML をインポート |
| CODESYS | V3.5.21.0 以降 | プロジェクト → 追加 → PLCopen XML をインポート |

詳細はメーカードキュメント参照（バージョンによりUIが変わる）。

---

## 副次ユースケース

### A. 既存XMLのレビュー（XML → テキスト）

ユーザーがエンジニアリングツールから書き出したXMLを差分管理したいとき：

```bash
<SKILL_DIR>/scripts/jiecc.exe -d existing.xml -o existing.txt
```

テキスト化すればGitでdiffが見やすい。

入力XMLにラダー/FBD/SFC部分が含まれていても逆変換は機能する。
ラダー部分は `{ld}~{end}` プラグマ内に IEC 61131-10 ネイティブXMLとして埋め込まれる。

### B. メーカー間移植

#### B-1. 入出力ともに対応言語が共通な場合（最も簡単）

例: オムロンのSTプロジェクトを三菱に移植：

```bash
# 1. オムロンXML → 中立テキスト
<SKILL_DIR>/scripts/jiecc.exe -d omron_project.xml -o source.txt

# 2. 三菱で通るよう手で調整（メーカー方言の違い・三菱独自データ型の活用等）

# 3. 三菱XMLとして書き出し
<SKILL_DIR>/scripts/jiecc.exe --retro_caps source.txt -t mitsubishi -o mitsubishi_project.xml
```

#### B-2. 入力にラダー等が含まれ、出力先が三菱/CODESYS の場合

例: オムロンのラダープロジェクトを三菱に移植：

```bash
# 1. オムロンXML → 中立テキスト（ラダー部分は {ld}~{end} で埋め込まれる）
<SKILL_DIR>/scripts/jiecc.exe -d omron_project.xml -o source.txt
```

→ source.txt 内のラダー部分を**手動でST言語に翻訳**する作業が発生する。
   この翻訳作業を本Skillでサポートする：

- ラダー回路ごとに、その動作を表すSTコードに置き換え
- タイマー命令 → `TIMER` 型変数 + ST制御
- カウンタ命令 → `COUNTER` 型変数 + ST制御
- 自己保持回路 → `if then ... elsif ... end_if` 構造
- エッジ検出 → `R_TRIG` / `F_TRIG` FB

```bash
# 2. ST化された source.txt を三菱XMLとして書き出し
<SKILL_DIR>/scripts/jiecc.exe --retro_caps source.txt -t mitsubishi -o mitsubishi_project.xml
```

メーカー間で構文が異なる箇所はプリプロセッサ `{#if _MITSUBISHI}` での分岐で吸収する。
`references/preprocessor.md` 参照。

### C. プリプロセッサでテンプレート生成

複数の型に同じFBを生成したい、メーカー別に共通ソースから出し分けたい等：

```bash
# マクロ展開だけ確認
<SKILL_DIR>/scripts/jiecc.exe -E source.txt -t mitsubishi
```

詳細は `references/preprocessor.md`。

---

## 基本コマンド

以下、便宜上 `jiecc.exe` と短く書いているが、実行時は
**`<SKILL_DIR>/scripts/jiecc.exe` の絶対パスに置き換えて呼び出す**こと。

```bash
# テキスト → XML（三菱は --retro_caps 必須）
jiecc.exe input.txt -t mitsubishi --retro_caps -o output.xml

# テキスト → XML（標準）
jiecc.exe input.txt -o output.xml

# XML → テキスト（逆変換）
jiecc.exe -d input.xml -o output.txt

# プリプロセスのみ
jiecc.exe -E input.txt
```

ターゲット名: `standard` (デフォルト) / `omron` / `keyence` / `mitsubishi` / `codesys`

| よく使うオプション | 用途 |
|---|---|
| `-D MACRO[=VAL]` | マクロ定義 |
| `-I PATH` | include検索パス追加 |
| `-N CRLF` | 改行コード（LF/CRLF/CR）。GX Works3との互換性ならCRLF推奨 |
| `--retro_caps` | キーワード大文字化（**三菱は必須**） |

詳細は `references/cli.md`。

## 応用コマンド

### ディレクトリ一括変換

```bash
# bash / WSL / Git Bash（JIECC変数で同梱版を参照）
JIECC="<SKILL_DIR>/scripts/jiecc.exe"
mkdir -p out && for f in src/*.txt; do
    "$JIECC" "$f" -t mitsubishi --retro_caps -o "out/$(basename "$f" .txt).xml"
done
```

```powershell
# PowerShell
$jiecc = "<SKILL_DIR>\scripts\jiecc.exe"
New-Item -ItemType Directory -Force out | Out-Null
Get-ChildItem src\*.txt | ForEach-Object {
    & $jiecc $_.FullName -t mitsubishi --retro_caps -o "out\$($_.BaseName).xml"
}
```

### 全ターゲットへの並行変換（移植時の比較用）

```bash
JIECC="<SKILL_DIR>/scripts/jiecc.exe"
mkdir -p out
for t in standard omron keyence mitsubishi codesys; do
    "$JIECC" main.txt -t "$t" -o "out/main.$t.xml" \
        && echo "  ✓ $t" || echo "  ✗ $t (方言の不一致の可能性)"
done
```

### CIで差分が安定する変換

```bash
"<SKILL_DIR>/scripts/jiecc.exe" \
    --set creation-datetime=2024-01-01T00:00:00+09:00 \
    -N CRLF --retro_caps main.txt -t mitsubishi -o main.xml
```

## ファイル構成

```
jiecc/
├── SKILL.md                    （このファイル）
├── LICENSE.txt                 Jiecc配布物のBSDライセンス
├── references/                 必要時にClaudeが読む詳細リファレンス
│   ├── cli.md                    jiecc.exe 全オプション
│   ├── language.md               IEC 61131-3 文法概要
│   ├── targets.md                メーカー別方言比較
│   ├── mitsubishi.md             ★GX Works3 詳細仕様
│   └── preprocessor.md           プリプロセッサとパターン集
├── scripts/                    実行ファイル同梱
│   ├── jiecc.exe                 ★Jiecc 本体（同梱）
│   └── README.md                 配置手順とバージョン記録
└── samples/                    Jiecc公式サンプル + 三菱電機公式サンプル
    ├── standard/   (80ファイル) 全機能・全言語サンプル
    ├── mitsubishi/ (44ファイル + 公式完全サンプル1ファイル)
    │   └── _official_complete_sample.xml ★三菱電機公式完全XML
    ├── omron/      (54ファイル)
    ├── keyence/    (42ファイル)
    └── codesys/    (62ファイル)
```

各サンプルは `<feature>.txt` (テキスト) と `<feature>.xml` (XML) が対。
新しいコードを書く前に**該当機能のサンプルを必ず確認**すること。
**三菱向けは `_official_complete_sample.xml` を必ず参照する**。

## トラブルシューティング

| 症状 | 対処 |
|---|---|
| `Body program section requires {st} and {end} pragmas` | ST本体が `//{st}` ～ `//{end}` で囲まれていない |
| 三菱向け新規にラダー/FBD/SFC/ILを依頼された | **本Skillの範囲外**。代替手段（メーカーツール直接編集、別Skill）を案内 |
| 三菱への移植入力にラダーが含まれる | **本Skillで対応**。逆変換 → ラダー部分をSTに手動翻訳 → 三菱XMLへ変換 |
| GX Works3でインポート時に「キーワードが認識されない」 | `--retro_caps` オプションを付け忘れている |
| GX Works3でインポート時にバージョンエラー | Ver.1.110Q 以降が必要 |
| `var constant retain` がキーエンスでエラー | キーエンスは constant と retain 同時不可 |
| `at %IX0.0` が三菱でエラー | 三菱は `%X0.0` 形式（I/Q/Mプレフィックス不可） |
| 逆変換で整形・コメントが失われる | XMLの仕様上一部失われる。整形は手動 |
| `jiecc.exe is not recognized` / `jiecc.exe not found` | `scripts/jiecc.exe` が同梱されていない可能性。`scripts/README.md` 参照 |
| WSL等の Linux環境で実行できない | jiecc.exeはWindows専用。`cmd.exe /c` 経由か Windows ホストで実行 |

## ライセンス

Jiecc 本体は Simplified BSD License (graviness.com)。
このSkillに同梱しているサンプルもJiecc配布物の一部であり、同ライセンスに従う。
公式完全サンプルXML（`samples/mitsubishi/_official_complete_sample.xml`）は
三菱電機株式会社の著作物。
詳細は `LICENSE.txt`。
