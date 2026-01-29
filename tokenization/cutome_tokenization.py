import tiktoken

enc = tiktoken.encoding_for_model('gpt-4o')

tokens = enc.encode("Hey, My name is Pratik")

# ENCODED TOKENS: [25216, 11, 3673, 1308, 382, 2284, 28368]
print(tokens)

print(enc.decode([25216, 11, 3673, 1308, 382, 2284, 28368]))
