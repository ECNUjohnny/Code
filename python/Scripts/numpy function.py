"""NumPy 进阶练习：30 题（题目与函数骨架，不含解答）。

使用方法：
1. 将函数里的 raise NotImplementedError 替换为自己的实现，可按任意顺序做题。
2. 默认只用 NumPy，不用 pandas / SciPy，不写逐元素 Python 循环；
   不用 np.vectorize 或 np.frompyfunc 绕过限制。题目明确允许的循环除外。
3. 不修改输入数组。除特别说明外，输入满足题目约束，无须额外校验参数。
4. 浮点结果用 np.testing.assert_allclose 检查，整数/索引用 assert_array_equal。
5. 提示只列可探索的函数，不要求全部使用；想增加难度可以先不看提示。
6. 生成随机数据推荐用 rng = np.random.default_rng(42)，避免全局随机状态。

难度：★★★ 熟练运用；★★★★ 多函数组合；★★★★★ 综合挑战。
直接运行本文件不会调用未完成的函数，可在文件底部选择一道题调试。
环境依赖：NumPy >= 1.20（需要 sliding_window_view）。
"""

import numpy as np


# 一、数组构造、形状、广播与索引


def q01_concentric_grid(n):
    """01｜同心方阵 ★★★

    输入：正奇数 n。返回 (n,n) 整数矩阵，元素等于它到中心点的切比雪夫距离，
    即横向距离、纵向距离中的较大值。
    示例：n=5 ->
        [[2,2,2,2,2],
         [2,1,1,1,2],
         [2,1,0,1,2],
         [2,1,1,1,2],
         [2,2,2,2,2]]
    边界：n=1 返回 [[0]]。
    提示：arange / indices / ogrid、abs、maximum、广播。
    加练：用相同坐标生成曼哈顿距离矩阵和欧氏距离矩阵。
    """
    raise NotImplementedError


def q02_block_mean(a, block_shape):
    """02｜二维分块降采样 ★★★

    输入：数值矩阵 a 为 (H,W)，block_shape=(bh,bw)，各维度为正整数；
    H、W 分别能被 bh、bw 整除。返回每个不重叠小块的均值，
    输出形状 (H//bh,W//bw)，保持空间位置一致。
    示例：a=np.arange(24).reshape(4,6)，block_shape=(2,3)，
    返回 [[4.,7.],[16.,19.]]。
    边界：a 可能是转置或切片产生的非连续数组。
    提示：reshape、mean 的 axis 元组，想清楚重排后各个轴的含义。
    加练：返回形状 (H//bh,W//bw,bh,bw) 的分块数组，并探索 shares_memory。
    """
    raise NotImplementedError


def q03_gather_per_row(a, indices):
    """03｜每行选择不同位置 ★★★

    输入：a 为 (N,M)，indices 为 (N,K) 的整数数组，-M <= index < M。
    返回 (N,K) 数组，满足 out[i,j] = a[i,indices[i,j]]，保留重复索引。
    示例：a=[[10,20,30],[40,50,60]]，indices=[[2,0],[-1,1]]，
    返回 [[30,10],[60,50]]。
    提示：take_along_axis、arange、高级索引。
    加练：实现两种写法，并解释为什么 a[:,indices] 不满足要求。
    """
    raise NotImplementedError


def q04_nearest_neighbors(x, k):
    """04｜向量的最近邻 ★★★★

    输入：有限浮点矩阵 x 为 (N,D)，1 <= k < N。
    返回 (indices,distances)，均为 (N,k)，表示每行最近的 k 个其他样本。
    使用欧氏距离，按距离升序；距离完全相同时原始行号小的优先。
    排除自身；不同样本即使坐标相同，仍可以成为距离为 0 的邻居。
    示例：x=[[0.],[2.],[5.]]，k=1 -> 索引 [[1],[0],[1]]，距离 [[2.],[2.],[3.]]。
    提示：广播、sum、sqrt、fill_diagonal、argsort(kind='stable')、take_along_axis。
    加练：通过矩阵乘法避免创建 (N,N,D) 数组，并处理舍入产生的微小负距离平方。
    """
    raise NotImplementedError


