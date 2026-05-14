# AIoT HW4 - Rock-Paper-Scissors 手勢辨識系統

本專案為 AIoT 系統實務課程作業 (HW4)。我們將原本基於灰階像素的猜拳 (剪刀、石頭、布) 辨識系統，升級為基於 **MediaPipe Hands** 的關鍵點 (Landmarks) 特徵提取架構，並在 **Raspberry Pi 4** 上進行即時推論展示。

## 🌟 專案亮點與特點

- **高精準特徵提取**：使用 MediaPipe 提取 21 個手部骨架關鍵點，將原本的像素特徵降維為 63 維的座標特徵。
- **抗干擾能力強**：針對骨架座標進行平移與比例正規化，徹底排除環境光線、背景雜訊以及手掌遠近大小的影響。
- **雙模型比較與優化**：訓練並比較了 SVM (支持向量機) 與 Random Forest (隨機森林) 的效能。最終採用準確率高達 93.77% 的 **SVM (RBF Kernel)** 模型。
- **即時邊緣運算**：在 Raspberry Pi 4 上透過 USB 攝影機即時讀取影像，並保持順暢的推論速度。支援辨識：`Rock` (石頭)、`Scissors` (剪刀)、`Paper` (布) 以及 `Error` (錯誤/無效手勢)。

---

## 📁 專案架構

```text
RSP_demo/
├── dataset/                    # 訓練與測試的原始影像資料集
├── train/                      # 訓練腳本目錄
│   ├── extract_landmarks.py    # 將影像資料集轉換為 MediaPipe 骨架特徵 (landmark_data.joblib)
│   └── train_advanced.py       # 訓練 SVM 與 Random Forest 模型，並輸出效能報告
├── demo/                       # 邊緣設備推論腳本目錄
│   ├── rps_svm_model.pkl       # 訓練好的 SVM 模型權重
│   ├── rps_rf_model.pkl        # 訓練好的隨機森林模型權重
│   ├── test.py                 # 針對靜態測試集圖片進行模型準確率驗證
│   ├── carema_svm.py           # (備用) 呼叫 SVM 模型的即時攝影機程式
│   ├── carema_rf.py            # (備用) 呼叫隨機森林模型的即時攝影機程式
│   └── carema_landmark.py      # 主要即時攝影機辨識程式 (預設載入最佳模型)
├── hand_landmarker.task        # MediaPipe Tasks API 所需的手部地標模型檔
├── Technical_Report.html       # 專案技術報告原檔
├── create_report.py            # 產生技術報告 PDF 的腳本
└── README.md                   # 專案說明文件
```

---

## 🚀 快速開始 (Raspberry Pi 4 部署)

### 1. 環境需求與安裝
確保您的 Raspberry Pi 4 運行的是 **64-bit OS**，並已連接 USB 攝影機。

開啟終端機並安裝必備套件：
```bash
sudo apt update
sudo apt install -y python3-pip python3-opencv libatlas-base-dev
pip3 install mediapipe opencv-python numpy scikit-learn joblib --break-system-packages
```
*(註：若使用虛擬環境，請先建立並進入 venv 後再執行 pip install。)*

### 2. 下載專案並執行測試集評估
```bash
# 進入 demo 資料夾
cd ~/RSP_demo/demo

# 執行測試集準確率驗證 (test.py)
python3 test.py
```

### 3. 執行即時攝影機手勢辨識
執行 `carema_landmark.py` 來啟動 USB 攝影機，並展示即時的剪刀、石頭、布辨識：
```bash
python3 carema_landmark.py
```
- 按下 `q` 鍵可退出程式。
- 按下 `s` 鍵可將當下畫面截圖並儲存。

---

## 📊 模型效能比較 (測試集實測)

本專案實作了兩種機器學習模型，經過正規化後的 MediaPipe 特徵訓練，其效能指標如下：

| 指標 (Metric) | SVM+mediapipe (最佳) | Random Forest |
|:---:|:---:|:---:|
| Accuracy (準確率) | **0.9377** | 0.7696 |
| Precision (精確率) | **0.9450** | 0.8647 |
| Recall (召回率) | **0.9377** | 0.7696 |
| F1-Score (F1值) | **0.9364** | 0.7447 |

**分析結論：**
SVM (RBF Kernel) 完美發揮了處理中低維度連續型資料的優勢，能精確地區分不同手勢間的幾何空間距離；而隨機森林在此類連續座標的切分上較易產生過度分割，導致在「布」等複雜特徵判斷上容易混淆。因此，部署至邊緣裝置時，我們選用效能最優的 SVM 模型。

---

## 📝 技術報告
本專案完整的技術細節、更改模型的原因以及詳細比較，皆收錄於本專案目錄下的 `Final_Report.pdf` (由 `create_report.py` 生成)。
