def save_blockchain(blockchain, filename="blockchain.json"):
    with open(filename, "w") as f:
        for block in blockchain:
            f.write(json.dumps(block.to_dict()) + "\n")