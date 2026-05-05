# jiecc.exe CLI リファレンス

`jiecc.exe --help` の出力を整理し、実用的な使い方を補足したもの。

## 基本構文

```
jiecc.exe [オプション] [ファイルパス...]
```

## モード（出力形式）

| オプション | 動作 |
|---|---|
| `-c`, `--output_iec_61131_10` | IEC 61131-3テキスト → IEC 61131-10 XML（デフォルト） |
| `-d`, `--output_iec_61131_3` | IEC 61131-10 XML → IEC 61131-3テキスト（逆変換） |
| `-E`, `--preprocess-only` | プリプロセスのみ実行（変換しない） |

`-c` と `-d` は排他。どちらも省略時は `-c`。

## 入出力

| オプション | 説明 |
|---|---|
| `filepath` | 入力ファイル（`-c`時はテキスト、`-d`時はXML）。複数指定可 |
| `-o OUTPUT`, `--output OUTPUT` | 出力ファイルパス。省略時は標準出力 |

## ターゲット指定

| オプション | 値 | エンジニアリングツール |
|---|---|---|
| `-t standard` | デフォルト | IEC 61131-10 規格準拠（汎用） |
| `-t omron` | OMRON | Sysmac Studio |
| `-t keyence` | KEYENCE | KV STUDIO（5.2~） |
| `-t mitsubishi` | MITSUBISHI | GX Works3（5.4~） |
| `-t codesys` | CODESYS | CODESYS V3.5.21~（5.8~） |

ターゲット名は大文字小文字どちらでも受理される（`-t OMRON` も可）。
ターゲットを指定すると、対応する `_OMRON` 等の組み込みマクロが定義される
（プリプロセッサで条件分岐に使える）。

## プリプロセッサ関連

| オプション | 説明 |
|---|---|
| `-D MACRO` | マクロを `1` で定義（`-D DEBUG`） |
| `-D MACRO=value` | マクロに値を割り当て（`-D V=10`） |
| `-I PATH`, `--syspath PATH` | include/import の検索パスを追加 |
| `--max-include-depth N` | include の最大ネスト深さ（デフォルト200） |
| `-nC`, `--remove-comments` | プリプロセス出力からコメント除去 |
| `--pp-output-pragma-style STYLE` | プリプロセス出力のプラグマ形式：`annotated` (`(*{~}*)`) または `standard` (`{~}`) |
| `-dM` | プリプロセス時に定義された全マクロをリスト出力（`-E` と併用） |

組み込みマクロの例：`_STD`, `_OMRON`, `_KEYENCE`, `_MITSUBISHI`, `_CODESYS`,
`__LINE__`, `__VA_ARGS__`, `__VA_ARGC__`

## 出力フォーマット

| オプション | 説明 |
|---|---|
| `-N LINE_SEPARATOR` | 改行コード：`LF`（デフォルト）/`CRLF`/`CR` |
| `--retro_caps` | IEC 61131-3キーワードを大文字で出力 |

## 実行制御

| オプション | 説明 |
|---|---|
| `--recursion-limit N` | 再帰深さ上限（デフォルトはシステム既定） |
| `--silent` | エラーメッセージ抑制 |
| `--set OPTION` | オプションの固定（例：`--set creation-datetime=2024-01-01T00:00:00+09:00`） |
| `--version` | バージョン表示 |
| `-h`, `--help` | ヘルプ表示 |

`--set` は CI などでXMLの差分を安定させたいときに有用。
`creationDateTime` を固定すれば毎回ヘッダが変わらず、Gitの差分がクリーンになる。

## よく使うコマンド例

### 標準的な変換

```bash
# テキスト → XML（GX Works3向け）
jiecc.exe main.txt -t mitsubishi -o main.xml

# XML → テキスト（レビュー用）
jiecc.exe -d main.xml -o main_review.txt

# プリプロセスだけ確認
jiecc.exe -E main.txt
```

### マクロ定義を伴う変換

```bash
# DEBUGマクロを有効にして変換
jiecc.exe -D DEBUG -D BUFFER_SIZE=256 main.txt -t mitsubishi -o main.xml
```

### include検索パスの指定

```bash
jiecc.exe -I ./lib -I ./common main.txt -t mitsubishi -o main.xml
```

### CI向けの安定出力

```bash
jiecc.exe \
  --set creation-datetime=2024-01-01T00:00:00+09:00 \
  -N CRLF \
  main.txt -t mitsubishi -o main.xml
```

### プリプロセス結果の保存とマクロ展開確認

```bash
# プラグマを通常表記で出力
jiecc.exe -E --pp-output-pragma-style standard main.txt -o expanded.txt

# 定義された全マクロも見たい
jiecc.exe -E -dM main.txt -o macros.txt
```

## 終了コード

`jiecc.exe` の終了コードはドキュメント化されていないが、
通常通り 0 = 成功、非ゼロ = 失敗 として扱って問題ない。
スクリプトでは標準エラー出力もキャプチャして判定するのが安全。

## Windows以外で実行したい場合

`jiecc.exe` は Windows 7以降の64bit OS 向けバイナリ。
WSL や Linux では直接実行できないので：

- Windows ホスト上で実行
- WSL なら `cmd.exe /c` 経由か `wsl.exe` の interop 経由で呼び出し
- macOS / Linux ネイティブなら Wine が必要だが公式サポート外

CI で動かす場合は Windows ランナー（GitHub Actions の `windows-latest` 等）を使う。
