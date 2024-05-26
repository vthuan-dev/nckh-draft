import pygame # sử dụng thư viện pygame để vẽ đồ họa
import hashlib # sử dụng thư viện hashlib để tạo mã băm , mã dc sử dụng là : SHA-256
import time # sử dụng thư viện time để lấy thời gian hiện tại 
import json  # sử dụng thư viện json để lưu trữ dữ liệu dưới dạng json

# Blockchain classes
class Block:#
    # khởi tạo các thuộc tính của block, self là tham chiếu đến chính đối tượng đó để truy cập các thuộc tính và phương thức của nó
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        # hash của block trước đó
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        # dữ liệu của block hiện tại là vị trí của player
        self.data = data
        # hash của block hiện tại được băm từ sha256
        self.hash = hash

    # phương thức tĩnh để tính toán hash của block, staticmethod cho phép gọi phương thức mà không cần tạo đối tượng
    @staticmethod
    def calculate_hash(index, previous_hash, timestamp, data):
        # ghép các giá trị của block thành một chuỗi và băm nó
        value = str(index) + str(previous_hash) + str(timestamp) + str(data)
        # trả về chuỗi hash
        return hashlib.sha256(value.encode('utf-8')).hexdigest()
    # chuyển block thành một dictionary để lưu trữ dưới dạng json , đọc hiểu thêm thì dô github của toai nhé =))
    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }
    # chuyển từ dictionary thành block
    @staticmethod
    def from_dict(block_dict):
        # trả về một block mới với các giá trị từ dictionary
        return Block(
            block_dict['index'],
            block_dict['previous_hash'],
            block_dict['timestamp'],
            block_dict['data'],
            block_dict['hash']
        )
# hàm tạo block đầu tiên của blockchain với index = 0, previous_hash = "0",
# timestamp = thời gian hiện tại, data = "Genesis Block"
#genisis block là block đầu tiên của blockchain, 
def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", Block.calculate_hash(0, "0", int(time.time()), "Genesis Block"))
#tạo block mới với index tăng dần, previous_block là block trước đó, 
def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    # tạo hash cho block mới
    hash = Block.calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)
# lưu blockchain vào file json
def save_blockchain(blockchain, filename="blockchain.json"):
    with open(filename, "w") as f:
        #khi mở file với chế độ "w" thì nó sẽ ghi đè lên file đó
        json.dump([block.to_dict() for block in blockchain], f)
# load blockchain từ file json
def load_blockchain(filename="blockchain.json"):
    try:
        # kho mở file để đọc dữ liệu
        with open(filename, "r") as f:
            # đọc dữ liệu từ file json, f là file json
            blockchain_data = json.load(f)
            # tạo blockchain từ dữ liệu đọc được
            blockchain = [Block.from_dict(block_dict) for block_dict in blockchain_data]
            if verify_blockchain(blockchain):
                #nếu blockchain hợp lệ thì return 1
                return blockchain
            else:
                raise ValueError("Blockchain is invalid")
    except (FileNotFoundError, ValueError):
        # nếu không tìm thấy file hoặc blockchain không hợp lệ thì tạo blockchain mới
        return [create_genesis_block()]
# xác nhận blockchain có hợp lệ không,
def verify_blockchain(blockchain):
    #kiểm tra từ block thứ 2 trở đi
    for i in range(1, len(blockchain)):
        # lấy block hiện tại và block trước đó
        current_block = blockchain[i]
        previous_block = blockchain[i - 1]
        # kiểm tra hash của block trước đó có trùng với previous_hash của block hiện tại không
        if current_block.previous_hash != previous_block.hash:
            #nếu không trùng thì return False
            return False
        # kiểm tra hash của block hiện tại có trùng với hash được tính toán từ các giá trị của block không
        if current_block.hash != Block.calculate_hash(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
            return False
        # return true nếu blockchain hợp lệ
    return True

# tải blockchain từ file
blockchain = load_blockchain()
# block cuối cùng của blockchain, -1 là phần tử cuối cùng của mảng
previous_block = blockchain[-1]

# Game classes
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_x = x  # Lưu vị trí x trước đó
        self.last_y = y  # Lưu vị trí y trước đó

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

# khởi tạo pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blockchain Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player
player = Player(WIDTH // 2, HEIGHT // 2)
player_size = 40

# khi game chạy thì running = True
running = True
clock = pygame.time.Clock() # tạo một đối tượng clock để giới hạn số lần lặp trong một giây , clock() trả về thời gian đã trôi qua

while running:
    # khi game chạy thì kiểm tra các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #di chuyển player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        player.move(5, 0)
    if keys[pygame.K_UP]:
        player.move(0, -5)
    if keys[pygame.K_DOWN]:
        player.move(0, 5)

    # Kiểm tra xem người chơi có di chuyển không
    if player.x != player.last_x or player.y != player.last_y:
        # Tạo block mới chỉ khi người chơi di chuyển
        new_block = create_new_block(previous_block, {"x": player.x, "y": player.y})
        blockchain.append(new_block)
        previous_block = new_block

        # Cập nhật vị trí trước đó của người chơi
        player.last_x = player.x
        player.last_y = player.y

    
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (player.x, player.y, player_size, player_size))
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
#lưu vào file json ở đây là blockchain.json
save_blockchain(blockchain)

# in ra các block trong blockchain
for block in blockchain:
    print(f"Index: {block.index}, Data: {block.data}, Hash: {block.hash}")

# đọc đến đây thì hãy đoán hàm này dùng để làm gì nhé =))
def get_block_count_from_file(filename):
    with open(filename, 'r') as f:
        blockchain = json.load(f)
    return len(blockchain)

block_count = get_block_count_from_file('blockchain.json')
print(f"Có {block_count} blocks trong blockchain hiện tại.")