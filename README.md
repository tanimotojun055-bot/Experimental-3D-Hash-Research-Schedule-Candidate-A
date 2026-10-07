# Experimental-3D-Hash-Research-Schedule-Candidate-A
 3D Hash (3DH) Experimental Research3DH is an experimental cryptographic hash research projectusing a three-dimensional 64-bit cell structure.Current prototype:3DH-v1 Schedule Candidate A


# 3D Hash (3DH) Experimental Research

3DH is an experimental cryptographic hash research project
using a three-dimensional 64-bit cell structure.

Current prototype:
3DH-v1 Schedule Candidate A

Current test profile:
- Grid: 64 x 64 x 64
- Cell width: 64 bit
- Rounds: 64
- Input difference: 1 bit

Observed avalanche result:
- Round 32:
  262,144 / 262,144 cells changed
  49.998772% of all bits changed

- Round 64:
  262,144 / 262,144 cells changed
  49.999648% of all bits changed

Android smartphone test:
- 64 rounds
- Elapsed time: 6.346357 seconds

WARNING:
This project is experimental research.
It has NOT been cryptographically validated.
Do not use it for production security.



3D Hash 暗号仕様書 Version 1

名称：3D Hash
略称：3DH
仕様バージョン：3DH-v1
標準出力：256 bit
内部状態：512 bit
基本セル：64 bit

状態：

Experimental
Cryptanalysis Required

---

1. 目的

3D Hashは、従来の一次元的なハッシュ処理とは異なり、入力情報を三次元セル空間へ配置し、

X方向
Y方向
Z方向

および、

+X
-X
+Y
-Y
+Z
-Z

の空間的関係を利用して情報を拡散するハッシュ方式とする。

最終出力はSHA-256と同じ、

256 bit
＝ 32 byte

とする。

したがって既存の256 bitハッシュを利用するシステムへ置換しやすい構造を目標とする。

---

2. 基本構造

基本処理は、

入力データ

↓

64 bit単位へ変換

↓

3Dセル空間へ配置

↓

3D Message Schedule

↓

3D Mixing Rounds

↓

512 bit内部状態

↓

Final Mix

↓

256 bit出力

とする。

---

3. 3Dセル

1セルは、

64 bit

とする。

セル表記は、

P[x][y][z]

とする。

x ＝ X方向座標
y ＝ Y方向座標
z ＝ Z方向座標

である。

---

4. 3D空間サイズ

正式なFULLプロファイルは、

256 × 256 × 256

とする。

セル総数：

256 × 256 × 256

＝ 16,777,216セル

＝ 2の24乗セル

1セル64 bitなので、

FULL状態容量

＝ 16,777,216 × 8 byte

＝ 134,217,728 byte

＝ 128 MiB

となる。

---

5. 計算能力別プロファイル

異なる計算能力の機器で利用できるよう、複数のプロファイルを持たせる。

TINY：

32 × 32 × 32

LIGHT：

64 × 64 × 64

MID：

128 × 128 × 128

FULL：

256 × 256 × 256

すべて、

1セル ＝ 64 bit

とする。

PC、Raspberry Pi、スマートフォン、ロボット制御装置等で同一3DH仕様を利用可能にする。

---

6. エンディアン

CPU内部では、そのCPUが得意なネイティブ形式を利用できる。

現在想定する、

x86-64
ARM64
Raspberry Pi

では通常Little Endianで処理する。

したがって内部処理は、

Internal Processing

＝ Native 64 bit

とする。

ただし外部保存・通信・比較については、

3DH Canonical Byte Order

＝ Big Endian

と固定する。

したがって、

内部Little Endian

↓

Canonical変換

↓

外部Big Endian

とする。

これにより異なるCPUでも同じ3DH値を得る。

---

7. 入力

3DHは任意長データを入力可能とする。

基本インターフェースは、

init()

update(data)

final()

のストリーム処理方式とする。

したがって巨大ファイルについても、全データを一度にメモリへ入れる必要はない。

