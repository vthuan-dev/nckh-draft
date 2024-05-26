# Dự án Simple Blockchain Demo bằng Python chỉ sử dụng sha 256

Dự án này là một minh họa đơn giản về blockchain bằng Python. Nó sử dụng thư viện `pygame` cho đồ họa, `hashlib` cho băm SHA-256, `time` cho dấu thời gian, và `json` cho lưu trữ dữ liệu.

## Cấu trúc Dự án

- `blockchain.json`: Tệp này lưu trữ dữ liệu blockchain.
- `test.py`: Đây là script Python chính chạy demo blockchain.
- `tempCodeRunnerFile.py`: Tệp này chứa hàm `save_blockchain`.

## Các lớp

- `Block`: Lớp này đại diện cho một khối trong blockchain.

## Các hàm

- `create_genesis_block()`: Hàm này tạo ra khối đầu tiên của blockchain.
- `create_new_block(previous_block, data)`: Hàm này tạo ra một khối mới với chỉ số tăng dần.
- `save_blockchain(blockchain, filename="blockchain.json")`: Hàm này lưu blockchain vào một tệp JSON.
- `load_blockchain(filename="blockchain.json")`: Hàm này tải blockchain từ một tệp JSON.
- `verify_blockchain(blockchain)`: Hàm này xác minh tính toàn vẹn của blockchain.
- `get_block_count_from_file(filename)`: Hàm này trả về số lượng khối trong blockchain được lưu trữ trong tệp đã cho.

## Cách chạy

1. Cài đặt các gói Python cần thiết: `pygame`, `hashlib`, `time`, và `json`.
2. Chạy `test.py` để bắt đầu demo blockchain.

## Lưu ý

Dự án này chỉ dùng cho mục đích học tập.