def q05_nan_standardize(x):
    """05｜缺失值与常量列的标准化 ★★★★

    输入：(N,D) 浮点矩阵，只含有限值或 NaN，N、D 为正。
    按列忽略 NaN 计算均值和标准差（ddof=0），返回标准化结果，保留原 NaN。
    常量列的非缺失值变成 0；全 NaN 列保持全 NaN。
    示例：[[1.,5.,np.nan],[3.,5.,np.nan]] ->
          [[-1.,0.,np.nan],[1.,0.,np.nan]]。
    要求：空列、除零均不得产生 RuntimeWarning，不能通过关闭警告掩盖问题。
    提示：isnan、sum、divide 的 out/where 参数、keepdims。
    思考：np.where(std == 0, 0, centered / std) 是否真的避免了除零运算？
    """
    raise NotImplementedError


def q06_winsorize(x, low=0.1, high=0.9):
    """06｜按列分位数截尾 ★★★

    输入：(N,D) 浮点矩阵，可含 NaN，每列至少一个有限值、不含无穷；
    0 <= low <= high <= 1。忽略 NaN 按列计算两个分位数，采用默认线性插值。
    低于下界的值替换为下界，高于上界的替换为上界，保留 NaN，返回同形状数组。
    示例：x=[[0.],[10.],[20.],[100.]]，low=.25，high=.75，
    返回 [[7.5],[10.],[20.],[40.]]。
    提示：nanquantile、clip、广播。
    """
    raise NotImplementedError


def q07_stable_topk(x, k):
    """07｜带确定性排序的 Top-K ★★★★

    输入：有限浮点矩阵 x 为 (N,M)，1 <= k <= M。
    返回 (values,indices)，均为 (N,k)。每行取最大的 k 个数，按值降序；
    值完全相同时列号小的优先，包括第 k 名边界上出现重复值的情况。
    示例：x=[[5.,5.,1.,5.]]，k=2 -> values=[[5.,5.]]，indices=[[0,1]]。
    提示：argsort(kind='stable')、lexsort、take_along_axis。
    加练：用 argpartition 减少排序量，同时正确处理第 k 名的并列元素。
    思考：对升序稳定排序结果直接反转，会怎样影响相同值的顺序？
    """
    raise NotImplementedError


# 二、分组、排序、查找与重复索引


def q08_category_encoding(labels):
    """08｜类别编码与还原 ★★★

    输入：一维整数数组或统一字符串类型的数组 labels。
    返回 (classes,codes,counts)：classes 升序且无重复，codes 与输入等长，
    counts 与 classes 等长；classes[codes] 应与 labels 完全一致。
    示例：['cat','dog','cat','bird'] -> classes=['bird','cat','dog']，
    codes=[1,2,1,0]，counts=[1,2,1]。空输入返回三个空数组。
    提示：unique 的 return_inverse / return_counts 参数。
    加练：让 classes 按首次出现顺序排列，同步调整 codes 和 counts。
    """
    raise NotImplementedError


def q09_group_statistics(labels, values):
    """09｜有缺号的分组统计 ★★★★

    输入：等长、非空的一维数组；labels 为非负整数，values 为有限浮点数。
    设 G=labels.max()+1，返回长度均为 G 的 (counts,sums,means)。
    位置 g 对应类别 g；未出现的类别 count=0、sum=0、mean=NaN，不得产生除零警告。
    示例：labels=[2,0,2]，values=[1.,4.,5.] ->
    counts=[1,0,2]，sums=[4.,0.,6.]，means=[4.,np.nan,3.]。
    提示：bincount、divide(out=...,where=...)、full。
    """
    raise NotImplementedError


def q10_scatter_add(shape, rows, cols, values):
    """10｜重复坐标累加 ★★★★

    输入：正整数二维 shape，以及等长的一维 rows、cols、values；
    坐标均非负、不越界，values 为有限浮点数。
    返回从全零开始、将每个 value 累加至对应坐标的矩阵，重复坐标必须累加。
    示例：shape=(2,3)，rows=[0,0,1]，cols=[1,1,2]，values=[2.,3.,4.]，
    返回 [[0.,5.,0.],[0.,0.,4.]]。空坐标返回全零矩阵。
    提示：add.at；也可探索 ravel_multi_index 和 bincount。
    思考：为什么 out[rows,cols] += values 在重复坐标处可能得不到正确结果？
    """
    raise NotImplementedError


