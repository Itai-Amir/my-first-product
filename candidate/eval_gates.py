from typing import Any, Dict, List, Tuple


def _to_list(x):
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return list(x)
    return [x]


def _extract_range(comp: Any) -> Tuple[float, float]:
    """Extract numeric min/max from a compensation object.

Accepts forms like: number (treated as exact), {min, max}, or {'expected_min','expected_max'}.
Raises ValueError if values are missing or not numbers.
"""
    if comp is None:
        raise ValueError("missing compensation")
    if isinstance(comp, (int, float)):
        return float(comp), float(comp)
    if isinstance(comp, dict):
        # support several common keys
        for a, b in (('min', 'max'), ('expected_min', 'expected_max'), ('low', 'high')):
            if a in comp and b in comp:
                return float(comp[a]), float(comp[b])
        # single number fields
        for k in ('expected', 'value'):
            if k in comp:
                v = comp[k]
                return float(v), float(v)
    raise ValueError("invalid compensation format")


def evaluate_hard_gates(job_profile: Dict[str, Any], kp: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate hard gates in fixed order: ai-core, work-mode, compensation.

    Returns a dict: {'passed': bool, 'failed_gate': Optional[str], 'reasons': List[str]}.

    Assumptions made:
    - job_profile may use keys 'ai_core_required'|'requires_ai_core'|'ai_core'.
    - work mode values are strings or lists and must intersect.
    - compensation is required on both sides and represented as number or {min,max}.
    - Missing required fields cause immediate failure.
    """
    reasons: List[str] = []

    # 1) AI-core gate
    ai_keys = ('ai_core_required', 'requires_ai_core', 'ai_core')
    ai_req = None
    for k in ai_keys:
        if k in job_profile:
            ai_req = bool(job_profile[k])
            break
    if ai_req:
        cand_ai = bool(kp.get('ai_core')) if isinstance(kp, dict) else False
        if not cand_ai:
            return {'passed': False, 'failed_gate': 'ai_core', 'reasons': ['candidate missing ai_core']}

    # 2) Work-mode gate
    # job_profile may specify 'work_mode' (str or list)
    if 'work_mode' in job_profile:
        job_modes = _to_list(job_profile['work_mode'])
        cand_modes = _to_list(kp.get('work_mode') or kp.get('work_modes'))
        # intersection check
        if not set(job_modes).intersection(set(cand_modes)):
            return {'passed': False, 'failed_gate': 'work_mode', 'reasons': ['work mode mismatch']}

    # 3) Compensation gate
    # job_profile expected to contain company compensation band under 'compensation' or 'company_compensation'
    comp_keys = ('compensation', 'company_compensation', 'company_band')
    job_comp = None
    for k in comp_keys:
        if k in job_profile:
            job_comp = job_profile[k]
            break
    cand_comp = kp.get('compensation') if isinstance(kp, dict) else None
    if job_comp is not None or cand_comp is not None:
        try:
            jmin, jmax = _extract_range(job_comp)
            cmin, cmax = _extract_range(cand_comp)
        except Exception:
            return {'passed': False, 'failed_gate': 'compensation', 'reasons': ['invalid or missing compensation range']}
        # no overlap => fail
        if cmax < jmin or cmin > jmax:
            return {'passed': False, 'failed_gate': 'compensation', 'reasons': ['no compensation overlap']}

    return {'passed': True, 'failed_gate': None, 'reasons': []}