---

8. SHA-256との外部互換性

3DHはSHA-256と同じハッシュ値を生成するものではない。

目的は、

同一値互換

ではなく、

置換互換

である。

SHA-256：

任意長入力

↓

256 bit / 32 byte出力

3DH-256：

任意長入力

↓

256 bit / 32 byte出力

とする。

例えば、

hash(data, "SHA-256")

を、

hash(data, "3DH-256")

へ交換できる構造を目標とする。

---

9. 内部状態

SHA-256では、

8 × 32 bit

＝ 256 bit

の内部状態を持つ。

3DHでは64 bit CPUとの親和性および内部拡散余裕を考慮し、

8 × 64 bit

＝ 512 bit

とする。

内部状態を、

S0
S1
S2
S3
S4
S5
S6
S7

とする。

各Sは64 bit。

したがって、

Internal State

＝ S0～S7

＝ 512 bit

となる。

---

10. 最終出力

内部状態512 bitをFinal Mixへ入れ、

256 bit

へ圧縮する。

最終状態を、

H0
H1
H2
H3

とする。

各Hは64 bit。

したがって、

4 × 64 bit

＝ 256 bit

となる。

外部出力：

H0 || H1 || H2 || H3

＝ 32 byte

とする。

単純に、

S0 XOR S4

等だけで圧縮する方式は採用しない。

512 bit全体を十分混合してから256 bitへ落とす。

---

11. 6方向空間

3Dセルには6方向を定義する。

+X
-X
+Y
-Y
+Z
-Z

3DHでは正方向と逆方向を別の情報として扱う。

---

12. 6面投影

3D空間から、

Projection(+X)

Projection(-X)

Projection(+Y)

Projection(-Y)

Projection(+Z)

Projection(-Z)

を生成可能とする。

各方向は別々の順序情報を保持する。

---

13. 24分岐

6面それぞれを4領域へ分割する。

1面 ＝ 4分岐

6面 × 4

＝ 24分岐

となる。

したがって3DHでは、

24 Branch Structure

を持つ。

---

14. 内部構造

6面情報だけでは三次元内部構造を完全に識別できない可能性がある。

そのため、

H_inner

という内部構造情報を持たせる。

内部状態は、

X方向走査
Y方向走査
Z方向走査

の情報を利用する。

---

15. SHA-256 Message Scheduleとの対応

SHA-256では、

512 bit入力

を、

32 bit × 16

に分割する。

これを、

W[0] ～ W[15]

とする。

その後、

W[16] ～ W[63]

を生成する。

SHA-256の基本式は、

W[t]

＝ sigma1(W[t-2])

＋ W[t-7]

＋ sigma0(W[t-15])

＋ W[t-16]

である。

つまり、

近い過去

＋

中距離の過去

＋

遠い過去

を混合している。

---

16. 3D Message Schedule

3DHではSHA-256のMessage Scheduleに対応するものとして、

3D Message Schedule

を定義する。

表記：

D[t]

または、

3DS[t]

とする。

tはラウンド番号で、

t ＝ 0 ～ 63

を第一候補とする。

3DS[t]は、

X方向セル

Y方向セル

Z方向セル

反対方向セル

過去ラウンド状態

等から生成する。

---

17. 3D座標参照

現在セルを、

A

＝ P[x][y][z]

とする。

X方向参照セル：

X

＝ P[x + dx[t]][y][z]

Y方向参照セル：

Y

＝ P[x][y + dy[t]][z]

Z方向参照セル：

Z

＝ P[x][y][z + dz[t]]

とする。

座標が範囲を超えた場合は、

mod N

によって反対側へ回す。

---

18. 距離スケジュール

dx[t]

dy[t]

dz[t]

は毎ラウンド同じ値にしない。

目的は、

近距離情報

中距離情報

遠距離情報

を全空間へ拡散することである。

したがって、

±1固定

だけにはしない。

正式な距離系列は暗号解析後に固定する。

