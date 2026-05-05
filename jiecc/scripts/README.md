# scripts/ — jiecc.exe 同梱ディレクトリ

このディレクトリには `jiecc.exe` を**同梱した状態で配布する**ことを想定している。

## 配布者向け：配布前の手順

1. https://www.graviness.com/iec_61131-3/jiecc.zip から最新版をダウンロード
2. ZIPを展開し、その中の `jiecc.exe` をこのディレクトリに配置
3. 必要なら `LICENSE.txt`（同梱物のもの）を確認し、Skillルートの `LICENSE.txt` と
   一致するかチェック（マイナーバージョン違いはあり得る）
4. 下記の **同梱バージョン記録** を更新
5. このSkill全体をZIP化して配布

```
jiecc/
├── SKILL.md
├── LICENSE.txt
├── references/
├── samples/
└── scripts/
    ├── README.md       (このファイル)
    └── jiecc.exe       ← ここに配置
```

## 同梱バージョン記録

| 項目 | 値 |
|---|---|
| 配置日 | _yyyy-mm-dd を記入_ |
| jiecc バージョン | _`jiecc.exe --version` の出力を記入_ |
| 取得元 | https://www.graviness.com/iec_61131-3/jiecc.zip |
| ライセンス | Simplified BSD License (Jiecc配布物の `LICENSE.txt` 参照) |

## 利用者向け（Skill展開後のセットアップは不要）

このSkillには jiecc.exe が同梱されているため、利用者側での追加設定は**不要**。
SkillをClaude Codeにインストールしたら、即座に変換コマンドが動く。

PATH追加・環境変数設定・別途インストールはすべて**不要**。

## 動作要件

- **OS**: Windows 7 以降の 64bit OS
- **アーキテクチャ**: x64

WSL や Linux ネイティブから直接実行することはできない。Claude Code を
Windows 上で動かすか、WSL からは `cmd.exe /c` 経由で呼び出す必要がある。

## 動作確認

配置後、以下で動作確認できる（Windows コマンドプロンプトまたは PowerShell）：

```cmd
scripts\jiecc.exe --version
```

バージョン情報が表示されればOK。
