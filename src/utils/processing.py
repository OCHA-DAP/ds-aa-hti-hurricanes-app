import pandas as pd

from src.constants import LAURA_ATCF_ID


def speed2cat(speed):
    if pd.isnull(speed):
        return None
    elif speed <= 33:
        return "TD"
    elif speed <= 63:
        return "TS"
    elif speed <= 82:
        return "1"
    elif speed <= 95:
        return "2"
    elif speed <= 112:
        return "3"
    elif speed <= 136:
        return "4"
    else:
        return "5"


def determine_triggers(lt_threshs, monitors, obsv_triggers, sid_atcf):
    dicts = []
    for atcf_id, group in monitors.groupby("atcf_id"):
        for lt_name, threshs in lt_threshs.items():
            dff = group[group["lt_name"] == lt_name]
            dff_p = dff[dff["roll2_rain_dist"] >= threshs.get("p")]
            dff_s = dff[dff["wind_dist"] >= threshs.get("s")]

            if not dff_p.empty and not dff_s.empty:
                pass

            dff_both = dff[
                (dff["roll2_rain_dist"] >= threshs.get("p"))
                & (dff["wind_dist"] >= threshs.get("s"))
            ]
            if not dff_both.empty:
                trig_date = dff_both["issue_time"].min()
                dicts.append(
                    {
                        "atcf_id": atcf_id,
                        "trig_date": trig_date,
                        "lt_name": lt_name,
                        "trig_type": "simul",
                    }
                )

    triggers = pd.DataFrame(dicts)

    triggers = (
        triggers.pivot(
            index=["atcf_id", "trig_type"],
            columns="lt_name",
            values="trig_date",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    triggers = triggers.merge(
        obsv_triggers[obsv_triggers["atcf_id"] != LAURA_ATCF_ID][
            ["atcf_id", "closest_time", "target", "affected_population"]
        ],
        how="outer",
    )
    triggers = triggers.merge(sid_atcf, how="left")
    triggers["target"] = triggers["target"].astype(bool)

    for lt_name in lt_threshs:
        triggers[f"{lt_name}_lt"] = triggers["closest_time"] - triggers[lt_name]
        triggers[f"FN_{lt_name}"] = triggers[lt_name].isna() & triggers["target"]
        triggers[f"FP_{lt_name}"] = ~triggers[lt_name].isna() & ~triggers["target"]
    return triggers