def q11_run_length_encode(x):
    """11｜游程编码 ★★★★

    输入：一维整数数组 x。返回 (values,lengths,starts)，分别表示每个
    连续相同值片段的值、长度和起始索引，保持原始顺序。
    示例：[3,3,3,1,1,3] -> ([3,1,3],[3,2,1],[0,3,5])。
    相同值被其他值隔开时属于不同片段；空输入返回三个空数组。
    提示：diff、flatnonzero、concatenate、repeat。
    加练：实现解码，验证 repeat(values,lengths) 可以还原原始数组。
    """
    raise NotImplementedError


def q12_sorted_group_reduce(group_ids, values):
    """12｜有序数据的分段归约 ★★★★

    输入：等长、非空的一维数组；group_ids 是非递减整数，可为负数、可缺号，
    values 为有限浮点数。返回 (groups,sums,counts,means)，
    groups 只包含出现过的组且升序，其他结果与它一一对应。
    示例：group_ids=[-2,-2,7,7,7]，values=[1.,3.,2.,4.,6.]，
    返回 ([-2,7],[4.,12.],[2,3],[2.,4.])。
    要求：求和必须使用 ufunc.reduceat，不创建按最大组号分配的大数组。
    提示：diff、flatnonzero、add.reduceat。
    """
    raise NotImplementedError


def q13_inner_join(left, right):
    """13｜包含重复键的内连接 ★★★★★

    输入：两个一维整数数组 left、right，可无序、可重复、可为空。
    返回 (left_indices,right_indices)，列出所有满足 left[i] == right[j]
    的索引对；相同键重复时保留全部配对，按 i 升序、再按 j 升序排列。
    示例：left=[2,1,2]，right=[2,2,3] -> ([0,0,2,2],[0,1,0,1])。
    无匹配返回两个空整数数组；禁止构造 (len(left),len(right)) 的比较矩阵。
    提示：稳定 argsort、searchsorted(side='left'/'right')、repeat、cumsum、arange。
    思考：如何从每个左侧元素的匹配数量，生成展开后的分段内偏移？
    """
    raise NotImplementedError


def q14_bin_assignment(x, edges):
    """14｜分箱与区间端点 ★★★★

    输入：有限浮点一维数组 x，edges 为至少两个严格递增的有限边界。
    返回 (bin_ids,counts)，bin_ids 与 x 等长，counts 长度为 len(edges)-1。
    第 i 箱为 [edges[i],edges[i+1])，最后一箱包含最右端点。
    超出整个边界范围的值标记为 -1，不计入 counts。
    示例：x=[-1.,0.,1.,2.,3.,4.]，edges=[0.,1.,3.] ->
    ([-1,0,1,1,1,-1],[1,3])。空 x 返回空 bin_ids 和全零 counts。
    要求：不用 histogram 生成答案，可用它验证 counts。
    提示：searchsorted / digitize、where、bincount。
    """
    raise NotImplementedError


def q15_linear_interpolation(xp, fp, x):
    """15｜手写向量化线性插值 ★★★★

    输入：xp 为至少两个严格递增的有限浮点坐标，fp 为等长有限浮点值；
    x 为任意形状的有限浮点查询数组。返回与 x 同形状的插值结果。
    区间内分段线性插值；小于 xp[0] 返回 fp[0]，大于 xp[-1] 返回 fp[-1]。
    示例：xp=[0.,2.,5.]，fp=[0.,4.,1.]，x=[-1.,1.,3.,8.] -> [0.,2.,3.,1.]。
    要求：不调用 interp 生成答案，但可用 np.interp 对照验证。
    提示：searchsorted、clip、索引、广播。注意查询点恰好等于端点的情况。
    """
    raise NotImplementedError


def q16_unique_rows_first_seen(a):
    """16｜按首次出现顺序去重行 ★★★★

    输入：(N,D) 整数矩阵 a，N、D 均为正。
    返回 (rows,inverse,counts)，rows 为按首次出现顺序排列的去重行，
    满足 rows[inverse] 与 a 一致，counts 与 rows 的顺序一致。
    示例：a=[[2,1],[1,2],[2,1],[3,0]] ->
    rows=[[2,1],[1,2],[3,0]]，inverse=[0,1,0,2]，counts=[2,1,1]。
    提示：unique(axis=0,return_index=True,return_inverse=True,return_counts=True)、argsort。
    思考：重排 unique 的输出后，如何构造“旧编码到新编码”的映射？
    """
    raise NotImplementedError


# 三、滑动窗口、图像运算与时间


