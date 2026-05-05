# IEC 61131-3 言語の概要

Jieccで扱うIEC 61131-3テキストの記法をまとめる。
**完全な言語仕様書ではない**。Jieccの入力として実用的な範囲をカバーする。

---

## 目次

1. ファイル構造とPOU
2. データ型
3. 変数宣言
4. ST文（Structured Text）
5. ファンクション・FB呼び出し
6. プラグマ（重要）
7. コメント
8. アクセス修飾子と属性

---

## 1. ファイル構造と POU

POU = Program Organization Unit。
ファイルは複数のPOUと型定義から構成できる。

```iec
// (任意) ユーザ定義型
type
    s_t: struct
        m0: int;
        m1: bool;
    end_struct;
end_type

// 関数
function add: int
var_input
    a, b: int;
end_var
//{st}
add := a + b;
//{end}
end_function

// ファンクションブロック
function_block counter_fb
var_input
    enable: bool;
end_var
var_output
    count: int;
end_var
var
    prev_enable: bool;
end_var
//{st}
if enable and not prev_enable then
    count := count + 1;
end_if;
prev_enable := enable;
//{end}
end_function_block

// プログラム
program Main
var
    counter_inst: counter_fb;
    n: int;
end_var
//{st}
counter_inst(enable := true);
n := counter_inst.count;
//{end}
end_program
```

---

## 2. データ型

### 基本型

| カテゴリ | 型 |
|---|---|
| 真偽値 | `bool` |
| 整数 | `sint`(8bit), `int`(16bit), `dint`(32bit), `lint`(64bit) |
| 符号なし整数 | `usint`, `uint`, `udint`, `ulint` |
| ビット列 | `byte`, `word`, `dword`, `lword` |
| 浮動小数点 | `real`(32bit), `lreal`(64bit) |
| 時間 | `time` (`t#1ms`, `t#1s500ms` 等) |
| 文字列 | `string`, `string[N]`, `wstring` |
| 日時 | `date`, `time_of_day`, `date_and_time` |

リテラル例：

```iec
ival := int#42;
bval := word#16#FFAA;       // 16進
hval := word#2#10101010;    // 2進
flt  := lreal#3.14;
tval := t#100ms;
```

### 配列

```iec
// 1次元
ary: array[0..9] of int;

// 多次元
mat: array[0..3, 0..3] of real;

// 初期値付き
vs: array[0..2] of int := [2, 3, 5];

// 繰り返し初期化
all_true: array[0..7] of bool := [8(true)];
```

### 構造体

```iec
type
    point_t: struct
        x: int;
        y: int;
    end_struct;
end_type

var
    p: point_t := (x := 1, y := 2);
end_var
```

### 列挙型（標準・OMRON・CODESYSのみ）

```iec
type
    color_t: (red, green, blue);
end_type

var
    c: color_t := red;       // STD/OMRON
    // c := color_t.red;     // CODESYS
    // c := color_t#red;     // STD
end_var
```

### 部分範囲型（標準のみ）

```iec
type
    temp_range: int (-40..125);
end_type
```

---

## 3. 変数宣言

### 種類

```iec
var               ... end_var    // 静的（インスタンス）変数
var_input         ... end_var    // 入力引数
var_output        ... end_var    // 出力引数
var_in_out        ... end_var    // 入出力引数（参照渡し）
var_temp          ... end_var    // テンポラリ
var_external      ... end_var    // 外部参照（グローバル変数の参照）
var_global        ... end_var    // グローバル変数（configuration内）
```

### 属性

```iec
var retain                       // 停電保持
    counter: int;
end_var

var constant                     // 定数
    PI: lreal := 3.14159265;
end_var

var constant retain              // 両方（キーエンス・CODESYSは不可）
    VERSION: int := 1;
end_var
```

### 直接アドレス指定

```iec
// 標準・OMRON
var
    inp at %IX0.0: bool;
    out at %QW0  : word;
end_var

// 三菱
var
    inp at %X0.0: bool;
    mem at %M100: word;
end_var

// キーエンス
var_global
    rly at %R0 : bool;
end_var
```

---

## 4. ST文（Structured Text）

### 代入

```iec
x := 10;
y := x * 2 + 1;
```

### 演算子

```iec
// 算術
+ - * / mod **        // ** はべき乗（CODESYS不可、EXPT()使用）

// ビット演算
and or xor not
&                     // ANDのエイリアス（CODESYS不可）

// 比較
< <= = <> >= >

// 単項
-x  +x   not x        // +x は三菱不可
```

### if 文

```iec
if x > 0 then
    sign := 1;
elsif x < 0 then
    sign := -1;
else
    sign := 0;
end_if;
```

