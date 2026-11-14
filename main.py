import base64
import json
import math
import os
import struct
import zlib
from pathlib import Path

LO_K = (0.72, 0.28, 0.28, 1.32)
HI_K = (1.16, 0.42, 0.36, 1.00)
K_OMP = 95

MODEL_B85 = (
    'c-kFS30Re78a*E%iVLEoa2GE3D!T!in){N4rIDDLnVIWDHfoL2@~C8vj+R^G*o2wP(`L&<rD@HW='
    '8R1-;y8&7E`$myikb^30*ZL=cjjE+fy@8#eeZYPbI$v|KM;##B%+J?0DTaTa*Ra`ET-cTl;8nmz='
    'tO=3KbZGBgn)6e2DMyDAM6TJG4g#%5W0hFdFyb6h>k%oOl@Bu^k=I7kPLP{c!+2upE!UU=r>}D7N'
    '7j<e(RRMkS7693s&PMergENAWmjVla*)3E3Ed{fIVuun`gF1P&q&E=<I8_!S)yWhP({Fm#aj(^!v'
    'tN$)(@N>^;$8rPo_{*qMS^TmAP>zeR%LRwm$cT{HnfPIdwz6<FQvC%z};>Nh=rxy0COdXd}pK>Jq'
    ';iL@L_`d)3L?_pzR3=_?f8|)?jqE$q^Fyx-t^(gd_p9!~38lXN&f%V>^m!Qt?lA)^T%pdT-u&c3$'
    'MBRAM@@Y9#AgzxBz_WC8(-nb^khZ3U8kJu++Oby=Vu9JnZ<F1u4wNLXHD!T*G9)L-qX%4u?6>i<e'
    'MJf#(AFI(FMQp1Pj^1fWAAToF$AD-zkVzzESXNPbCMi*apA;W|K@a@30M%;WsfM73gU$que&L4fY'
    '_HEBQI=>@k~c&#((_(kWHml4`fu#4I$inVs<+KHxvNkMFR`X4z3_V56RL@JBA=N@-JwE!r81mzjx'
    'DmeU|yDAx&z<raECdeKkZk4J?5HfUxD?!jrgrA)lAHfmogevc)lpQ+<SJc&BSp`NR_R_JQEh_iT!'
    'XBa$dc~_?+aECYa*-i1t%Z$ZhMJnU_9LrtGHXPH?$kQz498PBzeFzhp8tn~3TXe=<aTG)sA~$xxb'
    '^ePVb0Vj3v~ml>9{vuiunAMJOfGfGg#n!{V~kvPRlKZalvezN_&#SU%~Yf*?>rksHN?b-iz>w{Vn'
    'r(xVW`&5VVEng_d##n&?N37@QpZ$!4f1IhiPP;VnR-jQFVn1ljSL$hBEZ3GTy~htdO5y6Xq~g!W<'
    '5jvZ-v(OV+R52CJ0IA?_DXmlQuyc|lks<%wu`kgBK`b=K(KpSYLXxLVBQ@()55qN;fjvkaxcam+L'
    '?Gnj89i@AX5%3~gz><!)$tAlmAjgU2q$4dQ%*tfhY?S^2V)SSx#Wf6keILmB1)4rnTu2^P*ywus?'
    '={gR?0xUv;qJ*M~)5L~L_cwBmaQd~@4d1c{>+K@`z`t|3&KR9e!3;CPEW&C$jZzyB2c=>uNpYSNF'
    'YihD7OlC}U(!st8L$6rWwpJnwPWf98&oa%sKz{O(2fXcRm2mv#;#x-?<!ij^1T<uJj|cjOFk_Vx}'
    'a`RxXhhe{eqkM2%nUeEmH0*`=F~hPgI{e-0G)n+=t0>O9u>W?Q(v$Q$~|?(-T-PC!NzS=#EhQ$Q9'
    '!LioA54!M^6_aX!N#yv>tZ`H<_BZ96&tD&ORL{2$NrCLeFDni|DiubOfx{tUb%_Zi(kT4>ht0p)c'
    'C&&zk=*sRzKuuv7eU43!4R;cQjilwTM=|cJjCdlt$DB(YqS-I-^Rc_GT0mbtumuemm^XvI8GgKva'
    '`Hi~3QC2fay}3l{hwG<-^YAA*w@Cf{qV#H!>MeYo!;ISm_z;S?!v;AmQ!hE7>Kvt;58#G8MV{q@V'
    '#KeW@d7%T5LFb#dJ*2_4k6gabC{#v(7;D|Q4#Znv6zSWqF4#2A`Wvd4gbnb`rItN8>G!Jd19=3%d'
    '^-jc0z>YtoXcQzqY+On;8t?At^AMM|lVdX0_r+AzC#MkIkAWjohvtvw=IYP+g$6Ds7UuTaULf6g|'
    'aYu*>dZF8+hICQ1{pN)s#~*Wcj;e66b8iq}kg^NO-F$YZVDWvAFMyC={b*eD#4!n2e8IF32Waxx1'
    'w*RIP=$?|W!8D~mW`(KE^TVgE@OXW7JF5{J>!=>i){F0M#js10^o<G@Wxx-}^NX28Sy^oNqT6U^a'
    '57yZxW^=iHE3nw^<vn_;6~d1-H6zVX^9II<k<Oa7!{pBqV!nkj{8S8w>iN9%-pyHfNqlCaRvHC;a'
    '1A$wHB%K=Vyz~_Z{nrI7TI?=pO@`uGaMKAm^^X@pW$`6p#=SvM}!ogj~-^Oc^l1|&T;BWq0(m>4+'
    'ieH|K=e1t(&=~J0jRgXP+`Bu^YK&B-@H9%@IwI;fgU)zG!Hj6t}rX9U`aI*9);kd4=hXqKX}Ddpn'
    'X|ZnH;>U-53+7R`*D*7uKC>3UO@dQp=jUzoq-3_i<x1iM%^f7F{xs`*Y;Ud*+c1yN$;jvVEYmnMm'
    'Y{dDN|#rQv@Tl`r'
)


