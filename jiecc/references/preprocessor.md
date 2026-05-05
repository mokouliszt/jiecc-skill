# Jiecc プリプロセッサ

Jieccは独自のプリプロセッサを持ち、C言語風のマクロ・条件コンパイル・
ファイルインクルードに加え、可変長引数マクロやトークン連結も使える。

メーカー間の差異を1ソースで吸収したり、反復的な定義を生成したりするのに
強力。**メーカー横断のコード資産を作るときの肝**。

---

## プリプロセッサ命令の構文

すべて `{# ... }` または `{...}` で囲まれる。
コメントの中（`//` や `(* ... *)`）にあっても解釈される（ストリッピング前に評価）。

| 命令 | 用途 |
|---|---|
| `{#define MACRO body}` | マクロ定義 |
| `{#define MACRO(args) body}` | 関数マクロ定義 |
| `{#if cond}` ... `{#elif cond}` ... `{#else}` ... `{#endif}` | 条件コンパイル |
| `{include: "path"}` | ファイル取り込み（ヘッダ的にコピー） |
| `{import: "path"}` | ファイル取り込み（参照のみ、重複抑制） |

---

## 1. オブジェクトマクロ（単純な置換）

```iec
{#define R0 0}
{#define R1 5}
{#define RANGE R0..R1}
{#define T dint}

function my_sum: T
var_input
    in: array[RANGE] of T;
end_var
//{st}
my_sum := T#0;
//{end}
end_function
```

`RANGE` が `0..5`、`T` が `dint` に展開される。

---

## 2. 関数マクロ（引数付き）

### 基本形

```iec
{#define MAX2(x, y, o) if (x) > (y) then o := x; else o := y; end_if;}

program Main
var
    iv: int;
    rv: lreal;
end_var
//{st}
MAX2(1 + 2, 3 - 4, iv);
MAX2(1.0 + 2.0, 3.0 - 4.0, rv);
//{end}
end_program
```

### 複数行マクロ + トークン連結 `@@`

```iec
{#define DECL_ADD_FUNCTION(T)
    function add_@@T: T
    var_input
        in1, in2: T;
    end_var
    ${st$}
    add_@@T := in1 + in2;
    ${end$}
    end_function
}

DECL_ADD_FUNCTION(int);
DECL_ADD_FUNCTION(lreal);
```

→ `add_int` と `add_lreal` という2つの関数が生成される。

**ポイント:**

- マクロ本体は `{ ... }` で囲む（ネスト可）
- `@@T` で `T` の値を識別子に連結（`add_` + `int` → `add_int`）
- マクロ本体の中で `{st}` を書くと外側のプリプロセスと衝突するので
  `${st$}` ～ `${end$}` でエスケープ。展開後に `{st}` ～ `{end}` になる
- 行末セミコロンを忘れずに

---

## 3. 可変長引数マクロ

C99の `__VA_ARGS__` 風。`__VA_ARGC__` で引数の個数を取得できる。

```iec
{#define String_concat(...) _String_concat_n(__VA_ARGC__, __VA_ARGS__)}
    {#define String_concat_1(s1) s1}
    {#define String_concat_2(s1, s2) concat(s1, s2)}
    {#define String_concat_3(s1, s2, s3) concat(String_concat_2(s1, s2), s3)}
    {#define String_concat_4(s1, s2, s3, s4) concat(String_concat_3(s1, s2, s3), s4)}
    {#define _String_concat_n(n, ...) String_concat_@@n(__VA_ARGS__)}

{#define LOG(kind, lineno, ...) concat(kind, ':', lineno, ':', __VA_ARGS__)}

program Main
var
    msg1, msg2: string[255];
end_var
//{st}
msg1 := String_concat('error', {## __LINE__}, 'Divided by zero.');
msg2 := String_concat('warning', {## __LINE__}, 'Declaration', '&Redefine');
//{end}
end_program
```

`{## __LINE__}` で `__LINE__` を文字列化（C言語の `#` ステリンジファイ相当）。

---

## 4. 条件コンパイル `{#if}`

### ターゲットマクロ

`-t` オプションに応じて以下が定義される：

- `_STD`（デフォルト）
- `_OMRON`
- `_KEYENCE`
- `_MITSUBISHI`
- `_CODESYS`

### 使い方

```iec
{#if _MITSUBISHI}
    var
        sensor at %X0.0: bool;
    end_var
{#elif _OMRON}
    var
        sensor at %W0.0: bool;
    end_var
{#elif _KEYENCE}
    var
        sensor at %R0 : bool;
    end_var
{#else}
    var
        sensor at %IX0.0: bool;
    end_var
{#endif}
```

### 論理演算

```iec
{#if not (_KEYENCE or _MITSUBISHI)}
    // KEYENCEとMITSUBISHI以外
{#endif}

{#if _MITSUBISHI and _DEBUG}
    // 三菱かつデバッグビルド
{#endif}
```

### 値ベースの条件

```iec
{#define VERSION 3}

{#if VERSION >= 3}
    // バージョン3以降の機能
{#endif}
```

### マクロが定義済みかの判定