### case 文

```iec
case status of
    0:
        msg := 'idle';
    1, 2:
        msg := 'running';
    3..5:
        msg := 'error';
    else
        msg := 'unknown';
end_case;
```

### for 文

```iec
for i := 0 to 9 by 1 do
    sum := sum + ary[i];
    if sum < 0 then
        exit;                    // ループ脱出
    end_if;
    if sum = 100 then
        continue;                // 次イテレーション（三菱・OMRON不可）
    end_if;
end_for;
```

### while 文

```iec
while count < 100 do
    count := count + 1;
end_while;
```

### repeat 文

```iec
repeat
    n := n - 1;
until n = 0
end_repeat;
```

---

## 5. ファンクション・FB呼び出し

### 関数呼び出し

```iec
// 位置引数
result := add(2, 3);

// 名前付き引数
result := add(a := 2, b := 3);

// 出力引数（CODESYSは => 必須）
ok := func(in1 := x, in2 := y, o => out_val);
```

### FB呼び出し

```iec
var
    timer_inst: TON;
end_var

// 呼び出し
timer_inst(IN := start, PT := t#1s);

// 出力アクセス
done := timer_inst.Q;
```

---

## 6. プラグマ（重要）

### `{st}` ～ `{end}` （実行コード本体マーカー）

**必須**。プログラム/FB/関数の実行コード部はこれで囲む。
2形式あり、どちらでも可。

```iec
program Main
var ... end_var

//{st}              ← または (*{st}*)
x := x + 1;
//{end}             ← または (*{end}*)

end_program
```

これがないと `Body program section requires {st} and {end} pragmas.` エラー。

### `(*{key: value}*)` 注釈プラグマ

メタ情報の付加。タスクへのプログラム割り付けの実行順など：

```iec
program sub_program: SubProgram() (*{evaluation-order: 2}*);
```

---

## 7. コメント

```iec
// 行コメント
(* ブロックコメント *)
(* ネスト
   (* 可能 *)
*)
```

ドキュメンテーションコメントは `samples/standard/doc.txt` 参照。

---

## 8. アクセス修飾子と属性

### 変数アクセス指定

```iec
function_block fb1
    var_input
        in: bool;
    end_var
    var public                   // 標準のみ。CODESYSは制限あり
        pub_var: int;
    end_var
    var private
        priv_var: int;
    end_var
end_function_block
```

### エッジ検出（標準・OMRON・キーエンスのみ）

```iec
function_block fb1
    var_input
        in: bool r_edge;         // 立ち上がりエッジで検出
        // in: bool f_edge;      // 立ち下がりエッジ
    end_var
end_function_block
```

三菱とCODESYSでは非対応。代わりに `R_TRIG` / `F_TRIG` FBを使う：

```iec
var
    rising: R_TRIG;
end_var
//{st}
rising(CLK := input_signal);
if rising.Q then
    // 立ち上がり時の処理
end_if;
//{end}
```

---

## 9. その他の構成要素

### namespace（標準・OMRON・CODESYSのみ）

```iec
namespace utils
    function add: int
    var_input
        a, b: int;
    end_var
    //{st}
    add := a + b;
    //{end}
    end_function
end_namespace

program Main
//{st}
n := utils.add(2, 3);
//{end}
end_program
```

### configuration / resource / task

```iec
configuration MainConfiguration
    resource MainResource on plc
        var_global
            sensorv at %X0.0: bool;
        end_var

        task tsk_fast(interval := t#1ms, priority := 2);
        task tsk_slow(interval := t#100ms, priority := 3);

        program main_program with tsk_fast: Main();
    end_resource
end_configuration
```

---

## 10. オブジェクト指向（CODESYS と標準のみ）

### interface

```iec
interface i_drivable
    method drive
    var_input
        speed: int;
    end_var
    end_method
end_interface
```

### class

```iec
class car implements i_drivable
    method public drive
    var_input
        speed: int;
    end_var
    //{st}
    // ...
    //{end}
    end_method
end_class
```

### 参照型 ref_to

```iec
var
    cv: car;
    rv: ref_to car;
end_var
//{st}
rv := ref cv;     // 参照取得（CODESYSでは構文異なる）
cv := rv^;        // 参照外し
//{end}
```

---

## 機能ごとの完全サンプル

このSkillの `samples/<target>/<feature>.txt` に各機能の動作するサンプルが
ある。新しいコードを書く前にまず該当機能のサンプルを参照すること。

例：FB を書きたい → `samples/mitsubishi/fb.txt` を見る。
`samples/mitsubishi/fb.xml` で対応するXMLも確認できる。
