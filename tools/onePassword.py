import argparse
import base64
import hashlib
import getpass
import random
from cryptography.fernet import Fernet
from hashlib import sha256
from mnemonic import Mnemonic

# 固定字符集
LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGIT = "0123456789"
SYMB  = "@"
POOL  = LOWER + UPPER + DIGIT + SYMB

def phrase_to_password(phrase: str, pin: str, length: int = 10, rounds: int = 100_000) -> str:
    if length < 4:
        raise ValueError("length 至少为 4（需要覆盖四类字符）。")
    if not (pin.isdigit() and len(pin) == 6):
        raise ValueError("PIN 必须是 6 位数字。")

    # 派生足够多的字节
    dklen = max(length, 64)
    dk = hashlib.pbkdf2_hmac(
        "sha256",
        phrase.encode("utf-8"),
        pin.encode("utf-8"),  # 使用 6 位 PIN 作为 salt
        rounds,
        dklen=dklen
    )

    # 确保四类字符各一个
    picks = [
        LOWER[dk[0] % len(LOWER)],
        UPPER[dk[1] % len(UPPER)],
        DIGIT[dk[2] % len(DIGIT)],
        SYMB [dk[3] % len(SYMB )],
    ]

    # 剩余位置从全集补齐
    for i in range(4, length):
        picks.append(POOL[dk[i % len(dk)] % len(POOL)])

    # 洗牌
    j = 0
    for i in range(length - 1, 0, -1):
        j = (j + 1) % len(dk)
        k = dk[j] % (i + 1)
        picks[i], picks[k] = picks[k], picks[i]

    return "".join(picks)

def password_to_key(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_file(filename: str, key: bytes):
    fernet = Fernet(key)
    with open(filename, "rb") as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(filename + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"加密完成: {filename} → {filename}.enc")

def decrypt_file(filename: str, key: bytes):
    fernet = Fernet(key)
    with open(filename, "rb") as enc_file:
        encrypted = enc_file.read()
    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        print("错误：无法解密文件。可能是密码错误、文件损坏或该文件不是有效的加密文件。")
        exit(1)
    out_file = filename[:-4]  # 去掉 .enc
    with open(out_file, "wb") as dec_file:
        dec_file.write(decrypted)
    print(f"解密完成: {filename} → {out_file}")

def generate_mnemonic(sentence, pin, length=12, lang="english"):
    if length not in (12, 24):
        raise ValueError("助记词长度只能是 12 或 24")

    combined = f"{sentence}-{pin}"
    hash_bytes = sha256(combined.encode('utf-8')).digest()

    mnemo = Mnemonic(lang)
    entropy_bytes = hash_bytes[:16] if length == 12 else hash_bytes
    mnemonic_phrase = mnemo.to_mnemonic(entropy_bytes)
    return mnemonic_phrase

class HashTool:
    def __init__(self, pin=None):
        self.pin = pin if pin else self.generate_pin()

    def generate_pin(self, length=8):
        return ''.join(random.choices('0123456789', k=length))

    def encrypt(self, word):
        random.seed(self.pin)
        mapping = self._generate_mapping()
        return ''.join(mapping[char] if char in mapping else char for char in word)

    def decrypt(self, word):
        random.seed(self.pin)
        mapping = self._generate_mapping()
        reverse_mapping = {v: k for k, v in mapping.items()}
        return ''.join(reverse_mapping[char] if char in reverse_mapping else char for char in word)

    def _generate_mapping(self):
        chars = list('abcdefghijklmnopqrstuvwxyz')
        shuffled = chars[:]
        random.shuffle(shuffled)
        return dict(zip(chars, shuffled))

def main():
    parser = argparse.ArgumentParser(description="多功能工具：密码生成、文件加解密、助记词生成")
    subparsers = parser.add_subparsers(dest="command")

    # 密码生成
    pwd_parser = subparsers.add_parser("genpwd", help="生成强密码")
    pwd_parser.add_argument("--length", type=int, default=10, help="密码长度，默认10")

    # 文件加解密
    file_parser = subparsers.add_parser("file", help="文件加解密")
    file_parser.add_argument("filename", help="要加密/解密的文件")

    # 助记词生成
    mnemonic_parser = subparsers.add_parser("mnemonic", help="生成助记词")
    mnemonic_parser.add_argument("--length", type=int, default=24, choices=[12, 24], help="助记词长度，12 或 24")
    mnemonic_parser.add_argument("--lang", default="english", choices=["english", "chinese_simplified"], help="助记词语言")

    # 单词加解密
    hash_parser = subparsers.add_parser("hash", help="单词加解密")

    args = parser.parse_args()

    if args.command == "genpwd":
        phrase = getpass.getpass("请输入句子: ")
        pin = getpass.getpass("请输入 6 位数字 PIN: ")
        if not (pin.isdigit() and len(pin) == 6):
            print("错误: PIN 必须是 6 位数字。")
            exit(1)
        pwd = phrase_to_password(phrase, pin, args.length)
        print(f"生成的密码: {pwd}")

    elif args.command == "file":
        password = getpass.getpass("请输入密码: ")
        key = password_to_key(password)
        if args.filename.endswith(".enc"):
            decrypt_file(args.filename, key)
        else:
            encrypt_file(args.filename, key)

    elif args.command == "mnemonic":
        sentence = getpass.getpass("请输入一句话: ")
        pin = getpass.getpass("请输入 6 位数字 PIN: ")
        if not (pin.isdigit() and len(pin) == 6):
            print("错误: PIN 必须是 6 位数字。")
            exit(1)
        mnemonic_phrase = generate_mnemonic(sentence, pin, args.length, args.lang)
        print("生成的助记词：")
        print(mnemonic_phrase)

    elif args.command == "hash":
        pin = getpass.getpass("请输入密码: ")
        word = getpass.getpass("请输入单词: ")
        tool = HashTool(pin=pin)
        encrypted = tool.encrypt(word)
        decrypted = tool.decrypt(word)
        print(f"加密结果: {encrypted}")
        print(f"解密结果: {decrypted}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()