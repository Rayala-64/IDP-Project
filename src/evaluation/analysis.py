import os
import pandas as pd
import matplotlib.pyplot as plt

DENSITIES = ["No_Fog", "Medium_Fog", "Dense_Fog"]

def load_results(base_path="results"):
    data = {}
    for density in DENSITIES:
        path = os.path.join(base_path, density, "metrics", "results.csv")
        if os.path.exists(path):
            df = pd.read_csv(path)
            data[density] = df
        else:
            print(f"[WARN] Missing: {path}")
    return data

def compute_summary(data):
    summary = []
    for density, df in data.items():
        fog_det = df["fog_count"].mean()
        simple_det = df["simple_count"].mean()
        dcp_det = df["dcp_count"].mean()
        fog_conf = df["fog_avg_conf"].mean()
        simple_conf = df["simple_avg_conf"].mean()
        dcp_conf = df["dcp_avg_conf"].mean()

        fog_yield = fog_det * fog_conf
        simple_yield = simple_det * simple_conf
        dcp_yield = dcp_det * dcp_conf

        simple_pri = simple_yield / fog_yield if fog_yield != 0 else float("nan")
        dcp_pri = dcp_yield / fog_yield if fog_yield != 0 else float("nan")

        row = {
            "density": density,
            "fog_det": fog_det,
            "simple_det": simple_det,
            "dcp_det": dcp_det,
            "fog_conf": fog_conf,
            "simple_conf": simple_conf,
            "dcp_conf": dcp_conf,
            "simple_pri": simple_pri,
            "dcp_pri": dcp_pri,
        }
        summary.append(row)
    return pd.DataFrame(summary)

def plot_detection(summary, save_dir):
    plt.figure()
    x = summary["density"]
    plt.plot(x, summary["fog_det"], marker='o', label="Fog")
    plt.plot(x, summary["simple_det"], marker='o', label="Simple DCP")
    plt.plot(x, summary["dcp_det"], marker='o', label="Full DCP")
    plt.xlabel("Fog Density")
    plt.ylabel("Avg Detection Count")
    plt.title("Detection vs Fog Density")
    plt.legend()
    plt.savefig(os.path.join(save_dir, "detection.png"))
    plt.close()

def plot_confidence(summary, save_dir):
    plt.figure()
    x = summary["density"]
    plt.plot(x, summary["fog_conf"], marker='o', label="Fog")
    plt.plot(x, summary["simple_conf"], marker='o', label="Simple DCP")
    plt.plot(x, summary["dcp_conf"], marker='o', label="Full DCP")
    plt.xlabel("Fog Density")
    plt.ylabel("Avg Confidence")
    plt.title("Confidence vs Fog Density")
    plt.legend()
    plt.savefig(os.path.join(save_dir, "confidence.png"))
    plt.close()

def plot_pri(summary, save_dir):
    plt.figure()
    x = summary["density"]
    plt.plot(x, summary["simple_pri"], marker='o', label="Simple DCP PRI")
    plt.plot(x, summary["dcp_pri"], marker='o', label="Full DCP PRI")
    plt.xlabel("Fog Density")
    plt.ylabel("PRI")
    plt.title("Perception Recovery Index vs Fog Density")
    plt.legend()
    plt.savefig(os.path.join(save_dir, "pri.png"))
    plt.close()

def interpret_pri(pri):
    if pri < 1.0:
        return "Perception Degradation"
    if 1.0 <= pri < 1.5:
        return "Minimal Recovery"
    if 1.5 <= pri < 3.0:
        return "Moderate Recovery"
    return "Strong Recovery"

def print_insights(summary):
    print("\n===== SUMMARY =====\n")
    print(summary.round(3))
    print("\n===== KEY OBSERVATIONS =====\n")
    for _, row in summary.iterrows():
        d = row["density"]
        print(f"\n--- {d} ---")
        if row["simple_det"] > row["fog_det"]:
            print("✔ Simple DCP improves detection")
        else:
            print("❌ Simple DCP does NOT improve detection")
        if row["dcp_det"] > row["fog_det"]:
            print("✔ Full DCP improves detection")
        else:
            print("❌ Full DCP does NOT improve detection")
        if row["dcp_conf"] > row["simple_conf"]:
            print("✔ Full DCP better than Simple DCP (confidence)")
        else:
            print("❌ Full DCP not better than Simple DCP")
        print(f"Simple PRI = {row['simple_pri']:.3f} ({interpret_pri(row['simple_pri'])})")
        print(f"Full DCP PRI = {row['dcp_pri']:.3f} ({interpret_pri(row['dcp_pri'])})")

def run_analysis():
    data = load_results()
    summary = compute_summary(data)
    os.makedirs("results/plots", exist_ok=True)
    summary.to_csv("results/plots/summary.csv", index=False)
    plot_detection(summary, "results/plots")
    plot_confidence(summary, "results/plots")
    plot_pri(summary, "results/plots")
    print_insights(summary)
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    run_analysis()