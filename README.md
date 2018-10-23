# toyhash

Some simple hash function implementation with API similar to the real ones. Written for fun and self-education.
According to the rule "Don't roll your own crypto!" it shouldn't be used in any real project.

## Usage
```python3
from toyhash import toyhash256

hash = toyhash256(b'Gort!')
d1 = hash.digest()  # b"!'\x1a7\xa0\xed\x84\xf7>\x92\x14\r\xcaU=\x8fb\xe7\xb7\x06T|\xed3k\xd7\x7f\xd7\xcc\xb8\xc1\xd4"
hd1 = hash.hexdigest()  # '21271a37a0ed84f73e92140dca553d8f62e7b706547ced336bd77fd7ccb8c1d4'
hash.update(b'Klaatu barada nikto!')
hd2 = hash.hexdigest()  # 'f0bc994cc652a9e190a53db1aca206613d513bfeb1f7c60ea10938c443760549'
```