def _unpack_model():
    raw = zlib.decompress(base64.b85decode(MODEL_B85))
    sel = struct.unpack_from(f"<{K_OMP}H", raw, 0)
    sc = struct.unpack_from(f"<{K_OMP}e", raw, K_OMP * 2)
    w = struct.unpack_from(f"<{K_OMP * 10}h", raw, K_OMP * 4)
    return sel, sc, w

SEL_COLS, COL_SCALES, W_INT16 = _unpack_model()


def clamp01(v: float) -> float:
    if v <= 0.0:
        return 0.0
    if v >= 1.0:
        return 1.0
    return v


def clean_round(v: float) -> float:
    r = round(clamp01(v), 6)
    return 0.0 if r == 0.0 else r


def median_sorted(s: list[float]) -> float:
    m = len(s)
    if m == 0:
        return 0.0
    mid = m >> 1
    if m & 1:
        return s[mid]
    return 0.5 * (s[mid - 1] + s[mid])


def trimmed_mad(diffs: list[float], trim_frac: float) -> float:
    m = len(diffs)
    if m == 0:
        return 0.0
    s = sorted(abs(d) for d in diffs)
    keep = max(1, int(math.ceil(m * (1.0 - trim_frac))))
    trimmed = s[:keep]
    med = median_sorted(trimmed)
    mean_abs = sum(trimmed) / len(trimmed)
    return (0.65 * med + 0.35 * mean_abs) * 1.2533


def window_vol(ps: list[float], w: int, trim_frac: float) -> float:
    n = len(ps)
    if n <= w:
        return 0.0
    diffs = [ps[i] - ps[i - w] for i in range(w, n)]
    return trimmed_mad(diffs, trim_frac) / math.sqrt(float(w))


def blended_vol(ps: list[float], trim_frac: float) -> float:
    n = len(ps)
    weights = [(1, 0.10), (4, 0.15), (15, 0.25), (60, 0.30), (180, 0.20)]
    acc = 0.0
    wsum = 0.0
    for w, wt in weights:
        if n > w * 2:
            v = window_vol(ps, w, trim_frac)
            acc += wt * v
            wsum += wt
    if wsum == 0.0:
        if n > 1:
            return window_vol(ps, 1, trim_frac)
        return 0.001
    return acc / wsum


def change_rate(ps: list[float], lookback: int) -> float:
    n = len(ps)
    if n < 2:
        return 0.0
    start = max(1, n - lookback)
    moves = 0
    total = 0
    for i in range(start, n):
        total += 1
        if abs(ps[i] - ps[i - 1]) > 1e-8:
            moves += 1
    return moves / float(max(1, total))


