#!/usr/bin/env python3
"""
scripts/train_linear.py
Run a small linear regression experiment and save config/metrics/plot.
"""

import os
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def run(seed=42, test_size=0.2, outdir="experiments/week1"):
    np.random.seed(seed)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = float(mean_squared_error(y_test, y_pred))
    r2 = float(r2_score(y_test, y_pred))

    os.makedirs(outdir, exist_ok=True)

    config = {"seed": seed, "model": "LinearRegression(sklearn)", "test_size": test_size}
    with open(os.path.join(outdir, "config.json"), "w") as f:
        json.dump(config, f, indent=2)

    metrics = {"mse": mse, "r2": r2}
    with open(os.path.join(outdir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    plt.figure(figsize=(6,4))
    plt.scatter(X_train, y_train, label="train", alpha=0.6)
    plt.scatter(X_test, y_test, label="test", alpha=0.8)
    xs = np.linspace(0, 2, 100).reshape(-1,1)
    ys = model.predict(xs)
    plt.plot(xs, ys, label="predicted", linewidth=2)
    plt.xlabel("X")
    plt.ylabel("y")
    plt.title("Linear Regression")
    plt.legend()
    plot_path = os.path.join(outdir, "regression_plot.png")
    plt.savefig(plot_path, bbox_inches="tight")
    plt.close()

    print("Experiment saved to", outdir)
    print("Metrics:", metrics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--outdir", type=str, default="experiments/week1")
    args = parser.parse_args()
    run(seed=args.seed, test_size=args.test_size, outdir=args.outdir)
