文字搜尋問題：單一模式字串搜尋（KMP 演算法 vs. 動態規劃）
我建議選擇 單一模式字串搜尋（String Matching），比較「KMP（Knuth–Morris–Pratt）演算法」與「動態規劃（Dynamic Programming, DP）」。

這個題目適合用來探討動態規劃與非動態規劃的差異，因為兩者都可以用來處理文字比對，但在狀態設計、重複計算、時間複雜度與空間使用上，有明顯的不同。

一、問題定義
給定一段文字 
T
T 與一個要搜尋的模式字串 
P
P，找出 
P
P 在 
T
T 中第一次出現的位置，或找出所有出現的位置。

例如：

文字 
T
T：ABABABCABAB

模式 
P
P：ABABC

答案是從索引 2 開始出現（以 0 為起始索引）。

文字 T

A

B

A

B

A

B

C

A

B

A

B

模式 P

A

B

A

B

C

比對結果：從索引 2 開始，找到模式字串。

定義：

n
=
∣
T
∣
n=∣T∣：文字長度。

m
=
∣
P
∣
m=∣P∣：模式字串長度。

我們要比較兩種方法如何完成這個搜尋任務。

二、方法一：使用動態規劃（DP）
1. 核心原理
動態規劃的主要想法是：將大問題拆成較小的子問題，記錄已經算過的結果，避免重複計算。

在字串搜尋中，我們可以定義一個二維布林表格：

