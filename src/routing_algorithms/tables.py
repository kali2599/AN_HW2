"""
IF-THEN rules for the fuzzy system for initial route selection based only on the link related parameters
"""


def table_link_param(tr, es, fs):
    if tr == "m" and es == "l" and fs == "b":
        return 'o_vb'  # 1
    if tr == "h" and es == "l" and fs == "b":
        return "o_b"  # 2
    if tr == "m" and es == "h" and fs == "b":
        return "o_b"  # 3
    if tr == "h" and es == "h" and fs == "b":
        return "o_act"  # 4
    if tr == "m" and es == "l" and fs == "g":
        return "o_b"  # 5
    if tr == "h" and es == "l" and fs == "g":
        return "o_act"  # 6
    if tr == "m" and es == "h" and fs == "g":
        return "o_g"  # 7
    if tr == "h" and es == "h" and fs == "g":
        return "o_p"  # 8


"""
IF_THEN rules for the fuzzy system for selecting routing based on link and routh paramters
"""


def table_link_routh_param(tr, es, fs, hc, spdt):
    temp = table_link_param(tr, es, fs)
    if temp == "o_vb":  # first row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_vb"  # 1
        if hc == "sm" and spdt == "ln":
            return "o_b"  # 9
        if hc == "lg" and spdt == "sh":
            return "o_b"  # 17
        if hc == "sm" and spdt == "sh":
            return "o_b"  # 25

    if temp == "o_g":  # seven row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_act"  # 7
        if hc == "sm" and spdt == "ln":
            return "o_act"  # 15
        if hc == "lg" and spdt == "sh":
            return "o_act"  # 23
        if hc == "sm" and spdt == "sh":
            return "o_g"  # 31

    if temp == "o_p":  # eigth row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_act"  # 8
        if hc == "sm" and spdt == "ln":
            return "o_g"  # 16
        if hc == "lg" and spdt == "sh":
            return "o_g"  # 24
        if hc == "sm" and spdt == "sh":
            return "o_p"  # 32

    if tr == "h" and es == "l" and fs == "b":  # second row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_b"  # 2
        if hc == "sm" and spdt == "ln":
            return "o_b"  # 10
        if hc == "lg" and spdt == "sh":
            return "o_b"  # 18
        if hc == "sm" and spdt == "lh":
            return "o_b"  # 26

    if tr == "m" and es == "h" and fs == "b":  # third row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_b"  # 3
        if hc == "sm" and spdt == "ln":
            return "o_b"  # 11
        if hc == "lg" and spdt == "sh":
            return "o_b"  # 19
        if hc == "sm" and spdt == "sh":
            return "o_b"  # 27

    if tr == "h" and es == "h" and fs == "b":  # fourth row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_b"  # 4
        if hc == "sm" and spdt == "ln":
            return "o_b"  # 12
        if hc == "lg" and spdt == "sh":
            return "o_b"  # 20
        if hc == "sm" and spdt == "sh":
            return "o_b"  # 28

    if tr == "m" and es == "l" and fs == "g":  # fifth row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_b"  # 5
        if hc == "sm" and spdt == "ln":
            return "o_b"  # 13
        if hc == "lg" and spdt == "sh":
            return "o_b"  # 21
        if hc == "sm" and spdt == "sh":
            return "o_b"  # 29

    if tr == "h" and es == "l" and fs == "g":  # six row in table 1
        if hc == "lg" and spdt == "ln":
            return "o_b"  # 6
        if hc == "sm" and spdt == "ln":
            return "o_b"  # 14
        if hc == "lg" and spdt == "sh":
            return "o_b"  # 22
        if hc == "sm" and spdt == "sh":
            return "o_b"  # 30
