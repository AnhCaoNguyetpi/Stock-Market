# Vietnam Stock Market Research Pipeline

Pipeline nghiên cứu cổ phiếu Việt Nam cho HOSE, HNX và UPCOM. Phiên bản mới ưu tiên
khả năng tái lập, chia dữ liệu theo thời gian và ngăn data leakage.

> Đây là phần mềm nghiên cứu, không phải khuyến nghị đầu tư. Kết quả quá khứ không
> bảo đảm hiệu suất tương lai.

## Cài đặt

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
Copy-Item .env.example .env
```

Yêu cầu Python 3.10+. Điền credential vào `.env`, không ghi trực tiếp trong code.
Token và mật khẩu từng được commit phải được thu hồi và cấp lại trước khi sử dụng.

## Chuẩn bị dữ liệu

Đặt `VNINDEX_cleaned.xlsx`, `HNXINDEX_cleaned.xlsx` và `UPCOM_cleaned.xlsx` trong
`Cleaned data/`. Repository hiện thiếu file VNINDEX đã làm sạch; hãy tạo nó bằng
notebook làm sạch HOSE hoặc sửa `data.hose` trong `configs/default.yaml`.

Các cột tối thiểu: `timestamp`, `ticker`, `open`, `high`, `low`, `close`, `volume`.
Những feature kỹ thuật dùng để train cũng phải có trong file.

## Chạy pipeline

Sửa mốc thời gian trong `configs/default.yaml` cho phù hợp dữ liệu, sau đó chạy:

```powershell
stock-market --config configs/default.yaml train-risk --output artifacts
pytest -q
ruff check src tests
```

Pipeline chỉ train trên tập train, báo cáo validation riêng rồi mới đánh giá test.

## Cấu trúc

- `src/stock_market/data.py`: đọc dữ liệu, chuẩn hóa sàn và kiểm tra schema.
- `src/stock_market/features.py`: feature engineering nhân quả.
- `src/stock_market/labels.py`: nhãn tương lai riêng cho từng ticker.
- `src/stock_market/split.py`: chia train/validation/test theo ngày.
- `src/stock_market/model.py`: LightGBM kèm metadata feature.
- `src/stock_market/cli.py`: điểm chạy thống nhất.
- `tests/`: test lỗi xuyên ticker, tên sàn và split.

## Nguyên tắc đánh giá

- Không train bằng dữ liệu test hoặc chọn ngưỡng sau khi xem test.
- Feature ngày `t` chỉ dùng thông tin có sẵn đến ngày `t`.
- Tín hiệu cuối phiên chỉ được khớp sớm nhất ở phiên kế tiếp.
- Backtest phải tính phí, thuế, trượt giá, thanh khoản, bước giá và lô giao dịch.
- Cần so sánh benchmark và báo cáo CAGR, Sharpe, Sortino, max drawdown, turnover.

Các số liệu 29.35% return và 76.92% win rate trong notebook cũ chỉ là kết quả thử
nghiệm; cần chạy lại bằng pipeline không leakage trước khi công bố hoặc sử dụng.