def q17_rolling_nanmean(x, window, min_count=1):
    """17｜带有效数量门槛的滑动均值 ★★★★

    输入：长度 N 的浮点数组，只含有限值或 NaN；
    1 <= window <= N，1 <= min_count <= window。
    只输出完整窗口，结果长度 N-window+1。窗口内忽略 NaN 求均值，
    有效值少于 min_count 时返回 NaN，不得产生空切片或除零警告。
    示例：x=[1.,np.nan,3.,5.]，window=2，min_count=1 -> [1.,3.,4.]；
    min_count=2 -> [np.nan,np.nan,4.]。
    提示：lib.stride_tricks.sliding_window_view、isnan、sum、divide。
    加练：用 cumsum 实现 O(N) 算法，比较耗时和中间数组大小。
    """
    raise NotImplementedError


def q18_time_bins(timestamps, values, minutes=15):
    """18｜时间序列补齐空时间桶 ★★★★

    输入：非空一维 datetime64[m] 数组 timestamps，无 NaT，可无序；
    values 为等长有限浮点数，minutes 为正整数。
    以最早时间所在日期的 00:00 为起点，每 minutes 分钟划一桶，左闭右开。
    返回 (starts,counts,sums)：从起点到包含最后一个事件的桶，连续返回所有桶；
    空桶 count=0、sum=0，starts 记录每桶起始时间。
    示例：时间 ['2026-01-01T00:02','2026-01-01T00:31']，值 [2.,5.]，
    minutes=15 -> 起点为当天 [00:00,00:15,00:30]，counts=[1,0,1]，sums=[2.,0.,5.]。
    恰在桶边界的事件进入新桶；支持跨天，不考虑时区与夏令时。
    提示：astype('datetime64[D]')、timedelta64、整数除法、arange、bincount。
    """
    raise NotImplementedError


def q19_convolve2d_valid(image, kernel):
    """19｜二维有效卷积 ★★★★

    输入：有限浮点矩阵 image 为 (H,W)，kernel 为 (kh,kw)，
    1 <= kh <= H、1 <= kw <= W。返回 (H-kh+1,W-kw+1) 的卷积结果。
    本题卷积定义：每个窗口与“上下、左右同时翻转后的 kernel”对应相乘再求和。
    示例：image=[[1.,2.,3.],[4.,5.,6.],[7.,8.,9.]]，
    kernel=[[1.,0.],[0.,-1.]] -> [[4.,4.],[4.,4.]]。
    要求：不用 SciPy，不展开成 Python 窗口列表。
    提示：sliding_window_view、flip、einsum / tensordot。
    加练：支持 stride；再明确偶数核的补边规则，实现 same 模式。
    """
    raise NotImplementedError


def q20_rectangle_sums(image, rectangles):
    """20｜积分图批量查询矩形和 ★★★★

    输入：有限浮点矩阵 image 为 (H,W)，整数矩阵 rectangles 为 (Q,4)，
    每行 (top,left,bottom,right) 表示 image[top:bottom,left:right]。
    坐标满足 0 <= top <= bottom <= H，0 <= left <= right <= W。
    返回长度 Q 的矩形元素和，零面积矩形和为 0，空查询返回空数组。
    示例：image=np.arange(1,10).reshape(3,3)，
    rectangles=[[0,0,2,2],[1,1,3,3],[0,1,0,3]] -> [12.,28.,0.]。
    要求：O(HW) 建积分图，再 O(Q) 查询，不逐个切片求和。
    提示：cumsum、pad、高级索引。
    """
    raise NotImplementedError


def q21_binary_morphology(mask):
    """21｜二值图像的膨胀与腐蚀 ★★★★

    输入：(H,W) 布尔矩阵，H、W 均为正。返回同形状布尔数组 (dilated,eroded)。
    邻域为以当前像素为中心、含中心的 3×3 方形，图像之外一律视为 False。
    膨胀：邻域至少一个 True 即为 True；腐蚀：邻域全部 True 才为 True。
    示例：3×3 中仅中心为 True，膨胀结果全 True，腐蚀结果全 False；
    3×3 全 True 时，腐蚀结果只有中心为 True。
    提示：pad、sliding_window_view、any、all。
    加练：组合两种操作实现开运算和闭运算，观察边界补值的影响。
    """
    raise NotImplementedError


# 四、线性代数、随机采样与综合题