---

19. CH型 Direction Select Mix

SHA-256のChは、

Choose

つまり選択関数である。

基本形：

CH3(X,Y,Z)

＝

(X AND Y)

XOR

((NOT X) AND Z)

とする。

意味：

Xの各bitが1ならYを選択

Xの各bitが0ならZを選択

となる。

3DHでは、

ある方向の状態によって、

他方向のどちらを強く混合するか

を決めるために使用する。

---

20. MAJ型 3D Majority Mix

SHA-256のMajは、

Majority

つまり多数決である。

3DHでは、

MAJ3(X,Y,Z)

＝

(X AND Y)

XOR

(X AND Z)

XOR

(Y AND Z)

とする。

各bitについて、

1,1,0 → 1

0,0,1 → 0

となる。

3D構造では、

X方向

Y方向

Z方向

の多数決Mixとして利用する。

---

21. 64 bit回転

3DHでは64 bitセル内部で、

ROTL64

ROTR64

を使用可能とする。

回転量は、

1 ～ 63

とする。

64 bit回転において、

0回転

と

64回転

は同じ結果になるため、

0および64は使用しない。

回転量生成式の基本候補：

R

＝ (value mod 63) + 1

とする。

これにより必ず、

1 ～ 63

となる。

---

22. 3D回転量

各方向に、

R1[t]

R2[t]

R3[t]

を定義する。

例：

RX

＝ ROTL64(X, R1[t])

RY

＝ ROTR64(Y, R2[t])

RZ

＝ ROTL64(Z, R3[t])

とする。

回転量はラウンドごとに変化させる。

ただし時計時刻によって変化させてはならない。

同一入力は常に同一結果になる必要がある。

---

23. K[t] ラウンド定数

SHA-256には、

K[0] ～ K[63]

という64個の固定ラウンド定数が存在する。

ここで、

t

は時間ではない。

t

＝ ラウンド番号

である。

3DHでも、

K3D[0] ～ K3D[63]

という固定ラウンド定数を使用する案を採用する。

目的は、

各ラウンドの対称性を崩すこと

である。

K3D[t]は秘密値ではない。

公開仕様に含める。

---

24. ラウンド数

SHA-256は、

64 Round

である。

3DH-v1も現時点では、

64 Mixing Rounds

を第一候補とする。

表記：

Round 0

～

Round 63

とする。

ただし正式な64ラウンド採用は、

Avalanche試験

差分解析

速度試験

等によって確認する。

---

25. 3D-MIX64 基本候補

現段階の基本候補：

A

＝ 現在セル

X

＝ X方向セル

Y

＝ Y方向セル

Z

＝ Z方向セル

まず、

RX

＝ ROTL64(X,R1[t])

RY

＝ ROTR64(Y,R2[t])

RZ

＝ ROTL64(Z,R3[t])

を生成する。

次に、

T1

＝ RX

＋ CH3(X,Y,Z)

＋ K3D[t]

T2

＝ RY

＋ MAJ3(X,Y,Z)

T3

＝ RZ XOR A

とする。

その後、

NEW

＝ T1

XOR T2

XOR ROTL64(T3,R4[t])

とする候補を持つ。

加算は、

mod 2^64

とする。

ただしこの式は現段階では、

3D-MIX64 Candidate

であり、最終確定ではない。

---

26. 3D方向変化

毎ラウンド、

+X
-X
+Y
-Y
+Z
-Z

の組み合わせを変更可能とする。

目的は、

単方向だけに情報が流れることを防止するためである。

各ラウンドで、

方向

距離

回転量

ラウンド定数

を変化させる。

ただしすべては決定論的でなければならない。

---

27. 時刻情報

3DHハッシュ本体には、

現在時刻

を使用しない。

同一データについて、

今日計算しても

10年後に計算しても

同一3DH値になる必要がある。

ただしP2P通信では、

Timestamp

Nonce

Session ID

等を入力データへ含めることは可能である。

例えば、

