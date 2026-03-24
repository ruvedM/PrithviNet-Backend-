# Compliance Analyzer Engine
from .compliance_limits import LIMITS, RECOMMENDATIONS

def analyze_compliance(report):
    results = {}
    compliant = 0
    total = 0
    for section, params in report.items():
        if isinstance(params, dict):
            for param, value in params.items():
                total += 1
                limit = LIMITS.get(param)
                if limit is None:
                    continue
                if isinstance(limit, tuple):  # Range (e.g. pH)
                    min_limit, max_limit = limit
                    if min_limit <= value <= max_limit:
                        status = "Compliant"
                        excess = 0
                        compliant += 1
                    else:
                        status = "Violation"
                        excess = value - max_limit if value > max_limit else min_limit - value
                else:
                    if value <= limit:
                        status = "Compliant"
                        excess = 0
                        compliant += 1
                    else:
                        status = "Violation"
                        excess = value - limit
                results[param] = {
                    "value": value,
                    "limit": limit,
                    "status": status,
                    "excess": excess
                }
    score = (compliant / total) * 100 if total else 0
    return results, score

def generate_notice(report, analysis, score):
    violations = []
    recommendations = []
    for param, res in analysis.items():
        if res["status"] == "Violation":
            violations.append({
                "parameter": param,
                "value": res["value"],
                "limit": res["limit"],
                "excess": res["excess"]
            })
            rec = RECOMMENDATIONS.get(param)
            if rec:
                recommendations.append(rec)
    status = "Compliant" if not violations else "Non-Compliant"
    return {
        "industry": report["industry_name"],
        "status": status,
        "violations": violations,
        "recommendations": recommendations,
        "compliance_score": int(score)
    }
