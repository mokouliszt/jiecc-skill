# jiecc-skill

フリーソフトウェア [jiecc.exe](https://www.graviness.com/iec_61131-3/jiecc.html)を使用し、　**GX Works3 / Sysmac Studio / KV STUDIO / CODESYS** などにインポート可能な **IEC 61131-10 XML** を生成する [Claude Code](https://docs.claude.com/claude-code) の Skill です。同梱の `jiecc.exe` を使用するため、追加インストール不要で動作します。
MELSEC(GX Works3)向けの使用を想定して調整しており、特にメーカ指定のない場合はMELSECを想定して動作します。

## 対応メーカー・言語

| メーカー | インポート可能な言語 |
|---------|-------------------|
| 三菱電機 GX Works3 | ST、FB、関数（FUN） |
| オムロン Sysmac Studio | ST、FB、関数、LD |
| キーエンス KV STUDIO | ST、FB、関数、LD |
| CODESYS | ST、FB、関数、SFC |
| 標準（汎用） | ST/FB/FUN/LD/FBD/SFC/IL 全言語 |

## ディレクトリ構成

```
jiecc-skill/
├── jiecc/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── jiecc.exe           # IEC 61131-10 XML 生成ツール（同梱）
│   ├── samples/                # メーカー別サンプル（.txt / .xml ペア）
│   │   ├── mitsubishi/
│   │   ├── omron/
│   │   ├── keyence/
│   │   ├── codesys/
│   │   └── standard/
│   ├── references/
│   └── LICENSE.txt
└── LICENSE
```

## インストール方法

### 方法 A: フォルダをコピーする（推奨）

`jiecc` フォルダを、Claude Code の skills ディレクトリにコピーします。

- ユーザースコープ（全プロジェクトで使用）: `~/.claude/skills/`
- プロジェクトスコープ（特定プロジェクトのみ）: `<プロジェクトルート>/.claude/skills/`

例（macOS / Linux）:

```bash
cp -r jiecc ~/.claude/skills/
```

例（Windows PowerShell）:

```powershell
Copy-Item -Recurse jiecc $HOME\.claude\skills\
```

### 方法 B: claude.ai にアップロードする（ブラウザ／デスクトップ／モバイル）

`jiecc` フォルダを ZIP 圧縮し、拡張子を `.skill` に変更することで Anthropic 公式の **skill-creator 仕様** に準拠したパッケージとして利用できます。Claude Code 以外でも、以下の環境にアップロードして Skill として利用できます。

- [claude.ai](https://claude.ai)（ブラウザ版）
- Claude デスクトップアプリ
- Claude モバイルアプリ

手順（claude.ai の場合）:

1. 設定 → **Capabilities** → **Skills** を開く
2. 「Upload skill」から `.skill` ファイルをアップロード
3. アップロード後、対象の話題が会話に出ると Claude が自動的に Skill を呼び出す

> UI の名称や配置は変更されることがあります。最新の手順は [Anthropic 公式ドキュメント](https://docs.claude.com/) を参照してください。

## 使い方

インストール後、Claude Code を起動してプログラム実装を依頼するだけです。GX Works3 等へのインポートを意図した実装依頼を Claude が検出すると、自動的に Skill を呼び出して XML 生成を実行します。

## 出典

IEC 61131-3 / IEC 61131-10 規格、各エンジニアリングツールのインポート仕様

## 注意事項

- 本リポジトリは **三菱電機株式会社 オムロン株式会社 株式会社キーエンス とは無関係の非公式プロジェクト** です。
- [jiecc.exeの詳細な仕様はこちらのページを参考にしてください。](https://www.graviness.com/iec_61131-3/jiecc.html)
- 本 Skill が出力する情報は参考用途であり、安全関連の設計・運用判断は必ず公式マニュアルおよび有資格者による確認に基づいて行ってください。
- LLM の特性上、生成される回答に誤りが含まれる可能性があります。実機適用前にレビューしてください。

## ライセンス

[MIT License](LICENSE) — Copyright (c) 2026 mokouliszt

## コントリビューション

誤りの指摘・追記提案は Issue / Pull Request で歓迎します。