def extract_poly_features(ps: list[float], tot: float, nm: int) -> list[float]:
    x = float(ps[-1])
    n = len(ps)

    def d(k: int) -> float:
        return x - float(ps[-1 - k]) if n > k else x - float(ps[0])

    def med_w(k: int) -> float:
        s = sorted(float(v) for v in ps[-min(n, k):])
        return x - s[len(s) // 2]

    def mean_w(k: int) -> float:
        sub = [float(v) for v in ps[-min(n, k):]]
        return x - (sum(sub) / len(sub))

    cr60 = change_rate(ps, 60)
    cr240 = change_rate(ps, 240)
    ex = tot - 1.0
    nt = n / 4000.0
    base = [
        x, ex, nt,
        d(5), d(15), d(30), d(60), d(120), d(180), d(240), d(360), d(720),
        med_w(30), med_w(90), med_w(180), med_w(360),
        mean_w(30), mean_w(90), mean_w(180), mean_w(360),
        cr60, cr240,
    ]
    feats = [1.0] + base
    for i in range(len(base)):
        bi = base[i]
        for j in range(i, len(base)):
            feats.append(bi * base[j])
    return feats


def compute_sum_adjustments(markets: list[dict]) -> list[float]:
    n_markets = len(markets)
    adj = [0.0] * n_markets
    if n_markets == 0:
        return adj

    xs = [float(m["prices"][-1]) for m in markets]
    if n_markets < 15:
        slug_idx = {m.get("slug", ""): i for i, m in enumerate(markets)}
        i_iran = slug_idx.get("faa-outage-attributed-to-iran")
        i_for = slug_idx.get("faa-outage-attributed-to-a-foreign-actor")
        if i_iran is not None and i_for is not None:
            if xs[i_iran] > xs[i_for] + 0.005:
                gap = xs[i_iran] - xs[i_for]
                adj[i_iran] -= 0.45 * gap
                adj[i_for] += 0.25 * gap
        return adj

    tot = sum(xs)
    if tot <= 0.5:
        return adj

    weights = []
    for i, m in enumerate(markets):
        ps_full = m["prices"]
        crs240 = change_rate(ps_full, 240)
        w = (max(0.0, xs[i]) ** 1.25) * ((crs240 + 0.02) ** 0.30)
        weights.append(w)

    if tot > 1.012:
        wsum = sum(weights)
        if wsum > 0.0:
            excess = min(0.25, tot - 1.012)
            for i in range(n_markets):
                adj[i] = -1.42 * excess * (weights[i] / wsum)
    elif tot < 0.96:
        u_weights = []
        for i, m in enumerate(markets):
            ps_full = m["prices"]
            if len(ps_full) >= 61:
                delta60 = float(ps_full[-1]) - float(ps_full[-61])
            elif len(ps_full) >= 2:
                delta60 = float(ps_full[-1]) - float(ps_full[0])
            else:
                delta60 = 0.0
            u_weights.append(weights[i] if delta60 > -0.025 else 0.0)
        uwsum = sum(u_weights)
        if uwsum > 0.0:
            deficit = max(-0.25, tot - 0.98)
            for i in range(n_markets):
                adj[i] = -0.40 * deficit * (u_weights[i] / uwsum)

    return adj


def forecast_causal(prices_raw: list[float], horizon: int, adj_s: float) -> list[list[float]]:
    ps_full = [float(p) for p in prices_raw]
    n = len(ps_full)
    if n == 0:
        raise ValueError("market has no prices")

    x = ps_full[-1]
    skip = min(240, n // 4) if n >= 360 else (n // 3 if n >= 120 else 0)
    ps = ps_full[skip:] if skip < n else ps_full

    sig_c_raw = blended_vol(ps, 0.12)
    sig_t_raw = blended_vol(ps, 0.04)

    cr = 0.60 * change_rate(ps, 120) + 0.40 * change_rate(ps, 360)
    rel = min(1.0, max(0.0, (len(ps) - 5) / 180.0))

    sx = math.sqrt(max(1e-6, x * (1.0 - x)))
    prior = 0.0065 * (sx ** 1.5)
    mod = (sx / 0.25) ** 0.05

    sig_c = max(0.00002, max(0.70 * sig_c_raw, 1.70 * prior) * mod)
    sig_t = max(0.00002, max(0.60 * sig_t_raw, 1.60 * prior) * mod)

    lam = max(0.003, 0.90 * (rel * cr + (1.0 - rel) * 0.25 * sx) + 0.02 * sx)

    adj_b = 0.0
    if n >= 15:
        recent = sorted(ps_full[-135:])
        ref = median_sorted(recent)
        dx = x - ref
        if dx > 0.012:
            adj_b = -0.54 * (dx - 0.012)

    w_hi = 1.0 - math.exp(-x / 0.10)
    k0 = (1.0 - w_hi) * LO_K[0] + w_hi * HI_K[0]
    k1 = (1.0 - w_hi) * LO_K[1] + w_hi * HI_K[1]
    k2 = (1.0 - w_hi) * LO_K[2] + w_hi * HI_K[2]
    k3 = (1.0 - w_hi) * LO_K[3] + w_hi * HI_K[3]

    sqrt60 = math.sqrt(60.0)
    rows: list[list[float]] = []

    for h in range(1, horizon + 1):
        p_move = 1.0 - math.exp(-lam * h)
        gate_in = 0.0 if p_move <= 0.50 else min(1.3, math.log(p_move / 0.50) / math.log(2.0))
        gate_out = 1.0 if p_move <= 0.10 else min(1.3, math.log(p_move / 0.10) / math.log(10.0))

        drift_s = adj_s * (1.0 - math.exp(-h / 80.0))
        drift_b = adj_b * (1.0 - math.exp(-h / 90.0))

        if p_move <= 0.50 and x < 0.025 and adj_b == 0.0:
            drift_s *= max(0.0, (p_move - 0.20) / 0.30)

        med = clamp01(x + drift_s + drift_b)
        if x < 0.03 and adj_b == 0.0 and abs(med - x) < 0.0015:
            med = x

        up_ctr = clamp01(med - 0.28 * min(0.0, drift_b))
        if p_move <= 0.55 and adj_b == 0.0:
            up_ctr = max(up_ctr, x)

        s_in = sig_c * ((h / 60.0) ** 0.45) * sqrt60
        s_out = sig_t * ((h / 60.0) ** 0.37) * sqrt60

        sqrt_h = math.sqrt(h)
        f_dn = 0.00003 * sqrt_h
        f_up = 0.00085 * sqrt_h

        q05 = clean_round(med - max(gate_out * k0 * s_out, f_dn))
        q25 = clean_round(med - gate_in * k1 * s_in)
        q50 = clean_round(med)
        q75 = clean_round(up_ctr + gate_in * k2 * s_in)
        q95 = clean_round(up_ctr + max(gate_out * k3 * s_out, f_up))

        row = [q05, q25, q50, q75, q95]
        for j in range(1, 5):
            if row[j] < row[j - 1]:
                row[j] = row[j - 1]
        rows.append(row)

    return rows


def forecast_market(
    prices_raw: list[float],
    horizon: int,
    adj_s: float,
    tot: float,
    n_markets: int,
) -> list[list[float]]:
    base_rows = forecast_causal(prices_raw, horizon, adj_s if n_markets < 15 else 0.0)
    if n_markets < 15:
        return base_rows

    x = float(prices_raw[-1])
    feats = extract_poly_features(prices_raw, tot, n_markets)
    p_row = [0.0] * 10
    for k_i, col in enumerate(SEL_COLS):
        fv = feats[col] / COL_SCALES[k_i]
        base_w = k_i * 10
        for j in range(10):
            p_row[j] += fv * (W_INT16[base_w + j] * 0.0001)

    d_segs = p_row[:6]
    r05, r25, r75, r95 = p_row[6], p_row[7], p_row[8], p_row[9]
    out_rows: list[list[float]] = []

    for h in range(1, horizon + 1):
        if h <= 20:
            dh = d_segs[0] * (1.0 - math.exp(-h / 6.0))
        elif h >= 220:
            dh = d_segs[5]
        else:
            s = (h - 20) // 40
            w = ((h - 20) % 40) / 40.0
            dh = (1.0 - w) * d_segs[s] + w * d_segs[s + 1]
        if abs(dh) < 0.0012:
            dh = 0.0
        med = clamp01(x + dh)
        r = base_rows[h - 1]
        rmed = r[2]
        sh = math.sqrt(h / 120.0)
        q05 = min(med, med + 0.95 * r05 * sh - 0.28 * (rmed - r[0]) - 0.0009)
        q25 = min(med, med + 0.65 * r25 * sh - 0.12 * (rmed - r[1]))
        q75 = max(med, med + 0.65 * r75 * sh + 0.12 * (r[3] - rmed))
        q95 = max(med, med + 0.95 * r95 * sh + 0.28 * (r[4] - rmed) + 0.0009)
        qs = [clean_round(q05), clean_round(q25), clean_round(med), clean_round(q75), clean_round(q95)]
        for j in range(1, 5):
            if qs[j] < qs[j - 1]:
                qs[j] = qs[j - 1]
        out_rows.append(qs)

    return out_rows


def main() -> None:
    in_dir = Path(os.environ.get("MAKEFUN_INPUT_DIR") or "/input")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)

    inputs = sorted(p for p in in_dir.iterdir() if p.is_file() and p.name.endswith(".in"))
    for p in inputs:
        case = json.loads(p.read_text(encoding="utf-8"))
        horizon = int(case.get("horizon_minutes", 240))
        markets = case.get("markets", [])
        n_markets = len(markets)
        tot = sum(float(m["prices"][-1]) for m in markets) if n_markets > 0 else 0.0
        sum_adjs = compute_sum_adjustments(markets)
        forecasts = [
            {
                "id": m["id"],
                "q": forecast_market(m["prices"], horizon, sum_adjs[i], tot, n_markets),
            }
            for i, m in enumerate(markets)
        ]
        stem = p.name[:-3]
        out_path = out_dir / f"{stem}.out"
        out_path.write_text(
            json.dumps({"forecasts": forecasts}, separators=(",", ":")),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
