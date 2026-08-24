from pathlib import Path

p = Path("学习手册.md")
text = p.read_text(encoding="utf-8")
lines = text.splitlines()
print("lines", len(lines))
print("bytes", p.stat().st_size)
fence = "```"
fence_lines = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped.startswith(fence):
        fence_lines.append((i, stripped))
print("fence_count", len(fence_lines), "ODD" if len(fence_lines) % 2 else "EVEN")
stack = []
for i, s in fence_lines:
    if s.startswith(fence) and s != fence:
        stack.append((i, s))
    elif s == fence:
        if stack:
            stack.pop()
        else:
            print("EXTRA CLOSE at", i)
            break
if stack:
    print("UNCLOSED OPEN at", stack[-1])
    print("open stack size", len(stack))
    print("first unclosed", stack[0])
    print("last few opens", stack[-5:])