def q22_cosine_similarity(x, y):
    """22｜安全计算余弦相似度矩阵 ★★★★

    输入：有限浮点矩阵 x 为 (N,D)，y 为 (M,D)。
    返回 (N,M) 的余弦相似度矩阵，任一向量为零向量时该位置定义为 0。
    不得产生除零警告；不创建 (N,M,D) 中间数组；最终结果裁剪至 [-1,1]。
    示例：x=[[1.,0.],[0.,0.]]，y=[[1.,0.],[-1.,0.],[0.,1.]]，
    返回 [[1.,-1.,0.],[0.,0.,0.]]。
    提示：matmul / @、linalg.norm、divide(out=...,where=...)、clip。
    """
    raise NotImplementedError


def q23_batched_ridge(x, y, alpha):
    """23｜带截距的批量岭回归 ★★★★★

    输入：有限浮点数组 x 为 (B,N,D)，y 为 (B,N)，alpha>0，各维度为正。
    每批次独立最小化 sum((X @ w + b - y)**2) + alpha * sum(w**2)，截距 b 不受惩罚。
    返回 (weights,intercepts)，形状分别为 (B,D)、(B,)。
    要求：批量求解，不循环批次、不显式求逆；特征可线性相关。
    自测：x 全零、y 每批次为常数时，weights 接近零，intercepts 接近对应常数。
    提示：concatenate、swapaxes、matmul、eye、linalg.solve。
    注意：新版 solve 的批量单列右端可显式组织为 (B,D+1,1)，再移除末轴。
    加练：实现先中心化再求解的版本，与添加常数特征列的版本比较。
    """
    raise NotImplementedError


def q24_whiten(x):
    """24｜通过特征分解白化数据 ★★★★★

    输入：有限浮点矩阵 x 为 (N,D)，N>D，样本协方差正定且所有特征值 > 1e-10。
    返回 (z,mean,transform)，形状分别为 (N,D)、(D,)、(D,D)。
    transform 必须对称，z=(x-mean) @ transform；z 列均值接近 0，
    样本协方差（ddof=1）接近单位阵。
    要求：使用协方差的特征分解，不能以逐列标准化代替白化。
    自测：生成相关特征，用 np.cov(z,rowvar=False) 与 np.eye(D) 比较。
    提示：mean、matmul、linalg.eigh、diag；特征值对应特征向量的列。
    加练：协方差半正定或病态时如何处理？处理后还能否达到单位协方差？
    """
    raise NotImplementedError


def q25_pca(x, k):
    """25｜SVD 实现 PCA ★★★★★

    输入：有限浮点矩阵 x 为 (N,D)，N>=2，中心化后总方差大于 0，
    1 <= k <= min(N-1,D)。返回 (scores,components,explained_ratio)，
    形状分别为 (N,k)、(k,D)、(k,)，按主成分方差从大到小排列。
    scores=(x-x.mean(axis=0)) @ components.T。
    explained_ratio 的分母是全部主成分的总方差，而非仅前 k 个的方差之和。
    符号约定：每个主成分中绝对值最大的载荷须非负，并列时用最小列号决定符号。
    不要求重合奇异值对应的基在不同平台上完全一致。
    要求：使用 linalg.svd(full_matrices=False)，不用机器学习库。
    自测：components @ components.T 接近单位阵，重建误差随 k 增大不应增大。
    提示：argmax、take_along_axis、广播、sum。
    """
    raise NotImplementedError


def q26_fft_convolve(a, b):
    """26｜FFT 实现一维线性卷积 ★★★★★

    输入：两个非空一维有限实数数组 a、b，长度分别为 N、M。
    返回长度 N+M-1 的完整线性卷积，结果为实数数组。
    示例：a=[1.,2.,3.]，b=[2.,-1.] -> [2.,3.,4.,-3.]。
    要求：核心使用 fft.rfft / fft.irfft，不调用 convolve 生成答案；
    正确补零和截取，避免把循环卷积当作线性卷积。
    自测：用 np.convolve(a,b,mode='full') 比较，包含输出长度为奇数的情况。
    提示：变换长度至少 N+M-1；irfft 应显式传入所用变换长度。
    加练：取不小于所需长度的最小 2 的幂，比较不同规模下的耗时。
    """
    raise NotImplementedError


