# Jiecc サンプル集

Jiecc 公式配布物に含まれるIEC 61131-3テキストとIEC 61131-10 XMLの対応サンプル。
ターゲット別にディレクトリが分かれている。

## ディレクトリ構成

```
samples/
├── standard/     ← IEC 61131-10 規格準拠（80ファイル、全機能網羅）
├── mitsubishi/   ← 三菱電機 GX Works3 準拠（44ファイル）
├── omron/        ← オムロン Sysmac Studio 準拠（54ファイル）
├── keyence/      ← キーエンス KV STUDIO 準拠（42ファイル）
└── codesys/      ← CODESYS 準拠（62ファイル）
```

各ターゲットディレクトリには、機能ごとに対のファイルが置かれている：

- `<feature>.txt` — IEC 61131-3 ソーステキスト
- `<feature>.xml` — Jiecc が出力する IEC 61131-10 XML

例：`mitsubishi/fb.txt` を `jiecc.exe -t mitsubishi` で変換すると
`mitsubishi/fb.xml` と同等のXMLになる。

## 機能カテゴリ別の見方

### 言語の基礎を知りたい

- `program.txt` — プログラム POU の最小例
- `func.txt` — 関数の定義と呼び出し
- `fb.txt` — ファンクションブロックの定義と呼び出し
- `st.txt` — ST文の網羅的な例（演算子、if、case、for、while、repeat）
- `elementary_types.txt` — 基本データ型の使い方

### 変数まわり

- `array_var.txt` — 配列変数
- `struct.txt` — 構造体変数
- `string_var.txt` — 文字列変数
- `global_var.txt` — グローバル変数
- `var_attrs.txt` — `retain` / `constant` 等の属性

### プリプロセッサ

- `pp.omacro.txt` — オブジェクトマクロ（単純置換）
- `pp.fmacro1.txt` — 関数マクロ
- `pp.fmacro2.txt` — トークン連結による型多相
- `pp.ifmacro.txt` — 条件コンパイル
- `pp.vaargs.txt` — 可変長引数マクロ
- `include.txt` — ファイルインクルード
- `import.txt` — ファイルインポート

### 上位構造

- `configuration.txt` — コンフィグレーション
- `task.txt` — タスク定義とプログラム割り当て
- `header_info.txt` — ヘッダ情報

### オブジェクト指向（standard, codesys のみ）

- `interface.txt` — インタフェース
- `class.txt` — クラス（standardのみ）
- `oofb.txt` — オブジェクト指向FB
- `ref_to.txt` — 参照型
- `namespace.txt` — 名前空間

### 高度な型（standard中心）

- `enum.txt` — 列挙型
- `subrange_type.txt` / `subrange_var.txt` — 部分範囲型
- `array_type.txt` — 配列型定義
- `alias.txt` — 別名定義
- `variable_length_array.txt` — 可変長配列
- `named_value.txt` — 名前付き値

### その他の言語

- `ld.txt` — ラダー言語
- `il.txt` — IL言語（standardのみ）
- `fbd.txt` — FBD言語（standardのみ）
- `sfc.txt` — SFC言語

### ドキュメント

- `doc.txt` — ドキュメンテーションコメント
- `en_eno.txt` — EN/ENO（有効入力・有効出力）
- `var_access.txt` — 変数アクセス指定子
- `var_config.txt` — VAR_CONFIG（standardのみ）

## 移植・コンバート時の活用法

メーカーAからメーカーBへ移植したいときは、同じ機能の `.txt` を見比べる：

```bash
# 三菱の関数とCODESYSの関数を比較
diff samples/mitsubishi/func.txt samples/codesys/func.txt

# 三菱のFBとオムロンのFBを比較
diff samples/mitsubishi/fb.txt samples/omron/fb.txt
```

`{#if _MITSUBISHI}` 等の条件分岐がどう使われているかが見えるので、
同じソースを複数ターゲットで使うパターンが学べる。

## 完全な機能カバレッジ表

`references/targets.md` の末尾を参照。
どのターゲットがどの機能のサンプルを持つかが一覧できる。