3DH

(

Timestamp

＋ Nonce

＋ Robot ID

＋ Message

)

とする。

これにより通信値は毎回変化する。

---

28. 3DハッシュとP2P

ロボット間通信では、

Robot A

↓

Robot ID

↓

Timestamp

↓

Nonce

↓

Message

↓

3DH

↓

署名またはMAC

↓

暗号化通信

↓

Robot B

とする。

3DH単独を本人認証には使用しない。

署名・MAC・公開鍵暗号等と組み合わせる。

---

29. 3DH安全性目標

最終出力256 bitについて、

原像耐性：

約 2の256乗

第二原像耐性：

約 2の256乗

衝突耐性：

約 2の128乗

を目標とする。

ただしこれは、

設計目標

であり、

現在の3DHがこの安全性を証明済み

という意味ではない。

---

30. Avalanche目標

入力1 bitを変更した場合、

最終256 bit出力の約半分、

約128 bit

が変化することを目標とする。

平均変化率：

約50％

を目標とする。

---

31. 重要な設計条件

3DHは、

単純にSHA-256より計算を遅くすること

を安全性目標とはしない。

正規利用者は、

Raspberry Pi

スマートフォン

PC

ロボット制御装置

で現実的な時間内に計算できる必要がある。

一方、攻撃者については、

衝突探索

原像探索

構造攻撃

差分攻撃

等に近道が存在しないことを目標とする。

---

32. 互換性

3DH-v1は、

PC

Raspberry Pi

Android

ARM64

x86-64

等で同一結果になるようにする。

そのため、

64 bitセル

Canonical Big Endian

固定パディング

固定3D Schedule

固定K3D

固定回転規則

を正式仕様に含める。

---

33. 現時点で確定した主要項目

出力：

256 bit / 32 byte

内部状態：

512 bit

内部ワード：

8 × 64 bit

セル：

64 bit

FULL：

256 × 256 × 256

LIGHT：

64 × 64 × 64

MID：

128 × 128 × 128

外部表現：

Big Endian

内部処理：

Native 64 bit

分岐：

6面 × 4

＝ 24分岐

基本演算：

XOR

AND

NOT

64 bit ADD

ROTL64

ROTR64

CH3

MAJ3

ラウンド数：

64候補

回転量：

1～63

内部出力：

512 bit

最終出力：

256 bit

---

34. Version 1で今後確定する項目

以下はVersion 1完成までに正式決定する。

1. 

dx[t]

dy[t]

dz[t]

の正式な64ラウンド系列。

2. 

R1[t]

R2[t]

R3[t]

R4[t]

の正式な回転系列。

3. 

K3D[0～63]

の生成方法と固定値。

4. 

3D-MIX64の最終式。

5. 

入力パディング方式。

6. 

複数3Dブロックの接続方式。

7. 

512 bitから256 bitへのFinal Mix。

8. 

LIGHT / MID / FULL間の正式識別子。

9. 

標準テストベクトル。

10. 

暗号解析結果。

---

35. 全体処理

最終的な処理構造は、

Input

↓

Padding

↓

64 bit Word Conversion

↓

3D Cell Mapping

↓

3D Message Schedule

↓

3D-MIX64

↓

64 Mixing Rounds

↓

6 Face Processing

↓

24 Branch Processing

↓

Internal Structure Mix

↓

512 bit Internal State

↓

Final Mix

↓

256 bit Digest

↓

Canonical Big Endian

↓

32 byte Output

とする。

---

36. 基本目標

3DH-v1の目標は、

SHA-256と同じ256 bit出力形式を維持しながら、

64 bit CPUへ適合し、

3D空間構造を利用して、

X・Y・Z方向へ情報を拡散し、

PCだけでなく、

Raspberry Pi

スマートフォン

ロボット

分散AI端末

でも利用可能な暗号学的ハッシュ方式を構築することである。

---

3D Hash Cryptographic Specification

Version 1

3DH-v1

Current Draft