def q27_stratified_sample(labels, per_group, seed=42):
    """27｜可复现的分层不放回采样 ★★★★

    输入：非空一维整数类别 labels、正整数 per_group，每类样本数均不少于 per_group。
    每类随机抽取 per_group 个原始行号，返回一维整数索引数组；
    按类别值升序拼接，组内保留 rng.choice 的抽样顺序。
    相同 NumPy 环境中，相同输入和 seed 应得到相同结果，不能修改全局随机状态。
    本题允许遍历不同类别，不允许逐样本循环；不能在每个类别重新设置随机种子。
    自测：索引无重复，每组数量正确，同种子结果相同；不同种子可能偶然得到同一结果。
    提示：random.default_rng、unique、flatnonzero、Generator.choice(replace=False)。
    加练：用随机键与 lexsort 去掉组循环，只需满足相同采样分布及可复现性。
    """
    raise NotImplementedError


def q28_missing_pairwise_distance(x):
    """28｜缺失值感知的成对距离 ★★★★★

    输入：(N,D) 浮点矩阵，只含有限值或 NaN，各维度为正。
    每对行只比较双方都非 NaN 的特征，距离定义为这些特征的
    “差值平方的均值再开平方”。没有共同有效特征时为 np.inf。
    返回 (N,N) 矩阵；全 NaN 行到自身的距离也为 inf。
    示例：x=[[1.,np.nan,3.],[2.,4.,np.nan],[np.nan,np.nan,np.nan]] ->
    [[0.,1.,np.inf],[1.,0.,np.inf],[np.inf,np.inf,np.inf]]。
    要求：不分配 (N,N,D) 数组、不逐行循环；允许 (N,D)、(N,N) 中间结果。
    提示：isnan、where、astype、matmul、maximum、divide、sqrt。
    思考：如何用矩阵乘法求共同有效数量、平方项之和、交叉项？
    注意：布尔矩阵乘法不是整数计数；处理浮点舍入产生的微小负数。
    """
    raise NotImplementedError


def q29_classification_metrics(y_true, y_pred, n_classes):
    """29｜混淆矩阵与分类指标 ★★★★

    输入：等长一维整数标签 y_true、y_pred，可为空；C=n_classes 为正整数，
    标签范围 [0,C)。返回 (cm,precision,recall,f1,macro_f1)。
    cm 为整数矩阵，行是真实类别、列是预测类别；逐类指标为长度 C 的浮点数组。
    precision=TP/(TP+FP)，recall=TP/(TP+FN)，f1=2*precision*recall/(precision+recall)。
    分母为 0 时指标定义为 0；macro_f1 对全部 C 类平均，包括未出现的类别。
    示例：y_true=[0,1,1,2]，y_pred=[0,0,1,1]，C=3 ->
    cm=[[1,0,0],[1,1,0],[0,1,0]]，f1=[2/3,1/2,0]，macro_f1=7/18。
    要求：不循环类别、不产生除零警告。
    提示：bincount(minlength=...)、reshape、diagonal、sum(axis=...)、divide。
    """
    raise NotImplementedError


def q30_kmeans_step(x, centers):
    """30｜K-Means 的一次完整迭代 ★★★★★

    输入：有限浮点矩阵 x 为 (N,D)，旧中心 centers 为 (K,D)，各维度为正。
    返回 (labels,new_centers,inertia)：
    - labels：长度 N，按到旧中心的欧氏距离分组，并列时选择最小中心编号。
    - new_centers：(K,D)，每组样本均值；空组保留该组旧中心。
    - inertia：所有样本到所分配新中心的距离平方之和，使用本轮 labels，
      计算该值时不再次重新分配 labels。
    示例：x=[[0.],[2.],[10.]]，centers=[[0.],[10.],[100.]] ->
    labels=[0,0,1]，new_centers=[[1.],[10.],[100.]]，inertia=2.。
    要求：不逐样本或逐簇循环，不修改 centers，正确处理空簇。
    提示：广播 / matmul、argmin、add.at、bincount、divide、sum。
    加练：允许使用迭代循环完成完整 K-Means，设置最大迭代次数、收敛阈值和随机初始化，
    比较不同初始中心对最终目标值的影响。
    """
    raise NotImplementedError


if __name__ == "__main__":
    # 在这里选择一道已经实现的题进行调试，例如：
    # print(q01_concentric_grid(5))
    # np.testing.assert_array_equal(q01_concentric_grid(1), [[0]])
    pass


