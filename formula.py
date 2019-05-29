import numpy as np
import pandas as pd
# Monthly return amount


def monthlyReturnAmount(principal, months, monthlyRate):  # 投资金额、期数、月利率
    return(principal * monthlyRate * (1 + monthlyRate)**months / ((1 + monthlyRate)**months - 1))
# monthly Return Principal


def monthlyReturnPrincipal(principal, months, monthlyRate):  # 投资金额、期数、月利率
    monthsPrincipal = np.zeros((months))
    for month in range(months):
        monthsPrincipal[month] = monthlyReturnAmount(principal, month, monthlyRate)
    return(monthsPrincipal)


# 年利率、借款期数（月）、初始资金（元）、投资总周期（月）、坏账率
def annualIncome(annualYield, months, principal, T, BadDebtRate):
    monthlyRate = annualYield / 12
    # 每月可投总金额 （第i个月，第j笔还款）
    monthlyAmount = np.zeros((months, months))
    # 每月返还本金
    monthlyPrincipal = np.zeros((months, months))
    # 每月返还利息
    monthlyInterest = np.zeros((months, months))

    monthlyAmount[0,0] = principal
    # 当月现金流数据：月本金、回收金额、回收本金、回收利息、损失本金、净利润、月利率、平均年化利率
    cashFlow = pd.DataFrame(np.zeros((T + 1, 8)), columns=["月本金", "回收金额", "回收本金", "回收利息", "损失本金", "净利润", "月利率", "平均年化利率"])
    cashFlow[0, "月本金"] = principal
    for t in range(T + 1):
        cashFlow[t, "回收金额"] = sum(monthlyAmount[t,:])
        cashFlow[t, "回收本金"] = sum(monthlyPrincipal[t,:])
        cashFlow[t, "回收利息"] = sum(monthlyInterest[t,:])
        cashFlow[t, "损失本金"] = sum(monthlyPrincipal[t,:]) * BadDebtRate / (1 - BadDebtRate)
        cashFlow[t, "净利润"] = cashFlow[t, "回收利息"] - cashFlow[t, "损失本金"]
        if t == 0:
            cashFlow[t, "月利率"] = cashFlow[t, "净利润"] / cashFlow[t, "月本金"] * 100
        if t != 0:
            cashFlow[t, "月利率"] = cashFlow[t, "净利润"] / cashFlow[t - 1, "月本金"] * 100
            # 当月本金=上月本金+本月投标金额－本月应收回收本金
            cashFlow[t, "月本金"] = cashFlow[t - 1, "月本金"] + cashFlow[t, "回收金额"] - cashFlow[t, "回收本金"] / (1 - BadDebtRate)
            cashFlow[t, "平均年化利率"] = (((cashFlow[t, "净利润"] + principal) / principal)**(12 / t) - 1) * 100
        
        #计算各月回款写入返回矩阵
        monthlyAmount[0,:] = np.ones(months) * monthlyReturnAmount(cashFlow[t, "回收本金"], months, monthlyRate) * (1 - BadDebtRate)

        # 累计收益金额
        print(str(int(cashFlow["净利润"].sum() * 1e4) / 1e4))
        # 平均年化收益率
        try:
            print(str(int(cashFlow[t, "平均年化利率"] * 1e4) / 1e4))
        except:
            print('0.0')
