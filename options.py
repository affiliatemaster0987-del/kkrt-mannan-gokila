# ═══════════════════════════════════════════════
#  options.py — Option chain data store (extend here)
#  PCR / Max Pain / OI — broker API (smart_client.py)
#  connect pannina live data inga varum.
# ═══════════════════════════════════════════════
oc_store = {
    "pcr": None,
    "max_pain": None,
    "oi_buildup": None,     # "LONG BUILD" / "SHORT BUILD"
    "writing_bias": None,   # "PUT > CALL" / "CALL > PUT"
    "strikes": [],          # [{strike, call_oi, put_oi}]
}


def update_option_chain(pcr=None, max_pain=None, oi_buildup=None,
                        writing_bias=None, strikes=None):
    if pcr is not None:
        oc_store["pcr"] = pcr
    if max_pain is not None:
        oc_store["max_pain"] = max_pain
    if oi_buildup is not None:
        oc_store["oi_buildup"] = oi_buildup
    if writing_bias is not None:
        oc_store["writing_bias"] = writing_bias
    if strikes is not None:
        oc_store["strikes"] = strikes
    return oc_store


def get_option_chain():
    return oc_store
