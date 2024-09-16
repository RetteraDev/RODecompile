#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\data/formula_client_data.o
data = {10001: {'formula': lambda d: int((d['lv'] + 2.2) ** 1.45 / 2.0),
         'funName': 'flv'},
 10013: {'formula': lambda d: d['p1'] * d['itemLv'],
         'funName': 'flvqEp'},
 10014: {'formula': lambda d: (0.05 * (d['itemLv'] + 2.2) ** 1.45 * d['itemLv'] + 5) * d['p1'] * 150 * (min(0.5 * max(d['itemLv'] - 69, 0) ** 2 - 0.5 * max(d['itemLv'] - 69, 0) + 1, 22) + 3 * max(d['itemLv'] - 76, 0)),
         'funName': 'fstarlv'},
 10015: {'formula': lambda d: d['itemLv'] * (0.1 * (d['itemLv'] + 2.2) ** 1.45) + d['totalStarExp'] * min(max(d['quality'] - d['p2'] + 3, 0) * 0.3333, 1),
         'funName': 'fstarexp'},
 10017: {'formula': lambda d: max(min(d['p1'] / max(d['prob'], 1) - d['p2'], d['p3']), 0),
         'funName': 'enhanceProb'},
 10018: {'formula': lambda d: 1 + int(0.3333 * (d['maxStarLv'] + 1 + max(0, d['maxStarLv'] - 2) * 6 + +max(0, d['maxStarLv'] - 3) * 13) * d['p1']),
         'funName': 'starInactiveCost'},
 10020: {'formula': lambda d: max(1, int((d['itemLv'] - 5) * 0.1 + d['quality'] - 8) * d['p1']),
         'funName': 'starLvupCost'},
 10021: {'formula': lambda d: d['p1'] * d['enhanceLv'] + d['p2'] * d['enhanceRefining'] * d['orderFactor'] * 100,
         'funName': 'enhanceScore'},
 10022: {'formula': lambda d: int(d['itemLv'] * 10 * d['quality'] * d['p1']),
         'funName': 'equipFineRepairCost'},
 10023: {'formula': lambda d: (d['yangSlotsCnt'] + 1 + max(d['yangSlotsCnt'] - 1, 0)) * d['p1'],
         'funName': 'yangInactiveCost'},
 10024: {'formula': lambda d: (d['yinSlotsCnt'] + 1 + max(d['yinSlotsCnt'] - 1, 0)) * d['p1'],
         'funName': 'yinInactiveCost'},
 10025: {'formula': lambda d: d['p1'] * d['val'],
         'funName': 'juexingScore'},
 10026: {'formula': lambda d: d['p1'] * d['itemLv'] * d['starFactor'] * d['qualityFactor'],
         'funName': 'randPropFixScore'},
 10028: {'formula': lambda d: 50 * d['lv'] + 200 * d['quality'],
         'funName': 'yaoPeiTransferCost'},
 10029: {'formula': lambda d: (int(max(d['oldNum'] + d['delta'] - d['freeNum'], 0) / 10) + 1) * 1000 * (max(d['oldNum'] + d['delta'] - d['freeNum'], 0) - 5 * int(max(d['oldNum'] + d['delta'] - d['freeNum'], 0) / 10)) - (int(max(d['oldNum'] - d['freeNum'], 0) / 10) + 1) * 1000 * (max(d['oldNum'] - d['freeNum'], 0) - 5 * int(max(d['oldNum'] - d['freeNum'], 0) / 10)),
         'funName': 'yaoPeiExpCostFormula'},
 10030: {'formula': lambda d: d['p1'] * 2 ** (d['order'] - 10),
         'funName': 'unbindCost'},
 30002: {'formula': lambda d: d['p1'],
         'funName': 'fself'},
 30003: {'formula': lambda d: int((d['p1'] * d['lv'] + d['p2'] * max(d['lv'] - 9, 0) + d['p3'] * max(d['lv'] - 28, 0) + d['p4'] * max(d['lv'] - 38, 0) + d['p5'] * max(d['lv'] - 48, 0)) * d['p6']),
         'funName': 'fzhanli'},
 40001: {'formula': lambda d: d['p1'] * (d['lv'] + 5),
         'funName': 'flvhp'},
 40002: {'formula': lambda d: (d['lv'] < 80) * d['p1'] * int(1.0 * (d['lv'] - 1) / d['p2'] + 1) * min(int(d['lv'] / 21), 1) + (d['lv'] >= 80) * 96,
         'funName': 'fpoint'},
 40003: {'formula': lambda d: d['p1'] * (1 - min(int(d['lv'] / 21), 1)),
         'funName': 'fpb'},
 40004: {'formula': lambda d: (d['lv'] < 300) * d['p1'] * int(d['lv'] / d['p2'] + 1) + (d['lv'] >= 300) * d['p1'] * int(d['lv'] / d['p2'] + 20),
         'funName': 'fpc'},
 40005: {'formula': lambda d: 25 * d['p1'] * (d['lv'] + 5),
         'funName': 'flvmp'},
 40006: {'formula': lambda d: (d['lv'] < 80) * d['p1'] * d['lv'] + (d['lv'] >= 80) * (2 * (d['lv'] - 79) + d['p1'] * 79),
         'funName': 'fBase'},
 40007: {'formula': lambda d: 0.5,
         'funName': 'fBasePvp'},
 40008: {'formula': lambda d: int(4 * (d['lv'] + d['p1']) / 3) - d['p1'],
         'funName': 'fBasePlayer'},
 40009: {'formula': lambda d: 10 * int(0.5 * ((1 + (d['point'] + 6) * 4 / 15.0 * d['p1']) ** 0.5 - 1)) + int(round((d['point'] + 6) * d['p1'] / 3.0 / (int(0.5 * ((1 + (d['point'] + 6) * d['p1'] * 4 / 15.0) ** 0.5 - 1)) + 1) - 5 * int(0.5 * ((1 + (d['point'] + 6) * d['p1'] * 4 / 15.0) ** 0.5 - 1)) + 0.49)),
         'funName': 'fAddPoint'},
 40010: {'formula': lambda d: d['p1'] * (d['lv'] + 5),
         'funName': 'fBasePve'},
 40012: {'formula': lambda d: 10 + d['p1'] * d['lv'],
         'funName': 'fBaseyt'},
 50001: {'formula': lambda d: d['p1'] * (d['skLv'] + max(d['skLv'] - 4, 0) + max(d['skLv'] - 9, 0) + max(d['skLv'] - 14, 0) + max(d['skLv'] - 19, 0)),
         'funName': 'fskillpt'},
 50002: {'formula': lambda d: d['p1'] * d['skLv'],
         'funName': 'fskillws'},
 50005: {'formula': lambda d: 270 * d['skillEnhPoint'],
         'funName': 'skillEnhanceScore'},
 90003: {'formula': lambda d: min(10 * max(1, min(10, d['n'] - 9)) * max(1, min(10, d['n'] - 19)) * max(1, d['n'] - 29) + 20 * d['c'], 99999),
         'funName': 'mailfee'},
 90005: {'formula': lambda d: 100,
         'funName': 'jobCashNeed'},
 90006: {'formula': lambda d: 1 + (d['lastJobNum'] - d['lastJobAccNum']) / d['lastJobNum'] * 0.25 - d['accAll'] * (max(0.4 - d['tJobAll'], 0) / 0.4 * 0.15 + (1 - d['tJobAll']) * 0.1 + min(max(3 - d['tJobAll'] / max(d['tJobHalf'], 0.0001), 0), 1) * max(d['tJobAll'] - 0.7, 0) / 0.3 * 0.15),
         'funName': 'jobBonus'},
 90007: {'formula': lambda d: 1 + (d['accAll'] - 1) * (d['lastJobNum'] - d['lastJobAccNum']) / d['lastJobNum'] * 0.25 + d['accAll'] * (max(0.4 - d['tJobAll'], 0) / 0.4 * 0.15 + (1 - d['tJobAll']) * 0.1 - min(max(3 - d['tJobAll'] / max(d['tJobHalf'], 0.0001), 0), 1) * max(d['tJobAll'] - 0.7, 0) / 0.3 * 0.2),
         'funName': 'jobNum'},
 90011: {'formula': lambda d: d['vp'] / 5.0,
         'funName': 'quickVp'},
 90016: {'formula': lambda d: d['mlLv'] - 10,
         'funName': 'guideThresholdLvF'},
 90017: {'formula': lambda d: d['mlLv'] - 11,
         'funName': 'guideLowLvF'},
 90018: {'formula': lambda d: int((min(max(0, 61 - d['lv']), 1) * (66.3 * d['lv'] - 1263) + min(max(0, d['lv'] - 60), 1) * (125 * d['lv'] - 4785)) / 10.0) * 10,
         'funName': 'freeVp'},
 90019: {'formula': lambda d: int((max((d['x'] + d['m'] - d['c']) * 5, 0) + max((d['x'] + d['m'] - 2 * d['c']) * 1, 0) + max((d['x'] + d['m'] - 3 * d['c']) * 2, 0) + max((d['x'] + d['m'] - 4 * d['c']) * 3, 0) - max((d['x'] - d['c']) * 5, 0) - max((d['x'] - 2 * d['c']) * 1, 0) - max((d['x'] - 3 * d['c']) * 2, 0) - max((d['x'] - 4 * d['c']) * 3, 0)) / 50.0),
         'funName': 'costVp'},
 90020: {'formula': lambda d: min(d['lostTime'] / 86400 / 2, 30),
         'funName': 'fBackflowExpireTime'},
 90021: {'formula': lambda d: (int((min(d['lv'], d['plv'] + min(max(int((d['lv'] - d['plv']) / 2), 0), 5)) + 2.2) ** 1.45 * min(d['lv'], d['plv'] + min(max(int((d['lv'] - d['plv']) / 2), 0), 5)) * 0.05) + 5) * int(6 / 3.0) * 1.1 * 1.635,
         'funName': 'monsterExp'},
 90023: {'formula': lambda d: (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 5 * 60 * 5,
         'funName': 'xiuweiPool'},
 90025: {'formula': lambda d: (d['lv'] * 0.01 - 0.01 + 0.01 * min(d['lv'] - 3, 2)) * min(max(d['lv'] - 2, 0), 1),
         'funName': 'friendFame'},
 90029: {'formula': lambda d: int(min((d['lv'] + 2.2) ** 1.45 / 2.0, 150) * max(30, min(0.5 * d['lv'], 0.2 * d['lv'] + 18) + min(0.5 * d['lv'], 27)) * 0.1 + 5) * 1.25 * 3 * (1.8 + d['progress'] * 0.7 + int(d['progress'] / 6)),
         'funName': 'kjXiuWeiExp'},
 90030: {'formula': lambda d: 800 * (d['progress'] * 1 + int(d['progress'] / 10)),
         'funName': 'kjYunBiReward'},
 90055: {'formula': lambda d: max(int(d['exp'] / d['per'] + 0.2), 1),
         'funName': 'xiuPerMax'},
 90056: {'formula': lambda d: int(((int(d['lv'] * 0.1) * 10 + 11.2) ** 1.45 * (int(d['lv'] * 0.1) * 10 + 9) * 0.05 + 5) * 5 * 30 * 0.0001) * 10000,
         'funName': 'xiuweiPerNum'},
 90057: {'formula': lambda d: int(d['p1'] + d['lv'] * d['p2']),
         'funName': 'hjzcFun_I'},
 90058: {'formula': lambda d: d['p1'] + d['lv'] * d['p2'],
         'funName': 'hjzcFun_F'},
 90059: {'formula': lambda d: (1000 + 20 * d['lv']) * 2.1,
         'funName': 'hjzcFun_m_hp'},
 90060: {'formula': lambda d: (50 + d['lv']) * 2.1,
         'funName': 'hjzcFun_m_atk'},
 90061: {'formula': lambda d: d['lv'] * 4 * 2.1,
         'funName': 'hjzcFun_m_PhyDef'},
 90062: {'formula': lambda d: d['lv'] * 4 * 2.1,
         'funName': 'hjzcFun_m_MagDef'},
 90065: {'formula': lambda d: (int((d['n0'] - d['n1'] - 10 * d['n2']) * (1 - d['e'] ** (-(0.346 * d['n0'] - 1550.0) / d['n0'])) / 10.0) if d['n0'] > d['n1'] + 10 * d['n2'] else 0),
         'funName': 'pvpLevelChaseFun'},
 90066: {'formula': lambda d: (int((d['n0'] - d['n1'] - 15000) * (1 - d['e'] ** (-(d['n0'] * 0.198 + 26429.0) / d['n0'])) / 100.0) if d['n0'] > d['n1'] + 15000 else 0),
         'funName': 'amuletLevelChaseFun'},
 90067: {'formula': lambda d: (3 * d['lv'] - 2 if d['timePass'] < 2100 else (3 * d['lv'] - 2) * (1 + 0.02 * (d['timePass'] / 60 - 35))),
         'funName': 'hjzcFun_ReliveTime'},
 90068: {'formula': lambda d: min(d['attrAgi'] * (d['growthRatio'] * 0.000962306610407876 + d['aptitudeAgi'] * 1.04098101265823e-06), 1.5),
         'funName': 'spriteAttackMinusRatio'},
 90069: {'formula': lambda d: d['p1'] + d['lv'] * d['p2'],
         'funName': 'hjzcFun_F_normal'},
 90070: {'formula': lambda d: (d['growthRatio'] * 33.355231463233 + d['aptitudePhy'] * 0.0187623176980686) * (d['attrPhy'] + 2.3 * d['lv'] * (1 + d['baseMhpEnhRatio'])) * (1 + 0.00819327731092437 * d['lv']) * (1 + 0.0025 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': 'spriteMhp'},
 90071: {'formula': lambda d: 1.111 * (((1.0 * ((d['p12010'] + d['p12011']) / 2 * (1 + 0.01 * d['p12014']) + d['p12020'] + d['p17001'] + d['p17002'] + d['p17003'] + d['p17004'] + d['p17005'] + d['p17006'] + d['p17007']) * (min(1, 0.9 + 1.42857 * d['p12018'] / 74 / (d['lv'] + 5) + d['p12019']) + (d['p12016'] / (37.5 * (d['lv'] + 5)) + d['p12024']) * (d['p12017'] + d['p12040'] / (12.5 * (d['lv'] + 5)))) * (1 + d['p12025']) * (35 * (d['lv'] + 5) + 0.2 * d['lv'] ** 2) / max((35 - 25 * d['p12123']) * (d['lv'] + 5) + 0.2 * (1 - d['p12123']) * d['lv'] ** 2 - 0.7 * d['p12033'], 10 * (d['lv'] + 5)) * (1 + 0.5 * d['p16002'] / (37 * (d['lv'] + 5))) * (1 + 1.0 * d['p16004'] / (37 * (d['lv'] + 5))) * (1 + d['p16008']) * (1 + 0.33 * d['p12041'] / (25 * (d['lv'] + 5)) + 0.33 * d['p12042']) * (1 + d['p16009'] + 0.05 * d['p16010'] / (5 + d['lv'])) + 255.3) / 0.23) ** 0.5 + 6.7) ** 2 - 1678,
         'funName': 'atkScoreFormula1'},
 90072: {'formula': lambda d: 1.111 * (((1.0 * ((d['p12012'] + d['p12013']) / 2 * (1 + 0.01 * d['p12015']) + d['p17001'] + d['p17002'] + d['p17003'] + d['p17004']) * (min(1, 0.9 + 1.42857 * d['p12018'] / 74 / (d['lv'] + 5) + d['p12019']) + (d['p12016'] / (37.5 * (d['lv'] + 5)) + d['p12024']) * (d['p12017'] + d['p12040'] / (12.5 * (d['lv'] + 5)))) * (1 + d['p12026']) * (35 * (d['lv'] + 5) + 0.2 * d['lv'] ** 2) / max((35 - 25 * d['p12124']) * (d['lv'] + 5) + 0.2 * (1 - d['p12124']) * d['lv'] ** 2 - 0.7 * d['p12034'], 10 * (d['lv'] + 5)) * (1 + 0.5 * d['p16002'] / (37 * (d['lv'] + 5))) * (1 + 1.0 * d['p16004'] / (37 * (d['lv'] + 5))) * (1 + d['p16008']) * (1 + 0.33 * d['p12041'] / (25 * (d['lv'] + 5)) + 0.33 * d['p12042']) * (1 + d['p16009'] + 0.05 * d['p16010'] / (5 + d['lv'])) + 255.3) / 0.23) ** 0.5 + 6.7) ** 2 - 1678,
         'funName': 'atkScoreFormula2'},
 90073: {'formula': lambda d: 1.111 * (((1.0 * ((d['p12012'] + d['p12013']) / 2 * (1 + 0.01 * d['p12015']) + d['p17004'] + d['p17007']) * (min(1, 0.9 + 1.42857 * d['p12018'] / 74 / (d['lv'] + 5) + d['p12019']) + (d['p12016'] / (37.5 * (d['lv'] + 5)) + d['p12024']) * (d['p12017'] + d['p12040'] / (12.5 * (d['lv'] + 5)))) * (35 * (d['lv'] + 5) + 0.2 * d['lv'] ** 2) / max((35 - 25 * d['p12124']) * (d['lv'] + 5) + 0.2 * (1 - d['p12124']) * d['lv'] ** 2 - 0.7 * d['p12034'], 10 * (d['lv'] + 5)) * (1 + 0.5 * d['p16002'] / (37 * (d['lv'] + 5))) * (1 + 1.0 * d['p16004'] / (37 * (d['lv'] + 5))) * (1 + d['p16008']) * (1 + 0.33 * d['p12041'] / (25 * (d['lv'] + 5)) + 0.33 * d['p12042']) * (1 + d['p16009'] + 0.05 * d['p16010'] / (5 + d['lv'])) + 255.3) / 0.23) ** 0.5 + 6.7) ** 2 - 1678,
         'funName': 'atkScoreFormula3'},
 90074: {'formula': lambda d: 1.111 * (((1.0 * ((d['p12012'] + d['p12013']) / 2 * (1 + 0.01 * d['p12015']) + d['p17005'] + d['p17007']) * (min(1, 0.9 + 1.42857 * d['p12018'] / 74 / (d['lv'] + 5) + d['p12019']) + (d['p12016'] / (37.5 * (d['lv'] + 5)) + d['p12024']) * (d['p12017'] + d['p12040'] / (12.5 * (d['lv'] + 5)))) * (1 + d['p12026']) * (35 * (d['lv'] + 5) + 0.2 * d['lv'] ** 2) / max((35 - 25 * d['p12124']) * (d['lv'] + 5) + 0.2 * (1 - d['p12124']) * d['lv'] ** 2 - 0.7 * d['p12034'], 10 * (d['lv'] + 5)) * (1 + 0.5 * d['p16002'] / (37 * (d['lv'] + 5))) * (1 + 1.0 * d['p16004'] / (37 * (d['lv'] + 5))) * (1 + d['p16008']) * (1 + 0.33 * d['p12041'] / (25 * (d['lv'] + 5)) + 0.33 * d['p12042']) * (1 + d['p16009'] + 0.05 * d['p16010'] / (5 + d['lv'])) + 255.3) / 0.23) ** 0.5 + 6.7) ** 2 - 1678,
         'funName': 'atkScoreFormula4'},
 90075: {'formula': lambda d: d['aLv'],
         'funName': 'yitiaolongMonsterExpLv'},
 90076: {'formula': lambda d: int((int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5) * 1.635 * int(6 / 3.0) * 200 * 1.2),
         'funName': 'yitiaolongExpByStep1'},
 90077: {'formula': lambda d: int(int(int((d['lv'] + 2.2) ** 1.45 / 2.0) * d['lv'] * 0.1 + 5) * 5 * 5 * 15 * 0.75) * (0.8 + max(0.1 * d['carrierSatisfaction'], 0.15)),
         'funName': 'yitiaolongExpByStep2'},
 90078: {'formula': lambda d: int(16 * int(min(max(64, int((d['lv'] + 2.2) ** 1.45 / 2.0)), 273) * (0.5 * d['lv'] + max(12, min(0.5 * d['lv'], 35))) * 0.1 * 69.387)),
         'funName': 'yitiaolongExpByStep3'},
 90079: {'formula': lambda d: int(100 * (int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05) + 5)),
         'funName': 'yitiaolongExpByStep4'},
 90080: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 784.8 / 2301.24),
         'funName': 'yitiaolongExpBack1'},
 90081: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 281.25 / 2301.24),
         'funName': 'yitiaolongExpBack2'},
 90082: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 1110.19 / 2301.24),
         'funName': 'yitiaolongExpBack3'},
 90083: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 125 / 2301.24),
         'funName': 'yitiaolongExpBack4'},
 90089: {'formula': lambda d: d['mlLv'] + 2,
         'funName': 'fubenGuideLowLv'},
 90090: {'formula': lambda d: d['mlLv'] - 2,
         'funName': 'fubenGuideUpLv'},
 90096: {'formula': lambda d: min(3, d['attrSpr'] * (d['growthRatio'] * 0.000962306610407876 + d['aptitudeSpr'] * 1.04098101265823e-06) / (1 - (1 + d['attrSpr'] * (d['growthRatio'] * 0.000962306610407876 + d['aptitudeSpr'] * 1.04098101265823e-06)) * 0.2)),
         'funName': 'spellMinusRatio'},
 90097: {'formula': lambda d: (d['aptitudePw'] * 0.000821179871238996 + d['growthRatio'] * 1.4598753266471) * (d['attrPw'] + 1.3 * d['lv'] * (1 + d['basePhyAtkEnhRatio'])) * (1 + 0.008 * d['lv']) * (1 + 0.005 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': 'spritePhyAttack'},
 90098: {'formula': lambda d: (d['aptitudeInt'] * 0.000821179871238996 + d['growthRatio'] * 1.4598753266471) * (d['attrInt'] + 1.3 * d['lv'] * (1 + d['baseMagAtkEnhRatio'])) * (1 + 0.008 * d['lv']) * (1 + 0.005 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': 'spriteMagAttack'},
 90099: {'formula': lambda d: (d['aptitudeAgi'] * 0.00350598504540932 + d['growthRatio'] * 6.23286230294991) * (d['attrAgi'] + 1.7 * d['lv'] * (1 + d['basePhyDefEnhRatio'])) * (1 + 0.010987643020595 * d['lv']) * (1 + 0.0025 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': 'spritePhyDef'},
 90100: {'formula': lambda d: (d['aptitudeSpr'] * 0.00350598504540932 + d['growthRatio'] * 6.23286230294991) * (d['attrSpr'] + 1.7 * d['lv'] * (1 + d['baseMagDefEnhRatio'])) * (1 + 0.010987643020595 * d['lv']) * (1 + 0.0025 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': 'spriteMagDef'},
 90101: {'formula': lambda d: 0.8 + max(0.1 * d['satisfaction'], 0.15),
         'funName': 'satisfactionClientFormula'},
 90102: {'formula': lambda d: 0.3 * (20 * d['aptitudePw'] + 20 * d['aptitudeAgi'] + 20 * d['aptitudeSpr'] + 20 * d['aptitudePhy'] + 20 * d['aptitudeInt'] + 61500 * d['growth'] + 2902 * d['lv'] + 540.5 * d['fami'] + (20 + d['naturalLv']) * 470 * d['naturalNum'] + 1878 * (d['traitLv'] + 20) + d['juexing'] * 1878 * (d['awakeLv'] + 20) + 18782 * d['bonusNum'] + 15651.7 * (d['learnsHigh'] + 0.5 * d['learnsLow']) + d['boneLv'] * 500 + d['famiEffAdd'] * 1000),
         'funName': 'spriteScore'},
 90113: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 784.8 / 2301.24 * 0.12),
         'funName': 'yitiaolongExpBackscore1'},
 90114: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 281.25 / 2301.24 * 0.12),
         'funName': 'yitiaolongExpBackscore2'},
 90115: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 1110.19 / 2301.24 * 0.12),
         'funName': 'yitiaolongExpBackscore3'},
 90116: {'formula': lambda d: 2 * int((d['lv'] * 30 + 2000) * 0.4898 * 125 / 2301.24 * 0.12),
         'funName': 'yitiaolongExpBackscore4'},
 90117: {'formula': lambda d: max(5, min(60, int(0.5 * d['onlineNum'] / 80) + 1)),
         'funName': 'syzsDgNum'},
 90123: {'formula': lambda d: int(int((d['lv'] + 2.2) ** 1.45 / 2.0) * d['lv'] * 0.1 + 5) * d['times'] * 3,
         'funName': 'bfyTableFameReward'},
 90124: {'formula': lambda d: max(0.05 + 0.15 * d['result'], 0.15 * d['result'] + d['totalTimes'] * 0.004),
         'funName': 'bfyTableItemRate'},
 90126: {'formula': lambda d: 1 - (d['maxLv'] - d['currentLv']) * 0.01,
         'funName': 'shopYunbiLv'},
 90129: {'formula': lambda d: d['p1'] * d['naturalSkillNum'] + d['p2'] * d['bonusSkillNum'] + (0.1 if 7006 in d['bonusSkills'] else 0),
         'funName': 'spriteskillaccessoryEnh1'},
 90134: {'formula': lambda d: min(20, 20 - (d['lv'] - 59) * 0.6 + max(0, (d['lv'] - 65) * 0.1) + max(0, (d['lv'] - 69) * 0.16)) * int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05 + 5) * 5 * 24,
         'funName': 'inheritExp'},
 90135: {'formula': lambda d: min(20, 20 - (d['lv'] - 59) * 0.6 + max(0, (d['lv'] - 65) * 0.1) + max(0, (d['lv'] - 69) * 0.16)) * int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05 + 5) * 5 * 24 * 1.05,
         'funName': 'inheritXiuwei'},
 90136: {'formula': lambda d: d['mlv'] * 100,
         'funName': 'spriteTrainMoney'},
 90137: {'formula': lambda d: int((d['mlv'] + 2.2) ** 1.45 * d['mlv'] * 0.05) * 300 + d['mlv'] * 26667,
         'funName': 'spriteTrainExp'},
 90138: {'formula': lambda d: int(3000 * d['mlv'] ** (0.765 - min(max(d['mlv'] - 71, 0), 1) * 0.005) + d['mlv'] * 3333.33),
         'funName': 'spriteTrainFami'},
 90139: {'formula': lambda d: 1.0 * d['damageVal'] / 1500 + 1.0 * d['cureVal'] / 15000,
         'funName': 'wingWorldBossDonate'},
 90140: {'formula': lambda d: int(max(300 * 1.1 ** d['openStage'], (0.81 + 0.03 * d['openStage']) * d['lastWeekDonate'] * 0.9 * int(max(1, d['weekRemain'] - 2) / (13 - d['openStage'])))),
         'funName': 'wingDonateLimit'},
 90141: {'formula': lambda d: 0.2 * (13 * (d['aptPw'] - d['aptitudePwLow']) + 13 * (d['aptAgi'] - d['aptitudeAgiLow']) + 13 * (d['aptSpr'] - d['aptitudeSprLow']) + 13 * (d['aptPhy'] - d['aptitudePhyLow']) + 13 * (d['aptInt'] - d['aptitudeIntLow']) + 74530 * (d['growth'] - 1.03) + 465.7 * ((d['fami'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['fami'] / 30), 1) + d['fami'] * (1 - min(int(d['fami'] / 30), 1))) + (14 + d['naturalLv']) * 495.6 * d['naturalNum'] + 991.2 * d['traitLv'] + d['juexing'] * 991.2 * (d['awakeLv'] + 14) + 6195 * d['bonusNum'] + 9705 * (1.5 * d['learnsUltimate'] + d['learnsHigh'] + 0.5 * d['learnsLow']) + d['boneLv'] * 557 + d['famiEffAdd'] * 465.7) * (0.5 + d['lv'] / 158.0) + 0.05 * ((d['aptitudePwLow'] + d['aptitudeAgiLow'] + d['aptitudeSprLow'] + d['aptitudePhyLow'] + d['aptitudeIntLow']) * 5 * 13 / 79.0 + 1143.2) * d['lv'],
         'funName': 'spriteBattleScore'},
 90142: {'formula': lambda d: max(int((d['lv'] - 24) / 5), 0),
         'funName': 'wingWorldExpRainBuffLv'},
 90153: {'formula': lambda d: round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.34, 0),
         'funName': 'yitiaolongExpBackTb1'},
 90154: {'formula': lambda d: round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.12, 0),
         'funName': 'yitiaolongExpBackTb2'},
 90155: {'formula': lambda d: round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.48, 0),
         'funName': 'yitiaolongExpBackTb3'},
 90156: {'formula': lambda d: round((int((d['lv'] - 5) / 10) * 2 + 20) * 0.06, 0),
         'funName': 'yitiaolongExpBackTb4'},
 90159: {'formula': lambda d: min(d['totalFamiExp'] * 2.133e-05, 200000),
         'funName': 'spriteFamiCoverCost'},
 90160: {'formula': lambda d: d['scoreRatio'] * 0.005 * (1 - d['lv'] / 150) * pow((d['totalDmg'] - d['spriteDmg']) / 40 * (9778.9 * pow(d['lv'], 2) - 1960.8 * d['lv'] + 24408), 0.5),
         'funName': 'challengePlayerScoreFormula'},
 90161: {'formula': lambda d: d['scoreRatio'] * 0.01 * (1 - d['lv'] / 150) * pow(d['spriteDmg'] / 40 * (9778.9 * pow(d['lv'], 2) - 1960.8 * d['lv'] + 24408), 0.5),
         'funName': 'challengeSpriteScoreFormula'},
 90162: {'formula': lambda d: d['scoreRatio'] * 0.4 * (1 + pow(d['lv'], 2) / 100) * d['combatDuration'],
         'funName': 'challengeTimeScoreFormula'},
 90163: {'formula': lambda d: min(0.105 * (d['skyWingTgtAvatarLv'] + 50) / (d['lv'] + 50) * (d['killPlayer'] * 0.45) * (1 + d['isRevenge'] * 0.2 - d['isReduce'] * 0.5), 0.3) * d['tScore'] * 0.8,
         'funName': 'robPlayerScoreFormula'},
 90164: {'formula': lambda d: min(0.105 * (d['skyWingTgtAvatarLv'] + 50) / (d['lv'] + 50) * (d['killSprite'] * 0.45) * (1 + d['isRevenge'] * 0.2 - d['isReduce'] * 0.5), 0.3) * d['tScore'] * 0.8,
         'funName': 'robSpriteScoreFormula'},
 90165: {'formula': lambda d: min(15.749999999999998 / (d['combatDuration'] + 5) * 0.3 * (d['skyWingTgtAvatarLv'] + 50) / (d['lv'] + 50) * (d['killPlayer'] * 0.55 + d['killSprite'] * 0.45 ** (1 + d['isRevenge'] * 0.2 - d['isReduce'] * 0.5)), 0.3) * d['tScore'] * 0.2,
         'funName': 'robTimeScoreFormula'},
 90166: {'formula': lambda d: min(20, 20 - (d['lv'] - 59) * 0.6 + max(0, (d['lv'] - 65) * 0.1) + max(0, (d['lv'] - 69) * 0.16)) * int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05 + 5) * 5 * 24 * (min(max(d['maxXiuweiLv'] - d['xiuweiLv'] - 3, 0), 4) * 0.125 + 0.04 + min(d['maxXiuweiLv'] - d['xiuweiLv'], 3) * 0.02) * max(0, (d['maxLv'] >= 59) * 0.5 + min(0.5, int((d['maxLv'] - 59) / 5) * 0.125)),
         'funName': 'inheritExpNpc'},
 90167: {'formula': lambda d: min(20, 20 - (d['lv'] - 59) * 0.6 + max(0, (d['lv'] - 65) * 0.1) + max(0, (d['lv'] - 69) * 0.16)) * int((d['lv'] + 2.2) ** 1.45 * d['lv'] * 0.05 + 5) * 5 * 24 * 1.05 * (min(max(d['maxXiuweiLv'] - d['xiuweiLv'] - 3, 0), 4) * 0.125 + 0.04 + min(d['maxXiuweiLv'] - d['xiuweiLv'], 3) * 0.02) * max(0, (d['maxLv'] >= 59) * 0.5 + min(0.5, int((d['maxLv'] - 59) / 5) * 0.125)),
         'funName': 'inheritXiuweiNpc'},
 90168: {'formula': lambda d: 0.05 * ((d['aptitudePwLow'] + d['aptitudeAgiLow'] + d['aptitudeSprLow'] + d['aptitudePhyLow'] + d['aptitudeIntLow']) * 5 * 13 / 79.0 + 1143.2) * d['lv'] + (6195 * d['bonusNum'] + (14 + d['naturalLv']) * 495.6 * d['naturalNum']) * 0.2 * (0.5 + d['lv'] / 158.0),
         'funName': 'spriteScore1'},
 90169: {'formula': lambda d: (((d['fami'] + d['famiEffAdd'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['fami'] / 30), 1) + (d['fami'] + d['famiEffAdd']) * (1 - min(int(d['fami'] / 30), 1))) * 465.7 + 991.2 * d['traitLv'] + d['juexing'] * 991.2 * (d['awakeLv'] + 14)) * 0.2 * (0.5 + d['lv'] / 158.0),
         'funName': 'spriteScore2'},
 90170: {'formula': lambda d: 9705 * (1.5 * d['learnsUltimate'] + d['learnsHigh'] + 0.5 * d['learnsLow']) * 0.2 * (0.5 + d['lv'] / 158.0),
         'funName': 'spriteScore3'},
 90171: {'formula': lambda d: (13 * (d['aptPw'] - d['aptitudePwLow']) + 13 * (d['aptAgi'] - d['aptitudeAgiLow']) + 13 * (d['aptSpr'] - d['aptitudeSprLow']) + 13 * (d['aptPhy'] - d['aptitudePhyLow']) + 13 * (d['aptInt'] - d['aptitudeIntLow']) + 74530 * (d['growth'] - 1.03) + d['boneLv'] * 557) * 0.2 * (0.5 + d['lv'] / 158.0),
         'funName': 'spriteScore4'},
 90172: {'formula': lambda d: ((12010, d['enhPoint'] * 0.00031),
                     (12011, d['enhPoint'] * 0.00031),
                     (12012, d['enhPoint'] * 0.00031),
                     (12013, d['enhPoint'] * 0.00031),
                     (10053, d['enhPoint'] * 0.00031)),
         'funName': 'TianyuYanwuAvatarMonsterEnhPointFml'},
 90173: {'formula': lambda d: min(0.6, 0.03 * (0.6 + (d['skillLv'] - 1) * 0.04) + 0.03 * d['attrInt'] / (d['lv'] * 6.3)),
         'funName': 'yuezhangJuexingMpReduce'},
 90174: {'formula': lambda d: (22.5 * (d['lv'] + 5) * (1 + 0.9 * d['powerf']) if d['lv'] < 31 else 19503.7 * d['lv'] - 565608),
         'funName': 'TianyuLiuyiguangMana'},
 90175: {'formula': lambda d: d['mlv'] * 100,
         'funName': 'spriteExploreMoney'},
 90176: {'formula': lambda d: int((d['mlv'] + 2.2) ** 1.45 * d['mlv'] * 0.05 * 300 + d['mlv'] * 26667),
         'funName': 'spriteExploreExp'},
 90177: {'formula': lambda d: int(3000 * d['mlv'] ** (0.765 - min(max(d['mlv'] - 71, 0), 1) * 0.005) + d['mlv'] * 3333.33),
         'funName': 'spriteExploreFami'},
 90178: {'formula': lambda d: int((56 * (1 + 0.5 * d['srcRare']) + 10.0 - 1) / 10.0),
         'funName': 'qizhiItemNumNeed'},
 90179: {'formula': lambda d: d['srcScore'],
         'funName': 'qizhiItemNumConsumed'},
 90180: {'formula': lambda d: (int((d['lv'] + 2.2) ** 1.45 / 2.0) * d['lv'] * 0.1 + 5) * 5,
         'funName': 'funcName:quizzesExp'},
 90181: {'formula': lambda d: int(62.5 * (1.8 - 1 / (0.6667 + 9.2e-05 * d['propVal']))),
         'funName': 'spriteMiningAtkSpeed'},
 90182: {'formula': lambda d: int(62.5 * (1.8 - 1 / (0.6667 + 2.57e-05 * d['propVal']))),
         'funName': 'spriteMiningDefSpeed'},
 90183: {'formula': lambda d: int(62.5 * (1.8 - 1 / (0.6667 + 4.15e-06 * d['propVal']))),
         'funName': 'spriteMiningHpSpeed'},
 90184: {'formula': lambda d: max(1, int(10000 * (1.55 - 1 / (1.81818 + 0.443459 * d['pointNum']))) / float(10000)),
         'funName': 'spriteMiningGuildBonus'},
 90185: {'formula': lambda d: max(1, int(10000 * (3 - 1 / (0.5 + 0.004 * d['pointNum']))) / float(10000)),
         'funName': 'spriteMiningNationBonus'},
 90186: {'formula': lambda d: 32 * (d['dstRare'] - d['srcRare']),
         'funName': 'qiZhiItemNumNeed2'},
 90187: {'formula': lambda d: d['srcScore'] + 32 * (d['dstRare'] - d['srcRare']),
         'funName': 'qizhiItemNumConsumed2'},
 90188: {'formula': lambda d: int((56 * (1 + 0.5 * d['srcRare']) + 10.0 - 1) / 10.0) + 32 * (d['dstRare'] - d['srcRare']),
         'funName': 'qiZhiItemNumNeed3'},
 90189: {'formula': lambda d: d['srcScore'] + 32 * (d['dstRare'] - d['srcRare']),
         'funName': 'qizhiItemNumConsumed3'},
 90190: {'formula': lambda d: 7 - 3 * d['lv'],
         'funName': 'WWdmgAddRatioToBuilding'},
 90191: {'formula': lambda d: -1 + 0.05 * d['lv'],
         'funName': 'WWdmgAddRatioToPlayer'},
 90192: {'formula': lambda d: d['lv'] - 1,
         'funName': 'WWdmgAddRatioToCarrier'},
 90193: {'formula': lambda d: 0,
         'funName': 'WWskillCoolDownReduce'},
 90194: {'formula': lambda d: 200000 - 50000 * d['lv'],
         'funName': 'WWCarrierMHp'},
 90195: {'formula': lambda d: int(min(min(10 * d['cnt'], 8 * d['cnt'] + 400), d['cnt'] + 3000)),
         'funName': 'wingWorldXinmoObservers'},
 90196: {'formula': lambda d: 10000 * d['time'] * min(1.3, max(0.1, 1 + (d['avlScore'] - 500000) / 500000)) ** 2,
         'funName': 'shaxing_choose_11'},
 90197: {'formula': lambda d: 10000 * d['time'] * min(1.3, max(0.1, 1 + (d['avlScore'] - 550000) / 550000)) ** 2,
         'funName': 'shaxing_choose_12'},
 90198: {'formula': lambda d: 10000 * d['time'] * min(1.3, max(0.1, 1 + (d['avlScore'] - 600000) / 600000)) ** 2,
         'funName': 'shaxing_choose_13'},
 90199: {'formula': lambda d: 10000 * d['time'] * min(1.3, max(0.1, 1 + (d['avlScore'] - 700000) / 700000)) ** 2,
         'funName': 'shaxing_choose_14'},
 90200: {'formula': lambda d: 10000 * d['time'] * min(1.3, max(0.1, 1 + (d['avlScore'] - 800000) / 800000)) ** 2,
         'funName': 'shaxing_choose_15'},
 90204: {'formula': lambda d: 100000,
         'funName': 'wingWorldCarrierMhp'},
 90205: {'formula': lambda d: 1000000,
         'funName': 'wingWorldBuildingMhp'},
 90206: {'formula': lambda d: 10000,
         'funName': 'wingWorldCarrierAttack'},
 90207: {'formula': lambda d: 999,
         'funName': 'wingWorldCarrierDmgAddRatioToBuilding'},
 90208: {'formula': lambda d: -0.8,
         'funName': 'wingWorldCarrierDmgAddRatioToPlayer'},
 90209: {'formula': lambda d: 59,
         'funName': 'wingWorldCarrierDmgAddRatioToCarrier'},
 90210: {'formula': lambda d: 0,
         'funName': 'wingWorldCarrierSkillCoolDownReduce'},
 90212: {'formula': lambda d: d['srcScore'],
         'funName': 'qizhiItemNumConsumed4'},
 90228: {'formula': lambda d: round((1 - d['val']) * 50 + 10),
         'funName': '竞技场段位分计算1'},
 90229: {'formula': lambda d: round((1 - d['val']) * 60 + 0),
         'funName': '竞技场段位分计算2'},
 90230: {'formula': lambda d: round((1 - d['val']) * 32),
         'funName': '竞技场段位分计算3'},
 90231: {'formula': lambda d: round((1 - d['val']) * 32),
         'funName': '竞技场段位分计算4'},
 90232: {'formula': lambda d: 10,
         'funName': '竞技场段位分计算5'},
 90233: {'formula': lambda d: 0,
         'funName': '竞技场段位分计算6'},
 90234: {'formula': lambda d: round(-1 * d['val'] * 14),
         'funName': '竞技场段位分计算7'},
 90235: {'formula': lambda d: round(-1 * d['val'] * 32),
         'funName': '竞技场段位分计算8'},
 90236: {'formula': lambda d: 10,
         'funName': '竞技场段位分计算9'},
 90237: {'formula': lambda d: 0,
         'funName': '竞技场段位分计算10'},
 90238: {'formula': lambda d: 0,
         'funName': '竞技场段位分计算11'},
 90239: {'formula': lambda d: 0,
         'funName': '竞技场段位分计算12'},
 90240: {'formula': lambda d: round(-1 * d['val'] * 32),
         'funName': '竞技场段位分计算13'},
 90241: {'formula': lambda d: round(-1 * d['val'] * 32),
         'funName': '竞技场段位分计算14'},
 90242: {'formula': lambda d: 1 / (1.0 + 10 ** (-d['x'] / 400.0)),
         'funName': '竞技场段位分计算15'},
 90243: {'formula': lambda d: (0.0719 * d['star'] ** 3 - 0.0016 * d['star'] ** 4 - 1.0611 * d['star'] ** 2 + 6.9973 * d['star'] + 5.5981 if d['star'] < 13 else ((56.8710347362579 - 4.18012364863192 * d['star'] + 0.176637676369076 * d['star'] ** 2) / 1.12 if d['star'] < 21 else (42.6836129618674 * 1.08 ** (d['star'] - 20) if d['star'] < 25 else (67.8074404151165 * 1.05 ** (d['star'] - 25) if d['star'] < 30 else (101.940800002335 / 1.12 * 1.05 ** (d['star'] - 30) if d['star'] < 35 else (130.10516350948 / 1.12 * 1.05 ** (d['star'] - 35) if d['star'] < 40 else (185.670502893643 / 1.12 * 1.05 ** (d['star'] - 40) if d['star'] < 45 else (262.31787722249 / 1.12 * 1.05 ** (d['star'] - 45) if d['star'] < 50 else (372.0315586931868 if d['star'] == 50 else (357.638887458333 * 1.0141 ** (d['star'] - 51) * 1.2 / 1.12 if d['star'] < 60 else 357.638887458333 * 1.0141 ** (d['star'] - 51) * 1.2 * 1.33 / 1.12)))))))))) * 1.12,
         'funName': 'zhanmoji_hp'},
 90244: {'formula': lambda d: (1000 + 60 * d['star'] if d['star'] < 20 else (2600 + 80 * (d['star'] - 20) if d['star'] < 30 else (3400 + (d['star'] - 30) * 80 if d['star'] < 40 else (4830 + (d['star'] - 40) * 80 if d['star'] < 50 else (5645 + (d['star'] - 50) * 95 if d['star'] < 60 else 6988 + 110 * (d['star'] - 60)))))) * (d['isBoost'] * 1.5 if d['isBoost'] else 1) * (d['isLucky'] * 2 if d['isLucky'] else 1),
         'funName': 'zhanmoji_jf'},
 90245: {'formula': lambda d: round(0.5 * (0.6 + 0.4 / 8 * (d['weathLv'] - 1)) / 130 * d['power'] * 100),
         'funName': 'yaojinTicketBonus'},
 90246: {'formula': lambda d: min(10, 2 + int((d['junJieLv'] + 1) / 2)),
         'funName': 'ftbJunjieTask'},
 90247: {'formula': lambda d: min(7, 2 + int((d['qumoLv'] + 1) / 2)),
         'funName': 'ftbQumoTask'},
 90248: {'formula': lambda d: int(min(10, max(3, min(8, 2 + (d['combatScore'] > d['combatRank30']) + (d['combatScore'] > d['combatRank120']) + (d['combatScore'] > d['combatRank120'] * 0.87) + (d['combatScore'] > d['combatRank160'] * 0.75) + (d['combatScore'] > d['combatRank160'] * 0.69) + (d['combatScore'] > d['combatRank200'] * 0.62), (d['openDays'] + 32) / (11 + 60 / (2 + (d['combatScore'] > d['combatRank30']) + (d['combatScore'] > d['combatRank120']) + (d['combatScore'] > d['combatRank120'] * 0.87) + (d['combatScore'] > d['combatRank160'] * 0.75) + (d['combatScore'] > d['combatRank160'] * 0.69) + (d['combatScore'] > d['combatRank200'] * 0.62)))) + min(5, 1 + (d['guibao'] > d['guibaoRank20']) + (d['guibao'] > d['guibaoRank100']) + (d['guibao'] > d['guibaoRank100'] * 0.75) + (d['guibao'] > d['guibaoRank100'] * 0.6), (d['openDays'] + 10) / (11 + 20 / (1 + (d['guibao'] > d['guibaoRank20']) + (d['guibao'] > d['guibaoRank100']) + (d['guibao'] > d['guibaoRank100'] * 0.75) + (d['guibao'] > d['guibaoRank100'] * 0.6))))))),
         'funName': 'ftbLoginTask'},
 90252: {'formula': lambda d: 0.8,
         'funName': 'lowFbFameDiscoun'},
 90270: {'formula': lambda d: max(int(d['feedCount'] * 0.15), 1),
         'funName': 'feedretcoin'},
 90271: {'formula': lambda d: min(26, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))),
         'funName': 'serverAdd1'},
 90272: {'formula': lambda d: min(23, max(0, int(0.57 * d['openDay'] + 1 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.65, d['openDay'] / 10), 2.4749999999999996)))),
         'funName': 'serverAdd2'},
 90273: {'formula': lambda d: min(20, max(0, int(0.475 * d['openDay'] + 1.6 - (d['openDay'] <= 5) * 1 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.8, d['openDay'] / 10), 2.7)))),
         'funName': 'serverAdd3'},
 90274: {'formula': lambda d: min(17, max(0, int(0.42 * d['openDay'] + 1.3 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(2, d['openDay'] / 10), 3.0)))),
         'funName': 'serverAdd4'},
 90275: {'formula': lambda d: min(16, max(0, int(0.39 * d['openDay'] + 0.78 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(2.5, d['openDay'] / 10), 3.75)))),
         'funName': 'serverAdd5'},
 90276: {'formula': lambda d: min(14, max(0, int(0.36 * d['openDay'] + 0.25 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(3, d['openDay'] / 10), 4.5)))),
         'funName': 'serverAdd6'},
 90277: {'formula': lambda d: min(26, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))),
         'funName': 'digongLowXiuwei1'},
 90278: {'formula': lambda d: min(26, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))) + 1,
         'funName': 'digongHighXiuwei1'},
 90279: {'formula': lambda d: max(0, min(1, min(26, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))) - d['xiuweiLevel'] + 0.5)),
         'funName': 'digongMonster1'},
 90280: {'formula': lambda d: min(1, max(69.0 / 79.0, d['p10000'] / 79.0)),
         'funName': '业刹血刺、链击伤害等级函数（69低79高）'},
 90281: {'formula': lambda d: d['aLv'] + min(max(int((d['mLv'] - d['aLv']) / 5), 0), 2),
         'funName': 'digongLvExp'},
 90282: {'formula': lambda d: min(20, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))),
         'funName': 'digongLowXiuwei2'},
 90283: {'formula': lambda d: min(20, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))) + 1,
         'funName': 'digongHighXiuwei2'},
 90284: {'formula': lambda d: max(0, min(1, min(20, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))) - d['xiuweiLevel'] + 0.5)),
         'funName': 'digongMonster2'},
 90285: {'formula': lambda d: min(13, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))),
         'funName': 'digongLowXiuwei3'},
 90286: {'formula': lambda d: min(13, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))) + 1,
         'funName': 'digongHighXiuwei3'},
 90287: {'formula': lambda d: max(0, min(1, min(13, max(1, int(0.65 * d['openDay'] + 1.2 + 0.3 + (d['openDay'] >= 7) * (d['maxXiuweiLv'] - (0.65 * d['openDay'] + 1.2 + 3)) / min(max(1.5, d['openDay'] / 10), 2.25)))) - d['xiuweiLevel'] + 0.5)),
         'funName': 'digongMonster3'},
 90300: {'formula': lambda d: int(int(d['popularity'] ** 0.5 / 2.5) / 10 * d['daysNum']),
         'funName': 'zombieFansFormulaId'},
 90305: {'formula': lambda d: 2000 * min(max(d['lv'] - 69, 0), 1) + 1750 * min(max(70 - d['lv'], 0) * max(d['lv'] - 59, 0), 1) + 1500 * min(max(60 - d['lv'], 0), 1),
         'funName': '暴击防御上限'},
 90306: {'formula': lambda d: int((max(d['lastSignupCnt'] * 0.7, 80) * 2 if d['rNo'] < 3 else (max(d['lastSignupCnt'] * 0.7, 80) * 1.5 if d['rNo'] < 7 else (max(d['lastSignupCnt'] * 0.7, 80) * 1 if d['rNo'] < 13 else max(d['lastSignupCnt'] * 0.7, 80) * 32))) / 4),
         'funName': 'turnmaterialamountofcrystaldefence'},
 90327: {'formula': lambda d: int((max(d['lastSignupCnt'] * 0.7, 80) * 2 if d['rNo'] < 3 else (max(d['lastSignupCnt'] * 0.7, 80) * 1.5 if d['rNo'] < 7 else (max(d['lastSignupCnt'] * 0.7, 80) * 1 if d['rNo'] < 13 else max(d['lastSignupCnt'] * 0.7, 80) * 32))) / 4),
         'funName': 'turnmaterialamountofdragonfury'},
 90328: {'formula': lambda d: d['rSelf'] / d['rRight'] * d['rWrong'] * 0.8 + d['rSelf'],
         'funName': '通用竞猜的奖金计算公式'},
 90329: {'formula': lambda d: (d['Other'] * 0.8 + d['Self']) / d['Self'],
         'funName': '通用竞猜的赔率的计算公式'},
 90330: {'formula': lambda d: int(min(min(d['dmg'], 7762148) * 0.0002164 + min(max(d['dmg'] - 7762148, 0), 7762148) * 0.0001623 + min(max(d['dmg'] - 15524296, 0), 31048593) * 5.41e-05 + min(max(d['dmg'] - 46572889, 0), 46572890) * 3.61e-05 + min(max(d['dmg'] - 93145779, 0), 62097187) * 1.35e-05 + min(max(d['dmg'] - 155242966, 0), 103495310) * 1.22e-05, 8400)),
         'funName': '打图积分计算公式（单人）'},
 90331: {'formula': lambda d: int(min((min(d['dmg'], 43694585) * 0.0002523 + min(max(d['dmg'] - 43694585, 0), 80946940) * 0.000153 + min(max(d['dmg'] - 124641525, 0), 267597886) * 7.4e-05 + min(max(d['dmg'] - 392239411, 0), 275412795) * 7.2e-05 + min(max(d['dmg'] - 667652206, 0), 241939676) * 4.1e-05 + min(max(d['dmg'] - 909591882, 0), 306030390) * 4.1e-05) / 4, 14700)),
         'funName': '打图积分计算公式（组队）'},
 90332: {'formula': lambda d: int(min(min(d['dmg'], 8224941) * 0.0001277 + min(max(d['dmg'] - 8224941, 0), 4934964) * 0.0002128 + min(max(d['dmg'] - 13159905, 0), 11514918) * 0.0001459 + min(max(d['dmg'] - 24674823, 0), 24674644) * 6.81e-05 + min(max(d['dmg'] - 49349467, 0), 32899945) * 2.55e-05 + min(max(d['dmg'] - 82249412, 0), 82249412) * 1.28e-05, 7350)),
         'funName': '打图积分计算公式（英灵）'},
 90333: {'formula': lambda d: 0,
         'funName': 'spriteFamiCoverCost'},
 90334: {'formula': lambda d: 500,
         'funName': 'needZhanxun1'},
 90335: {'formula': lambda d: max(500, 1500 - 100 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun2'},
 90336: {'formula': lambda d: max(500, 3800 - 150 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun3'},
 90337: {'formula': lambda d: max(500, 8000 - 200 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun4'},
 90338: {'formula': lambda d: max(500, 9900 - 200 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun5'},
 90339: {'formula': lambda d: max(500, 12300 - 200 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun6'},
 90340: {'formula': lambda d: max(500, 18000 - 250 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun7'},
 90341: {'formula': lambda d: max(500, 25000 - 250 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun8'},
 90342: {'formula': lambda d: max(500, 30000 - 250 * max(0, d['week'] - 10)),
         'funName': 'needZhanxun9'},
 90343: {'formula': lambda d: (40 + 2 * d['progress'] + 2 * max(0, d['progress'] - 20)) * min(7 * d['levelMode'], 10),
         'funName': 'spriteCahllengeFameReward'},
 90344: {'formula': lambda d: int(min(int(min(min(d['dmg'], 15045843) * 0.000133 + min(max(d['dmg'] - 50152810, 0), 32954157) * 0.000114 + min(max(d['dmg'] - 50152810, 0), 96126219) * 2.1e-05 + min(max(d['dmg'] - 146279029, 0), 94036519) * 1.6e-05 + min(max(d['dmg'] - 240315548, 0), 73139515) * 2.9e-05 + min(max(d['dmg'] - 313455063, 0), 104485021) * 2e-05, 14000) * 1) * 0.65, 8000)),
         'funName': '打图积分计算公式（大BOSS）'},
 90357: {'formula': lambda d: int(max(1, 300 * (0.3 * (d['makeType'] == 1) * (d['sPrice'] / 20000.0) + 0.35 * (d['makeType'] == 2) * (d['sPrice'] / 20000.0 + 0.3 * d['extraCost1']) + 0.4 * (d['makeType'] == 3) * (d['sPrice'] / 20000.0 + 4.8 * d['extraCost2']) + 0.55 + (d['lvReq'] > 69) * 0.2 + (d['lvReq'] > 59) * 0.15 + (d['lvReq'] > 49) * 0.1))),
         'funName': 'NPC好感度-手工装'},
 90358: {'formula': lambda d: int(max(1, 300 * ((d['quality'] <= 2) * 0.003 + (d['quality'] == 3) * 0.01 + (d['quality'] == 4) * (0.01 + (d['lvReq'] > 69) * 0.01 + (d['lvReq'] > 59) * 0.01) + (d['quality'] >= 5) * (0.03 + (d['lvReq'] > 69) * 0.25 + (d['lvReq'] > 59) * 0.16 + (d['lvReq'] > 49) * 0.06)))),
         'funName': 'NPC好感度-其他装备'},
 90359: {'formula': lambda d: int(max(1, 300 * (0.5 * (d['runeType'] < 3) * (0.3 * 3 ** (min(5, d['lv']) - 1) + 0.3 * (3 ** (min(5, d['lv']) - 1) - 1) / 2 + 2.5 * (3 ** max(0, min(5, d['lv']) - 4) - 1) / 2 + 1.5 * (d['type'] == 24) * (min(5, d['lv']) > 4) * 4.0 * 3 ** (min(5, d['lv']) - 5)) + 0.5 * (d['runeType'] == 3) * (0.8 * 5 ** (min(5, d['lv']) - 1) + 0.3 * (5 ** (min(5, d['lv']) - 1) - 1) / 4 + 2.5 * (5 ** max(0, min(5, d['lv']) - 3) - 1) / 4)))),
         'funName': 'NPC好感度-神格'},
 90360: {'formula': lambda d: int(max(1, 120.0 * (0.2 * 4 ** (min(min(5, d['lv']), 5) - 1) * 3 ** max(0, min(5, d['lv']) - 5) + (min(5, d['lv']) > 5) * 120 * 4 ** (min(5, d['lv']) - 6)))),
         'funName': 'NPC好感度-纹印'},
 90361: {'formula': lambda d: int(max(1, 300 * ((d['quality'] == 3) * 0.3 * 5 + (d['quality'] == 4) * 0.3 * 180 + (d['quality'] >= 5) * 0.3 * 1800))),
         'funName': 'NPC好感度-符文'},
 90362: {'formula': lambda d: int(max(1, 300 * ((d['quality'] == 3) * 0.3 * 6 + (d['quality'] == 4) * 0.3 * 60 + (d['quality'] >= 5) * 0.3 * 2000))),
         'funName': 'NPC好感度-英灵技能诀'},
 90363: {'formula': lambda d: 0.35,
         'funName': '星级BOSS出现概率（普通层参数）'},
 90364: {'formula': --- This code section failed: ---

0	LOAD_FAST         'd'
3	LOAD_CONST        'maxStar'
6	BINARY_SUBSCR     None
7	LOAD_CONST        0
10	COMPARE_OP        '=='
13	POP_JUMP_IF_FALSE '23'
16	LOAD_CONST        1
19	BUILD_LIST_1      None
22	RETURN_END_IF     None
23	LOAD_FAST         'd'
26	LOAD_CONST        'maxStar'
29	BINARY_SUBSCR     None
30	LOAD_CONST        1
33	COMPARE_OP        '=='
36	POP_JUMP_IF_FALSE '49'
39	LOAD_CONST        0.5
42	LOAD_CONST        0.5
45	BUILD_LIST_2      None
48	RETURN_END_IF     None
49	LOAD_FAST         'd'
52	LOAD_CONST        'maxStar'
55	BINARY_SUBSCR     None
56	LOAD_CONST        2
59	COMPARE_OP        '=='
62	POP_JUMP_IF_FALSE '78'
65	LOAD_CONST        0.25
68	LOAD_CONST        0.25
71	LOAD_CONST        0.5
74	BUILD_LIST_3      None
77	RETURN_END_IF     None
78	LOAD_FAST         'd'
81	LOAD_CONST        'maxStar'
84	BINARY_SUBSCR     None
85	LOAD_CONST        3
88	COMPARE_OP        '=='
91	POP_JUMP_IF_FALSE '110'
94	LOAD_CONST        0.17
97	LOAD_CONST        0.17
100	LOAD_CONST        0.17
103	LOAD_CONST        0.49
106	BUILD_LIST_4      None
109	RETURN_END_IF     None
110	LOAD_FAST         'd'
113	LOAD_CONST        'maxStar'
116	BINARY_SUBSCR     None
117	LOAD_CONST        4
120	COMPARE_OP        '=='
123	POP_JUMP_IF_FALSE '145'
126	LOAD_CONST        0.135
129	LOAD_CONST        0.135
132	LOAD_CONST        0.135
135	LOAD_CONST        0.135
138	LOAD_CONST        0.46
141	BUILD_LIST_5      None
144	RETURN_END_IF     None
145	LOAD_FAST         'd'
148	LOAD_CONST        'maxStar'
151	BINARY_SUBSCR     None
152	LOAD_CONST        5
155	COMPARE_OP        '=='
158	POP_JUMP_IF_FALSE '183'
161	LOAD_CONST        0.11
164	LOAD_CONST        0.11
167	LOAD_CONST        0.11
170	LOAD_CONST        0.11
173	LOAD_CONST        0.11
176	LOAD_CONST        0.45
179	BUILD_LIST_6      None
182	RETURN_END_IF     None
183	LOAD_FAST         'd'
186	LOAD_CONST        'maxStar'
189	BINARY_SUBSCR     None
190	LOAD_CONST        6
193	COMPARE_OP        '=='
196	POP_JUMP_IF_FALSE '224'
199	LOAD_CONST        0.085
202	LOAD_CONST        0.095
205	LOAD_CONST        0.095
208	LOAD_CONST        0.095
211	LOAD_CONST        0.095
214	LOAD_CONST        0.095
217	LOAD_CONST        0.44
220	BUILD_LIST_7      None
223	RETURN_END_IF     None
224	LOAD_FAST         'd'
227	LOAD_CONST        'maxStar'
230	BINARY_SUBSCR     None
231	LOAD_CONST        7
234	COMPARE_OP        '=='
237	POP_JUMP_IF_FALSE '268'
240	LOAD_CONST        0.08
243	LOAD_CONST        0.08
246	LOAD_CONST        0.08
249	LOAD_CONST        0.08
252	LOAD_CONST        0.08
255	LOAD_CONST        0.08
258	LOAD_CONST        0.09
261	LOAD_CONST        0.43
264	BUILD_LIST_8      None
267	RETURN_END_IF     None
268	LOAD_FAST         'd'
271	LOAD_CONST        'maxStar'
274	BINARY_SUBSCR     None
275	LOAD_CONST        8
278	COMPARE_OP        '=='
281	POP_JUMP_IF_FALSE '315'
284	LOAD_CONST        0.075
287	LOAD_CONST        0.075
290	LOAD_CONST        0.075
293	LOAD_CONST        0.075
296	LOAD_CONST        0.075
299	LOAD_CONST        0.075
302	LOAD_CONST        0.075
305	LOAD_CONST        0.075
308	LOAD_CONST        0.4
311	BUILD_LIST_9      None
314	RETURN_END_IF     None
315	LOAD_FAST         'd'
318	LOAD_CONST        'maxStar'
321	BINARY_SUBSCR     None
322	LOAD_CONST        9
325	COMPARE_OP        '=='
328	POP_JUMP_IF_FALSE '365'
331	LOAD_CONST        0.08
334	LOAD_CONST        0.08
337	LOAD_CONST        0.08
340	LOAD_CONST        0.08
343	LOAD_CONST        0.09
346	LOAD_CONST        0.09
349	LOAD_CONST        0.09
352	LOAD_CONST        0.09
355	LOAD_CONST        0.09
358	LOAD_CONST        0.23
361	BUILD_LIST_10     None
364	RETURN_END_IF     None
365	LOAD_CONST        0.08
368	LOAD_CONST        0.08
371	LOAD_CONST        0.08
374	LOAD_CONST        0.08
377	LOAD_CONST        0.08
380	LOAD_CONST        0.08
383	LOAD_CONST        0.08
386	LOAD_CONST        0.08
389	LOAD_CONST        0.08
392	LOAD_CONST        0.28
395	BUILD_LIST_10     None
398	RETURN_VALUE      None
-1	LAMBDA_MARKER     None

Syntax error at or near `RETURN_VALUE' token at offset 398,
         'funName': '星级BOSS出现概率（星级BOSS参数）'},
 90365: {'formula': --- This code section failed: ---

0	LOAD_FAST         'd'
3	LOAD_CONST        'star'
6	BINARY_SUBSCR     None
7	LOAD_CONST        1
10	COMPARE_OP        '=='
13	POP_JUMP_IF_FALSE '20'
16	LOAD_CONST        500
19	RETURN_END_IF     None
20	LOAD_FAST         'd'
23	LOAD_CONST        'star'
26	BINARY_SUBSCR     None
27	LOAD_CONST        2
30	COMPARE_OP        '=='
33	POP_JUMP_IF_FALSE '40'
36	LOAD_CONST        600
39	RETURN_END_IF     None
40	LOAD_FAST         'd'
43	LOAD_CONST        'star'
46	BINARY_SUBSCR     None
47	LOAD_CONST        3
50	COMPARE_OP        '=='
53	POP_JUMP_IF_FALSE '60'
56	LOAD_CONST        700
59	RETURN_END_IF     None
60	LOAD_FAST         'd'
63	LOAD_CONST        'star'
66	BINARY_SUBSCR     None
67	LOAD_CONST        4
70	COMPARE_OP        '=='
73	POP_JUMP_IF_FALSE '80'
76	LOAD_CONST        1500
79	RETURN_END_IF     None
80	LOAD_FAST         'd'
83	LOAD_CONST        'star'
86	BINARY_SUBSCR     None
87	LOAD_CONST        5
90	COMPARE_OP        '=='
93	POP_JUMP_IF_FALSE '100'
96	LOAD_CONST        2000
99	RETURN_END_IF     None
100	LOAD_FAST         'd'
103	LOAD_CONST        'star'
106	BINARY_SUBSCR     None
107	LOAD_CONST        6
110	COMPARE_OP        '=='
113	POP_JUMP_IF_FALSE '120'
116	LOAD_CONST        2500
119	RETURN_END_IF     None
120	LOAD_FAST         'd'
123	LOAD_CONST        'star'
126	BINARY_SUBSCR     None
127	LOAD_CONST        7
130	COMPARE_OP        '=='
133	POP_JUMP_IF_FALSE '140'
136	LOAD_CONST        4000
139	RETURN_END_IF     None
140	LOAD_FAST         'd'
143	LOAD_CONST        'star'
146	BINARY_SUBSCR     None
147	LOAD_CONST        8
150	COMPARE_OP        '=='
153	POP_JUMP_IF_FALSE '160'
156	LOAD_CONST        4500
159	RETURN_END_IF     None
160	LOAD_FAST         'd'
163	LOAD_CONST        'star'
166	BINARY_SUBSCR     None
167	LOAD_CONST        9
170	COMPARE_OP        '=='
173	POP_JUMP_IF_FALSE '180'
176	LOAD_CONST        5500
179	RETURN_END_IF     None
180	LOAD_CONST        7500
183	RETURN_VALUE      None
-1	LAMBDA_MARKER     None

Syntax error at or near `RETURN_VALUE' token at offset 183,
         'funName': '星级BOSS击杀积分公式'},
 90366: {'formula': lambda d: (d['growthRatio'] * 33.355231463233 + d['aptitudePhy'] * 0.0187623176980686) * (d['attrPhy'] + 2.3 * d['lv'] * (1 + d['baseMhpEnhRatio'])) * (1 + 0.00819327731092437 * d['lv']) * (1 + 0.05 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': '亲密度放大mhp-20倍'},
 90367: {'formula': lambda d: (d['aptitudePw'] * 0.000821179871238996 + d['growthRatio'] * 1.4598753266471) * (d['attrPw'] + 1.3 * d['lv'] * (1 + d['basePhyAtkEnhRatio'])) * (1 + 0.008 * d['lv']) * (1 + 0.1 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': '亲密度放大物理攻击-20倍'},
 90368: {'formula': lambda d: (d['aptitudeInt'] * 0.000821179871238996 + d['growthRatio'] * 1.4598753266471) * (d['attrInt'] + 1.3 * d['lv'] * (1 + d['baseMagAtkEnhRatio'])) * (1 + 0.008 * d['lv']) * (1 + 0.1 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': '亲密度放大法术攻击-20倍'},
 90369: {'formula': lambda d: (d['aptitudeAgi'] * 0.00350598504540932 + d['growthRatio'] * 6.23286230294991) * (d['attrAgi'] + 1.7 * d['lv'] * (1 + d['basePhyDefEnhRatio'])) * (1 + 0.010987643020595 * d['lv']) * (1 + 0.05 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': '亲密度放大物理防御-20倍'},
 90370: {'formula': lambda d: (d['aptitudeSpr'] * 0.00350598504540932 + d['growthRatio'] * 6.23286230294991) * (d['attrSpr'] + 1.7 * d['lv'] * (1 + d['baseMagDefEnhRatio'])) * (1 + 0.010987643020595 * d['lv']) * (1 + 0.05 * ((d['famiEffLv'] + d['famiExp'] * 1.0 / d['famiMaxExp']) * min(int(d['familiar'] / 30), 1) + d['famiEffLv'] * (1 - min(int(d['familiar'] / 30), 1)))),
         'funName': '亲密度放大法术防御-20倍'},
 90371: {'formula': lambda d: d['layer'] * 1,
         'funName': '亲密度等级加成'},
 90372: {'formula': lambda d: min(max(0, int(0.333 * (24 * d['killCnt'] + 8 * d['assistCnt'] + min(90, d['damage'] * 0.0001) + d['bossCnt'] * 50 + d['treasureCnt'] * 50))), 130),
         'funName': 'pubgBattleFormulaId'},
 90373: {'formula': lambda d: min(max(0, int(0.15 * (d['interval'] + d['interval'] * (d['interval'] >= 5) + d['interval'] * (d['interval'] >= 13) + d['itemScore']))), 25),
         'funName': 'pubgActiveFormulaId'},
 90374: {'formula': lambda d: int(d['battleScore'] + d['activeScore'] + d['rankParam'] * 1.2),
         'funName': 'pubgFameFormulaId'},
 90375: {'formula': lambda d: int(15 * d['rankParam'] * (1 + (d['comboWin'] >= 3) * min(0.5, d['comboWin'] * 0.1 - 0.1) + (d['killCnt'] >= 3) * min(d['killCnt'] * 0.1, 1) * 0.4) * max(min(1.5, 1 - int((d['rankPoint'] - d['averagePoint']) / 100) * 0.05), 0.5)),
         'funName': 'pubgRankPointFormulaId'},
 90376: {'formula': lambda d: (992.656249999757 + -316.388585372634 * d['star'] + 197.066051136239 * d['star'] ** 2 + -23.8027170745744 * d['star'] ** 3 + 1.11310096153763 * d['star'] ** 4) * max(1, 1.464 * (d['star'] > 4)),
         'funName': '斩魔极星级BOSS血量公式'},
 90377: {'formula': lambda d: d['spritePower'] * 0.15,
         'funName': '派遣格积分获取公式'},
 90378: {'formula': lambda d: 0,
         'funName': '状态未满概率触发好感加成'},
 90392: {'formula': lambda d: d['tSign'] - 9000 + max(d['power'] - 500000, 0) ** 2 / 100000000 * 2 + max(6 - d['guildRank'], 0) * 20 + int(d['isCaptain']) * 1 + min(d['lastContri'] / 100, 1000),
         'funName': 'yishijiequeue'},
 90394: {'formula': lambda d: max(10.0 / max(d['passTime'] - 1, 1) ** 2, 0.5),
         'funName': 'flyUpRollSpeedFunc'},
 90395: {'formula': lambda d: (d['week'] - 25) * 0.00224 + 0.58176,
         'funName': 'monsterAtkChangeWeekly_qingyuan'},
 90396: {'formula': lambda d: (d['week'] - 25) * 0.00194788235294118 + 0.637693882352941,
         'funName': 'monsterHpChangeWeekly__qingyuan'},
 90399: {'formula': lambda d: 0.1 * d['maxCombatScore'],
         'funName': 'guildBattleScore'},
 90400: {'formula': lambda d: (2 * d['yangSlotsCnt'] - 2) * d['p2'] - (2 * d['yangSlotsCnt'] - 2) * d['p1'] * 0.9 + (2 * d['yinSlotsCnt'] - 2) * d['p2'] - (2 * d['yinSlotsCnt'] - 2) * d['p1'] * 0.9,
         'funName': 'UpGradeGemInactiveCost'},
 90401: {'formula': lambda d: (1 + int(3.333 * d['p2']) - (1 + int(3.333 * d['p1'])) * 0.9) * (d['maxStarLv'] - 3),
         'funName': 'UpGradeStarInactiveCost'},
 90402: {'formula': lambda d: (1 + int(3.333 * d['p1'])) * (d['maxStarLv'] - 3) + d['p2'],
         'funName': 'UpGradeMoneyInactiveCost'},
 90403: {'formula': lambda d: max(-0.99, min(0, (d['avatarQuota'] > d['monsterQuota']) * (d['avatarQuota'] - d['monsterQuota']) * 0.001) + (d['avatarQuota'] <= d['monsterQuota']) * (d['avatarQuota'] - d['monsterQuota']) * 0.02),
         'funName': 'pveQuotaFormulaId'},
 90404: {'formula': lambda d: min(0, max(-0.6, (d['avatarQuota'] > d['monsterQuota']) * (d['monsterQuota'] - d['avatarQuota']) * 0.01) + (d['avatarQuota'] <= d['monsterQuota']) * (d['monsterQuota'] - d['avatarQuota']) * 0.01),
         'funName': 'evpQuotaFormulaId'},
 90405: {'formula': lambda d: (d['itemLv'] < 85) * 1.07 + min(4, (d['itemLv'] >= 85) * (1.07 + 0.08 * (d['itemLv'] - 84))),
         'funName': 'wearArg1'},
 90406: {'formula': lambda d: (d['itemLv'] < 85) * 0.54 + min(2, (d['itemLv'] >= 85) * (0.54 + 0.06 * (d['itemLv'] - 84))),
         'funName': 'wearArg2'},
 90407: {'formula': lambda d: (d['itemLv'] < 85) * 1.07 + min(4, (d['itemLv'] >= 85) * (1.07 + 0.08 * (d['itemLv'] - 84))),
         'funName': 'wearArg3'},
 90408: {'formula': lambda d: (d['itemLv'] < 85) * 0.54 + min(2, (d['itemLv'] >= 85) * (0.54 + 0.06 * (d['itemLv'] - 84))),
         'funName': 'wearArg4'},
 90409: {'formula': lambda d: (d['itemLv'] < 85) * 0.27 + min(2, (d['itemLv'] >= 85) * (0.27 + 0.03 * (d['itemLv'] - 84))),
         'funName': 'wearArg5'},
 90410: {'formula': lambda d: (d['itemLv'] < 85) * 0.2 + min(0.6, (d['itemLv'] >= 85) * (0.2 + 0.004 * (d['itemLv'] - 84))),
         'funName': 'repairArg1'},
 90411: {'formula': lambda d: (d['itemLv'] < 85) * 0.1 + min(0.6, (d['itemLv'] >= 85) * (0.1 + 0.0025 * (d['itemLv'] - 84))),
         'funName': 'repairArg2'},
 90412: {'formula': lambda d: (d['itemLv'] < 85) * 0.05 + min(0.6, (d['itemLv'] >= 85) * (0.05 + 0.00125 * (d['itemLv'] - 84))),
         'funName': 'repairArg3'},
 90413: {'formula': lambda d: (d['itemLv'] < 85) * 0.025 + min(0.6, (d['itemLv'] >= 85) * (0.025 + 0.0005 * (d['itemLv'] - 84))),
         'funName': 'repairArg4'},
 90414: {'formula': lambda d: (d['itemLv'] < 85) * 0.05 + min(0.6, (d['itemLv'] >= 85) * (0.05 + 0.001 * (d['itemLv'] - 84))),
         'funName': 'repairArg5'},
 90423: {'formula': lambda d: 60,
         'funName': 'zhisheng_lv_60'},
 90424: {'formula': lambda d: 69,
         'funName': 'zhisheng_lv_69'},
 90425: {'formula': lambda d: 79,
         'funName': 'zhisheng_lv_79'},
 90426: {'formula': lambda d: d['minTopLv'] * 1,
         'funName': 'zhisheng_lv_79_huigui'}}