```iec
{#if defined(MY_FLAG)}
    // MY_FLAG が定義されている場合
{#endif}
```

---

## 5. include / import

### include — テキストとして展開

```iec
{include: "./common/types.txt"}
```

- 指定ファイルの内容がその場に展開される
- 同じファイルを複数回 include すると重複定義になりエラー

### import — 重複抑制つき

```iec
{import: "./common/types.txt"}
```

- 同じファイルを複数回 import してもエラーにならない（1回だけ展開）
- C/C++ の `#pragma once` 相当

検索パスは `-I` オプション（`--syspath`）で追加できる：

```bash
jiecc.exe -I ./lib -I ./common main.txt -t mitsubishi -o main.xml
```

---

## 6. プリプロセスのみ実行

`-E` オプションで変換せず展開結果だけ出力：

```bash
jiecc.exe -E main.txt
```

展開結果のプラグマ表記スタイルを選べる：

```bash
# (*{st}*) 形式（デフォルト・annotated）
jiecc.exe -E main.txt

# {st} 形式（standard）
jiecc.exe -E --pp-output-pragma-style standard main.txt

# コメント除去
jiecc.exe -E -nC main.txt

# 全マクロ定義リスト
jiecc.exe -E -dM main.txt
```

---

## 7. 実用パターン

### パターン A: メーカー横断のFB資産

```iec
// common/edge_detect.iec
{#if not (_MITSUBISHI or _CODESYS)}
function_block edge_detect_native
    var_input
        in: bool r_edge;
    end_var
end_function_block
{#else}
// r_edge 非対応PLC向けの代替実装
function_block edge_detect_native
    var_input
        in: bool;
    end_var
    var
        prev: bool;
    end_var
    var_output
        rising: bool;
    end_var
    //{st}
    rising := in and not prev;
    prev := in;
    //{end}
end_function_block
{#endif}
```

```iec
// main.iec
{import: "./common/edge_detect.iec"}

program Main
var
    detector: edge_detect_native;
end_var
//{st}
detector(in := input_signal);
//{end}
end_program
```

### パターン B: 多型関数の自動生成

```iec
{#define DECL_CLAMP(T)
    function clamp_@@T: T
    var_input
        v, lo, hi: T;
    end_var
    ${st$}
    if v < lo then
        clamp_@@T := lo;
    elsif v > hi then
        clamp_@@T := hi;
    else
        clamp_@@T := v;
    end_if;
    ${end$}
    end_function
}

DECL_CLAMP(int);
DECL_CLAMP(dint);
DECL_CLAMP(real);
DECL_CLAMP(lreal);
```

→ 4種類の型に対応する `clamp_int`, `clamp_dint`, `clamp_real`, `clamp_lreal` が生成される。

### パターン C: ターゲットごとの定数

```iec
{#if _MITSUBISHI}
    {#define BUFFER_SIZE 512}     // 三菱はメモリ余裕あり
{#elif _KEYENCE}
    {#define BUFFER_SIZE 128}     // キーエンスは抑える
{#else}
    {#define BUFFER_SIZE 256}
{#endif}

program Main
var
    buf: array[0..(BUFFER_SIZE - 1)] of word;
end_var
end_program
```

### パターン D: デバッグビルド切り替え

```bash
# リリース
jiecc.exe main.txt -t mitsubishi -o release.xml

# デバッグ
jiecc.exe -D DEBUG main.txt -t mitsubishi -o debug.xml
```

```iec
program Main
var
    counter: int;
{#if defined(DEBUG)}
    debug_log: string[255];
{#endif}
end_var
//{st}
counter := counter + 1;
{#if defined(DEBUG)}
debug_log := concat('counter = ', int_to_string(counter));
{#endif}
//{end}
end_program
```

---

## 8. ハマりやすいポイント

### マクロ本体内の `{st}` プラグマ

`{#define ... { ... ${st$} ... ${end$} ... } }` のように
内側を `${st$}` ～ `${end$}` でエスケープしないと、外側のプリプロセスが
誤って解釈する。展開後は `{st}` ～ `{end}` になる。

### `@@` の前後

トークン連結 `@@` は前後の空白に注意：

```iec
add_@@T          // OK → add_int
add_ @@ T        // 空白入りはNG
```

### include パスの相対基準

`include` / `import` のパスは、`jiecc.exe` の**実行ディレクトリ**ではなく
**includeしているファイルの位置**からの相対パスとして解釈される
（C プリプロセッサと同じ動作）。

### `_STD` は `-t standard` でのみ定義

`-t` を省略しても `_STD` は定義される。`-t omron` のときは
`_STD` は定義されず `_OMRON` のみ。

---

## サンプル一覧

`samples/<target>/pp.*` にプリプロセッサ機能の動作サンプル：

- `pp.fmacro1.txt` — シンプルな関数マクロ
- `pp.fmacro2.txt` — トークン連結を使った関数生成
- `pp.ifmacro.txt` — 条件コンパイル
- `pp.omacro.txt` — オブジェクトマクロ
- `pp.vaargs.txt` — 可変長引数マクロ

`include.txt` / `import.txt` も参照。