d
p
[
i
]
[
j
]
=
{
true
,
若 
P
[
0
:
j
]
 是 
T
[
0
:
i
]
 的後綴
false
,
否則
dp[i][j]={ 
true,
false,
​
  
若 P[0:j] 是 T[0:i] 的後綴
否則
​
 
這裡的 
i
i 與 
j
j 分別表示已考慮的文字長度與模式長度。換句話說，dp[i][j] 表示模式的前 
j
j 個字元，是否剛好匹配文字前 
i
i 個字元的最後 
j
j 個字元。

狀態轉移如下：

d
p
[
i
]
[
j
]
=
d
p
[
i
−
1
]
[
j
−
1
]
∧
(
T
[
i
−
1
]
=
P
[
j
−
1
]
)
dp[i][j]=dp[i−1][j−1]∧(T[i−1]=P[j−1])
當文字和模式的最後一個字元相同，而且前面的部分已經匹配，整個部分才會匹配。

初始條件為：

d
p
[
i
]
[
0
]
=
true
dp[i][0]=true
因為空字串可以匹配任何位置的空後綴。

當 
d
p
[
i
]
[
m
]
=
true
dp[i][m]=true 時，代表在文字的索引 
i
−
m
i−m 處找到模式字串。

2. 演算法流程
建立大小約為 
(
n
+
1
)
×
(
m
+
1
)
(n+1)×(m+1) 的 DP 表格。

初始化空模式字串的狀態。

逐一比較文字與模式的字元，計算每個狀態。

找出所有滿足 dp[i][m] = true 的位置。

以下為 Python 範例：


python
def search_dp(text, pattern):
    n, m = len(text), len(pattern)

    if m == 0:
        return list(range(n + 1))

    dp = [[False] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, min(i, m) + 1):
            dp[i][j] = (
                dp[i - 1][j - 1]
                and text[i - 1] == pattern[j - 1]
            )

    return [
        i - m
        for i in range(m, n + 1)
        if dp[i][m]
    ]


print(search_dp("ABABABCABAB", "ABABC"))
# [2]
3. 複雜度分析
時間複雜度： 
O
(
n
m
)
O(nm)。最壞情況下，需要計算大量的文字與模式前綴組合。

空間複雜度： 
O
(
n
m
)
O(nm)。需要保存二維 DP 表格。

空間最佳化： 因為每個狀態只依賴前一列，可以將空間降至 
O
(
m
)
O(m)，但必須小心更新順序與保存前一個狀態。

三、方法二：非動態規劃（KMP 演算法）
1. 核心原理
KMP 是一種專門為字串搜尋設計的演算法。它不建立文字與模式的完整二維 DP 表格，而是利用模式字串本身的重複結構，減少不必要的比較。

KMP 的關鍵是 LPS（Longest Proper Prefix which is also Suffix）表，也就是「最長的、不是整個字串的前綴，同時也是後綴」的長度。

例如模式字串：

ABABAC

其 LPS 表如下：

字元

A

B

A

B

A

C

LPS

0

0

1

2

3

0

當比對失敗時，KMP 不會直接把文字指標退回去，而是依據 LPS 表，保留已知可以匹配的前綴資訊。

例如已匹配 ABABA，下一個字元卻不符合時，KMP 可以利用已匹配部分的重複結構，將模式的匹配位置調整到 AB 之後可能接續的位置，而不用重新比較整段文字。

2. 演算法流程
先掃描模式字串，建立 LPS 表。

使用兩個指標，分別掃描文字與模式。

字元相同時，兩個指標一起前進。

字元不同時，根據 LPS 表調整模式指標；不需要重新掃描已經匹配過的文字。

模式全部匹配時，記錄起始索引。

Python 範例：


python
def search_kmp(text, pattern):
    n, m = len(text), len(pattern)

    if m == 0:
        return list(range(n + 1))

    # 建立 LPS 表
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            i += 1

    # 搜尋文字
    result = []
    i = j = 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == m:
                result.append(i - m)
                j = lps[j - 1]
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1

    return result


print(search_kmp("ABABABCABAB", "ABABC"))
# [2]
3. 複雜度分析
時間複雜度： 
O
(
n
+
m
)
O(n+m)。建立 LPS 表需要 
O
(
m
)
O(m)，搜尋文字需要 
O
(
n
)
O(n)。

空間複雜度： 
O
(
m
)
O(m)。只需要保存模式字串的 LPS 表。

主要優勢： 文字指標不需要因為失敗而反覆往回移動，因此可以避免暴力搜尋的重複比較。

嚴格來說，KMP 的 LPS 建構也具有利用先前結果的特性，與動態規劃有相似之處；不過，KMP 通常被分類為利用前綴函數進行字串匹配的專用演算法，而非以 DP 狀態表為核心的演算法。

四、兩種方法比較
比較項目

動態規劃（DP）

KMP（非傳統 DP）

核心思想

建立子問題狀態並保存結果

利用模式字串的前綴與後綴結構

預處理

初始化 DP 表格

建立 LPS 表

時間複雜度

O
(
n
m
)
O(nm)

O
(
n
+
m
)
O(n+m)

空間複雜度

O
(
n
m
)
O(nm)

O
(
m
)
O(m)

重複計算

以儲存狀態避免重複計算

以 LPS 避免重複比對

實作方式

二維表格，概念直觀

需要理解前綴與後綴

適合情境

教學、狀態分析、可擴充的比對問題

大量文字中的精確模式搜尋

五、效能差異範例
假設文字長度 
n
=
1,000,000
n=1,000,000，模式長度 
m
=
100
m=100。

最壞情況的漸進運算量估算

動態規劃

約 1 億個狀態
KMP

約 100 萬級
這是根據漸進複雜度推算的示意，不是實測時間；實際比較次數會依資料內容而異。

在這個例子中，DP 的主要計算量與 
n
m
nm 成正比，而 KMP 的計算量與 
n
+
m
n+m 成正比。當文字非常長時，KMP 通常更有效率。

六、結論
這個問題展示了兩種解題思維的差異：

動態規劃： 將問題拆成子問題，透過狀態轉移保存結果。優點是容易理解、方便擴充；缺點是可能需要較多計算與記憶體。

KMP： 利用特定問題的數學結構，設計更精簡的資訊保存方式。優點是搜尋時間達到線性複雜度，且空間需求較低；缺點是需要理解 LPS 表的建構與更新規則。

因此，若目標是理解動態規劃的基本概念，DP 是不錯的起點；若目標是在大量文字中快速搜尋一個固定模式，KMP 通常更合適。

報告題目建議：「單一模式字串搜尋：動態規劃與 KMP 演算法之原理、複雜度與效能比較」。
