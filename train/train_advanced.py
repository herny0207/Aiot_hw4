"""
train_advanced.py
使用 MediaPipe 關鍵點資料訓練兩個模型:
  Model A: SVM (RBF Kernel)
  Model B: Random Forest
比較兩者的 Accuracy, Precision, Recall, F1-Score，
並自動選擇最佳模型儲存至 demo 資料夾。
"""
import os
import joblib
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix
)


def evaluate_model(name, model, X_test, y_test, threshold=0.6):
    """
    評估模型效能，並加入信心值門檻 (threshold) 判斷。
    若預測機率低於門檻，則歸類為 Error (-1)，用以排除非剪刀、石頭、布的未知手勢。
    """
    y_proba = model.predict_proba(X_test)
    y_pred = []
    for p in y_proba:
        if np.max(p) < threshold:
            y_pred.append(-1)  # -1 代表 Error / Unknown
        else:
            y_pred.append(np.argmax(p))
            
    y_pred = np.array(y_pred)
    
    # 計算一般指標時，我們只看非 Error 的部分，或是把 Error 當成預測錯誤
    # 這裡我們把 -1 也當作一個類別來計算
    labels_with_error = [-1, 0, 1, 2]
    target_names = ['Error', 'Rock', 'Paper', 'Scissors']
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, labels=[0, 1, 2], average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, labels=[0, 1, 2], average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, labels=[0, 1, 2], average='weighted', zero_division=0)

    print(f"\n{'=' * 45}")
    print(f"  📊 {name} Results (Threshold = {threshold})")
    print(f"{'=' * 45}")
    print(f"  Accuracy (incl. Error): {acc:.4f}")
    print(f"  Precision (RPS only):   {prec:.4f}")
    print(f"  Recall (RPS only):      {rec:.4f}")
    print(f"  F1-Score (RPS only):    {f1:.4f}")
    
    error_count = np.sum(y_pred == -1)
    print(f"  🚨 Rejections (Error):  {error_count} / {len(y_test)} samples")

    print(f"\n  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=labels_with_error)
    print(f"  {'':>10s} {'Pred_Err':>9s} {'Pred_R':>8s} {'Pred_P':>8s} {'Pred_S':>8s}")
    # y_test 中不會有 -1，所以實際類別只有 Rock, Paper, Scissors (對應 index 1, 2, 3)
    for i, true_label in enumerate(['Rock', 'Paper', 'Scissors']):
        row = cm[i + 1] # +1 因為 cm 的第 0 個 row 是 true_label=-1
        print(f"  {true_label:>10s} {row[0]:>9d} {row[1]:>8d} {row[2]:>8d} {row[3]:>8d}")
        
    print(f"\n  Detailed Classification Report:")
    # 由於 y_test 沒有 -1，classification_report 可能會給出 warning，所以我們安全處理
    print(classification_report(y_test, y_pred, labels=labels_with_error, target_names=target_names, zero_division=0))

    return {'name': name, 'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'model': model}


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'train', 'landmark_data.joblib')

    if not os.path.exists(data_path):
        print(f"❌ Error: Landmark data not found at {data_path}")
        print("   Please run extract_landmarks.py first!")
        return

    print("=" * 50)
    print("  Advanced Model Training (Landmark-based)")
    print("=" * 50)

    # === Load Data ===
    print("\n⏳ Loading landmark data...")
    data = joblib.load(data_path)
    X_train, y_train = data['X_train'], data['y_train']
    X_test, y_test = data['X_test'], data['y_test']
    print(f"   Train: {len(X_train)} samples, Test: {len(X_test)} samples")
    print(f"   Features per sample: {X_train.shape[1]}")

    # === Model A: SVM (RBF Kernel) ===
    print("\n🔧 Training Model A: SVM (RBF Kernel, C=10.0)...")
    svm_model = SVC(kernel='rbf', probability=True, C=10.0, gamma='scale')
    svm_model.fit(X_train, y_train)
    results_svm = evaluate_model("SVM (RBF)", svm_model, X_test, y_test)

    # === Model B: Random Forest ===
    print("\n🔧 Training Model B: Random Forest (n=200, depth=15)...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1  # 使用所有 CPU 核心
    )
    rf_model.fit(X_train, y_train)
    results_rf = evaluate_model("Random Forest", rf_model, X_test, y_test)

    # === Comparison Summary ===
    print("\n" + "=" * 50)
    print("  🏆 Model Comparison Summary")
    print("=" * 50)
    print(f"  {'Metric':<12s} {'SVM':>10s} {'RF':>10s} {'Winner':>10s}")
    print(f"  {'-' * 42}")

    metrics = [('Accuracy', 'acc'), ('Precision', 'prec'), ('Recall', 'rec'), ('F1-Score', 'f1')]
    for label, key in metrics:
        svm_val = results_svm[key]
        rf_val = results_rf[key]
        winner = "SVM" if svm_val >= rf_val else "RF"
        print(f"  {label:<12s} {svm_val:>10.4f} {rf_val:>10.4f} {winner:>10s}")

    # === Save Best Model ===
    best = results_svm if results_svm['acc'] >= results_rf['acc'] else results_rf
    print(f"\n  🥇 Best Model: {best['name']} (Accuracy: {best['acc']:.4f})")

    demo_dir = os.path.join(base_dir, 'demo')
    os.makedirs(demo_dir, exist_ok=True)

    model_save_path = os.path.join(demo_dir, 'best_landmark_model.pkl')
    joblib.dump(best['model'], model_save_path)
    print(f"\n✅ Best model saved to: {model_save_path}")
    print("   → Use this model with carema_landmark.py for real-time demo.")


if __name__ == "__main__":
    main()
